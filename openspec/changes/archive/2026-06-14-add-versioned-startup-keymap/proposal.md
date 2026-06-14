## Why

Omoospace Blender 插件已经随包分发了按 Blender 版本区分的默认配置文件，包括 keymap 文件 `Omoospace.py` 和 startup file `startup.blend`。目前这些配置不会在插件注册后自动对用户可用，用户需要手动查找、复制或安装，容易选错版本，也不利于跨平台使用。

插件需要在注册后把匹配当前 Blender 版本的 keymap 安装到 Blender 用户配置目录，并在 `File > Defaults` 菜单顶部提供 `Use Omoospace Startup`，让用户可以把随插件分发的 startup file 安装为 Blender 用户 startup file。

## What Changes

1. 新增按 Blender 版本选择配置目录的逻辑，从 `src/omoospaceblender/configs/b*` 中选择不高于当前 Blender 主次版本的最高版本。
2. 插件注册时复制所选目录中的 `Omoospace.py` 到 Blender 用户 keyconfig presets 目录。
3. 使用 Blender API 获取用户配置路径，keymap 使用 `bpy.utils.user_resource("SCRIPTS", path="presets/keyconfig", create=True)`，startup 使用 `bpy.utils.user_resource("CONFIG", create=True)`。
4. 新增 `Use Omoospace Startup` operator，把所选目录中的 `startup.blend` 复制到 Blender 用户配置目录并替换用户 startup file。
5. 替换 startup file 前，如果用户配置目录中已有 `startup.blend`，先备份为 `startup.bak.blend`。
6. 在 `File > Defaults` 菜单顶部插入 `Use Omoospace Startup` 菜单项，并在其下方添加分界线。
7. 注销插件时移除菜单项、删除已安装的 keymap preset，并在存在备份时恢复原来的 startup file。

## Capabilities

### New Capabilities

- `versioned-default-configs`: 根据当前 Blender 版本选择并安装 Omoospace keymap preset，同时提供把 Omoospace startup file 安装为用户 startup file 的菜单入口。

## Impact

- **New file**: `src/omoospaceblender/default_configs.py`，集中处理版本目录选择、keymap 安装、startup 安装和恢复。
- **Modified files**: `src/omoospaceblender/menus.py`，添加 `File > Defaults` 菜单入口注册和注销。
- **Modified files**: `src/omoospaceblender/operators.py`，新增安装 Omoospace startup file 的 operator。
- **Modified files**: `src/omoospaceblender/__init__.py`，在插件注册流程中安装 keymap preset，并在注销流程中清理 keymap 与恢复 startup。
- **No new dependency**: 仅使用 Python 标准库和 Blender `bpy` API。
- **Behavior change**: 用户点击 `Use Omoospace Startup` 会替换 Blender 用户 startup file，但不会打开该文件或替换当前 scene。
