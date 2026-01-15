import json
from typing import Any
import bpy
from omoospace import Omoospace, Opath, extract_pathname

SUBSPACE_JSON = "omoospace_subspace.json"


def bpath_to_opath(bpath: str, blend_file: str = None) -> Opath:
    start = Opath(blend_file).parent if blend_file else None
    return Opath(bpy.path.abspath(bpath, start=start)).resolve()


def opath_to_bpath(path: Opath, blend_file: str = None) -> str:
    start = Opath(blend_file).parent if blend_file else None
    return bpy.path.relpath(str(path.resolve()), start=start)


def is_content(bpath: str):
    omoospace = get_omoospace()
    return omoospace.is_content(bpath_to_opath(bpath), False)


def is_sequence(bpath: str):
    path = bpath_to_opath(bpath)
    last = path.stem.split(".")[-1]
    return last.isnumeric() and len(last) >= 3


def get_type(cls):
    return type(cls).__name__


def copy_to(src, dir):
    src = Opath(src).resolve()
    dir = Opath(dir).resolve()

    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {src}")

    if src == dir / src.name:
        return src

    try:
        if "<UDIM>" in str(src):
            udims = src.parent.glob(src.name.replace("<UDIM>", "*"))
            for udim in udims:
                return Opath(udim).copy_to(dir)
        else:
            return Opath(src).copy_to(dir)
    except FileExistsError:
        pass
    except Exception as err:
        raise err


def get_omoospace():
    try:
        blend_path = Opath(bpy.data.filepath)
        omoospace = Omoospace(blend_path)
        return omoospace
    except:
        return None


def get_pathname():
    blend_path = Opath(bpy.data.filepath)
    return extract_pathname(blend_path)


def get_subspace_data(key: str) -> Any:
    # 检查文本数据块是否存在
    if SUBSPACE_JSON not in bpy.data.texts:
        bpy.data.texts.new(SUBSPACE_JSON)

    # 加载并解析数据
    subspace_text = bpy.data.texts[SUBSPACE_JSON]
    try:
        subspace_data = json.loads(subspace_text.as_string())
    except:
        subspace_data = {}

    return subspace_data.get(key, None)


def set_subspace_data(key: str, value: Any):
    # 获取或创建文本数据块
    if SUBSPACE_JSON not in bpy.data.texts:
        bpy.data.texts.new(SUBSPACE_JSON)

    subspace_text = bpy.data.texts[SUBSPACE_JSON]
    try:
        subspace_data = json.loads(subspace_text.as_string())
    except:
        subspace_data = {}

    subspace_data[key] = value

    subspace_text.clear()
    subspace_text.write(json.dumps(subspace_data, indent=4))
