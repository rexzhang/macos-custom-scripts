# Hammerspoon

## Install

- 符号连接 `hammerspoon` 目录到目录 `~/.hammerspoon`

## 模块

### 半角(`modules.banjiao`)

> 在撰写 MarkDown 文档时,需要在中文输入法模式下键入大量的 MarkDown 控制符;但这些控制符需要使用半角

- 键盘输入内容全角符号自动替换为半角
- 通过修改` app_map``replace_map `这两个字典调整脚本的行为

### Apple Music(`modules.applemusic`)

> 锁屏时自动暂停,解锁后自动继续播放

#### 权限问题

- 系统设置 > 隐私与安全 > 辅助功能，勾选 Hammerspoon
- 如果不勾选不会主动触发权限请求
