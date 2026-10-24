# Capri · 摩羯桌宠

**碎片发焰，会变色的小 AI。**

一个以《赛博朋克：边缘行者 2》Capri（摩羯）为灵感的非官方桌宠素材项目，面向支持 v2 精灵图集的 ChatGPT / Pets 工作流。包含透明图集、动画预览、生成简报，以及可独立运行的帧提取和重组工具。

[English](README.en.md) · [使用指南](docs/USAGE.md) · [素材格式](docs/FORMAT.md) · [授权说明](ASSET_RIGHTS.md)

![Capri 动画预览](previews/all-states.gif)

## 角色特点

- **断裂的火焰头部**：保留红色几何发焰、透明间隙和悬浮碎片。
- **会变色的脸**：常态为绿色，受挫动画切换为白色，再恢复绿色。
- **不对称身体色块**：红、黑、绿色几何面保持左右差异，左右移动分别绘制。
- **9 组动作、16 向视线**：眨眼、跑动、招手、跳跃、受挫、等待、思考和检查。

角色性格通过俏皮、慵懒和疑惑的视觉表情呈现。桌面悬浮、拖动、任务状态和光标交互由宿主客户端提供。

## 立即使用

1. 下载 [透明精灵图集](assets/spritesheet.png)，保持原始尺寸和透明背景。
2. 在支持 **v2（1536 × 2288）图集** 的 Pets 导入／创建流程中，提供该 PNG，先校验再创建宠物。
3. 在客户端的 **Settings → Pets** 中刷新并选择宠物；桌面版可通过 **Show pet** 或 `/pet` 显示。Windows 默认唤出快捷键为 **Win + Alt + P**。入口以当前客户端为准，参见 [OpenAI 官方 Pets 文档](https://learn.chatgpt.com/docs/pets)。

当前图集是 v2。部分界面仍只接受 v1（1536 × 1872），此时需要升级或使用支持 v2 的导入流程；不要直接缩放图片来适配。仓库不包含账号绑定的宠物 ID，下载文件后需要在自己的账号中导入。

## 动作与预览

| 动作 | 帧数 | 视觉表现 |
| --- | ---: | --- |
| 待机 | 6 | 眨眼、轻微呼吸 |
| 向右移动 | 8 | 朝右交替迈步 |
| 向左移动 | 8 | 朝左交替迈步 |
| 招手 | 4 | 挥手与眨眼 |
| 跳跃 | 5 | 蓄力、离地、落回基线 |
| 受挫 | 8 | 绿色 → 白色 → 绿色脸 |
| 等待 | 6 | 合手、摊手，等待回应 |
| 思考／处理中 | 6 | 触碰太阳穴、手指思考动作 |
| 检查 | 6 | 托腮、观察、点头 |
| 视线 | 16 | 从上方开始顺时针环视 |

![四种表情与动作](previews/four-stills.png)

[视线循环](previews/look-loop.gif) · [跳跃衔接](previews/idle-jump-idle.gif) · [全部动作视频](previews/all-states.mp4)

部分相邻视线角度的区别较细微。绿色和白色脸来自参考图；本项目没有将其他颜色与情绪的对应关系标为官方设定。

## 修改素材

需要 Python 3.10+。只播放预览或导入 PNG 时不需要安装 Python。

```bash
git clone https://github.com/s263804-afk/capri-desktop-pet.git
cd capri-desktop-pet
python -m pip install -r requirements.txt

# 检查图集结构
python scripts/pet_assets.py validate assets/spritesheet.png

# 导出全部 73 帧，保留每格 192 × 208 和原始透明度
python scripts/pet_assets.py extract assets/spritesheet.png --out exported-frames

# 修改帧文件后，重组为新的 PNG
python scripts/pet_assets.py assemble exported-frames --out build/spritesheet.png

# 运行测试
python -m unittest discover -s tests -v
```

脚本不会自动裁切、缩放、镜像或删除悬浮火焰组件，也不会覆盖已有输出文件。结构检查与视觉检查的范围见 [素材格式说明](docs/FORMAT.md)。

## 项目结构

```text
assets/          透明图集、帧布局清单
previews/        GIF、MP4 和表情预览
prompts/         角色约束与各状态生成简报
scripts/         可移植的帧处理工具
tests/           透明度、布局和重组测试
docs/            使用、格式与发布说明
```

## 制作与来源

基础形象和动作使用 OpenAI 内置图像生成工具制作，随后进行透明背景处理、逐帧提取、注册和拼接。AI 图像生成具有随机性，提示词不能保证逐像素复现现有素材。

身体色块参考 [官方授权的 Capri 海报](https://displate.com/displate/11144097)，比例与表情参考用户提供的 Q 版图。原始参考 JPEG 和官方海报未打包进本仓库。详见 [来源与制作记录](docs/PROVENANCE.md)。

## 授权与贡献

**代码和项目说明采用 [MIT](LICENSE)；角色衍生素材不纳入 MIT 授权，见 [ASSET_RIGHTS.md](ASSET_RIGHTS.md)。** 公开仓库不代表取得了对原作角色、商标或第三方图像的再授权。

本项目为非官方同人作品，与 CD PROJEKT RED、TRIGGER、Netflix 或 OpenAI 无隶属或背书关系。使用原作相关内容时请同时查阅 [CD PROJEKT RED 同人内容指南](https://www.cdprojektred.com/en/fan-content) 及相关权利人的规则。

欢迎通过 Issue 或 Pull Request 改进动作衔接、视线可读性、文档和工具。贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。
