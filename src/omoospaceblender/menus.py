import bpy
from .utils import get_omoospace, get_pathname
from .manage_paths import ManageInputPaths, ManageOutputPaths
from .operators import CreateOmoospace, RevealPath, CopyToClipboard


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
            op = layout.operator(RevealPath.bl_idname, text=f"├─ Contents")
            op.path = str(omoospace.contents_dir)
            op = layout.operator(RevealPath.bl_idname, text=f"╰─ Subspaces")
            op.path = str(omoospace.subspaces_dir)

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
    omoospace = get_omoospace()
    if not omoospace:
        return

    quick_dir_list = bpy.context.window_manager.quick_dir_list

    layout.template_list(
        listtype_name="OMOOSPACE_UL_QuickDirList",
        list_id="quick_dirs",
        dataptr=quick_dir_list,
        propname="quick_dirs",
        active_dataptr=quick_dir_list,
        active_propname="quick_dirs_active",
        item_dyntip_propname="path",
        rows=3,
    )


def add():
    bpy.types.TOPBAR_MT_editor_menus.prepend(TOPBAR)
    bpy.types.FILEBROWSER_PT_bookmarks_favorites.prepend(FILE_BROWSER)


def remove():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR)
    bpy.types.FILEBROWSER_PT_bookmarks_favorites.remove(FILE_BROWSER)
