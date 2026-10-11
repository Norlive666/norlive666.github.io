# GNOME 实用扩展推荐

推荐、顺便记录一下本人使用的gnome拓展，可以极大的美观、简化桌面，提高便捷性。

- 生成时间：2026-10-11
- 桌面版本：GNOME Shell 50.5
- 范围：当前用户的 GNOME Shell 扩展，不包含浏览器扩展和编辑器插件。
- 数据来源：本机扩展元数据和 GNOME 的实时扩展状态；用途根据扩展自带说明整理。

## 扩展详情

| 扩展                        | 主要用途      | 运行会话报告版本  |
| ------------------------- | --------- | --------- |
| Clipman Clipboard Monitor | 剪贴板历史集成   | 7         |
| Removable Drive Menu      | 移动设备菜单    | 50.4 (82) |
| Just Perfection           | 桌面外观与行为调整 | 37        |
| Input Method Panel        | 输入法面板     | 92        |
| Logo Menu                 | 顶栏标志菜单    | 25.2 (45) |
| Tiling Shell              | 窗口平铺管理    | 17.3 (76) |

### Clipman Clipboard Monitor

监听 Wayland 下的剪贴板变化并传给 Clipman 后台，同时提供模拟粘贴和窗口定位功能。历史列表由 Clipman 应用提供，扩展需要 clipman.service 配合运行。

- 标识：`clipman@clipman.com`
- 安装位置：`/home/norlive/.local/share/gnome-shell/extensions/clipman@clipman.com`
- 项目：[Clipman Clipboard Monitor](https://github.com/MohammedEl-sayedAhmed/clipman)

### Removable Drive Menu

在顶栏提供移动存储设备菜单，方便访问和卸载 U 盘、移动硬盘等设备。

- 标识：`drive-menu@gnome-shell-extensions.gcampax.github.com`
- 安装位置：`/home/norlive/.local/share/gnome-shell/extensions/drive-menu@gnome-shell-extensions.gcampax.github.com`
- 项目：[Removable Drive Menu](https://gitlab.gnome.org/GNOME/gnome-shell-extensions)

### Just Perfection

调整 GNOME Shell 的界面和行为，显示或隐藏界面元素。具体哪些调整生效取决于你的扩展设置。

- 标识：`just-perfection-desktop@just-perfection`
- 安装位置：`/home/norlive/.local/share/gnome-shell/extensions/just-perfection-desktop@just-perfection`
- 项目：[Just Perfection](https://gitlab.gnome.org/jrahmatzadeh/just-perfection)

### Input Method Panel

通过 KDE 的 Kimpanel 协议把输入法面板集成到 GNOME Shell，用于显示输入法状态、候选词等界面。实际功能取决于输入法是否提供该协议；扩展本身不是输入法引擎。本人搭配Fcitx5使用以取得更美观的输入栏以及更加好用的提示。

- 标识：`kimpanel@kde.org`
- 安装位置：`/home/norlive/.local/share/gnome-shell/extensions/kimpanel@kde.org`
- 项目：[Input Method Panel](https://github.com/wengxt/gnome-shell-extension-kimpanel)

### Logo Menu

在顶栏左侧放置可自定义的 Linux/BSD 标志和菜单，提供类似 macOS 的菜单入口。可配置活动入口、默认终端和软件中心，并支持强制退出功能。

- 标识：`logomenu@aryan_k`
- 安装位置：`/home/norlive/.local/share/gnome-shell/extensions/logomenu@aryan_k`
- 项目：[Logo Menu](https://github.com/Aryan20/Logomenu)

### Tiling Shell

把窗口按预设区域排列，支持自定义布局、多显示器、自动平铺和快捷键，并提供类似 Windows 11 的贴靠辅助。适合同时查看多个窗口。

- 标识：`tilingshell@ferrarodomenico.com`
- 安装位置：`/home/norlive/.local/share/gnome-shell/extensions/tilingshell@ferrarodomenico.com`
- 项目：[Tiling Shell](https://github.com/domferr/tilingshell)
