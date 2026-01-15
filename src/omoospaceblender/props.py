import bpy


class OMOOSPACE_OldPath(bpy.types.PropertyGroup):
    parm: bpy.props.StringProperty()  # type: ignore
    path: bpy.props.StringProperty()  # type: ignore


class OMOOSPACE_InputPath(bpy.types.PropertyGroup):
    selected: bpy.props.BoolProperty(default=False)  # type: ignore
    icon: bpy.props.StringProperty(default="None")  # type: ignore
    users: bpy.props.IntProperty(default=0)  # type: ignore
    label: bpy.props.StringProperty()  # type: ignore
    parm: bpy.props.StringProperty()  # type: ignore
    path: bpy.props.StringProperty()  # type: ignore

    category: bpy.props.StringProperty(default="Misc")  # type: ignore
    folder: bpy.props.StringProperty(default="")  # type: ignore
    include_pathname: bpy.props.BoolProperty(default=False)  # type: ignore
    include_folder: bpy.props.BoolProperty(default=False)  # type: ignore
    is_packed: bpy.props.BoolProperty(default=False)  # type: ignore


class OMOOSPACE_OutputPath(bpy.types.PropertyGroup):
    selected: bpy.props.BoolProperty(default=False)  # type: ignore
    icon: bpy.props.StringProperty(default="None")  # type: ignore
    label: bpy.props.StringProperty()  # type: ignore
    parm: bpy.props.StringProperty()  # type: ignore
    path: bpy.props.StringProperty()  # type: ignore

    category: bpy.props.StringProperty(default="Misc")  # type: ignore
    name: bpy.props.StringProperty()  # type: ignore
    suffix: bpy.props.StringProperty()  # type: ignore
    in_folder: bpy.props.BoolProperty(default=False)  # type: ignore


class OMOOSPACE_QuickDir(bpy.types.PropertyGroup):
    label: bpy.props.StringProperty()  # type: ignore
    path: bpy.props.StringProperty(subtype="DIR_PATH")  # type: ignore


def update_quick_dirs(self, context):
    quick_dir_list = bpy.context.window_manager.quick_dir_list
    quick_dirs = quick_dir_list.quick_dirs
    quick_dirs_active = quick_dir_list.quick_dirs_active

    if quick_dirs_active != -1:
        bpy.context.space_data.params.directory = str(
            quick_dirs[quick_dirs_active].path
        ).encode()

        quick_dir_list.quick_dirs_active = -1


class OMOOSPACE_QuickDirList(bpy.types.PropertyGroup):
    quick_dirs: bpy.props.CollectionProperty(type=OMOOSPACE_QuickDir)  # type: ignore
    quick_dirs_active: bpy.props.IntProperty(
        default=-1, name="Quick Directories", update=update_quick_dirs, options=set()
    )  # type: ignore
