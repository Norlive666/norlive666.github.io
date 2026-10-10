# VSCode Vim 快捷键配置记录

记录日期：2026-09-20

## 背景

在 VSCode 里装了 VSCodeVim 扩展，需要一套「常用、好用」的快捷键。本文件记录这次改了哪些地方、为什么这么改，以及怎么回退。

## 环境

- 编辑器：VSCode（`/usr/bin/code`）
- 扩展：VSCodeVim `vscodevim.vim` 1.32.4
- 输入法：fcitx5
- 配置文件：`~/.config/Code/User/settings.json`（**全局用户配置**，所有项目通用）

## 改动范围

只改了一个文件：`~/.config/Code/User/settings.json`。

原有的 5 项设置（字号、字体连字、Claude Code 面板位置、Dev Containers 两项）全部保留，在其后追加 Vim 相关配置。没有新建项目级 `.vscode/` 目录，所以在 `car_f4`、`h723_test` 这些项目里都是同一套快捷键。

配置里写了中文注释。VSCode 的 `settings.json` 支持注释（JSONC），随便改不会报错。

### 可靠性说明

所有设置项名称都对照已安装扩展的 `package.json` 校对过；所有 VSCode 命令 ID 都在本机 `/usr/share/code` 里 grep 确认过存在。命令 ID 写错的话按键会静默失效，所以这一步是必须的。

## 一、Vim 基础行为

| 设置 | 值 | 作用 |
| --- | --- | --- |
| `vim.leader` | `<space>` | leader 键改成空格，比默认的反斜杠好按 |
| `vim.useSystemClipboard` | `true` | `y` 复制的内容直接进系统剪贴板，能和浏览器、终端互相粘贴 |
| `vim.incsearch` / `vim.hlsearch` | `true` | 搜索实时预览 + 所有匹配高亮 |
| `vim.ignorecase` / `vim.smartcase` | `true` | 全小写搜索忽略大小写，含大写则严格匹配 |
| `vim.timeout` | `500` | 映射等待时间从 1000ms 调短，按键更跟手 |
| `vim.whichwrap` | `b,s,<,>,[,]` | 方向键和 `[` `]` 可以跨行移动；`h` `l` 保持原生不跨行 |
| `vim.highlightedyank.enable` | `true` | 复制时闪一下高亮，知道复制了哪一段 |
| `vim.cursorStylePerMode.*` | 方块 / 细线 | 普通模式方块光标，插入模式细线，一眼看出当前模式 |
| `vim.showmodename` / `vim.showcmd` | `true` | 状态栏显示当前模式和正在输入的命令 |
| `vim.handleKeys` | `<C-s>` `<C-z>` `<C-f>` = `false` | 这三个 Ctrl 键交回 VSCode 处理 |
| `extensions.experimental.affinity` | `vscodevim.vim: 1` | 官方推荐的性能优化 |

关于 `vim.handleKeys`：这里的 `false` 表示**交给 VSCode 处理**，`true` 表示由 Vim 接管。

- `Ctrl+S` = 普通保存，`Ctrl+Z` = 普通撤销，不用记 Vim 那套
- `Ctrl+F` = VSCode 原生「文件内查找」，比 Vim 的翻页更常用（翻页还有 `Ctrl+D` / `Ctrl+U`）

## 二、配合 Vim 的编辑器设置

| 设置 | 值 | 作用 |
| --- | --- | --- |
| `editor.lineNumbers` | `relative` | 相对行号，显示「离光标几行」，配合 `12k`、`d8j` 特别好用 |
| `vim.smartRelativeLine` | `true` | 插入模式自动切回绝对行号 |
| `editor.cursorSurroundingLines` | `8` | 相当于 Vim 的 `scrolloff=8`，光标永远不贴屏幕边缘 |
| `editor.cursorSurroundingLinesStyle` | `all` | 让上面那条在所有模式下都生效 |
| `editor.renderLineHighlight` | `all` | 高亮当前行号 |

## 三、快捷键速查

`<leader>` = **空格**。下面每条都是「空格 + 一个键」，没有前缀冲突，不会卡顿。

### 文件 / 查找

| 按键 | 功能 |
| --- | --- |
| `<空格>w` / `<空格>W` | 保存 / 全部保存 |
| `<空格>q` | 关闭当前标签页 |
| `<空格>n` | 新建文件 |
| `<空格>f` | 按文件名快速跳转（等于 `Ctrl+P`） |
| `<空格>s` | 全项目搜索（等于 `Ctrl+Shift+F`） |
| `<空格>p` | 命令面板（等于 `Ctrl+Shift+P`） |
| `<空格>h` | 清除搜索高亮（Vim 的 `:noh`） |

### 界面 / 分屏

| 按键 | 功能 |
| --- | --- |
| `<空格>e` / `<空格>E` | 开关侧边栏 / 光标跳到资源管理器 |
| `<空格>t` | 终端开关 |
| `<空格>v` / `<空格>V` | 向右分屏 / 向下分屏 |
| `Ctrl+h/j/k/l` | 在分屏之间跳转（normal 和 visual 模式都可用） |

### 写代码（依赖语言服务）

| 按键 | 功能 |
| --- | --- |
| `<空格>a` | 代码操作 / 快速修复 |
| `<空格>r` | 重命名符号 |
| `<空格>F` | 格式化整个文件 |
| `gd` / `gD` | 跳转到定义 / 悬浮预览定义（不跳走） |
| `gr` | 查找所有引用 |
| `gh` / `gO` / `gi` | 悬浮文档 / 大纲 / 回到上次插入位置（插件自带，未改动） |

### 跳转与重复

| 按键 | 功能 |
| --- | --- |
| `[d` / `]d` | 上一个 / 下一个错误警告 |
| `[b` / `]b` | 上一个 / 下一个标签页 |
| `jk`（插入模式连按） | 等于 `Esc`，手不离开主键区 |
| `Y` | 复制到行尾（原生 Vim 的 `Y` 等于 `yy`，反直觉） |
| `H` / `L`（操作符模式） | `dH` 删到行首、`yL` 复制到行尾，比 `d0` / `y$` 好按 |
| `>` / `<`（可视模式） | 缩进后保持选中，可以连按 |

## 四、如何生效

配置改完需要重启 VSCode 窗口：

```text
Ctrl+Shift+P → 输入 Reload Window → 回车
```

## 五、如何回退

### 只想去掉某一条快捷键

打开配置文件：

```text
Ctrl+Shift+P → Preferences: Open User Settings (JSON)
```

找到对应那一行删掉即可，比如觉得 `jk` 退插入模式别扭（打字偶尔会连出 `jk`），就把 `vim.insertModeKeyBindingsNonRecursive` 整段删掉。

### 全部恢复默认

删掉所有 `"vim.` 开头的行、`"editor.lineNumbers"`、`"editor.cursorSurroundingLines"`、`"editor.renderLineHighlight"`、`"editor.cursorSurroundingLinesStyle"`、`"extensions.experimental.affinity"` 这几项，剩下的就是改动前的状态：

```json
{
    "editor.fontSize": 16,
    "editor.fontLigatures": false,
    "claudeCode.preferredLocation": "panel",
    "containers.containerClient": "com.microsoft.visualstudio.containers.docker",
    "containers.orchestratorClient": "com.microsoft.visualstudio.orchestrators.dockercompose"
}
```

## 六、预留但未启用的选项

以下几项已经写在配置文件里，但处于注释状态，去掉 `//` 就能用。

### 中文输入法自动切换

效果是普通模式自动切英文、插入模式自动切回中文。**当前未启用**，原因：VSCodeVim 需要一个「按名字切换输入法」的命令，而 `fcitx5-remote` 只能返回 `1` / `2` 这种序号，直接填进去不会生效，需要先写一个小脚本中转。

需要的话可以后续补上，配置里的注释位置已经留好。

### 其他

| 选项 | 说明 |
| --- | --- |
| `vim.easymotion` | `<leader><leader>w` 之类全屏范围内跳转，跳得远时很好用 |
| `vim.sneak` | `s` + 两个字符快速跳转/删除，可以替代 `f` / `t` |
| `vim.gdefault` | 打开后 `:s/a/b/` 默认就是全局替换，不用打最后的 `g` |

## 附：完整配置内容

以下是 2026-09-20 配置完成时的快照。**实际生效的是 `~/.config/Code/User/settings.json`**，两边不一致时以那个文件为准。

```jsonc
{
    // ===================== 原有设置 =====================
    "editor.fontSize": 16,
    "editor.fontLigatures": false,
    "claudeCode.preferredLocation": "panel",
    "containers.containerClient": "com.microsoft.visualstudio.containers.docker",
    "containers.orchestratorClient": "com.microsoft.visualstudio.orchestrators.dockercompose",

    // ===================== Vim 基础行为 =====================
    // leader 键设为空格（最常用的方案，比默认的反斜杠好按太多）
    "vim.leader": "<space>",

    // y 复制的内容直接进系统剪贴板，可以和浏览器/终端互相粘贴
    "vim.useSystemClipboard": true,

    // 搜索时实时高亮 + 全部匹配高亮，大小写智能判断
    // （全小写 = 忽略大小写；含大写 = 严格匹配）
    "vim.incsearch": true,
    "vim.hlsearch": true,
    "vim.ignorecase": true,
    "vim.smartcase": true,

    // 映射的等待时间调短一点，按键更跟手
    "vim.timeout": 500,

    // 光标允许用方向键 / [ ] 跨行移动（h l 保持 Vim 原生行为，不跨行）
    "vim.whichwrap": "b,s,<,>,[,]",

    // 复制时闪一下，知道自己复制了哪一段
    "vim.highlightedyank.enable": true,
    "vim.highlightedyank.duration": 150,

    // 不同模式用不同光标形状：普通模式方块，插入模式细线
    "vim.cursorStylePerMode.normal": "block",
    "vim.cursorStylePerMode.insert": "line-thin",
    "vim.cursorStylePerMode.visual": "block-outline",

    // 状态栏显示当前模式 / 正在输入的命令
    "vim.showmodename": true,
    "vim.showcmd": true,

    // Ctrl+S / Ctrl+Z 交回 VSCode（就是最普通的保存和撤销，不用记 Vim 的那套）
    // 把 Ctrl+F 还给 VSCode 原生的「文件内查找」，比 Vim 的翻页更常用
    // （翻页还有 Ctrl+D / Ctrl+U 可以用）
    // 说明：这里的 false = 交给 VSCode 处理，true = 由 Vim 接管
    "vim.handleKeys": {
        "<C-s>": false,
        "<C-z>": false,
        "<C-f>": false
    },

    // VSCodeVim 官方推荐的性能优化：让 Vim 扩展优先被唤醒
    "extensions.experimental.affinity": {
        "vscodevim.vim": 1
    },

    // ===================== 配合 Vim 的编辑器设置 =====================
    // 相对行号：普通模式下显示「离光标几行」，配合 5j / 12k / d8j 极其好用
    "editor.lineNumbers": "relative",
    "vim.smartRelativeLine": true, // 插入模式自动切回绝对行号
    "editor.renderLineHighlight": "all",
    "editor.cursorSurroundingLines": 8, // 相当于 Vim 的 scrolloff=8，光标永远不贴边
    "editor.cursorSurroundingLinesStyle": "all",

    // ===================== Leader 快捷键 =====================
    // <leader> = 空格。下面每条都是「空格 + 一个键」，没有前缀冲突，不卡顿
    "vim.normalModeKeyBindingsNonRecursive": [
        // ---- 文件 ----
        { "before": ["<leader>", "w"], "commands": ["workbench.action.files.save"] }, // 保存
        { "before": ["<leader>", "W"], "commands": ["workbench.action.files.saveAll"] }, // 全部保存
        { "before": ["<leader>", "q"], "commands": ["workbench.action.closeActiveEditor"] }, // 关闭当前标签
        { "before": ["<leader>", "n"], "commands": ["workbench.action.files.newUntitledFile"] }, // 新建文件

        // ---- 查找 / 命令 ----
        { "before": ["<leader>", "f"], "commands": ["workbench.action.quickOpen"] }, // 按文件名快速跳转（= Ctrl+P）
        { "before": ["<leader>", "s"], "commands": ["workbench.action.findInFiles"] }, // 全项目搜索（= Ctrl+Shift+F）
        { "before": ["<leader>", "p"], "commands": ["workbench.action.showCommands"] }, // 命令面板（= Ctrl+Shift+P）
        { "before": ["<leader>", "h"], "commands": [":nohlsearch"] }, // 清除搜索高亮（Vim 的 :noh）

        // ---- 界面 ----
        { "before": ["<leader>", "e"], "commands": ["workbench.action.toggleSidebarVisibility"] }, // 开关侧边栏
        { "before": ["<leader>", "E"], "commands": ["workbench.action.focusSideBar"] }, // 光标跳到资源管理器
        { "before": ["<leader>", "t"], "commands": ["workbench.action.terminal.toggleTerminal"] }, // 终端开关

        // ---- 分屏 ----
        { "before": ["<leader>", "v"], "commands": ["workbench.action.splitEditorRight"] }, // 向右分屏
        { "before": ["<leader>", "V"], "commands": ["workbench.action.splitEditorDown"] }, // 向下分屏

        // ---- 写代码（依赖语言服务，写 C/C++ 装了 clangd 或 C/C++ 扩展后可用）----
        { "before": ["<leader>", "a"], "commands": ["editor.action.codeAction"] }, // 代码操作 / 快速修复
        { "before": ["<leader>", "r"], "commands": ["editor.action.rename"] }, // 重命名符号
        { "before": ["<leader>", "F"], "commands": ["editor.action.formatDocument"] }, // 格式化整个文件

        // ---- g 系列：和原生 Vim 手感一致的跳转 ----
        { "before": ["g", "d"], "commands": ["editor.action.revealDefinition"] }, // 跳转到定义
        { "before": ["g", "D"], "commands": ["editor.action.peekDefinition"] }, // 悬浮预览定义（不跳走）
        { "before": ["g", "r"], "commands": ["editor.action.goToReferences"] }, // 查找所有引用
        // （gh 悬浮文档、gO 大纲、gi 回到上次插入位置 是插件自带的，不用配）

        // ---- [ / ] 系列：成对的「上一个 / 下一个」----
        { "before": ["[", "d"], "commands": ["editor.action.marker.prev"] }, // 上一个错误/警告
        { "before": ["]", "d"], "commands": ["editor.action.marker.next"] }, // 下一个错误/警告
        { "before": ["[", "b"], "commands": ["workbench.action.previousEditor"] }, // 上一个标签页
        { "before": ["]", "b"], "commands": ["workbench.action.nextEditor"] }, // 下一个标签页

        // ---- 分屏之间跳转：Ctrl + hjkl，和 tmux 一致，比 Vim 的 Ctrl+W hjkl 顺手 ----
        { "before": ["<C-h>"], "commands": ["workbench.action.focusLeftGroup"] },
        { "before": ["<C-j>"], "commands": ["workbench.action.focusBelowGroup"] },
        { "before": ["<C-k>"], "commands": ["workbench.action.focusAboveGroup"] },
        { "before": ["<C-l>"], "commands": ["workbench.action.focusRightGroup"] },

        // ---- Y 复制到行尾（保持和 C / D 一致；原生 Vim 的 Y 等于 yy，反直觉）----
        { "before": ["Y"], "after": ["y", "$"] }
    ],

    // 可视模式下也支持 Ctrl+hjkl 切分屏
    "vim.visualModeKeyBindingsNonRecursive": [
        { "before": ["<C-h>"], "commands": ["workbench.action.focusLeftGroup"] },
        { "before": ["<C-j>"], "commands": ["workbench.action.focusBelowGroup"] },
        { "before": ["<C-k>"], "commands": ["workbench.action.focusAboveGroup"] },
        { "before": ["<C-l>"], "commands": ["workbench.action.focusRightGroup"] },
        // 缩进后保持选中，可以连续按 > 一直往里缩
        { "before": [">"], "after": [">", "g", "v"] },
        { "before": ["<"], "after": ["<", "g", "v"] }
    ],

    // 操作符等待模式：dH 删到行首、yL 复制到行尾，比 d0 / y$ 好按
    "vim.operatorPendingModeKeyBindingsNonRecursive": [
        { "before": ["H"], "after": ["^"] },
        { "before": ["L"], "after": ["$"] }
    ],

    // 插入模式下连按 jk 等于 Esc，手不用离开主键区
    // 如果觉得别扭（比如偶尔会打出 "jk"），把这一整段删掉即可
    "vim.insertModeKeyBindingsNonRecursive": [
        { "before": ["j", "k"], "after": ["<Esc>"] }
    ]

    // ===================== 可选：中文输入法自动切换 =====================
    // 效果：普通模式自动切英文，插入模式自动切回中文。你的机器用的是 fcitx5。
    // VSCodeVim 需要一个能「按名字」切换输入法的命令，而 fcitx5-remote 只能返回
    // 1/2 这种序号，没法直接填，得先用小脚本中转。想启用的话跟我说，我写好再打开下面几行。
    //
    // "vim.autoSwitchInputMethod.enable": true,
    // "vim.autoSwitchInputMethod.defaultIM": "keyboard-us",
    // "vim.autoSwitchInputMethod.obtainIMCmd": "/home/norlive/.local/bin/im-get",
    // "vim.autoSwitchInputMethod.switchIMCmd": "/home/norlive/.local/bin/im-set {im}"

    // ===================== 其他可选项（默认关，按需打开）=====================
    // "vim.easymotion": true,   // <leader><leader>w 之类，全屏范围内跳转，跳得远时很好用
    // "vim.sneak": true,        // s + 两个字符 = 快速跳转/删除，可以替代 f/t
    // "vim.gdefault": true,     // 打开后 :s/a/b/ 默认就是全局替换，不用打最后的 g
}
```
