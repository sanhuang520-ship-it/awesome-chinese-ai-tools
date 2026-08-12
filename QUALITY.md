# 本站原创 Skill：质量与安全标签

> 静态检查日期：**2026-08-12** · 机器可读记录：[data/quality.json](data/quality.json) · 校验脚本：[scripts/check_quality.py](scripts/check_quality.py)

这不是安全认证，也不保证 AI 输出正确。它回答的是安装前最基本的几个问题：仓库里带了什么文件、有没有独立可执行脚本、演示是否需要联网、哪些领域需要人工复核。

## 检查结论

- 13 个本站原创 Skill 均已覆盖。
- 当前没有 `.py`、`.js`、`.sh` 等独立可执行脚本随 Skill 打包。
- `guofeng-threejs` 的两个浏览器 Demo 会从 `unpkg.com` 加载固定版本 `three@0.170.0`；其余 Skill 没有发现运行时网络依赖。
- 部分 Skill 带 Markdown 参考资料、CSS、HTML Demo 或 DESIGN.md 模板；“没有独立脚本”不等于内容无需审查。

## 明细

| Skill | 随附内容 | 独立可执行脚本 | 运行时联网 | 需要人工注意的边界 |
|---|---|---:|---:|---|
| `ai-learning-coach` | 指令、参考模板 | 无 | 无 | 医疗、法律、投资决策 |
| `book-digest-cn` | 指令 | 无 | 无 | 不编造未提供的书籍内容 |
| `bookkeeping-cn` | 指令 | 无 | 无 | 流水隐私；不做税务、投资建议 |
| `chinese-design-md` | 指令、8 套模板 | 无 | 无 | 字体授权 |
| `chinese-lesson-plan` | 指令、参考模板 | 无 | 无 | 教材与课程事实需核对来源 |
| `chinese-typography` | 指令 | 无 | 无 | 字体授权、地区排版规范 |
| `chinese-web-themes` | 指令、本地 CSS/HTML Demo | 无 | 无 | 字体授权 |
| `chinese-work-report` | 指令 | 无 | 无 | 不得编造业务数据 |
| `ecommerce-copywriting` | 指令 | 无 | 无 | 广告宣称与受监管商品 |
| `github-readme-cn` | 指令、实测数据 | 无 | 无 | 增长相关性不等于因果 |
| `guochao-visual-cn` | 指令、纹样参考 | 无 | 无 | 文化准确性、艺术家风格边界 |
| `guofeng-threejs` | 指令、浏览器 Demo | 无 | **有** | Demo 从 unpkg 加载 Three.js |
| `homework-tutor-cn` | 指令 | 无 | 无 | 不提供可直接抄写的答案 |

## 如何理解这些标签

1. **运行时联网**只指随附材料在运行时主动请求第三方资源；SKILL.md 中普通文档链接不计入。
2. HTML 内联 JavaScript 属于浏览器 Demo 的主动内容，但本表的“独立可执行脚本”专指 `.py`、`.js`、`.sh` 等脚本文件。
3. 静态检查无法证明提示注入安全、输出事实正确或第三方 CDN 永远可信。涉及真实账户、生产环境或敏感数据时仍需隔离测试和最小权限。
4. 第三方收录的 171 个 Skill 尚未完成同等级审查，不能套用本站原创的结论。
