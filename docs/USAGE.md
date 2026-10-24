# 使用指南

## 在支持 v2 的 Pets 流程中使用

1. 保存仓库中的 `assets/spritesheet.png`，不要另存为 JPG，不要缩放。
2. 将 PNG 提供给支持自定义 v2 图集的 Pets 创建／导入流程，要求先校验尺寸、透明背景和帧布局，再创建宠物。
3. 在自己的客户端中刷新宠物列表，选择新宠物。下载本仓库不会自动改变账号中的宠物选择。
4. 桌面悬浮宠物通常由 Settings → Pets、Show pet 或 `/pet` 显示；Windows 的默认全局快捷键是 Win + Alt + P。以 [当前官方文档](https://learn.chatgpt.com/docs/pets) 和客户端可见功能为准。

网页内宠物和桌面悬浮窗口的入口、表现可能不同。部分上传界面只接受 v1 图集；本项目的图集为 v2，须使用对应的支持流程。

## 查看动画

`previews/all-states.gif` 可直接播放基础动作，`all-states.mp4` 是视频副本。`look-loop.gif` 显示 16 向视线，`idle-jump-idle.gif` 检查落地衔接。单个状态的 GIF 位于 `previews/states/`。

## 修改与重组

在仓库根目录运行：

```bash
python -m pip install -r requirements.txt
python scripts/pet_assets.py extract assets/spritesheet.png --out exported-frames
```

保持单帧的 192 × 208 尺寸、透明背景和原有文件名；移动画面时保留完整的发焰碎片，不要将各帧分别放大到填满单元格。左右色块不对称，直接镜像会改变角色细节。

```bash
python scripts/pet_assets.py assemble exported-frames --out build/spritesheet.png
python scripts/pet_assets.py validate build/spritesheet.png
```

输出路径必须为新的文件或空目录，工具不会覆盖已有素材。重组后的图片仍需播放检查，并通过目标 Pets 导入流程校验。

## 常见情况

- **宠物不出现**：检查客户端的 Pets 列表、显示开关、版本与工作区功能。
- **宠物不动**：检查系统是否启用了减少动态效果；客户端可能因此显示静帧。
- **上传尺寸不接受**：确认入口支持 1536 × 2288 的 v2 图集；不要将 v2 图片直接压缩成 v1 高度。
- **只想看预览**：直接打开 GIF 或 MP4，无需 Python 环境。
