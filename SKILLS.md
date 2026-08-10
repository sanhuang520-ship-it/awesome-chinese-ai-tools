# 🧩 AI Agent Skills 中文合集

> **156 个 Skill｜63 个中文原创｜✍️ 12 个本站原创**  
> 每一个都经 GitHub API 验证仓库真实存在  
> 🔄 最近自动复检：**2026-08-10**（复检仓库是否还在、星数是否变化；超半年没更新的标 🕰）

📋 **[看原创 Skill 实际输出什么 → EXAMPLES.md](EXAMPLES.md)**　🌐 [在线浏览（可搜索/筛选）](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)

---

## 什么是 Skills

**一句话：Skills 是给 AI 助手加的「专业技能包」。**

一个文件夹 + 一份 `SKILL.md` 说明书，告诉 AI 什么时候该用、按什么步骤做。AI 自动判断何时激活。

| | 是什么 | 解决什么 |
|---|--------|---------|
| **Skills** | 一份工作说明书（Markdown + 可选脚本） | 教 AI **怎么做**某类任务 |
| **MCP** | 一个后台服务 | 让 AI **连上**外部系统（数据库、浏览器） |
| **插件** | 打包分发的组合 | 把 skills + MCP 打包一键装 |

---

## 怎么安装

```bash
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --list          # 先看有哪些
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill guochao-visual-cn
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill '*'             # 全部
```

> ⚠️ **实测提醒（CLI 1.5.22）**：`npx skills add` 把文件装到 `~/.agents/skills/`（多家 agent 共用），
> 再在 `~/.claude/skills/` 建符号链接指过去 —— Claude Code 读的是后者，两处都能看到。
> 而部分教程（包括 7 万星仓库）写的 `~/.config/claude-code/skills/`，本机实测**并不存在**。

装好后重启 Claude Code，**无需手动调用**——描述任务，AI 自动激活。

---

## Skill 清单

### ✍️ 本站原创（12 个）

> 我们自己编写维护，每个都写明「不做什么」。可直接 `npx skills add` 安装。

| Skill | 说明 |
|-------|------|
| [ai-learning-coach](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/ai-learning-coach) | AI 学习教练（本站原创）：不直接给答案，带你走完整学习循环——定目标→主动回忆→输出→纠错→间隔复习→项目交付，含错因分析模板 |
| [book-digest-cn](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/book-digest-cn) | 拆书助手（本站原创）：三层拆解（作者在答什么问题→核心主张→对我有什么用），拒绝抄目录式笔记 |
| [bookkeeping-cn](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/bookkeeping-cn) | 记账整理助手（本站原创）：流水分类、收支表、预算跟踪；明确不做税务与投资建议 |
| [chinese-lesson-plan](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-lesson-plan) | 中文教案助手（本站原创）：按新课标三维目标生成中小学教案，含分层作业、板书设计、说课稿 |
| [chinese-typography](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-typography) | 中文排版助手（本站原创）：中英间距、CJK 断行避头尾、字体栈、标点全半角、行高行宽，附可直接用的 CSS 与公众号排版规则 |
| [chinese-web-themes](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-web-themes) | 中式网页主题库（本站原创）：8 套中国美学 CSS 主题（水墨/青绿/宋韵/敦煌/朱砂/新中式/竹韵/夜宴），内置中文排版规范，对比度均超 WCAG AA。可在线预览 |
| [chinese-work-report](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-work-report) | 职场汇报助手（本站原创）：周报/月报/述职/项目汇报，结论先行、卖点翻价值，含 PPT 大纲 |
| [ecommerce-copywriting](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/ecommerce-copywriting) | 电商文案助手（本站原创）：商品标题/详情页/卖点提炼，分平台规则，含广告法违禁词红线 |
| [github-readme-cn](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/github-readme-cn) | GitHub 中文项目门面优化（本站原创）：首屏结构、真实截图怎么截、命名与 topics、发布前自查清单。附 15 个高增长仓库的实测数据，明确区分相关性与不可验证的部分，不承诺涨星 |
| [guochao-visual-cn](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/guochao-visual-cn) | 国潮视觉助手（本站原创）：12 种中国美学画风配方（水墨/工笔/青绿/敦煌/年画/剪纸/国漫等），输出可直接用的提示词，附纹样寓意与传统配色速查 |
| [guofeng-threejs](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/guofeng-threejs) | 国风 Three.js 渲染（本站原创）：水墨 shader 三技法（墨分五色/边缘积墨/笔触扰动），含可运行 demo 与移动端性能要点。只做中式渲染，不做通用 Three.js 教程 |
| [homework-tutor-cn](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/homework-tutor-cn) | 家长辅导作业助手（本站原创）：不给答案给引导话术，分学科方法，含情绪对抗处理 |

### 🇨🇳 中文原创（52 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [humanizer-zh](https://github.com/op7418/humanizer-zh) | ⭐14,953 | 去除文本里的 AI 生成痕迹。基于维基百科「AI 写作特征」整理，检测并修复：夸大的象征意义、宣传性语言、-ing 结尾的肤浅分析、模糊归因、破折号过度使用、三段式法则、AI 词汇、否定式排比 🕰<sub>2026-01-19 后未更新</sub> |
| [zhangxuefeng-skill](https://github.com/alchaincyf/zhangxuefeng-skill) | ⭐10,101 | 张雪峰的思维框架与表达方式：基于 5 本著作、15+ 篇采访、30+ 条语录整理出 5 个心智模型与 8 条决策启发式。用于分析教育选择、职业规划、阶层流动 |
| [dbskill](https://github.com/dontbesilent2025/dbskill) | ⭐9,358 | 个人技能合集（30 个）：公众号 HTML 排版、用阿德勒心理学框架诊断执行阻滞（知道该做却拖延时用）等 |
| [superpowers-zh](https://github.com/jnMetaCode/superpowers-zh) | ⭐7,575 | superpowers 中文版：26万⭐框架完整汉化 + 6 个中国原创 skill |
| [gzh-design-skill](https://github.com/isjiamu/gzh-design-skill) | ⭐2,947 | 微信公众号排版引擎：Markdown → 可直接粘进公众号编辑器的 HTML。6 套主题 + 主题生成器，自动章节编号、引言卡片、目录导航，支持 Word/PDF 输入 |
| [codex-claude-academic-skills](https://github.com/zLanqing/codex-claude-academic-skills) | ⭐2,716 | 学术科研三件套：文献阅读、论文写作、科学计算全流程 |
| [everything-claude-code-zh](https://github.com/xu-xiang/everything-claude-code-zh) | ⭐1,840 | Claude Code 完整配置中文翻译（agents/skills/hooks/commands） |
| [agent-skills-with-anthropic](https://github.com/datawhalechina/agent-skills-with-anthropic) | ⭐1,449 | 吴恩达 DeepLearning.AI 课程的中文翻译与知识整理 |
| [shuorenhua](https://github.com/MrGeDiao/shuorenhua) | ⭐986 | 「说人话」去 AI 味改写：保事实、分场景、改完可直接发 |
| [Awesome-Journal-Skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills) | ⭐965 | 主流期刊投稿技能包（AER、QJE 等经济学顶刊） |
| [speak-human-tw](https://github.com/Raymondhou0917/speak-human-tw) | ⭐766 | 繁体中文去 AI 味：抓 38 种 AI 写作痕迹，校正用语与标点 |
| [claude-code-skills-zh](https://github.com/laolaoshiren/claude-code-skills-zh) | ⭐747 | 面向中文开发者的技能库，按场景分类、复制即装 |
| [higgsfield-seedance2-jineng](https://github.com/beshuaxian/higgsfield-seedance2-jineng) | ⭐741 | AI 视频生成 15 个 prompt skill（Seedance 2.0 × Higgsfield） |
| [xiaohu-wechat-format](https://github.com/xiaohuailabs/xiaohu-wechat-format) | ⭐680 | 公众号一键排版发布：Markdown → 微信 HTML，30 套主题 |
| [Enterprise-ai-scenario-map-skill](https://github.com/MetaInFLow/Enterprise-ai-scenario-map-skill) | ⭐625 | 咨询向：为任何企业自动生成 AI 应用场景地图报告。含企业画像、业务诊断、行业实践、场景全量表、实施路径 |
| [Claude_skills_zh-CN](https://github.com/LeastBit/Claude_skills_zh-CN) | ⭐561 | 官方 anthropics/skills 的中文学习版 🕰<sub>2026-01-19 后未更新</sub> |
| [cuimao-translator](https://github.com/Cuimao777/cuimao-translator) | ⭐462 | 一键把英文 PDF 翻译成流畅中文 |
| [video-recap-skills](https://github.com/worldwonderer/video-recap-skills) | ⭐446 | 把任意视频剪成解说式短片 |
| [yupi-skill](https://github.com/liyupi/yupi-skill) | ⭐406 | 程序员鱼皮技能包：编程学习、求职面试、技术选型、创业经验 |
| [xiaohongshu-skills](https://github.com/vivy-yi/xiaohongshu-skills) | ⭐364 | 139 个小红书运营技能：内容创作、账号运营、电商转化等 9 大类 🕰<sub>2026-01-23 后未更新</sub> |
| [docx-skill-4-cn-paper](https://github.com/Gostyan/docx-skill-4-cn-paper) | ⭐355 | 中文论文排版规范：课程论文、数模竞赛、毕业论文 |
| [humanities-writing-companion](https://github.com/tizzy916/humanities-writing-companion) | ⭐355 | 人文学科写作助手：11 种模式覆盖构思到成稿 |
| [opencode-skills](https://github.com/zrt-ai-lab/opencode-skills) | ⭐266 | 技能库：视频生成、图片生成、Agent 互联、智能问数 |
| [universal-examprep-skill](https://github.com/ZeKaiNie/universal-examprep-skill) | ⭐266 | 考前突击教练：把课件资料变成应试重点 |
| [skills_collection](https://github.com/wwwzhouhui/skills_collection) | ⭐259 | 个人实用技能集，覆盖开发效率与内容创作 |
| [humanizer-zh-academic](https://github.com/redbaronyyyyy-eng/humanizer-zh-academic) | ⭐241 | 降低中文学术写作 AIGC 检测率 |
| [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) | ⭐236 | 热门 Skills 中文学习版 + 教程，7000+ 收录 |
| [Bloom](https://github.com/Li-Evan/Bloom) | ⭐224 | 私人 AI 家教：识别你的学习方式，安排下一课 |
| [niubiskill](https://github.com/nathanskill/niubiskill) | ⭐208 | 中文变现决策：判断一件事是否接近收入再投入 |
| [technical-writing](https://github.com/luoling8192/technical-writing) | ⭐208 | 中文技术写作：设计文档、评审稿、复盘、分享稿 |
| [Vibe_coding_guide](https://github.com/Lling0000/Vibe_coding_guide) | ⭐206 | 中文优先的 Vibe Coding 工程化流程指南 |
| [SecSkills](https://github.com/Arenbai/SecSkills) | ⭐203 | 渗透测试技能模块，遵循 PTES 标准全阶段覆盖 |
| [openclaw-guide](https://github.com/liyupi/openclaw-guide) | ⭐184 | OpenClaw 中文文档站：安装部署、Agent 架构、Skills 配置 |
| [makeownsrt](https://github.com/joshhu/makeownsrt) | ⭐175 | 从 MKV 提取英文字幕并翻成繁中双语 SRT |
| [Auto-CV](https://github.com/flamingoTOM/Auto-CV) | ⭐166 | LaTeX 中文简历模板 + 自动提取内容生成 |
| [JobOK](https://github.com/GresonKwan/JobOK) | ⭐119 | 中文求职：优势挖掘、岗位匹配、简历优化、面试训练 |
| [openclaw-xhs](https://github.com/zhjiang22/openclaw-xhs) | ⭐117 | 小红书内容工具：搜笔记、取详情与评论、发图文/视频笔记、点赞收藏、热点话题跟踪、帖子导出长图。117 星但 1.1 万安装 |
| [hermes-arxiv-agent](https://github.com/genggng/hermes-arxiv-agent) | ⭐111 | 每天自动抓 arXiv 论文，生成中文摘要推送到飞书 |
| [kc_ai_skills](https://github.com/KerberosClaw/kc_ai_skills) | ⭐77 | 中文优先的 Claude Code / Codex skills 合集 |
| [wechat-writing-style](https://github.com/yaoleifly/wechat-writing-style) | ⭐76 | 微信公众号中文写作风格 |
| [stop-slop-zh](https://github.com/VincentOld/stop-slop-zh) | ⭐62 | 消除中文 AI 写作痕迹：拆排比、去名词化、换具体细节 |
| [cnki-aigc---skill](https://github.com/qingshanliuci/cnki-aigc---skill) | ⭐34 | 知网 AIGC 降重：实测把 AI 率从 20.6% 降到 10.1% |
| [awesome-skills-zh](https://github.com/yzfly/awesome-skills-zh) | ⭐26 | 精选 Claude / Agent / LLM Skills 中文资源列表 |
| [awesome-claude-skills-zh-TW](https://github.com/ammosu/awesome-claude-skills-zh-TW) | ⭐24 | awesome-claude-skills 繁体中文化版本 🕰<sub>2025-12-15 后未更新</sub> |
| [scholar-wendao-skill](https://github.com/tizzy916/scholar-wendao-skill) | ⭐20 | 学者问道：把学者视角提炼成可复用框架 |
| [refine-legal-chinese](https://github.com/katejianglaw/refine-legal-chinese) | ⭐13 | 法言法语：把口语化表述改写为规范法律中文 |
| [awesome-claude-skills-zh](https://github.com/shishirui/awesome-claude-skills-zh) | ⭐13 | 中文社区优先的 Claude skills 精选收录 |
| [ip-character-designer](https://github.com/Beatatata/ip-character-designer) | ⭐11 | 自媒体 IP 配图生成器：10 种画风 × 双版本 × 中文提示词 |
| [awesome-claude-skills-cn](https://github.com/bbylw/awesome-claude-skills-cn) | ⭐9 | Awesome Claude Skills 中文版 🕰<sub>2026-01-14 后未更新</sub> |
| [cn-humanizer-academic](https://github.com/ranranrannervous/cn-humanizer-academic) | ⭐5 | 中文学术论文降 AI 痕迹，针对 BERT 语义检测器 |
| [CN-The-Complete-Guide-to-Building-Skill-for-Claude](https://github.com/chenqing0106/CN-The-Complete-Guide-to-Building-Skill-for-Claude) | ⭐5 | 《为 Claude 构建技能的完整指南》中文翻译：结构、模式、测试、分发 |
| [ai-video-creator](https://github.com/Frank-oll/ai-video-creator) | ⭐5 | 把生活妙招选题端到端做成可发布的竖屏 AI 短视频（含配音） |

### 📄 文档办公（9 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [docx](https://github.com/anthropics/skills/tree/main/skills/docx) | 官方 | Word 文档全流程：创建、读取、编辑、修订标记、批注、排版 |
| [pdf](https://github.com/anthropics/skills/tree/main/skills/pdf) | 官方 | PDF 处理：提取文字/表格/元数据、合并、拆分、批注 |
| [pptx](https://github.com/anthropics/skills/tree/main/skills/pptx) | 官方 | PPT 演示文稿：读取、生成幻灯片、调整版式与模板 |
| [xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx) | 官方 | Excel 表格：公式计算、图表生成、数据转换 |
| [doc-coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) | 官方 | 结构化文档协作撰写流程，引导多人共同完成文档 |
| [NotebookLM Integration](https://github.com/PleasePrompto/notebooklm-skill) | ⭐7,592 | 让 Claude Code 直接对话 NotebookLM，做有出处的问答 🕰<sub>2025-11-21 后未更新</sub> |
| [article-extractor](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/article-extractor) | ⭐516 | 从网页提取完整文章正文与元数据 |
| [Markdown to EPUB Converter](https://github.com/smerchek/claude-epub-skill) | ⭐149 | 把 Markdown 文档转成专业 EPUB 电子书 🕰<sub>2025-10-18 后未更新</sub> |
| [Master Claude for Legal](https://github.com/sboghossian/master-claude-for-legal) | ⭐53 | 法务技能包：NDA 审阅、多方版本对比、引用核验 |

### 💻 开发工程（25 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | 官方 | 写 Skill 的 Skill —— 创建、改进、评估技能，新手从这个开始 |
| [mcp-builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) | 官方 | 构建高质量 MCP（Model Context Protocol）服务的完整指南 |
| [web-artifacts-builder](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) | 官方 | 构建复杂多组件网页应用（React / Tailwind / shadcn-ui 技术栈） |
| [webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | 官方 | 本地 Web 应用的交互测试工具集 |
| [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | 官方 | 前端视觉设计指导，做出有辨识度、有意图的界面 |
| [claude-api](https://github.com/anthropics/skills/tree/main/skills/claude-api) | 官方 | Claude API 使用参考：模型 ID、定价、参数、流式、工具调用、缓存 |
| [test-driven-development](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) | ⭐269,732 | 测试驱动开发全流程指导，写代码前先写测试 |
| [using-git-worktrees](https://github.com/obra/superpowers/blob/main/skills/using-git-worktrees/) | ⭐269,732 | 自动创建隔离的 git worktree，多分支并行开发不打架 |
| [finishing-a-development-branch](https://github.com/obra/superpowers/tree/main/skills/finishing-a-development-branch) | ⭐269,732 | 开发分支收尾：合并、清理、发布的标准流程 |
| [planning-with-files](https://github.com/othmanadi/planning-with-files) | ⭐26,070 | Manus 式的文件化持久规划：把 task_plan.md / findings.md / progress.md 落到磁盘，上下文丢了工作也不丢。含 18 个子技能 |
| [baoyu-skills](https://github.com/jimliu/baoyu-skills) | ⭐24,768 | 宝玉的技能合集（22 个）：公众号摘要、发布流程自动化（自动识别版本文件与 changelog，支持 Node/Python/Rust/Claude Plugin）等 |
| [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) | ⭐14,734 | 把任意文档网站自动转成 Claude Skill —— 造 skill 的利器 |
| [fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) | ⭐9,798 | 生成技术图表：软件架构、数据流、流程图、时序图、C4 模型、云部署、事件流 |
| [reddit-fetch](https://github.com/ykdojo/claude-code-tips/tree/main/skills/reddit-fetch) | ⭐9,581 | 当 WebFetch 被拦时，通过 Gemini CLI 抓取 Reddit 内容 |
| [drawio-skill](https://github.com/Agents365-ai/drawio-skill) | ⭐7,360 | 用自然语言生成 draw.io 图表：11 种预设（UML、SysML/MBSE、BPMN、网络拓扑、C4 架构等），36 个工具 |
| [lean-ctx](https://github.com/yvgude/lean-ctx) | ⭐3,555 | AI 编程代理的上下文运行时，管理会话与上下文 |
| [Playwright Browser Automation](https://github.com/lackeyjb/playwright-skill) | ⭐3,005 | 用 Playwright 做浏览器自动化测试与验证 🕰<sub>2025-12-19 后未更新</sub> |
| [subagent-driven-development](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/sadd/skills/subagent-driven-development) | ⭐1,308 | 把任务拆给多个子智能体并行处理，加速复杂开发 |
| [software-architecture](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/ddd/skills/software-architecture) | ⭐1,308 | 实现整洁架构、SOLID 等设计模式 |
| [prompt-engineering](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/customaize-agent/skills/prompt-engineering) | ⭐1,308 | 系统讲解提示词工程的技巧与模式 |
| [iOS Simulator](https://github.com/conorluddy/ios-simulator-skill) | ⭐1,208 | 操作 iOS 模拟器做 App 测试 |
| [AppGenesisForge](https://github.com/pcliangx/AppGenesisForge) | ⭐414 | 19 个角色协作的 AI Agent 团队脚手架，按阶段门禁推进 |
| [aws-skills](https://github.com/zxkane/aws-skills) | ⭐346 | AWS 开发：CDK 最佳实践、成本优化、Serverless 架构 |
| [D3.js Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill) | ⭐219 | 用 D3 做交互式数据可视化图表 🕰<sub>2025-10-18 后未更新</sub> |
| [great_cto](https://github.com/avelikiy/great_cto) | ⭐75 | 7 个专业子智能体（技术负责人、资深工程师等）组成的技术团队 |

### 🎨 创意设计（10 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design) | 官方 | 用设计原理创作视觉作品，输出 PNG / PDF |
| [algorithmic-art](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art) | 官方 | 用 p5.js 创作算法艺术，支持随机种子与交互 |
| [theme-factory](https://github.com/anthropics/skills/tree/main/skills/theme-factory) | 官方 | 为作品套用主题配色的工具集（幻灯片、网页等） |
| [brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) | 官方 | 把品牌配色与字体规范应用到各类产出物 |
| [slack-gif-creator](https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator) | 官方 | 制作适配 Slack 的动图 GIF |
| [youtube-transcript](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/youtube-transcript) | ⭐516 | 抓取 YouTube 视频字幕并整理成摘要 |
| [imagen](https://github.com/sanjay3290/ai-skills/tree/main/skills/imagen) | ⭐395 | 调用 Google Gemini 图像生成 API 出图 |
| [swiftui-design-skill](https://github.com/wholiver/swiftui-design-skill) | ⭐164 | SwiftUI 前端设计（中文）：反 AI 味六条铁律、设计顾问、五维评审 |
| [anydesign](https://github.com/uxKero/anydesign) | ⭐153 | 分析任意图片/网址/Figma 文件，生成结构化设计规范 |
| [pakco-html](https://github.com/pakco77/pakco-html) | ⭐70 | HTML 审美库（中文）：60+ 视觉风格、演示页/长页模板，一键复制 Prompt |

### 💼 办公协作（10 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [internal-comms](https://github.com/anthropics/skills/tree/main/skills/internal-comms) | 官方 | 撰写各类内部沟通文案的资源集 |
| [brainstorming](https://github.com/obra/superpowers/tree/main/skills/brainstorming) | ⭐269,732 | 把粗略想法通过结构化提问变成完整方案 |
| [kaizen](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/kaizen/skills/kaizen) | ⭐1,308 | 持续改进方法论，多种分析框架 |
| [Brand Build Skills](https://github.com/rampstackco/claude-skills) | ⭐524 | 59 个 skill 的品牌与网站全生命周期库 |
| [tapestry](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/tapestry) | ⭐516 | 把相关文档互联并总结成知识网络 |
| [ship-learn-next](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/ship-learn-next) | ⭐516 | 基于进展帮你决定下一步该做什么/学什么 |
| [google-workspace-skills](https://github.com/sanjay3290/ai-skills/tree/main/skills) | ⭐395 | Google 全家桶集成：Gmail、日历、Chat 等 |
| [n8n-skills](https://github.com/haunchen/n8n-skills) | ⭐386 | 让 AI 直接理解和操作 n8n 工作流 |
| [seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) | ⭐143 | SEO / GEO（生成式引擎优化）技能集，20 个子技能：外链分析、关键词研究、内容写作等。139 星但 2.6 万安装 —— 星数完全反映不出使用量 |
| [solo-skills](https://github.com/rockscy/solo-skills) | ⭐6 | 独立开发者双语（中英）技能包：7 个 solo 场景 |

### 📊 数据研究（5 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [root-cause-tracing](https://github.com/obra/superpowers/tree/main/skills/root-cause-tracing) | ⭐269,732 | 错误深藏在执行链路时，追溯根本原因 |
| [CSV Data Summarizer](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill) | ⭐446 | 自动分析 CSV 文件并生成完整数据报告 🕰<sub>2025-10-16 后未更新</sub> |
| [deep-research](https://github.com/sanjay3290/ai-skills/tree/main/skills/deep-research) | ⭐395 | 调用 Gemini Deep Research 做自主多步研究 |
| [postgres](https://github.com/sanjay3290/ai-skills/tree/main/skills/postgres) | ⭐395 | 对 PostgreSQL 执行安全的只读 SQL 查询 |
| [recursive-research](https://github.com/Anjos2/recursive-research) | ⭐37 | 跨领域递归研究，可深入到博士级别 |

### 🔐 安全取证（5 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | ⭐22,518 | 逆向工程与授权渗透测试的 Skill 路由包 |
| [computer-forensics](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/computer-forensics) | ⭐659 | 数字取证分析与调查技术 |
| [metadata-extraction](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/metadata-extraction) | ⭐659 | 提取分析文件元数据用于取证 |
| [file-deletion](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/file-deletion) | ⭐659 | 安全删除文件与数据清除方法 |
| [FFUF Web Fuzzing](https://github.com/jthack/ffuf_claude_skill) | ⭐205 | 集成 ffuf 做 Web 模糊测试 🕰<sub>2025-10-16 后未更新</sub> |

---

## 怎么自己写一个 Skill

```
my-skill/
└── SKILL.md          # 必需
    references/       # 可选
```

**一个建议**：写清楚「不做什么」和「能做什么」同样重要。
我们 12 个原创 Skill 都写明了边界——记账不做税务筹划、辅导作业不给答案、
学习教练不替你完成输出、国潮视觉不伪造文物。

推荐用官方 [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 生成。

---

## ⚠️ 安全提醒

Skills 可含**可执行脚本**。装第三方前先看 `SKILL.md` 和 `scripts/` 内容。

---

*本文件由脚本从 `data/skills.json` 自动生成，最后更新 2026-08-10。*  
*收录有误或想推荐新 Skill？欢迎 [提 Issue](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues)*
