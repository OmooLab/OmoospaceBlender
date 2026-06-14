from .props import OMOOSPACE_QuickDirList, OMOOSPACE_OldPath
from . import auto_load
from . import default_configs
from . import menus

import bpy


auto_load.init()


def register():
    auto_load.register()
    default_configs.install_keymap_preset()
    bpy.types.WindowManager.quick_dir_list = bpy.props.PointerProperty(
        type=OMOOSPACE_QuickDirList
    )
    bpy.types.WindowManager.old_path_list = bpy.props.CollectionProperty(
        type=OMOOSPACE_OldPath
    )
    menus.add()


def unregister():
    menus.remove()
    default_configs.restore_installed_configs()
    auto_load.unregister()
