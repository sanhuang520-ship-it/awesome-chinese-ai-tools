# Awesome Chinese AI Tools 🇨🇳

> **AI 工具导航 + Skills 中文合集** —— 47 个工具标注真实免费额度、链接每日实测；87 个 Agent Skill 全部验证真实（含 30 个中文原创）

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![GitHub Stars](https://img.shields.io/github/stars/sanhuang520-ship-it/awesome-chinese-ai-tools?style=flat-square)](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/stargazers)
[![Last Update](https://img.shields.io/github/last-commit/sanhuang520-ship-it/awesome-chinese-ai-tools?style=flat-square&label=最近更新)](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/commits)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

🌐 **在线使用**：https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/

---

## 🎯 为什么用这个导航

市面上的 AI 导航站，要么堆满广告，要么信息过时、链接早就失效。这个项目只做三件事：

| 我们做的 | 别人常见的做法 |
|----------|----------------|
| ✅ **链接每天自动实测**，失效/迁移立刻修 | ❌ 收录后就不管了，点进去 404 |
| ✅ **只标真实免费额度**，付费明确写出来 | ❌ 模糊写「免费试用」，进去才发现要付费 |
| ✅ **不转述新闻**，只给官方公告页链接 | ❌ 转载未经核实的「今日爆炸新闻」 |

**真实修复记录**（都是自动检测发现的）：
- `cursor.sh` → `cursor.com` 域名迁移
- Windsurf 被 Cognition 收购、并入 Devin Desktop
- Flux `blackforestlabs.ai` → `bfl.ai` 迁移
- Runway `runwayml.com` → `runway.com` 迁移

---

---

## ✍️ 本站原创 Skill（5 个）

市面上的 Skill 资源基本都是英文的，中文场景几乎是空白。所以我们**自己写了这些**，
不是翻译、不是搬运，是针对中文用户的真实工作场景从零编写并持续维护的。

| Skill | 面向 | 做什么 |
|-------|------|--------|
| **[💰 记账整理助手](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/bookkeeping-cn)** | 个人 / 小店主 | 流水分类、收支表、预算跟踪；明确不做税务与投资建议 |
| **[📚 家长辅导助手](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/homework-tutor-cn)** | 中小学生家长 | 不给答案给引导话术，分学科方法；含「家长要发火时怎么办」 |
| **[📊 职场汇报助手](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-work-report)** | 全体职场人 | 周报/月报/述职/项目汇报，结论先行、卖点翻价值，含汇报 PPT 大纲 |
| **[🛒 电商文案助手](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/ecommerce-copywriting)** | 淘宝/拼多多/抖音卖家 | 商品标题、详情页、卖点提炼，分平台规则；内置广告法违禁词红线 |
| **[👩‍🏫 中文教案助手](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-lesson-plan)** | 中小学教师 | 按新课标三维目标出教案，含学情分析、分层作业、板书设计、说课稿。内置防套话机制 |

📋 **[看看它们实际输出什么 → EXAMPLES.md](EXAMPLES.md)**（真实片段：教案目标怎么写、电商文案怎么避违禁词、辅导话术长什么样）

**安装任意一个**：

```bash
# 先看看仓库里有哪些（不安装）
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --list

# 装单个（推荐）
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill chinese-lesson-plan

# 全部装上
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill '*'
```

或手动把 `skills/<名称>/` 复制到 `~/.claude/skills/` 下。

> ✅ 上述命令已用 `skills@1.5.21` 实测验证，能正确识别本仓库的 5 个 Skill。

> 这些 Skill 都写了明确的**边界与红线**——比如电商那个列了广告法违禁词，
> 记账那个明确不做税务筹划，辅导作业那个坚持不直接给答案。
> 我们认为一个好的 Skill 不只是"会做什么"，更要清楚"不做什么"。

📖 [完整 110 个 Skill 合集 → SKILLS.md](SKILLS.md)

## 🧩 AI Agent Skills 中文合集（110 个）

Skills 是给 AI 助手加的「专业技能包」。这块资源目前基本都是英文的，中文用户既看不懂说明、
也不知道有哪些中文 skill 可用 —— 所以我们做了 **87 个 Skill 的中文合集，其中 30 个中文原创**。

| 分类 | 代表 Skill |
|------|-----------|
| 🇨🇳 **中文原创（30 个）** | 去 AI 味改写、中文论文排版、学术降 AIGC、小红书运营 139 技能、公众号一键排版、求职简历 |
| 📄 文档办公 | docx / pdf / pptx / xlsx（官方）、Markdown→EPUB、法务技能包 |
| 💻 开发工程 | 测试驱动开发、git worktrees、MCP 构建、Playwright 自动化 |
| 🎨 创意设计 | 算法艺术、主题配色、HTML 审美库、AI 视频生成 |

**一键安装**：

```bash
npx skills add <GitHub 仓库地址>
```

> ⚠️ **实测纠错**：多个高星英文仓库把安装路径写成 `~/.config/claude-code/skills/`，
> 经本机实测，macOS 上**实际生效的是 `~/.claude/skills/`**。

📖 [完整清单与安装指南 → SKILLS.md](SKILLS.md) ｜ 🌐 [在线浏览（可搜索筛选）](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)

---

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| 收录工具 | **47** 个 |
| 有免费额度 | **45** 个 |
| 中文支持优秀 | **32** 个 |
| 分类 | **10** 类 |
| 🧩 Agent Skills | **87** 个（30 中文原创 / 17 官方） |
| 最近链接检测 | 2026-08-04 |

---

## 图例

| 标记 | 含义 |  | 标记 | 含义 |
|------|------|--|------|------|
| ⭐ | 编辑推荐 |  | 🆓 | 有免费额度 |
| 💰 | 付费为主 |  | 🇨🇳 | 中文支持优秀 |
| 🌐 | 需科学上网 |  | ★★★★★ | 综合评级 |

---

## 目录

- [💬 大语言模型](#大语言模型)
- [🎨 图像生成](#图像生成)
- [🎬 视频生成](#视频生成)
- [💻 编程辅助](#编程辅助)
- [✍️ 写作与文案](#写作与文案)
- [🌐 翻译工具](#翻译工具)
- [🎙️ 语音与 TTS](#语音与)
- [🔎 搜索增强](#搜索增强)
- [⚡ 效率工具](#效率工具)
- [🤖 多模态与 Agent](#多模态与)
- [🗺️ 按场景选工具](SCENARIOS.md) —— 学生 / 程序员 / 创作者 / 打工人
- [🧩 AI Skills 中文合集](SKILLS.md) —— 87 个 Skill，30 个中文原创
- [📰 AI 官方信源](#-ai-官方信源)

---

## 工具清单

### 💬 大语言模型

| 工具 | 免费额度 | 评级 | 说明 |
|------|----------|------|------|
| [DeepSeek](https://chat.deepseek.com) ⭐🆓🇨🇳 | 网页免费，API 极低价 | ★★★★★ | 开源推理模型，代码和数学能力比肩 GPT-4，API 价格是 OpenAI 的 1/10，国产性价比之王。 |
| [Kimi](https://kimi.moonshot.cn) ⭐🆓🇨🇳 | 网页版免费，API 有额度 | ★★★★★ | 200k 超长上下文，直接上传论文 / 合同 / 报告问重点，月之暗面出品。 |
| [通义千问 Qwen3](https://tongyi.aliyun.com) ⭐🆓🇨🇳 | 网页+API 有免费额度 | ★★★★★ | 阿里云旗舰，Qwen3-235B 参数，推理能力强，多模态，API 免费额度充足。 |
| [Claude](https://claude.ai) ⭐🆓🌐 | 每日有限次数免费 | ★★★★ | Anthropic 出品，长文档分析和代码能力顶级，对话逻辑清晰，需要梯子。 |
| [豆包](https://www.doubao.com) 🆓🇨🇳 | 网页完全免费 | ★★★★★ | 字节跳动出品，多模态联网，日常创作和对话场景均衡稳定，完全免费。 |
| [文心一言](https://yiyan.baidu.com) 🆓🇨🇳 | 网页版免费 | ★★★★★ | 百度出品，整合百度搜索，知识库问答和搜索增强场景有独特优势。 |
| [讯飞星火](https://xinghuo.xfyun.cn) 🆓🇨🇳 | 每日免费次数 | ★★★★★ | 科大讯飞，语音交互能力国内最强，适合语音+对话组合场景。 |
| [智谱清言](https://chatglm.cn) 🆓🇨🇳 | 网页+API 免费额度 | ★★★★★ | 清华背景，GLM-4，支持代码解释器和 Agent，API 免费额度开发者友好。 |
| [ChatGPT](https://chatgpt.com) 🆓🌐 | GPT-4o mini 免费 | ★★★★ | OpenAI 旗舰，生态最完善，插件和 GPTs 数量最多，覆盖场景最广。 |
| [Gemini](https://gemini.google.com) 🆓🌐 | 网页免费 | ★★★★ | Google 出品，深度整合 Gmail/Docs/Drive，重度 Google 生态用户首选。 |

### 🎨 图像生成

| 工具 | 免费额度 | 评级 | 说明 |
|------|----------|------|------|
| [即梦 AI](https://jimeng.jianying.com) ⭐🆓🇨🇳 | 每日免费积分 | ★★★★★ | 字节出品，中文提示词理解极佳，不需要学英文，每天免费额度充足，上手最快。 |
| [LiblibAI](https://www.liblib.art) ⭐🆓🇨🇳 | 每日免费算力 | ★★★★★ | 国内最大的 SD 模型社区，二次元、写实、国风模型极其丰富，可在线直接跑。 |
| [文心一格](https://yige.baidu.com) 🆓🇨🇳 | 每日免费电量 | ★★★★★ | 百度出品，国风、古风、水墨风格尤为出色，适合中式内容创作。 |
| [通义万相](https://tongyi.aliyun.com/wanxiang) 🆓🇨🇳 | API 有免费额度 | ★★★★★ | 阿里出品，针对中文场景专项训练，商业插图和电商图片质量稳定。 |
| [Adobe Firefly](https://firefly.adobe.com) 🆓🌐 | 每月免费积分 | ★★★★ | 商用授权最安全，Adobe 合规训练数据，生成结果可直接用于商业项目。 |
| [Midjourney](https://midjourney.com) 💰🌐 | 无免费额度，需订阅 | ★★★ | 商业设计质量顶级，好莱坞和广告公司御用，但无免费额度，需梯子。 |
| [Flux](https://bfl.ai) 🆓🌐 | 开源版本免费 | ★★★ | 新一代开源图像模型，质量超越同期 SD，可本地部署无限生成。 |

### 🎬 视频生成

| 工具 | 免费额度 | 评级 | 说明 |
|------|----------|------|------|
| [可灵 AI](https://klingai.kuaishou.com) ⭐🆓🇨🇳 | 每日免费积分 | ★★★★★ | 快手出品，720p 高质量，人物运动和物理效果在国产方案中最自然，每天有免费积分。 |
| [即梦视频](https://jimeng.jianying.com) 🆓🇨🇳 | 每日免费积分 | ★★★★★ | 字节出品，与即梦图像同平台，工作流顺畅，中文描述直接生成视频。 |
| [海螺视频](https://hailuoai.video) 🆓🇨🇳 | 每日免费次数 | ★★★★★ | MiniMax 出品，人物运动尤其流畅，适合有人物出镜的短视频片段。 |
| [Runway](https://runwayml.com) 💰🌐 | 每月少量免费积分 | ★★★ | 好莱坞采用的专业视频 AI 工具，奥斯卡获奖影片有实际使用案例。 |

### 💻 编程辅助

| 工具 | 免费额度 | 评级 | 说明 |
|------|----------|------|------|
| [通义灵码](https://lingma.aliyun.com) ⭐🆓🇨🇳 | 完全免费 | ★★★★★ | 阿里出品，VS Code 和 JetBrains 插件，完全免费，国内访问流畅，中文注释理解好。 |
| [Cursor](https://cursor.com) ⭐🆓 | 每月 2000 次补全免费 | ★★★★ | AI 原生 IDE，能理解整个项目上下文，复杂功能开发体验远超普通补全工具。 |
| [Windsurf](https://devin.ai/desktop) ⭐🆓 | 已并入 Devin Desktop（Cascade 7/1 EOL） | ★★★★ | Codeium 出品，功能与 Cursor 相近，完全免费是最大优势，国内可直接用。 |
| [MarsCode](https://www.marscode.cn) 🆓🇨🇳 | 云 IDE 免费 | ★★★★★ | 字节出品的在线云 IDE，内置 AI 助手，无需本地配置，适合快速验证想法。 |
| [Bolt](https://bolt.new) 🆓 | 每日免费额度 | ★★★★ | 一句话生成可运行的全栈 web 应用，适合快速原型，当天可上线演示。 |
| [v0](https://v0.dev) 🆓 | 每月免费积分 | ★★★★ | Vercel 出品，专注 UI 组件生成，输出 React/Tailwind 代码质量高，前端神器。 |

### ✍️ 写作与文案

| 工具 | 免费额度 | 评级 | 说明 |
|------|----------|------|------|
| [秘塔写作猫](https://xiezuocat.com) ⭐🆓🇨🇳 | 基础功能免费 | ★★★★★ | 国内老牌中文写作助手，语法检查、改写润色效果自然，不像 AI 腔，学生和职场必备。 |
| [Gamma](https://gamma.app) ⭐🆓 | 每月免费积分 | ★★★★ | 文字大纲一键生成精美 PPT，模板质量远超普通模板，适合快速出提案。 |
| [笔灵 AI](https://ibiling.cn) 🆓🇨🇳 | 每日免费字数 | ★★★★★ | 论文、报告、简历专项，格式规范，学生和需要正式文体的职场人适用。 |

### 🌐 翻译工具

| 工具 | 免费额度 | 评级 | 说明 |
|------|----------|------|------|
| [沉浸式翻译](https://immersivetranslate.com) ⭐🆓🇨🇳 | 基础功能完全免费 | ★★★★★ | 浏览器双语对照神器，网页、PDF、字幕全支持，不破坏原文排版，装上就离不开。 |
| [DeepL](https://deepl.com) ⭐🆓 | 每月 50 万字符免费 | ★★★★★ | 欧洲语言翻译质量全球最佳，中英互译自然度也高，每月 50 万字符免费。 |
| [彩云小译](https://caiyunapp.com) 🆓🇨🇳 | 每月免费字符 | ★★★★★ | 日语翻译国内最佳，支持实时字幕翻译，追日语内容的用户必备。 |
| [有道翻译](https://fanyi.youdao.com) 🆓🇨🇳 | 网页完全免费 | ★★★★★ | 网易出品，词典+翻译双合一，生词本和例句库是英语学习者的好帮手。 |

### 🎙️ 语音与 TTS

| 工具 | 免费额度 | 评级 | 说明 |
|------|----------|------|------|
| [讯飞配音](https://peiyin.xunfei.cn) ⭐🆓🇨🇳 | 每日免费字符 | ★★★★★ | 国内 TTS 标杆，音色数量最多，新闻播报到有声书多种风格，每天有免费额度。 |
| [Fish Audio](https://fish.audio) ⭐🆓🇨🇳 | 每月免费额度 | ★★★★★ | 支持中文方言，音色克隆效果国产最佳，上传 1 分钟样本就能克隆你的声音。 |
| [Azure TTS](https://azure.microsoft.com/zh-cn/products/ai-services/text-to-speech) 🆓🇨🇳 | 每月 50 万字符免费 | ★★★★★ | 微软出品，中文音色自然度高，每月 50 万字符免费，适合开发者集成到应用。 |

### 🔎 搜索增强

| 工具 | 免费额度 | 评级 | 说明 |
|------|----------|------|------|
| [秘塔搜索](https://metaso.cn) ⭐🆓🇨🇳 | 完全免费 | ★★★★★ | 国内最好用的 AI 搜索，无广告，学术模式+深度模式，引用可追溯，替代百度首选。 |
| [Perplexity](https://perplexity.ai) ⭐🆓🌐 | 每日有限次数 | ★★★★ | AI 搜索国际标杆，引用来源准确，技术和学术查询效果最佳，需要梯子。 |
| [天工 AI 搜索](https://search.tiangong.cn) 🆓🇨🇳 | 完全免费 | ★★★★★ | 昆仑万维出品，中文时事资讯查询强，支持多轮追问，完全免费无广告。 |

### ⚡ 效率工具

| 工具 | 免费额度 | 评级 | 说明 |
|------|----------|------|------|
| [WPS AI](https://ai.wps.cn) ⭐🆓🇨🇳 | 基础功能免费 | ★★★★★ | Office 场景 AI 助手，文档摘要、公式生成、PPT 美化，对中文职场文档最熟悉。 |
| [飞书多维表格](https://feishu.cn) 🆓🇨🇳 | 免费版功能充足 | ★★★★★ | AI+电子表格组合，自动化流程强，适合团队协作和数据管理场景。 |
| [Gamma](https://gamma.app) 🆓 | 每月免费积分 | ★★★★ | AI 一键生成 PPT 和文档，模板精美，适合快速出提案，每月有免费积分。 |

### 🤖 多模态与 Agent

| 工具 | 免费额度 | 评级 | 说明 |
|------|----------|------|------|
| [Coze](https://coze.cn) ⭐🆓🇨🇳 | 国内版完全免费 | ★★★★★ | 字节出品 Agent 平台，拖拽式配置，插件生态丰富，搭建个人 AI 助手和自动化流程首选。 |
| [FastGPT](https://fastgpt.in) ⭐🆓🇨🇳 | 开源+云版本有免费额度 | ★★★★★ | 知识库问答平台，RAG 效果在开源方案中最稳定，把内部文档变成智能助手。 |
| [Dify](https://dify.ai) ⭐🆓🇨🇳 | 开源可自部署 | ★★★★ | 国产 LLMOps 开源标杆，GitHub 50k+ stars，可视化编排 Agent，支持私有化部署。 |
| [MaxKB](https://maxkb.cn) 🆓🇨🇳 | 开源免费 | ★★★★★ | 1Panel 出品，知识库问答，安装简单，中小团队快速搭建内部知识库。 |

---

## 📰 AI 官方信源

本站**不转述任何新闻**。想看最新动态，请直接访问官方公告页：

| 厂商 | 官方公告 |
|------|----------|
| OpenAI | https://openai.com/news/ |
| Anthropic (Claude) | https://www.anthropic.com/news |
| Google DeepMind | https://deepmind.google/ |
| DeepSeek | https://api-docs.deepseek.com/ |
| 月之暗面 Kimi | https://kimi.moonshot.cn/ |
| 通义千问 | https://tongyi.aliyun.com/ |
| 智谱 GLM | https://www.zhipuai.cn/ |
| 字节豆包 | https://www.doubao.com/ |

> 为什么这么做？见 [内容准则与维护说明](内容准则与维护说明.md)

---

## 🤝 参与贡献

发现工具信息有误、链接失效、或想推荐新工具？
欢迎 [提交 Issue](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues) 或 PR，我每天都在维护。

## ⚠️ 免责声明

免费额度政策变动频繁，**付费前请务必到官网确认当前政策**。本站为个人维护的公益导航，不对第三方信息准确性负责。

---

**觉得有用？点个 ⭐ Star 让更多人看到**
