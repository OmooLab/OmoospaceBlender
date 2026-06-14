import bpy
from .utils import get_omoospace, get_pathname
from .manage_paths import ManageInputPaths, ManageOutputPaths
from .operators import (
    CopyToClipboard,
    CreateOmoospace,
    LoadOmoospaceStartup,
    RevealPath,
)


class OmoospaceMenu(bpy.types.Menu):
    bl_idname = "OMOOSPACE_MT_OMOOSPACE"
    bl_label = "Omoospace"

    def draw(self, context):
        omoospace = get_omoospace()
        layout = self.layout

        if omoospace:
            omoospace_root = str(omoospace.root_dir)

            subspace_pathname = get_pathname()

            op = layout.operator(RevealPath.bl_idname, text=f"Omoospace")
            op.path = str(omoospace.root_dir)
            op = layout.operator(RevealPath.bl_idname, text=f"├─ contents")
            op.path = str(omoospace.contents_dir)
            op = layout.operator(RevealPath.bl_idname, text=f"╰─ subspaces")
            op.path = str(omoospace.subspaces_dir)

            if subspace_pathname is None:
                layout.label(text=f"*Not a subspace", icon="ERROR")
            else:
                op = layout.operator(
                    CopyToClipboard.bl_idname,
                    text=f"       ╰─ {subspace_pathname}",
                )
                op.text = subspace_pathname

            layout.separator()
            layout.operator(ManageInputPaths.bl_idname)
            layout.operator(ManageOutputPaths.bl_idname)
            layout.separator()

        layout.operator(CreateOmoospace.bl_idname)


def TOPBAR(self, context):
    layout = self.layout
    layout.menu(OmoospaceMenu.bl_idname)


def FILE_BROWSER(self, context):
    layout = self.layout
    quick_dir_list = bpy.context.window_manager.quick_dir_list

    layout.template_list(
        listtype_name="OMOOSPACE_UL_QuickDirList",
        list_id="quick_dirs",
        dataptr=quick_dir_list,
        propname="quick_dirs",
        active_dataptr=quick_dir_list,
        active_propname="quick_dirs_active",
        item_dyntip_propname="path",
        rows=len(quick_dir_list.quick_dirs),
    )


def FILE_DEFAULTS(self, context):
    layout = self.layout
    layout.operator(LoadOmoospaceStartup.bl_idname)
    layout.separator()


def _has_file_defaults_menu():
    return hasattr(bpy.types, "TOPBAR_MT_file_defaults")


def add():
    bpy.types.TOPBAR_MT_editor_menus.prepend(TOPBAR)
    bpy.types.FILEBROWSER_PT_bookmarks_favorites.prepend(FILE_BROWSER)
    if _has_file_defaults_menu():
        bpy.types.TOPBAR_MT_file_defaults.prepend(FILE_DEFAULTS)
    else:
        print("Blender File Defaults menu not found.")


def remove():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR)
    bpy.types.FILEBROWSER_PT_bookmarks_favorites.remove(FILE_BROWSER)
    if _has_file_defaults_menu():
        bpy.types.TOPBAR_MT_file_defaults.remove(FILE_DEFAULTS)
