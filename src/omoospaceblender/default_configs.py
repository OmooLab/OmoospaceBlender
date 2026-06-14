import re
import shutil
from pathlib import Path

import bpy


CONFIGS_DIR = Path(__file__).parent / "configs"
KEYMAP_FILE = "Omoospace.py"
STARTUP_FILE = "startup.blend"
STARTUP_BACKUP_FILE = "startup.bak.blend"


def get_blender_version_number(version=None):
    if version is None:
        version = bpy.app.version
    return version[0] * 10 + version[1]


def iter_config_dirs(configs_dir=CONFIGS_DIR):
    if not configs_dir.exists():
        return

    for path in configs_dir.iterdir():
        if not path.is_dir():
            continue

        match = re.fullmatch(r"b(\d+)", path.name)
        if match is None:
            continue

        yield int(match.group(1)), path


def get_config_dir(version=None, configs_dir=CONFIGS_DIR):
    current_version = get_blender_version_number(version)
    candidates = [
        (config_version, path)
        for config_version, path in iter_config_dirs(configs_dir)
        if config_version <= current_version
    ]

    if not candidates:
        return None

    return max(candidates, key=lambda item: item[0])[1]


def get_keymap_source(version=None):
    config_dir = get_config_dir(version)
    if config_dir is None:
        return None

    source = config_dir / KEYMAP_FILE
    if not source.is_file():
        return None

    return source


def get_startup_source(version=None):
    config_dir = get_config_dir(version)
    if config_dir is None:
        return None

    source = config_dir / STARTUP_FILE
    if not source.is_file():
        return None

    return source


def iter_startup_sources(configs_dir=CONFIGS_DIR):
    for _, config_dir in iter_config_dirs(configs_dir):
        source = config_dir / STARTUP_FILE
        if source.is_file():
            yield source


def get_keyconfig_dir(create=True):
    path = bpy.utils.user_resource(
        "SCRIPTS", path="presets/keyconfig", create=create
    )
    if not path:
        return None

    return Path(path)


def get_startup_dir(create=True):
    path = bpy.utils.user_resource("CONFIG", create=create)
    if not path:
        return None

    return Path(path)


def install_keymap_preset():
    source = get_keymap_source()
    if source is None:
        print("Omoospace keymap preset source not found.")
        return False

    target_dir = get_keyconfig_dir()
    if target_dir is None:
        print("Blender user keyconfig preset directory not found.")
        return False

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / KEYMAP_FILE
        if target.exists() and target.read_bytes() == source.read_bytes():
            return True

        shutil.copy2(source, target)
        return True
    except OSError as error:
        print(f"Failed to install Omoospace keymap preset: {error}")
        return False


def remove_keymap_preset():
    target_dir = get_keyconfig_dir(create=False)
    if target_dir is None:
        return False

    target = target_dir / KEYMAP_FILE
    if not target.exists():
        return True

    try:
        target.unlink()
        return True
    except OSError as error:
        print(f"Failed to remove Omoospace keymap preset: {error}")
        return False


def install_startup_file():
    source = get_startup_source()
    if source is None:
        return False, "Omoospace startup source not found."

    target_dir = get_startup_dir()
    if target_dir is None:
        return False, "Blender user startup directory not found."

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / STARTUP_FILE
        backup = target_dir / STARTUP_BACKUP_FILE

        if target.exists() and not backup.exists():
            shutil.copy2(target, backup)

        shutil.copy2(source, target)
        return True, f"Installed Omoospace startup file to {target}"
    except OSError as error:
        return False, f"Failed to install Omoospace startup file: {error}"


def restore_startup_file():
    target_dir = get_startup_dir(create=False)
    if target_dir is None:
        return False

    target = target_dir / STARTUP_FILE
    backup = target_dir / STARTUP_BACKUP_FILE
    if not backup.exists():
        if is_bundled_startup_file(target):
            try:
                target.unlink()
                return True
            except OSError as error:
                print(f"Failed to remove Omoospace startup file: {error}")
                return False

        return True

    try:
        if target.exists():
            target.unlink()
        backup.rename(target)
        return True
    except OSError as error:
        print(f"Failed to restore Blender startup file: {error}")
        return False


def is_bundled_startup_file(path):
    if not path.exists():
        return False

    try:
        content = path.read_bytes()
        return any(content == source.read_bytes() for source in iter_startup_sources())
    except OSError as error:
        print(f"Failed to inspect Blender startup file: {error}")
        return False


def restore_installed_configs():
    remove_keymap_preset()
    restore_startup_file()
