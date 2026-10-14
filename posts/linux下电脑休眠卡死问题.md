# 电脑休眠问题

## 问题现象

电脑合上屏幕后进入休眠，再次打开屏幕时，系统可能卡死在锁屏界面，无法正常操作，只能强制重启。

## 设备与系统环境

- 设备：Lenovo Legion 笔记本
- 系统：Fedora Linux 44（GNOME Wayland）
- 显卡：NVIDIA GeForce RTX 5060 Laptop GPU
- NVIDIA 驱动：610.57.04
- 内核：Linux 7.1.13-200.fc44.x86_64
- 原休眠模式：`deep`（S3 深度睡眠）

## 原因分析

系统日志显示，问题发生在内核从 `deep`（S3）休眠状态恢复的过程中，而不是锁屏密码或锁屏界面本身。

主要依据：

- 多次休眠时出现音频控制器错误：`CORB reset timeout`。
- 正常唤醒时日志包含 `PM: suspend exit`。
- 故障发生时，日志停在 `PM: suspend entry (deep)`，没有后续的 `PM: suspend exit`。
- BIOS/ACPI 日志中存在固件错误。
- 电脑使用 NVIDIA 专有驱动，显卡、音频控制器、BIOS 与 S3 深度睡眠之间可能存在兼容性问题。

因此，最可能的原因是当前 Legion 固件及驱动组合与 Linux 的 `deep`（S3）睡眠模式兼容性不佳。

## 已验证的解决方案

将休眠模式由 `deep` 切换为 `s2idle` 后，合盖再打开可以正常恢复。

### 临时切换

运行：

```bash
echo s2idle | sudo tee /sys/power/mem_sleep
```

检查当前模式：

```bash
cat /sys/power/mem_sleep
```

如果输出如下，方括号中的 `s2idle` 表示当前已经启用：

```text
[s2idle] deep
```

临时设置会在重启后失效。

## 永久设置

在 Fedora 中，将 `s2idle` 加入所有已安装内核的启动参数：

```bash
sudo grubby --update-kernel=ALL --args=mem_sleep_default=s2idle
```

命令执行完成后重启电脑：

```bash
systemctl reboot
```

重启后验证：

```bash
cat /sys/power/mem_sleep
```

预期输出：

```text
[s2idle] deep
```

也可以检查当前内核命令行：

```bash
cat /proc/cmdline
```

其中应包含：

```text
mem_sleep_default=s2idle
```

## 回退方法

如果需要恢复原来的 `deep` 默认模式，删除该内核参数：

```bash
sudo grubby --update-kernel=ALL --remove-args=mem_sleep_default=s2idle
```

然后重启电脑，再运行以下命令检查：

```bash
cat /sys/power/mem_sleep
```

原模式通常显示为：

```text
s2idle [deep]
```

## 注意事项

- `s2idle` 的兼容性通常更好，但待机耗电可能高于 `deep`。
- 更新内核或 NVIDIA 驱动后，可以再次测试 `deep` 是否恢复正常。
- 如果使用 `s2idle` 后仍发生卡死，应收集上一次启动的内核日志：

```bash
journalctl -b -1 -k | grep -Ei 'suspend|resume|nvidia|drm|gpu|error|timeout'
```

