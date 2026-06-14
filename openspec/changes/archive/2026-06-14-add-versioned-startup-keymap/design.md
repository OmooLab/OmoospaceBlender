## Context

插件包内已有 `src/omoospaceblender/configs/b42`、`b45`、`b50` 等目录。目录名中的数字表示 Blender 主版本和次版本，例如 `b45` 对应 Blender 4.5。每个目录包含：

- `Omoospace.py`: Blender keymap preset 文件
- `startup.blend`: Omoospace startup file

Blender 用户配置目录在不同操作系统中不同，不应硬编码。Blender Python API 提供 `bpy.utils.user_resource()` 用于获取用户资源路径，其中：

- `bpy.utils.user_resource("SCRIPTS", path="presets/keyconfig", create=True)` 是 keyconfig preset 所在目录。
- `bpy.utils.user_resource("CONFIG", create=True)` 是用户 `startup.blend` 所在目录。

## Goals / Non-Goals

**Goals:**
- 注册插件后自动安装当前 Blender 版本适用的 `Omoospace.py` keymap preset
- 当精确版本目录不存在时，向下选择可用的最高版本目录
- 在 `File > Defaults` 菜单顶部添加 `Use Omoospace Startup`
- 用户点击菜单项后，把所选版本目录中的 `startup.blend` 替换为 Blender 用户配置目录中的 startup file
- 替换 startup file 前，如果用户配置目录中已有 `startup.blend`，先备份为 `startup.bak.blend`
- 保持跨平台路径处理，不硬编码 Windows、macOS 或 Linux 配置路径
- 注销插件时复原插件造成的配置变更：删除已安装的 keymap preset，并在存在备份时恢复原来的 startup file

**Non-Goals:**
- 不在注册插件时自动覆盖当前 Blender scene
- 不在点击菜单项时打开所选版本目录中的 `startup.blend`
- 不自动设置用户当前 active keymap
- 不生成或修改随插件分发的 `startup.blend` 与 `Omoospace.py` 内容

## Decisions

### 1. 用版本向下取策略选择配置目录

**Decision**: 根据 `bpy.app.version` 取 `(major, minor)`，转换为 `major * 10 + minor`，例如 Blender 4.5 转为 `45`。扫描 `configs` 下符合 `b\d+` 的目录，选择数值小于等于当前版本且最大的目录。

**Rationale**: 用户要求 Blender 4.3 没有 `b43` 时使用 `b42`。数值比较直接、可测试，也支持未来 `b50`、`b51` 等目录。

**Alternative**: 使用字符串排序选择目录。字符串排序在 `b9`、`b10` 等情况下可能产生错误顺序，不采用。

### 2. Keymap preset 安装使用 `bpy.utils.user_resource`

**Decision**: 使用 `bpy.utils.user_resource("SCRIPTS", path="presets/keyconfig", create=True)` 获取目标目录，再复制 `Omoospace.py`。

**Rationale**: 这是 Blender 提供的跨平台用户资源路径 API，可以避免为 Windows、macOS、Linux 分别维护配置路径。

**Alternative**: 直接操作 `bpy.context.window_manager.keyconfigs` 创建 keymap。现有输入是完整 keymap preset 文件，复制到 presets 目录更符合 Blender preset 使用方式，也避免重写 preset 内容。

### 3. Keymap 文件采用幂等覆盖复制

**Decision**: 注册插件时如果目标 `Omoospace.py` 不存在或内容不同，则复制；如果内容相同则跳过。复制失败时打印错误，不阻断插件注册。

**Rationale**: 用户升级插件或 Blender 版本后需要拿到新的 preset。覆盖同名插件 preset 是预期行为；失败不应导致插件无法启用。

**Alternative**: 只在目标不存在时复制。这样无法更新已安装 preset，不采用。

### 4. Startup file 通过显式菜单 operator 安装为用户 startup

**Decision**: 新增 `omoospace.load_startup` operator。用户点击 `Use Omoospace Startup` 后，解析所选版本目录中的 `startup.blend`，把它复制到 `bpy.utils.user_resource("CONFIG", create=True) / "startup.blend"`。如果目标 startup file 已存在，先备份为 `startup.bak.blend`，再执行替换。

**Rationale**: 用户要求点击后把所选版本目录中的 `startup.blend` 替换为新的 startup 文件，而不是打开它。复制到 Blender 用户 `CONFIG` 目录符合 Blender 默认 startup file 的存放方式，也避免当前 scene 被替换。

**Alternative**: 打开随插件分发的 startup file。该行为会替换当前打开文件，不符合需求。

### 5. 注销时恢复 startup 与 keymap

**Decision**: 插件注销时删除用户 keyconfig preset 目录中的 `Omoospace.py`。如果用户配置目录中存在 `startup.bak.blend`，则删除当前 `startup.blend` 并把 `startup.bak.blend` 恢复为 `startup.blend`。

**Rationale**: startup 和 keymap 都是插件安装到用户配置目录中的内容。注销时复原这些变更可以避免插件卸载后继续影响 Blender 默认行为。

**Trade-off**: 如果用户在安装 Omoospace startup 后手动修改了用户 `startup.blend`，注销时会被备份恢复覆盖。实现时可以只恢复存在备份的情况，并通过诊断信息说明行为。

### 6. 菜单入口注册在 `menus.py`

**Decision**: 在 `menus.py` 中新增 `FILE_DEFAULTS` draw function，并通过 `bpy.types.TOPBAR_MT_file_defaults.prepend(FILE_DEFAULTS)` 添加菜单入口。菜单项下方添加 separator，让它和 Blender 原有 defaults 操作分组。

**Rationale**: 当前项目已有 `menus.add()` 和 `menus.remove()` 统一管理菜单挂载，把新入口放在同一模块符合现有组织方式。

## Risks / Trade-offs

[Risk] 当前 Blender 版本低于所有配置目录，找不到可用配置。
**Mitigation**: 返回 `None` 并打印明确错误；keymap 安装跳过，startup operator 报告错误。

[Risk] 用户目录没有写权限或复制失败。
**Mitigation**: 捕获 `OSError`，打印错误或通过 `self.report` 提示，并允许插件继续注册。

[Risk] `bpy.types.TOPBAR_MT_file_defaults` 在某些 Blender 版本不可用。
**Mitigation**: 注册菜单前使用 `hasattr` 检查；不可用时跳过菜单注册并打印错误。

[Risk] 恢复备份会覆盖用户在安装 Omoospace startup 后对 startup file 的修改。
**Mitigation**: 只在存在 `startup.bak.blend` 时恢复，并把该限制写入实现说明和测试场景。
