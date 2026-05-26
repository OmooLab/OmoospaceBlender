import bpy
import re
from bpy.app.handlers import persistent
from pathlib import Path

from .manage_paths import (
    correct_path_on_save_pre,
    restore_path_on_save_post,
    correct_path_on_load_post,
)
from .utils import get_omoospace


def update_profile():
    """Load profile for the current omoospace on file load."""

    PROFILE_PATTERN = re.compile(r"omoospace\..*", re.IGNORECASE)

    profiles_to_remove = [
        text for text in bpy.data.texts if PROFILE_PATTERN.match(text.name)
    ]
    for text in profiles_to_remove:
        bpy.data.texts.remove(text)

    omoospace = get_omoospace()
    if not omoospace:
        return

    profile_file = bpy.path.relpath(str(omoospace.profile_file))

    try:
        bpy.data.texts.load(profile_file, internal=False)
    except Exception as e:
        print(f"[Omoospace] Failed to load profile {profile_file}: {e}")


def update_quick_dirs():
    preferences = bpy.context.preferences.addons[__package__].preferences
    home = preferences.omoospace_home

    quick_dirs = bpy.context.window_manager.quick_dir_list.quick_dirs
    quick_dirs.clear()

    quick_dir = quick_dirs.add()
    quick_dir.label = "Home"
    quick_dir.path = home

    omoospace = get_omoospace()
    if not omoospace:
        return

    quick_dir = quick_dirs.add()
    quick_dir.label = "Omoospace"
    quick_dir.path = str(omoospace.root_dir)

    # Only add if the directory exists
    if omoospace.contents_dir.exists():
        quick_dir = quick_dirs.add()
        quick_dir.label = "├─ contents"
        quick_dir.path = str(omoospace.contents_dir)

    if omoospace.contents_dir.exists():
        quick_dir = quick_dirs.add()
        quick_dir.label = "╰─ subspaces"
        quick_dir.path = str(omoospace.subspaces_dir)


@persistent
def on_load_post(dummy):
    update_quick_dirs()
    update_profile()
    correct_path_on_load_post()


@persistent
def on_save_post(blend_file: str):
    update_quick_dirs()
    update_profile()
    restore_path_on_save_post(blend_file)


@persistent
def on_save_pre(blend_file: str):
    correct_path_on_save_pre(blend_file)


def register():
    bpy.app.handlers.load_post.append(on_load_post)
    bpy.app.handlers.save_pre.append(on_save_pre)
    bpy.app.handlers.save_post.append(on_save_post)


def unregister():
    bpy.app.handlers.load_post.remove(on_load_post)
    bpy.app.handlers.save_pre.remove(on_save_pre)
    bpy.app.handlers.save_post.remove(on_save_post)
