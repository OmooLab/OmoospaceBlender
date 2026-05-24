import bpy
from pathlib import Path

from .utils import bpath_to_opath
from omoospace import create_omoospace, normalize_name, copy_to_clipboard, Opath


class CreateOmoospace(bpy.types.Operator):
    bl_idname = "omoospace.create_omoospace"
    bl_label = "Create an Omoospace"
    bl_description = "Create an omoospace from current blender file"
    bl_options = {"UNDO"}

    under: bpy.props.StringProperty(
        name="Home", subtype="DIR_PATH", default=str(Path.home())
    )  # type: ignore

    dirname: bpy.props.StringProperty(name="Name")  # type: ignore
    name: bpy.props.StringProperty(name="Name")  # type: ignore
    description: bpy.props.StringProperty(name="Description")  # type: ignore
    subspace_name: bpy.props.StringProperty(name="File Name")  # type: ignore
    contents_dir: bpy.props.StringProperty(
        name="contents/", default="contents"
    )  # type: ignore
    subspaces_dir: bpy.props.StringProperty(
        name="subspaces/", default="subspaces"
    )  # type: ignore

    def invoke(self, context, event):
        preferences = context.preferences.addons[__package__].preferences
        self.under = preferences.omoospace_home
        context.window_manager.invoke_props_dialog(self, width=300)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        file_name = bpy.path.basename(bpy.data.filepath) or "Untitled"
        dirname = self.dirname or file_name

        omoospace_dir = Opath(self.under, dirname)

        try:
            subspace_name = normalize_name(self.subspace_name)
        except ValueError:
            subspace_name = normalize_name(file_name)

        try:
            omoospace = create_omoospace(
                omoospace_dir,
                contents_dir=self.contents_dir,
                subspaces_dir=self.subspaces_dir,
                reveal_in_explorer=True,
            )
        except FileExistsError:
            self.report({"ERROR"}, "Omoospace already exists.")
            return {"CANCELLED"}

        blend_path = str(omoospace.subspaces_dir / f"{subspace_name}.blend")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)

        tool = omoospace.add_tool("Blender")
        tool.version = bpy.app.version_string.split(" ")[0]
        return {"FINISHED"}

    def draw(self, context):
        file_name = bpy.path.basename(bpy.data.filepath) or "Untitled"
        dirname = self.dirname or file_name

        try:
            subspace_name = normalize_name(self.subspace_name)
        except ValueError:
            subspace_name = normalize_name(file_name)

        omoospace_dir = Opath(self.under, dirname)
        contents_dir = self.contents_dir or "contents"
        subspaces_dir = self.subspaces_dir or ""

        layout = self.layout
        layout.prop(self, "under", text="")
        layout.label(text="Folder Structure")
        box = layout.box()
        if subspaces_dir:
            box.label(text=f"{str(omoospace_dir)}")
            box.label(text=f"├─ {str(contents_dir)}")
            box.label(text=f"╰─ {str(subspaces_dir)}")
            box.label(text=f"       ╰─ {str(f'{subspace_name}.blend')}")
        else:
            box.label(text=f"{str(omoospace_dir)}")
            box.label(text=f"├─ {str(contents_dir)}")
            box.label(text=f"╰─ {str(f'{subspace_name}.blend')}")

        layout.separator()
        layout.prop(self, "dirname")
        layout.prop(self, "contents_dir")
        layout.prop(self, "subspaces_dir")

        layout.separator()
        layout.prop(self, "subspace_name")


class CopyToClipboard(bpy.types.Operator):
    bl_idname = "omoospace.copy_to_clipboard"
    bl_label = "Copy"
    bl_description = "Copy the current text to clipboard"
    bl_options = {"UNDO"}

    text: bpy.props.StringProperty(name="Text to Copy", default="")  # type: ignore

    def execute(self, context):
        copy_to_clipboard(self.text)
        self.report({"INFO"}, f"Successfully copyed '{self.text}'")
        return {"FINISHED"}


class RevealPath(bpy.types.Operator):
    bl_idname = "omoospace.reveal_path"
    bl_label = "Reveal Current Path"
    bl_description = "Reveal the current path in file explorer"
    bl_options = {"UNDO"}

    path: bpy.props.StringProperty(name="Path to Reveal", default="")  # type: ignore

    def execute(self, context):
        if not self.path:
            return {"CANCELLED"}

        opath = bpath_to_opath(self.path)

        if opath.is_file():
            opath.parent.reveal_in_explorer()
        elif opath.is_dir():
            opath.reveal_in_explorer()

        return {"FINISHED"}
