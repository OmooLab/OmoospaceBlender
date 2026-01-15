import bpy
from pathlib import Path

from .operators import RevealPath
from .utils import (
    bpath_to_opath,
    copy_to,
    get_omoospace,
    get_pathname,
    get_subspace_data,
    get_type,
    is_content,
    is_sequence,
    opath_to_bpath,
    set_subspace_data,
)
from .props import OMOOSPACE_InputPath, OMOOSPACE_OutputPath, OMOOSPACE_OldPath
from omoospace import normalize_name, Opath, Omoospace

CATEGORY_ICON = {
    "Images": "IMAGE_DATA",
    "Volumes": "VOLUME_DATA",
    "Dynamics": "FORCE_WIND",
    "Libraries": "LIBRARY_DATA_DIRECT",
    "Misc": "FILE",
    "Renders": "OUTPUT",
    "Videos": "FILE_MOVIE",
    "Audios": "FILE_SOUND",
    "GeometryNodes": "NODETREE",
}


def correct_input_path(
    input_path: Opath,
    category="Misc",
    folder="",
    include_folder=False,
    include_pathname=False,
) -> Opath:
    omoospace = get_omoospace()
    main_folder = omoospace.contents_dir

    end_name = (
        f"{input_path.parent.name}/{input_path.name}"
        if include_folder
        else input_path.name
    )

    if include_pathname:
        pathname = get_pathname()
        folder = f"{pathname}_{folder}" if folder else pathname

    if folder:
        new_path = main_folder / category / folder / end_name
    else:
        new_path = main_folder / category / end_name

    return new_path


def correct_output_path(name, in_folder=False, category="Misc", suffix=""):

    omoospace = get_omoospace()
    pathname = get_pathname()
    main_folder = omoospace.contents_dir

    suffix.removeprefix(".")
    name = f"{pathname}_{name}" if name else pathname
    filename = f"{name}.{suffix}" if suffix else name

    if in_folder:
        new_path = main_folder / category / name / filename
    else:
        new_path = main_folder / category / filename

    return new_path


video_format = (
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".wmv",
    ".flv",
    ".webm",
)


def collect_input_paths():
    input_path_dict = {}

    # TODO: 是否应该包括要那些没有在使用的资源？
    for image in bpy.data.images:
        if not image.filepath:
            continue

        parm = f"bpy.data.images['{image.name}'].filepath"
        input_path_dict[parm] = {
            "label": image.name,
            "path": image.filepath,
            "users": image.users,
            "category": "Videos" if image.filepath.endswith(video_format) else "Images",
            "is_sequence": is_sequence(image.filepath),
            "is_packed": bool(image.packed_file),
        }

    for sound in bpy.data.sounds:
        if not sound.filepath:
            continue

        parm = f"bpy.data.sounds['{sound.name}'].filepath"
        input_path_dict[parm] = {
            "label": sound.name,
            "path": sound.filepath,
            "users": sound.users,
            "category": "Videos" if sound.filepath.endswith(video_format) else "Audios",
            "is_sequence": False,
            "is_packed": bool(sound.packed_file),
        }

    for volume in bpy.data.volumes:
        if not volume.filepath:
            continue

        parm = f"bpy.data.volumes['{volume.name}'].filepath"
        input_path_dict[parm] = {
            "label": volume.name,
            "path": volume.filepath,
            "users": volume.users,
            "category": "Volumes",
            "is_sequence": volume.is_sequence,
            "is_packed": bool(volume.packed_file),
        }

    for cache_file in bpy.data.cache_files:
        if not cache_file.filepath:
            continue

        parm = f"bpy.data.cache_files['{cache_file.name}'].filepath"
        input_path_dict[parm] = {
            "label": cache_file.name,
            "path": cache_file.filepath,
            "users": cache_file.users,
            "category": "Dynamics",
            "is_sequence": is_sequence(cache_file.filepath),
            "is_packed": False,
        }

    for library in bpy.data.libraries:
        if not library.filepath:
            continue

        if library.filepath == "<startup.blend>" or library.filepath.endswith(
            "startup.blend"
        ):
            continue

        parm = f"bpy.data.libraries['{library.name}'].filepath"
        input_path_dict[parm] = {
            "label": library.name,
            "path": library.filepath,
            "users": library.users,
            "category": "Libraries",
            "is_sequence": False,
            "is_packed": bool(library.packed_file),
        }

    for scene in bpy.data.scenes:
        if not scene.sequence_editor:
            continue
        for strip in scene.sequence_editor.strips_all:
            parm = None
            category = None
            path = None

            if strip.type == "IMAGE":
                category = "Images"
                path = strip.directory
                parm = f"bpy.data.scenes['{scene.name}'].sequence_editor.strips_all['{strip.name}'].directory"
            elif strip.type == "MOVIE":
                category = "Videos"
                path = strip.filepath
                parm = f"bpy.data.scenes['{scene.name}'].sequence_editor.strips_all['{strip.name}'].filepath"

            if not parm:
                continue

            input_path_dict[parm] = {
                "label": strip.name,
                "path": path,
                "users": 0,
                "category": category,
                "is_sequence": False,
                "is_packed": False,
            }

    return input_path_dict


def collect_output_paths():
    output_paths = {}
    for scene in bpy.data.scenes:
        parm = f"bpy.data.scenes['{scene.name}'].render.filepath"
        not_video = scene.render.image_settings.file_format not in [
            "AVI_JPEG",
            "AVI_RAW",
            "FFMPEG",
        ]

        output_paths[parm] = {
            "label": f"{scene.name}",
            "path": scene.render.filepath,
            "category": "Renders",
            "name": normalize_name(scene.name),
            "suffix": "####" if not_video else "",
            "in_folder": not_video,
        }

    for obj in bpy.data.objects:
        for modifier in obj.modifiers:
            if get_type(modifier) == "NodesModifier" and hasattr(
                modifier, "bake_directory"
            ):
                parm = f"bpy.data.objects['{obj.name}'].modifiers['{modifier.name}'].bake_directory"
                output_paths[parm] = {
                    "label": f"{obj.name} {modifier.name}",
                    "path": modifier.bake_directory,
                    "category": "GeometryNodes",
                    "name": normalize_name(modifier.name),
                    "suffix": "",
                    "in_folder": False,
                }

    return output_paths


class OMOOSPACE_UL_InputPathList(bpy.types.UIList):
    invaild_only: bpy.props.BoolProperty(
        name="Show Invaild Path Only", options=set(), default=True
    )  # type: ignore

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname
    ):
        input_path: OMOOSPACE_InputPath = item

        if input_path.selected:
            old_opath = bpath_to_opath(input_path.path)
            is_packed = input_path.is_packed
            include_folder = input_path.include_folder and not is_packed
            new_opath: Opath = correct_input_path(
                old_opath,
                category=input_path.category,
                folder=input_path.folder,
                include_folder=include_folder,
                include_pathname=input_path.include_pathname,
            )

            path_str = f"{'⁉️ 'if new_opath.exists() else ''}{opath_to_bpath(new_opath)}"
        else:
            path_str = input_path.path

        label = f"{input_path.users} {input_path.label}"

        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.split(factor=0.02)
            row.prop(input_path, "selected", text="")
            row = row.split(factor=0.2)
            row.label(text=label, icon=input_path.icon)
            row = row.split(factor=0.1)
            row.prop(input_path, "category", text="")
            row = row.split(factor=0.04)

            row.prop(
                input_path,
                "include_pathname",
                text="",
                icon="EVENT_S",
                toggle=True,
            )
            row = row.split(factor=0.15)
            row.prop(input_path, "folder", text="")

            row = row.split(factor=0.05)
            if not input_path.is_packed:
                row.prop(
                    input_path,
                    "include_folder",
                    text="",
                    icon="FILE_FOLDER",
                    toggle=True,
                )
            else:
                row.label(
                    text="",
                    icon="FILE_FOLDER",
                )
            row = row.split(factor=1)
            op = row.operator(
                RevealPath.bl_idname,
                text=path_str,
                depress=input_path.selected,
                icon="PACKAGE" if input_path.is_packed else "UGLYPACKAGE",
            )
            op.path = path_str
            # row.label(
            #     text=path_str,
            #     icon="PACKAGE" if input_path.is_packed else "UGLYPACKAGE",
            # )

        elif self.layout_type == "GRID":
            ...

    def draw_filter(self, context, layout):
        layout.prop(self, "invaild_only")

    def filter_items(self, context, data, propname):
        input_paths = getattr(data, propname)

        # Default return values.
        flt_flags = [self.bitflag_filter_item] * len(input_paths)

        for index, input_path in enumerate(input_paths):
            if self.invaild_only and is_content(input_path.path):
                flt_flags[index] &= ~self.bitflag_filter_item

        flt_neworder = bpy.types.UI_UL_list.sort_items_by_name(input_paths, "parm")

        return flt_flags, flt_neworder


def update_input_paths(self, context):
    input_paths_active = self.input_paths_active
    if input_paths_active != -1:
        self.input_paths_active = -1


class ManageInputPaths(bpy.types.Operator):
    bl_idname = "omoospace.manage_input_paths"
    bl_label = "Manage Input Paths"
    bl_description = "Manage all input paths in current file"
    bl_options = {"UNDO"}

    input_paths: bpy.props.CollectionProperty(
        type=OMOOSPACE_InputPath, options={"SKIP_SAVE"}
    )  # type: ignore

    input_paths_active: bpy.props.IntProperty(
        name="Input Paths", options=set(), default=-1, update=update_input_paths
    )  # type: ignore

    def invoke(self, context, event):
        for parm, item in collect_input_paths().items():
            input_path: OMOOSPACE_InputPath = self.input_paths.add()

            input_path.parm = parm
            input_path.users = item["users"]
            input_path.label = item["label"]
            input_path.path = item["path"]
            input_path.category = item["category"]
            input_path.icon = CATEGORY_ICON[item["category"]]

            if item["is_sequence"]:
                input_path.include_folder = True

            input_path.is_packed = item["is_packed"]

        context.window_manager.invoke_props_dialog(self, width=800)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        input_paths: list[OMOOSPACE_InputPath] = self.input_paths

        for input_path in input_paths:
            # skip
            if not input_path.selected:
                continue

            parm: str = input_path.parm
            old_bpath = input_path.path
            is_packed = input_path.is_packed
            include_folder = input_path.include_folder and not is_packed

            old_opath = bpath_to_opath(old_bpath)
            new_opath = correct_input_path(
                old_opath,
                category=input_path.category,
                folder=input_path.folder,
                include_folder=include_folder,
                include_pathname=input_path.include_pathname,
            )
            new_bpath: str = opath_to_bpath(new_opath)

            # TODO: 需要更好的方案去解决打包的文件，目前只实现了图片类的问题，而且处理的不好
            try:
                if is_packed:
                    exec(f"{parm.removesuffix('.filepath')}.unpack()")
                    old_opath = bpath_to_opath(f"//textures/{old_opath.name}")

                if include_folder:
                    copy_to(old_opath.parent, new_opath.parent.parent)
                else:
                    copy_to(old_opath, new_opath.parent)

                exec(f"{parm}=r'{new_bpath}'")

                # repack to confirm filepath
                if is_packed:
                    old_opath.remove()
                    exec(f"{parm.removesuffix('.filepath')}.pack()")

                self.report({"INFO"}, f"{old_bpath} -> {new_bpath}")
            except Exception as err:
                print(err)
                self.report({"WARNING"}, f"Fail to copy, skip '{parm}'.")

        local_unpack_dir = bpath_to_opath(f"//textures")
        if local_unpack_dir.exists():
            if len(local_unpack_dir.get_children(recursive=False)) == 0:
                local_unpack_dir.remove()

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        row = layout.split(factor=0.03)
        row.label(text="")
        row = row.split(factor=0.2)
        row.label(text="Label")
        row = row.split(factor=0.1)
        row.label(text="Category")
        row = row.split(factor=0.2)
        row.label(text="Folder")
        row = row.split(factor=0.15)
        row.label(text="Preview")
        row = row.split(factor=1)
        row.label(text="⁉️= file already exists, only change path")

        layout.template_list(
            listtype_name="OMOOSPACE_UL_InputPathList",
            list_id="input_paths",
            dataptr=self,
            propname="input_paths",
            active_dataptr=self,
            active_propname="input_paths_active",
            item_dyntip_propname="path",
            rows=20,
        )


class OMOOSPACE_UL_OutputPathList(bpy.types.UIList):

    invaild_only: bpy.props.BoolProperty(
        name="Show Invaild Path Only", options=set(), default=True
    )  # type: ignore

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname
    ):
        output_path: OMOOSPACE_OutputPath = item

        if output_path.selected:
            new_opath: Path = correct_output_path(
                output_path.name,
                in_folder=output_path.in_folder,
                category=output_path.category,
                suffix=output_path.suffix,
            )

            path_str = opath_to_bpath(new_opath)
        else:
            path_str = output_path.path

        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.split(factor=0.02)
            row.prop(output_path, "selected", text="")
            row = row.split(factor=0.15)
            row.label(text=output_path.label, icon=output_path.icon)

            row = row.split(factor=0.1)
            row.prop(output_path, "category", text="")
            row = row.split(factor=0.15)
            row.prop(output_path, "name", text="")
            row = row.split(factor=0.15)
            row.prop(output_path, "suffix", text="")
            row = row.split(factor=0.05)
            row.prop(output_path, "in_folder", text="", icon="FILE_FOLDER", toggle=1)

            row = row.split(factor=1)
            op = row.operator(
                RevealPath.bl_idname, text=path_str, depress=output_path.selected
            )
            op.path = path_str

        elif self.layout_type == "GRID":
            ...

    def draw_filter(self, context, layout):
        layout.prop(self, "invaild_only")

    def filter_items(self, context, data, propname):
        output_paths = getattr(data, propname)

        # Default return values.
        flt_flags = [self.bitflag_filter_item] * len(output_paths)

        for index, output_path in enumerate(output_paths):
            if self.invaild_only and is_content(output_path.path):
                flt_flags[index] &= ~self.bitflag_filter_item

        flt_neworder = bpy.types.UI_UL_list.sort_items_by_name(output_paths, "parm")

        return flt_flags, flt_neworder


def update_output_paths(self, context):
    output_paths_active = self.output_paths_active
    if output_paths_active != -1:
        self.output_paths_active = -1


class ManageOutputPaths(bpy.types.Operator):
    bl_idname = "omoospace.manage_output_paths"
    bl_label = "Manage Output Paths"
    bl_description = "Manage all output paths in current file"
    bl_options = {"UNDO"}

    output_paths: bpy.props.CollectionProperty(
        type=OMOOSPACE_OutputPath, options={"SKIP_SAVE"}
    )  # type: ignore

    output_paths_active: bpy.props.IntProperty(
        name="Output Paths", options=set(), default=-1, update=update_output_paths
    )  # type: ignore

    def invoke(self, context, event):
        for parm, item in collect_output_paths().items():
            output_path: OMOOSPACE_OutputPath = self.output_paths.add()
            output_path.label = item["label"]
            output_path.parm = parm
            output_path.path = item["path"]
            output_path.category = item["category"]
            output_path.icon = CATEGORY_ICON[item["category"]]
            output_path.name = item["name"]
            output_path.suffix = item["suffix"]
            output_path.in_folder = item["in_folder"]

        context.window_manager.invoke_props_dialog(self, width=900)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        output_paths: list[OMOOSPACE_OutputPath] = self.output_paths

        for output_path in output_paths:
            # skip
            if not output_path.selected:
                continue

            parm = output_path.parm
            old_bpath = output_path.path
            new_opath = correct_output_path(
                output_path.name,
                in_folder=output_path.in_folder,
                category=output_path.category,
                suffix=output_path.suffix,
            )

            new_bpath: str = opath_to_bpath(new_opath)

            exec(f"{parm}=r'{new_bpath}'")
            self.report({"INFO"}, f"{old_bpath} -> {new_bpath}")

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        row = layout.split(factor=0.03)
        row.label(text="")
        row = row.split(factor=0.15)
        row.label(text="Label")
        row = row.split(factor=0.1)
        row.label(text="Category")
        row = row.split(factor=0.15)
        row.label(text="Name")
        row = row.split(factor=0.15)
        row.label(text="Suffix")
        row = row.split(factor=1)
        row.label(text="Preview")

        layout.template_list(
            listtype_name="OMOOSPACE_UL_OutputPathList",
            list_id="output_paths",
            dataptr=self,
            propname="output_paths",
            active_dataptr=self,
            active_propname="output_paths_active",
            item_dyntip_propname="path",
            rows=20,
        )


def correct_path_on_save_pre(blend_file: str):
    # if new file is not in omoospace, no need to correct
    try:
        old_contents_dir = get_omoospace().contents_dir
        new_contents_dir = Omoospace(blend_file).contents_dir
    except AttributeError:
        return

    new_rel_contents_dir = opath_to_bpath(new_contents_dir, blend_file)
    set_subspace_data("rel_contents_dir", new_rel_contents_dir)

    # if in same dir, no need to correct
    if Opath(bpy.data.filepath).parent == Opath(blend_file).parent:
        return

    wm = bpy.context.window_manager
    wm.old_path_list.clear()

    output_paths = [
        {"parm": parm, "path": item["path"]}
        for parm, item in collect_output_paths().items()
        if is_content(item["path"])
    ]

    for output_path in output_paths:
        parm = output_path["parm"]
        old_bpath = output_path["path"]

        old_opath = bpath_to_opath(old_bpath)
        old_rel_bpath = str(old_opath.relative_to(old_contents_dir))
        new_bpath: str = f"{new_rel_contents_dir}/{old_rel_bpath}"

        exec(f"{parm}=r'{new_bpath}'")

        old_path: OMOOSPACE_OldPath = wm.old_path_list.add()
        old_path.parm = parm
        old_path.path = old_bpath

    # if in same omoospace, no need to correct input paths
    # blender will handle all relative input paths
    if old_contents_dir == new_contents_dir:
        return

    input_paths = [
        {"parm": parm, "is_packed": item["is_packed"], "path": item["path"]}
        for parm, item in collect_input_paths().items()
        if is_content(item["path"])
    ]

    for input_path in input_paths:
        parm = input_path["parm"]
        old_bpath = input_path["path"]
        is_packed = input_path["is_packed"]

        old_opath = bpath_to_opath(old_bpath)
        old_rel_bpath = str(old_opath.relative_to(old_contents_dir))
        new_opath = new_contents_dir / old_rel_bpath
        try:
            new_bpath: str = opath_to_bpath(new_opath)
        except ValueError:
            new_bpath = str(new_opath)

        # if copy fail, skip change path
        try:
            if is_packed:
                exec(f"{parm.removesuffix('.filepath')}.unpack()")
                old_opath = bpath_to_opath(f"//textures/{old_opath.name}")

            copy_to(old_opath, new_opath.parent)

            exec(f"{parm}=r'{new_bpath}'")
            print(f"{old_bpath} -> {new_bpath}")

            old_path: OMOOSPACE_OldPath = wm.old_path_list.add()
            old_path.parm = parm
            old_path.path = old_bpath

            # repack to confirm filepath
            if is_packed:
                old_opath.remove()
                exec(f"{parm.removesuffix('.filepath')}.pack()")

        except Exception as err:
            print(err)

    local_unpack_dir = bpath_to_opath(f"//textures")
    if local_unpack_dir.exists():
        if len(local_unpack_dir.get_children(recursive=False)) == 0:
            local_unpack_dir.remove()


def restore_path_on_save_post(blend_file: str):
    wm = bpy.context.window_manager

    # if is "save as", no need to restore
    if bpy.data.filepath == blend_file:
        return

    for path_item in wm.old_path_list:
        parm = path_item.parm
        old_bpath = path_item.path
        exec(f"{parm}=r'{old_bpath}'")


def correct_path_on_load_post():
    # if not in omoospace, no need to correct
    try:
        contents_dir = get_omoospace().contents_dir
        old_rel_contents_dir = get_subspace_data("rel_contents_dir")
        new_rel_contents_dir = opath_to_bpath(contents_dir)
    except AttributeError:
        return

    all_paths = {**collect_input_paths(), **collect_output_paths()}

    for parm, item in all_paths.items():
        old_bpath = item["path"]

        # 如果是内容，则绝对路径改为相对路径
        if is_content(old_bpath) and not old_bpath.startswith("//"):

            new_bpath = bpy.path.relpath(old_bpath)
            exec(f"{parm}=r'{new_bpath}'")
            print(f"{old_bpath} -> {new_bpath}")
            old_bpath = new_bpath

        if old_rel_contents_dir == new_rel_contents_dir or old_rel_contents_dir is None:
            continue

        # 如果符合记录中的相对位置，改为新的相对位置
        if old_bpath.startswith(old_rel_contents_dir):

            new_bpath = old_bpath.replace(old_rel_contents_dir, new_rel_contents_dir)
            exec(f"{parm}=r'{new_bpath}'")
            print(f"{old_bpath} -> {new_bpath}")
