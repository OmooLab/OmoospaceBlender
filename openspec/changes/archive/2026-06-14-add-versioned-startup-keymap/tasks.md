## 1. Add Versioned Config Resolver

- [x] 1.1 新增 `default_configs.py`
- [x] 1.2 实现扫描 `configs/b*` 目录的函数
- [x] 1.3 实现按 `bpy.app.version` 向下选择最高可用版本目录的函数
- [x] 1.4 为找不到可用目录、缺少文件等情况返回明确结果或错误信息

## 2. Install Keymap Preset on Register

- [x] 2.1 实现获取用户 keyconfig preset 目录的函数，使用 `bpy.utils.user_resource("SCRIPTS", path="presets/keyconfig", create=True)`
- [x] 2.2 实现 `Omoospace.py` 幂等复制逻辑
- [x] 2.3 在插件 `register()` 流程中调用 keymap 安装函数
- [x] 2.4 复制失败时捕获异常并打印错误，不阻断插件注册

## 3. Add Startup Installer Operator

- [x] 3.1 新增 `LoadOmoospaceStartup` operator
- [x] 3.2 operator 执行时解析当前版本对应的 `startup.blend`
- [x] 3.3 实现获取用户 startup 目录的函数，使用 `bpy.utils.user_resource("CONFIG", create=True)`
- [x] 3.4 替换用户 `startup.blend` 前，把已有文件备份为 `startup.bak.blend`
- [x] 3.5 把所选版本目录中的 `startup.blend` 复制为用户配置目录中的 `startup.blend`
- [x] 3.6 找不到 startup file 或复制失败时通过 `self.report` 提示错误

## 4. Restore Installed Configs on Unregister

- [x] 4.1 注销插件时删除用户 keyconfig preset 目录中的 `Omoospace.py`
- [x] 4.2 如果用户配置目录中存在 `startup.bak.blend`，注销时恢复为 `startup.blend`
- [x] 4.3 清理和恢复失败时捕获异常并打印错误，不阻断插件注销

## 5. Add File Defaults Menu Entry

- [x] 5.1 在 `menus.py` 新增 `FILE_DEFAULTS` draw function
- [x] 5.2 使用 `bpy.types.TOPBAR_MT_file_defaults.prepend(FILE_DEFAULTS)` 把菜单项放在顶部
- [x] 5.3 在 `menus.remove()` 中移除该菜单项
- [x] 5.4 对缺少 `TOPBAR_MT_file_defaults` 的 Blender 版本做兼容处理

## 6. Testing

- [x] 6.1 测试 Blender 4.5 选择 `configs/b45`
- [x] 6.2 测试 Blender 4.3 在没有 `b43` 时选择 `configs/b42`
- [x] 6.3 测试 keymap preset 被复制到用户 keyconfig preset 目录
- [x] 6.4 测试重复注册不会产生错误，且可更新已有 `Omoospace.py`
- [ ] 6.5 测试 `File > Defaults` 顶部出现 `Use Omoospace Startup`，且其下方有分界线
- [x] 6.6 测试点击菜单项会备份已有用户 `startup.blend` 并复制对应版本的 `startup.blend`
- [x] 6.7 测试点击菜单项不会打开随插件分发的 `startup.blend`，也不会替换当前 scene
- [x] 6.8 测试注销插件会删除 keymap preset，并在存在备份时恢复原来的 startup file
- [ ] 6.9 测试找不到配置目录、无写权限、缺少 startup file 时有可诊断的错误输出
