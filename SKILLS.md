# 🧩 AI Agent Skills 中文合集

> **194 个 Skill 条目｜72 个中文条目｜✍️ 13 个本站原创**<br>
> 来源仓库经 GitHub API 核验真实存在；第三方说明来自上游资料或维护者摘要，不等于逐项功能实测<br>
> 🔄 最近自动复检：**2026-08-22**（复检仓库是否还在、星数是否变化；超半年没更新的标 🕰）

🧪 **[Codex 13/13 自动触发实测 → COMPATIBILITY.md](COMPATIBILITY.md)**　🧰 [4 组开箱组合](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/bundles/)　📋 [原创 Skill 输出示例](EXAMPLES.md)　🔎 [按场景找 Skill](#skill-catalog)　🌐 [在线浏览（可搜索/筛选）](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)

🛡️ **[安装第三方 Skill 前：运行只读本地审计器](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/audit-skill/)**（检查脚本、联网、凭据词与高风险命令；不执行目标，0 项命中不等于安全）

> 兼容性边界：当前只有 Codex 的任务级实测；Claude Code 与 Cursor 待测。成功、失败或未触发均可通过[结构化表单提交](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)。

---

## 什么是 Skills

**一句话：Skills 是给 AI 助手加的「专业技能包」。**

一个文件夹 + 一份 `SKILL.md` 说明书，告诉 AI 什么时候该用、按什么步骤做。支持 Skills 的客户端可以按任务自动激活；是否触发取决于客户端、版本、安装位置和任务措辞，需分别实测。

| | 是什么 | 解决什么 |
|---|--------|---------|
| **Skills** | 一份工作说明书（Markdown + 可选脚本） | 教 AI **怎么做**某类任务 |
| **MCP** | 一个后台服务 | 让 AI **连上**外部系统（数据库、浏览器） |
| **插件** | 打包分发的组合 | 把 skills + MCP 打包一键装 |

---

## 怎么安装

```bash
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --list          # 先看有哪些
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill guochao-visual-cn -g   # -g = 全局安装
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill '*' -g          # 全部
```

> ⚠️ **实测提醒（CLI 1.5.23，2026-08-19 复测）**：`npx skills add` **默认是项目级**，
> 把文件装进**你当前所在的目录**（`./.agents/skills/`），不是家目录；
> 加 `-g` 才装到用户级的 `~/.agents/skills/`。CLI 帮助原文：
> `-g, --global  Install skill globally (user-level) instead of project-level`。
> 两种情况都会在同级的 `.claude/skills/` 建符号链接，所以两处能看到同一份文件；
> 这只证明安装结果，本轮尚未运行 Claude Code。
> 而部分教程（包括 7 万星仓库）写的 `~/.config/claude-code/skills/`，本机实测**并不存在**。

> 📌 本页此前写的是「装到 `~/.agents/skills/`」，不准确——当初那次实测在家目录下跑，
> 把「当前目录恰好是家目录」当成了工具行为。2026-08-19 换目录交叉验证后更正。

装好后重启你使用的客户端，用一个**不点名 Skill 名称**的自然任务测试是否自动触发。不同客户端与版本的行为可能不同；当前只有 Codex 的任务级实测。遇到问题先看[安装与排错页](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/install/)。

安装第三方 Skill 前，可先运行 `python3 scripts/audit_skill.py /path/to/skill` 做只读静态扫描；它只提供人工复核线索，不是恶意代码检测或安全认证。

### 30 秒选一个真实任务

只装当前需要的一项，重启客户端，再复制自然任务。任务中不点名 Skill，才能观察客户端是否会主动选择它。

| 需求 | 安装 | 复制给 AI | 本仓库记录 |
|---|---|---|---|
| 审查中文网页排版 | `npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill chinese-typography -g` | `请检查这段 CSS 的中文字体、行高、断词和两端对齐问题，只审查，不修改文件。` | [Codex 单任务实测](cases/chinese-typography-codex.md) |
| 整理不编数据的周报 | `npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill chinese-work-report -g` | `把这些工作素材整理成给老板看的周报；结果数据没有提供，不要编造。` | [Codex 单任务实测](cases/chinese-work-report-codex.md) |
| 校对商品文案事实边界 | `npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill ecommerce-copywriting -g` | `根据已知参数整理可写、待补和不应发布的信息；没有的参数、认证和功效不要编。` | [Codex 单任务实测](cases/ecommerce-copywriting-codex.md) |
| 制定能动手练习的学习计划 | `npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill ai-learning-coach -g` | `我想两周入门 SQL。先了解目标和基础，再制定有练习、输出和复盘的计划。` | [Codex 校准实测](cases/ai-learning-coach-codex.md) |

**[→ 查看全部 13 个单项安装命令与可复制首次任务](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/try-agent-skills/)**：7 条历史逐字原文与 6 条前瞻任务严格分开；前瞻任务 6 条均已执行。

这些链接只记录一次特定 Codex 版本与任务的结果，不保证其他客户端、版本或措辞得到相同结果。

---

<a id="skill-catalog"></a>
## Skill 清单

### 按场景直达

| 场景 | 条目数 | 跳转 |
|---|---:|---|
| ✍️ 本站原创 | 13 | [查看](#catalog-original) |
| 🇨🇳 其他中文条目 | 61 | [查看](#catalog-cn) |
| 📄 文档办公 | 10 | [查看](#catalog-doc) |
| 📊 PPT 演示 | 19 | [查看](#catalog-ppt) |
| 💻 开发工程 | 36 | [查看](#catalog-dev) |
| 🤖 Agent 与调研 | 8 | [查看](#catalog-agent) |
| 🎨 创意设计 | 12 | [查看](#catalog-design) |
| 💼 办公协作 | 13 | [查看](#catalog-biz) |
| 📊 数据研究 | 5 | [查看](#catalog-data) |
| 🔐 安全取证 | 7 | [查看](#catalog-sec) |
| 🧊 3D 与图形 | 5 | [查看](#catalog-3d) |
| 🎮 游戏开发 | 5 | [查看](#catalog-game) |

<a id="catalog-original"></a>
### ✍️ 本站原创（13 个）

> 我们自己编写维护，每个都写明「不做什么」。以下是安装前静态检查标签，不是安全认证；完整方法见 [QUALITY.md](QUALITY.md)。

| Skill | 做什么 | 安装前标签 |
|-------|--------|------------|
| [ai-learning-coach](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/learning/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/ai-learning-coach) | AI 学习教练（本站原创）：不直接给答案，带你走完整学习循环——定目标→主动回忆→输出→纠错→间隔复习→项目交付，含错因分析模板 | 说明与本地参考资料；无独立可执行脚本；未发现运行时联网；**边界：**医疗、法律与投资决策不能只依赖学习计划 |
| [book-digest-cn](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/reading/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/book-digest-cn) | 拆书助手（本站原创）：三层拆解（作者在答什么问题→核心主张→对我有什么用），拒绝抄目录式笔记 | 仅说明文件；无独立可执行脚本；未发现运行时联网；**边界：**未标记敏感决策边界，仍需核对输出 |
| [bookkeeping-cn](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/bookkeeping/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/bookkeeping-cn) | 记账整理助手（本站原创）：流水分类、收支表、预算跟踪；明确不做税务与投资建议 | 仅说明文件；无独立可执行脚本；未发现运行时联网；**边界：**财务隐私；不提供税务筹划或投资建议 |
| [chinese-design-md](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/design/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-design-md) | 中式 DESIGN.md 设计系统（本站原创）：8 套可直接丢进项目根目录的设计文档，AI 读了就按规范生成界面。含中文排版规则（行高 1.75 / 不用 justify / 着重号代替斜体 / CJK 避头尾），对比度逐项实测并标出不达标项 | 说明与本地设计模板；无独立可执行脚本；未发现运行时联网；**边界：**字体授权需由使用者核对 |
| [chinese-lesson-plan](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/lesson-plan/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-lesson-plan) | 中文教案助手（本站原创）：先核对学段、教材版本和适用课标，再按学科核心素养、学习任务与评价证据组织目标，含分层作业、板书设计和说课稿 | 说明与本地参考资料；无独立可执行脚本；未发现运行时联网；**边界：**课程事实与教材版本需要来源确认 |
| [chinese-typography](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/typography/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-typography) | 中文排版助手（本站原创）：中英间距、CJK 断行避头尾、字体栈、标点全半角、行高行宽，附可直接用的 CSS 与公众号排版规则 | 仅说明文件；无独立可执行脚本；未发现运行时联网；**边界：**字体授权与地区排版规范需另行核对 |
| [chinese-web-themes](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/themes/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-web-themes) | 中式网页主题库（本站原创）：8 套中国美学 CSS 主题（水墨/青绿/宋韵/敦煌/朱砂/新中式/竹韵/夜宴），内置中文排版规范，对比度均超 WCAG AA。可在线预览 | 说明与本地演示资源；无独立可执行脚本；未发现运行时联网；**边界：**字体授权需由使用者核对 |
| [chinese-work-report](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/work-report/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-work-report) | 职场汇报助手（本站原创）：周报/月报/述职/项目汇报，结论先行、卖点翻价值，含 PPT 大纲 | 仅说明文件；无独立可执行脚本；未发现运行时联网；**边界：**不能编造业务数据或把动作冒充结果 |
| [ecommerce-copywriting](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/ecommerce-copywriting/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/ecommerce-copywriting) | 电商文案助手（本站原创）：商品标题、主图与详情页写作，按平台和用户决策路径组织；先核对事实、证明材料与高风险宣称，不把机械禁词替换当作合规保证 | 仅说明文件；无独立可执行脚本；未发现运行时联网；**边界：**广告宣称与受监管品类需核对当前规则和证明材料 |
| [github-readme-cn](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/readme-audit/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/github-readme-cn) | GitHub 中文项目门面优化（本站原创）：首屏结构、真实截图怎么截、命名与 topics、发布前自查清单。附 15 个高增长仓库的实测数据，明确区分相关性与不可验证的部分，不承诺涨星 | 说明与本地参考资料；无独立可执行脚本；未发现运行时联网；**边界：**增长相关性不等于因果，不承诺涨星 |
| [guochao-visual-cn](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/guochao/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/guochao-visual-cn) | 国潮视觉助手（本站原创）：12 种中国美学画风配方（水墨/工笔/青绿/敦煌/年画/剪纸/国漫等），输出可直接用的提示词，附纹样寓意与传统配色速查 | 说明与本地参考资料；无独立可执行脚本；未发现运行时联网；**边界：**文化准确性与艺术家个人风格边界 |
| [guofeng-threejs](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/guofeng-threejs/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/guofeng-threejs) | 国风 Three.js 渲染（本站原创）：水墨 shader 三技法（墨分五色/边缘积墨/笔触扰动），含可运行 demo 与移动端性能要点。只做中式渲染，不做通用 Three.js 教程 | 说明与浏览器演示；无独立可执行脚本；浏览器 Demo 从 unpkg.com 加载 three@0.170.0；**边界：**未标记敏感决策边界，仍需核对输出 |
| [homework-tutor-cn](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/homework/) · [源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/homework-tutor-cn) | 家长辅导作业助手（本站原创）：不生成给孩子直接抄写的成品，先给家长引导话术，再单列核对结果；含分学科方法与情绪对抗处理 | 仅说明文件；无独立可执行脚本；未发现运行时联网；**边界：**不生成供孩子直接抄写的答案；可另给家长核对结果 |

<a id="catalog-cn"></a>
### 🇨🇳 其他中文条目（61 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [colleague-skill](https://github.com/titanwings/colleague-skill) | ⭐23,763 | 中文向数字生命人格类 Skill，根目录同时有 SKILL.md 和 skills/ |
| [khazix-skills](https://github.com/kkkkhazix/khazix-skills) | ⭐19,937 | 中文数字生命博主卡兹克开源的 Skill 合集，扁平目录结构，每个子目录独立一个 SKILL.md |
| [agency-agents-zh](https://github.com/jnmetacode/agency-agents-zh) | ⭐19,705 | 267 个即插即用的中文 AI 专家角色，覆盖 20 个部门，含 52 个面向中国市场的原创智能体，兼容 18 种工具 |
| [humanizer-zh](https://github.com/op7418/humanizer-zh) | ⭐15,841 | 去除文本里的 AI 生成痕迹。基于维基百科「AI 写作特征」整理，检测并修复：夸大的象征意义、宣传性语言、-ing 结尾的肤浅分析、模糊归因、破折号过度使用、三段式法则、AI 词汇、否定式排比 🕰<sub>2026-01-19 后未更新</sub> |
| [awesome-chatgpt-zh](https://github.com/embraceagi/awesome-chatgpt-zh) | ⭐11,651 | ChatGPT 中文指南：指令、应用开发与资源清单，2023-03 建仓 |
| [garden-skills](https://github.com/conardli/garden-skills) | ⭐10,485 | ConardLi 开源的 Skills 合集，含网页设计、知识检索、图像生成等方向（中文作者） |
| [zhangxuefeng-skill](https://github.com/alchaincyf/zhangxuefeng-skill) | ⭐10,181 | 张雪峰的思维框架与表达方式：基于 5 本著作、15+ 篇采访、30+ 条语录整理出 5 个心智模型与 8 条决策启发式。用于分析教育选择、职业规划、阶层流动 |
| [dbskill](https://github.com/dontbesilent2025/dbskill) | ⭐9,666 | 个人技能合集（30 个）：公众号 HTML 排版、用阿德勒心理学框架诊断执行阻滞（知道该做却拖延时用）等 |
| [wechatdownload](https://github.com/qiye45/wechatdownload) | ⭐9,041 | 微信公众号文章批量下载，支持评论与合集，可导出 html/md/pdf/docx，提供 MCP/Skill 调用方式 |
| [superpowers-zh](https://github.com/jnMetaCode/superpowers-zh) | ⭐7,779 | superpowers 中文增强版：14 个核心工作流汉化 + 6 个中国开发场景 Skill；上游 README 当前列出 20 个 Skill |
| [oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode) | ⭐5,918 | 网文/小说写作 skill 包，覆盖扫榜、拆文、写作、去 AI 味、封面图全流程 |
| [anbeime-skill-store](https://github.com/anbeime/skill) | ⭐5,625 | 中文 Skill 商店，收录文档处理、内容创作、编程开发、机器学习、自动化工作流等领域的技能包合集 |
| [gzh-design-skill](https://github.com/isjiamu/gzh-design-skill) | ⭐3,250 | 微信公众号排版引擎：Markdown → 可直接粘进公众号编辑器的 HTML。6 套主题 + 主题生成器，自动章节编号、引言卡片、目录导航，支持 Word/PDF 输入 |
| [codex-claude-academic-skills](https://github.com/zLanqing/codex-claude-academic-skills) | ⭐3,083 | 学术科研三件套：文献阅读、论文写作、科学计算全流程 |
| [everything-claude-code-zh](https://github.com/xu-xiang/everything-claude-code-zh) | ⭐1,898 | Claude Code 完整配置中文翻译（agents/skills/hooks/commands） |
| [agent-skills-with-anthropic](https://github.com/datawhalechina/agent-skills-with-anthropic) | ⭐1,475 | 吴恩达 DeepLearning.AI 课程的中文翻译与知识整理 |
| [shuorenhua](https://github.com/MrGeDiao/shuorenhua) | ⭐1,174 | 「说人话」去 AI 味改写：保事实、分场景、改完可直接发 |
| [Awesome-Journal-Skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills) | ⭐1,013 | 主流期刊投稿技能包（AER、QJE 等经济学顶刊） |
| [claude-skill-web-clone](https://github.com/Jane-xiaoer/claude-skill-web-clone) | ⭐959 | 网站复刻方法论：先拿真源码 → 判路径 → 逆向拆解 → 搭工程 → 替换内容。覆盖静态站/React/WebGL/Canvas/Three.js。作者强调不靠 AI 幻觉出来的代码 |
| [speak-human-tw](https://github.com/Raymondhou0917/speak-human-tw) | ⭐875 | 繁体中文去 AI 味：抓 38 种 AI 写作痕迹，校正用语与标点 |
| [claude-code-skills-zh](https://github.com/laolaoshiren/claude-code-skills-zh) | ⭐784 | 面向中文开发者的技能库，按场景分类、复制即装 |
| [higgsfield-seedance2-jineng](https://github.com/beshuaxian/higgsfield-seedance2-jineng) | ⭐769 | AI 视频生成 15 个 prompt skill（Seedance 2.0 × Higgsfield） |
| [xiaohu-wechat-format](https://github.com/xiaohuailabs/xiaohu-wechat-format) | ⭐688 | 公众号一键排版发布：Markdown → 微信 HTML，30 套主题 |
| [Enterprise-ai-scenario-map-skill](https://github.com/MetaInFLow/Enterprise-ai-scenario-map-skill) | ⭐626 | 咨询向：为任何企业自动生成 AI 应用场景地图报告。含企业画像、业务诊断、行业实践、场景全量表、实施路径 |
| [Claude_skills_zh-CN](https://github.com/LeastBit/Claude_skills_zh-CN) | ⭐565 | 官方 anthropics/skills 的中文学习版 🕰<sub>2026-01-19 后未更新</sub> |
| [cuimao-translator](https://github.com/Cuimao777/cuimao-translator) | ⭐469 | 一键把英文 PDF 翻译成流畅中文 |
| [video-recap-skills](https://github.com/worldwonderer/video-recap-skills) | ⭐468 | 把任意视频剪成解说式短片 |
| [yupi-skill](https://github.com/liyupi/yupi-skill) | ⭐411 | 程序员鱼皮技能包：编程学习、求职面试、技术选型、创业经验 |
| [xiaohongshu-skills](https://github.com/vivy-yi/xiaohongshu-skills) | ⭐390 | 139 个小红书运营技能：内容创作、账号运营、电商转化等 9 大类 🕰<sub>2026-01-23 后未更新</sub> |
| [docx-skill-4-cn-paper](https://github.com/Gostyan/docx-skill-4-cn-paper) | ⭐376 | 中文论文排版规范：课程论文、数模竞赛、毕业论文 |
| [humanities-writing-companion](https://github.com/tizzy916/humanities-writing-companion) | ⭐362 | 人文学科写作助手：11 种模式覆盖构思到成稿 |
| [JobOK](https://github.com/GresonKwan/JobOK) | ⭐350 | 中文求职：优势挖掘、岗位匹配、简历优化、面试训练 |
| [opencode-skills](https://github.com/zrt-ai-lab/opencode-skills) | ⭐271 | 技能库：视频生成、图片生成、Agent 互联、智能问数 |
| [universal-examprep-skill](https://github.com/ZeKaiNie/universal-examprep-skill) | ⭐269 | 考前突击教练：把课件资料变成应试重点 |
| [skills_collection](https://github.com/wwwzhouhui/skills_collection) | ⭐262 | 个人实用技能集，覆盖开发效率与内容创作 |
| [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) | ⭐257 | 汇集多个上游 Skill 项目的中文学习版与教程；各子项目翻译范围以当前 README 为准 |
| [humanizer-zh-academic](https://github.com/redbaronyyyyy-eng/humanizer-zh-academic) | ⭐253 | 面向中文学术文本的 AI 写作特征审查与改写；检测率变化仅为上游案例，本仓库未独立复现 |
| [Bloom](https://github.com/Li-Evan/Bloom) | ⭐238 | 私人 AI 家教：识别你的学习方式，安排下一课 |
| [SecSkills](https://github.com/Arenbai/SecSkills) | ⭐216 | 渗透测试技能模块，遵循 PTES 标准全阶段覆盖 |
| [Vibe_coding_guide](https://github.com/Lling0000/Vibe_coding_guide) | ⭐213 | 中文优先的 Vibe Coding 工程化流程指南 |
| [technical-writing](https://github.com/luoling8192/technical-writing) | ⭐209 | 中文技术写作：设计文档、评审稿、复盘、分享稿 |
| [niubiskill](https://github.com/nathanskill/niubiskill) | ⭐208 | 中文变现决策：判断一件事是否接近收入再投入 |
| [openclaw-guide](https://github.com/liyupi/openclaw-guide) | ⭐186 | OpenClaw 中文文档站：安装部署、Agent 架构、Skills 配置 |
| [makeownsrt](https://github.com/joshhu/makeownsrt) | ⭐175 | 从 MKV 提取英文字幕并翻成繁中双语 SRT |
| [Auto-CV](https://github.com/flamingoTOM/Auto-CV) | ⭐174 | LaTeX 中文简历模板 + 自动提取内容生成 |
| [openclaw-xhs](https://github.com/zhjiang22/openclaw-xhs) | ⭐118 | 小红书 MCP 工作流：搜索与读取笔记、评论互动、发布、热点跟踪及长图导出；写操作需复核上游配置与账号权限 |
| [hermes-arxiv-agent](https://github.com/genggng/hermes-arxiv-agent) | ⭐117 | 每天自动抓 arXiv 论文，生成中文摘要推送到飞书 |
| [wechat-writing-style](https://github.com/yaoleifly/wechat-writing-style) | ⭐78 | 微信公众号中文写作风格 |
| [kc_ai_skills](https://github.com/KerberosClaw/kc_ai_skills) | ⭐78 | 中文优先的 Claude Code / Codex skills 合集 |
| [stop-slop-zh](https://github.com/VincentOld/stop-slop-zh) | ⭐68 | 消除中文 AI 写作痕迹：拆排比、去名词化、换具体细节 |
| [cnki-aigc---skill](https://github.com/qingshanliuci/cnki-aigc---skill) | ⭐37 | 针对知网 AIGC 标记段落的中文改写工作流；效果数字仅为上游案例，本仓库未独立复现 |
| [awesome-skills-zh](https://github.com/yzfly/awesome-skills-zh) | ⭐29 | 精选 Claude / Agent / LLM Skills 中文资源列表 |
| [awesome-claude-skills-zh-TW](https://github.com/ammosu/awesome-claude-skills-zh-TW) | ⭐25 | awesome-claude-skills 繁体中文化版本 🕰<sub>2025-12-15 后未更新</sub> |
| [scholar-wendao-skill](https://github.com/tizzy916/scholar-wendao-skill) | ⭐20 | 学者问道：把学者视角提炼成可复用框架 |
| [refine-legal-chinese](https://github.com/katejianglaw/refine-legal-chinese) | ⭐15 | 法言法语：把口语化表述改写为规范法律中文 |
| [awesome-claude-skills-zh](https://github.com/shishirui/awesome-claude-skills-zh) | ⭐15 | 中文社区优先的 Claude skills 精选收录 |
| [ip-character-designer](https://github.com/Beatatata/ip-character-designer) | ⭐11 | 自媒体 IP 配图生成器：10 种画风 × 双版本 × 中文提示词 |
| [awesome-claude-skills-cn](https://github.com/bbylw/awesome-claude-skills-cn) | ⭐9 | Awesome Claude Skills 中文版 🕰<sub>2026-01-14 后未更新</sub> |
| [cn-humanizer-academic](https://github.com/ranranrannervous/cn-humanizer-academic) | ⭐6 | 中文学术论文降 AI 痕迹，针对 BERT 语义检测器 |
| [CN-The-Complete-Guide-to-Building-Skill-for-Claude](https://github.com/chenqing0106/CN-The-Complete-Guide-to-Building-Skill-for-Claude) | ⭐5 | 《为 Claude 构建技能的完整指南》中文翻译：结构、模式、测试、分发 |
| [ai-video-creator](https://github.com/Frank-oll/ai-video-creator) | ⭐5 | 把生活妙招选题端到端做成可发布的竖屏 AI 短视频（含配音） |

<a id="catalog-doc"></a>
### 📄 文档办公（10 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [docx](https://github.com/anthropics/skills/tree/main/skills/docx) | 官方 | Word 文档全流程：创建、读取、编辑、修订标记、批注、排版 |
| [pdf](https://github.com/anthropics/skills/tree/main/skills/pdf) | 官方 | PDF 处理：提取文字/表格/元数据、合并、拆分、批注 |
| [pptx](https://github.com/anthropics/skills/tree/main/skills/pptx) | 官方 | PPT 演示文稿：读取、生成幻灯片、调整版式与模板 |
| [xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx) | 官方 | Excel 表格：公式计算、图表生成、数据转换 |
| [doc-coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) | 官方 | 结构化文档协作撰写流程，引导多人共同完成文档 |
| [open-notebook](https://github.com/lfnovo/open-notebook) | ⭐37,270 | NotebookLM 的开源替代，灵活度和功能更强。含发布流程编排技能（变更日志审计、风险分级测试矩阵、Docker 镜像门禁） |
| [NotebookLM Integration](https://github.com/PleasePrompto/notebooklm-skill) | ⭐7,667 | 让 Claude Code 直接对话 NotebookLM，做有出处的问答 🕰<sub>2025-11-21 后未更新</sub> |
| [article-extractor](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/article-extractor) | ⭐524 | 从网页提取完整文章正文与元数据 |
| [Markdown to EPUB Converter](https://github.com/smerchek/claude-epub-skill) | ⭐154 | 把 Markdown 文档转成专业 EPUB 电子书 🕰<sub>2025-10-18 后未更新</sub> |
| [Master Claude for Legal](https://github.com/sboghossian/master-claude-for-legal) | ⭐56 | 法务技能包：NDA 审阅、多方版本对比、引用核验 |

<a id="catalog-ppt"></a>
### 📊 PPT 演示（19 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [ppt-master](https://github.com/hugohe3/ppt-master) | ⭐48,524 | 生成可编辑的原生 PPTX：原生形状、转场动画、数据图表；可建可复用的品牌/风格/版式工作区，也能填充现有 PPTX 模板或增强已完成的稿子 |
| [frontend-slides](https://github.com/zarazhangrui/frontend-slides) | ⭐27,933 | 用前端能力做网页幻灯片：从零生成或把 PPT/PPTX 转成网页，动画丰富，面向不做设计的人 |
| [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | ⭐24,596 | 横向翻页网页 PPT（单 HTML）：含 WebGL 背景、演讲者视图、观众屏同步、讲稿备注。两种风格——「电子杂志×电子墨水」和「瑞士国际主义」 |
| [banana-slides](https://github.com/anionex/banana-slides) | ⭐15,486 | 基于 nano banana pro 的 AI PPT 生成应用，支持上传模板图片、一句话/大纲生成、导出可编辑 ppt |
| [html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) | ⭐8,008 | HTML PPT Studio：24 套主题、31 种版式、20+ 动画，模板驱动的静态 HTML 演示 |
| [dashi-ppt-skill](https://github.com/chuspeeism/dashi-ppt-skill) | ⭐5,904 | 基于预置视觉主题组合页面，生成可离线打开、可在浏览器编辑的 HTML 演示，支持导出 PPTX / PDF |
| [qiaomu-anything-to-notebooklm](https://github.com/joeseesun/qiaomu-anything-to-notebooklm) | ⭐5,776 | 多源内容处理器：公众号、网页、YouTube、播客（小宇宙/喜马拉雅）、PDF、Markdown → 自动上传 NotebookLM 并生成播客/PPT/思维导图 |
| [codex-ppt-skill](https://github.com/ningzimu/codex-ppt-skill) | ⭐5,110 | 用 GPT-Image-2 从文章、报告、论文、笔记或大纲生成视觉统一的图片式 PPTX |
| [bento](https://github.com/nyblnet/bento) | ⭐4,416 | 把一套办公软件塞进单个文件：.bento.html 演示稿，文档本身是 JSON，双击就能编辑与放映，自带演讲者窗口 |
| [NanoBanana-PPT-Skills](https://github.com/op7418/NanoBanana-PPT-Skills) | ⭐3,216 | 自动生成高质量 PPT 图片和视频，支持智能转场与交互式播放 🕰<sub>2026-01-19 后未更新</sub> |
| [GordenPPTSkill](https://github.com/GordenSun/GordenPPTSkill) | ⭐2,967 | 21 套内置中文 PPT 模板（也支持自带 .pptx）：只替换文字、不破坏原排版配色字号，内置出框检测与同级标题字号校验。适合工作汇报、述职竞聘、开题答辩 |
| [image-to-editable-ppt-skill](https://github.com/ningzimu/image-to-editable-ppt-skill) | ⭐2,099 | 把幻灯片截图、扫描件、图片式 PPTX 和 PDF 还原成对象级可编辑的 PowerPoint |
| [GordenSuperPPTSkills](https://github.com/GordenSun/GordenSuperPPTSkills) | ⭐1,791 | 把图片格式的 PPT 逆向还原成可编辑 .pptx：复刻背景 + 绿幕抠框架 + 抠元素图标 + GPT 视觉提取文字，再合成（文字是真文本框） |
| [CyberPPT](https://github.com/crazyykhllc-bit/CyberPPT) | ⭐1,625 | 把 DOCX/PDF/TXT/XLSX、研究报告、原始数据转成高密度、可编辑的咨询风格 PPTX，支持 SCR 叙事、风格确认与渲染质检 |
| [harness-anything](https://github.com/yb2460/harness-anything) | ⭐1,503 | AI 控制中枢：WPS、MS Office、Zotero、Photoshop，47 个 CLI 命令 + 27 个学术技能。含 JSON 数据驱动的 PPT 自动生成 |
| [ian-handdrawn-ppt](https://github.com/helloianneo/ian-handdrawn-ppt) | ⭐1,345 | 中文手绘技术 PPT 整页图像生成：21:9 封面 + 16:9 正文配图，PNG 输出 |
| [ppt-image-first](https://github.com/NyxTides/ppt-image-first) | ⭐1,196 | 对话优先的演示规划：先聊清楚要讲什么，再给多个视觉方向的预览图，最后才写稿 |
| [gpt-image2-ppt-skills](https://github.com/JuneYaooo/gpt-image2-ppt-skills) | ⭐1,196 | 克隆任意 .pptx 的版式做成自己的稿子：gpt-image-2 模仿版式，你提供内容。内置 10 套风格，输出高清 PNG 与 16:9 .pptx |
| [ppt-agent-skills](https://github.com/sunbigfly/ppt-agent-skills) | ⭐884 | 像做软件工程一样做演示：模拟顶级 PPT 设计公司的完整流程（需求调研→资料搜集→大纲策划→策划稿→设计稿），输出 HTML |

<a id="catalog-dev"></a>
### 💻 开发工程（36 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 官方 | Anthropic 官方维护的 Claude Code 插件目录，plugins/ 下按插件组织 |
| [agent-skills](https://github.com/vercel-labs/agent-skills) | 官方 | Vercel 官方的 agent skills 集合，仓库根目录 skills/ 下直接可取 |
| [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | 官方 | 写 Skill 的 Skill —— 创建、改进、评估技能，新手从这个开始 |
| [mcp-builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) | 官方 | 构建高质量 MCP（Model Context Protocol）服务的完整指南 |
| [web-artifacts-builder](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) | 官方 | 构建复杂多组件网页应用（React / Tailwind / shadcn-ui 技术栈） |
| [webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | 官方 | 本地 Web 应用的交互测试工具集 |
| [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | 官方 | 前端视觉设计指导，做出有辨识度、有意图的界面 |
| [claude-api](https://github.com/anthropics/skills/tree/main/skills/claude-api) | 官方 | Claude API 使用参考：模型 ID、定价、参数、流式、工具调用、缓存 |
| [test-driven-development](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) | ⭐275,770 | 测试驱动开发全流程指导，写代码前先写测试 |
| [using-git-worktrees](https://github.com/obra/superpowers/blob/main/skills/using-git-worktrees/) | ⭐275,770 | 自动创建隔离的 git worktree，多分支并行开发不打架 |
| [finishing-a-development-branch](https://github.com/obra/superpowers/tree/main/skills/finishing-a-development-branch) | ⭐275,770 | 开发分支收尾：合并、清理、发布的标准流程 |
| [composio-awesome-claude-skills](https://github.com/composiohq/awesome-claude-skills) | ⭐72,989 | Claude Skills 与 Plugins 清单型索引；清单本身不提供所列项目的统一功能实测 |
| [system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks) | ⭐63,340 | 各家 AI 产品的系统提示词收集：Anthropic（Claude Fable 5 / Opus 5 / Claude Code）、OpenAI（GPT-5.6-Sol / Codex）等，持续更新。含 9 个 SKILL.md |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | ⭐52,795 | Claude Code 资源精选清单，覆盖工作流、命令、配置等（清单型） |
| [wshobson-agents](https://github.com/wshobson/agents) | ⭐39,011 | 跨 harness 的 agent 插件市场，同时支持 Claude Code / Codex CLI / Cursor / OpenCode / Copilot / Gemini |
| [awesome-agent-skills](https://github.com/voltagent/awesome-agent-skills) | ⭐30,798 | 汇总 1000+ 个来自官方团队与社区的 agent skill 的索引清单（清单型） |
| [planning-with-files](https://github.com/othmanadi/planning-with-files) | ⭐26,269 | Manus 式的文件化持久规划：把 task_plan.md / findings.md / progress.md 落到磁盘，上下文丢了工作也不丢。含 18 个子技能 |
| [baoyu-skills](https://github.com/jimliu/baoyu-skills) | ⭐25,235 | 宝玉的技能合集（22 个）：公众号摘要、发布流程自动化（自动识别版本文件与 changelog，支持 Node/Python/Rust/Claude Plugin）等 |
| [claude-skills-345](https://github.com/alirezarezvani/claude-skills) | ⭐24,785 | 330+ skill、30+ agent、70+ 自定义命令的合集，.claude/ 与 agents/ 分开组织 |
| [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) | ⭐14,794 | 把任意文档网站自动转成 Claude Skill —— 造 skill 的利器 |
| [claude-seo](https://github.com/agricidaniel/claude-seo) | ⭐14,768 | Claude Code 的 SEO Skill，含子技能与子 agent，覆盖技术 SEO、E-E-A-T、schema 等方向 |
| [travisvn-awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | ⭐14,767 | Claude Skills 清单型索引，偏重工作流定制方向 |
| [fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) | ⭐10,753 | 生成技术图表：软件架构、数据流、流程图、时序图、C4 模型、云部署、事件流 |
| [reddit-fetch](https://github.com/ykdojo/claude-code-tips/tree/main/skills/reddit-fetch) | ⭐9,843 | 当 WebFetch 被拦时，通过 Gemini CLI 抓取 Reddit 内容 |
| [drawio-skill](https://github.com/Agents365-ai/drawio-skill) | ⭐7,881 | 用自然语言生成 draw.io 图表：11 种预设（UML、SysML/MBSE、BPMN、网络拓扑、C4 架构等），36 个工具 |
| [lean-ctx](https://github.com/yvgude/lean-ctx) | ⭐3,626 | AI 编程代理的上下文运行时，管理会话与上下文 |
| [Playwright Browser Automation](https://github.com/lackeyjb/playwright-skill) | ⭐3,049 | 用 Playwright 做浏览器自动化测试与验证 |
| [oh-my-mermaid](https://github.com/oh-my-mermaid/oh-my-mermaid) | ⭐2,199 | 把代码库结构转成可导航的架构图 skill，基于 Claude Code，输出 Mermaid 图 |
| [subagent-driven-development](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/sadd/skills/subagent-driven-development) | ⭐1,348 | 把任务拆给多个子智能体并行处理，加速复杂开发 |
| [software-architecture](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/ddd/skills/software-architecture) | ⭐1,348 | 实现整洁架构、SOLID 等设计模式 |
| [prompt-engineering](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/customaize-agent/skills/prompt-engineering) | ⭐1,348 | 系统讲解提示词工程的技巧与模式 |
| [iOS Simulator](https://github.com/conorluddy/ios-simulator-skill) | ⭐1,222 | 操作 iOS 模拟器做 App 测试 |
| [aws-skills](https://github.com/zxkane/aws-skills) | ⭐351 | AWS 开发：CDK 最佳实践、成本优化、Serverless 架构 |
| [D3.js Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill) | ⭐223 | 用 D3 做交互式数据可视化图表 🕰<sub>2025-10-18 后未更新</sub> |
| [great_cto](https://github.com/avelikiy/great_cto) | ⭐81 | 7 个专业子智能体（技术负责人、资深工程师等）组成的技术团队 |
| [clone-any-website-skill](https://github.com/promptwhisper/clone-any-website-skill) | ⭐64 | Codex 技能：把公开网站重建成干净可维护的本地项目，讲究视觉、交互、媒体与多端还原度 |

<a id="catalog-agent"></a>
### 🤖 Agent 与调研（8 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [Agent-Reach](https://github.com/Panniantong/Agent-Reach) | ⭐73,946 | 给 AI 装上看全网的眼睛：读取与搜索 Twitter、Reddit、YouTube、GitHub、B 站、小红书。一个 CLI，零 API 费用。中文触发词齐全（全网调研 / 查一下 / 看看大家怎么评价） |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | ⭐58,920 | 调研某个话题最近 30 天大家实际在说什么：抓 Reddit、X、YouTube、TikTok、HN、Polymarket、GitHub 的帖子与互动数据，输出带引用的总结。自带健康检查诊断失效数据源 |
| [OpenMontage](https://github.com/calesthio/OpenMontage) | ⭐49,345 | 开源的智能体视频生产系统：12 条流水线、100+ 工具、700+ agent 技能，含 130 个 SKILL.md。覆盖配乐生成、素材处理、剪辑决策全流程 |
| [awesome-claude-code-subagents](https://github.com/voltagent/awesome-claude-code-subagents) | ⭐24,531 | 100+ 个 Claude Code 专用 subagent，覆盖较广的开发场景 |
| [agent-skills-for-context-engineering](https://github.com/muratcankoylan/agent-skills-for-context-engineering) | ⭐17,797 | 面向上下文工程与多 agent 架构的 skill 集，根目录同时有 SKILL.md 和 skills/ |
| [video-shotcraft](https://github.com/vincentwei1021/video-shotcraft) | ⭐5,994 | 面向 Claude Code / Codex 的产品视频生成 skill，含分镜卡片与运镜手法库，基于 Remotion 渲染 |
| [watch-skill](https://github.com/oxbshw/watch-skill) | ⭐304 | 让 AI 看懂视频：把视频、直播流、以及 agent 自己的录屏转成可理解的内容并自我校验。含 11 个 SKILL.md，一键装 ffmpeg/yt-dlp 与 MCP |
| [super-video-maker-skill](https://github.com/Bomx/super-video-maker-skill) | ⭐226 | 端到端 AI 视频生产：HeyGen 数字人、Seedance/字节素材、OpenAI 配图、Remotion 合成，覆盖制作/剪辑/字幕/配乐/导出 |

<a id="catalog-design"></a>
### 🎨 创意设计（12 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design) | 官方 | 用设计原理创作视觉作品，输出 PNG / PDF |
| [algorithmic-art](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art) | 官方 | 用 p5.js 创作算法艺术，支持随机种子与交互 |
| [theme-factory](https://github.com/anthropics/skills/tree/main/skills/theme-factory) | 官方 | 为作品套用主题配色的工具集（幻灯片、网页等） |
| [brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) | 官方 | 把品牌配色与字体规范应用到各类产出物 |
| [slack-gif-creator](https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator) | 官方 | 制作适配 Slack 的动图 GIF |
| [taste-skill](https://github.com/Leonxlnx/taste-skill) | ⭐79,068 | 让 AI 别再生成套路化口水内容。13 个子技能：品牌套件、极简、粗野主义、图生代码、前端配图（Web/移动端）等，主打有审美的产出 |
| [ian-xiaohei-illustrations](https://github.com/helloianneo/ian-xiaohei-illustrations) | ⭐10,018 | 中文小黑怪诞正文配图生成 Skill，16:9 白底手绘风格，Codex Skill 形态（与已收录 ian-handdrawn-ppt 同作者） |
| [youtube-transcript](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/youtube-transcript) | ⭐524 | 抓取 YouTube 视频字幕并整理成摘要 |
| [imagen](https://github.com/sanjay3290/ai-skills/tree/main/skills/imagen) | ⭐401 | 调用 Google Gemini 图像生成 API 出图 |
| [swiftui-design-skill](https://github.com/wholiver/swiftui-design-skill) | ⭐172 | SwiftUI 前端设计（中文）：反 AI 味六条铁律、设计顾问、五维评审 |
| [anydesign](https://github.com/uxKero/anydesign) | ⭐161 | 分析任意图片/网址/Figma 文件，生成结构化设计规范 |
| [pakco-html](https://github.com/pakco77/pakco-html) | ⭐71 | HTML 审美库（中文）：60+ 视觉风格、演示页/长页模板，一键复制 Prompt |

<a id="catalog-biz"></a>
### 💼 办公协作（13 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [internal-comms](https://github.com/anthropics/skills/tree/main/skills/internal-comms) | 官方 | 撰写各类内部沟通文案的资源集 |
| [brainstorming](https://github.com/obra/superpowers/tree/main/skills/brainstorming) | ⭐275,770 | 把粗略想法通过结构化提问变成完整方案 |
| [pm-skills](https://github.com/phuryn/pm-skills) | ⭐25,513 | 产品经理技能市场：68 个 PM Skill + 42 条链式工作流，打包成 9 个插件。覆盖需求发现、产品策略、执行、上线到增长。⚠️ 方法论偏国外语境，国内 PM 可作参考 |
| [product-manager-skills](https://github.com/deanpeters/product-manager-skills) | ⭐6,586 | 面向产品经理的 skill 框架，适配 Claude Code / Cowork / Codex 等多个 agent 客户端 |
| [aaron-marketing-skills](https://github.com/aaron-he-zhu/aaron-marketing-skills) | ⭐2,619 | 面向市场营销的 Claude Code 插件形态 skill 合集，覆盖 SEO/GEO、红人营销、付费投放等方向 |
| [kaizen](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/kaizen/skills/kaizen) | ⭐1,348 | 持续改进方法论，多种分析框架 |
| [Brand Build Skills](https://github.com/rampstackco/claude-skills) | ⭐569 | 59 个 skill 的品牌与网站全生命周期库 |
| [tapestry](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/tapestry) | ⭐524 | 把相关文档互联并总结成知识网络 |
| [ship-learn-next](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/ship-learn-next) | ⭐524 | 基于进展帮你决定下一步该做什么/学什么 |
| [google-workspace-skills](https://github.com/sanjay3290/ai-skills/tree/main/skills) | ⭐401 | Google 全家桶集成：Gmail、日历、Chat 等 |
| [n8n-skills](https://github.com/haunchen/n8n-skills) | ⭐389 | 让 AI 直接理解和操作 n8n 工作流 |
| [seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) | ⭐159 | SEO / GEO（生成式引擎优化）技能集，20 个子技能：外链分析、关键词研究、内容写作等；另记录 skills.sh 安装次数，该数值不等于独立用户或实际使用 |
| [solo-skills](https://github.com/rockscy/solo-skills) | ⭐7 | 独立开发者双语（中英）技能包：7 个 solo 场景 |

<a id="catalog-data"></a>
### 📊 数据研究（5 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [root-cause-tracing](https://github.com/obra/superpowers/tree/main/skills/root-cause-tracing) | ⭐275,770 | 错误深藏在执行链路时，追溯根本原因 |
| [CSV Data Summarizer](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill) | ⭐452 | 自动分析 CSV 文件并生成完整数据报告 🕰<sub>2025-10-16 后未更新</sub> |
| [deep-research](https://github.com/sanjay3290/ai-skills/tree/main/skills/deep-research) | ⭐401 | 调用 Gemini Deep Research 做自主多步研究 |
| [postgres](https://github.com/sanjay3290/ai-skills/tree/main/skills/postgres) | ⭐401 | 对 PostgreSQL 执行安全的只读 SQL 查询 |
| [recursive-research](https://github.com/Anjos2/recursive-research) | ⭐40 | 跨领域递归研究，可深入到博士级别 |

<a id="catalog-sec"></a>
### 🔐 安全取证（7 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | ⭐27,279 | 逆向工程与授权渗透测试的 Skill 路由包 |
| [skillspector](https://github.com/nvidia/skillspector) | ⭐14,859 | NVIDIA 出品的 AI agent skill 安全扫描器，检测漏洞、恶意模式与 prompt injection 风险 |
| [claude-bughunter](https://github.com/elementalsouls/claude-bughunter) | ⭐3,722 | 面向漏洞挖掘与外部红队工作的 Claude Code skill 合集，含多个 slash 命令 |
| [computer-forensics](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/computer-forensics) | ⭐662 | 数字取证分析与调查技术 |
| [metadata-extraction](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/metadata-extraction) | ⭐662 | 提取分析文件元数据用于取证 |
| [file-deletion](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/file-deletion) | ⭐662 | 安全删除文件与数据清除方法 |
| [FFUF Web Fuzzing](https://github.com/jthack/ffuf_claude_skill) | ⭐207 | 集成 ffuf 做 Web 模糊测试 🕰<sub>2025-10-16 后未更新</sub> |

<a id="catalog-3d"></a>
### 🧊 3D 与图形（5 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [img2threejs](https://github.com/img2threejs/img2threejs) | ⭐12,674 | 把参考图还原成纯代码的程序化 Three.js 模型，带质量门禁、可直接做动画。用于图生 3D、物体精细重建、风格化人物 |
| [threejs-skills](https://github.com/CloudAI-X/threejs-skills) | ⭐3,080 | Three.js 分领域技能包（10 个子技能）：场景与相机基础、几何体、材质、贴图、光照、动画、交互、着色器、后期处理、模型加载 |
| [img2obj](https://github.com/vinhhien112/img2obj) | ⭐1,607 | Codex 插件：给一张物体图，校验并把它重建为可编辑的程序化 Three.js 资产 |
| [threejs-game-skills](https://github.com/majidmanzarpour/threejs-game-skills) | ⭐1,325 | 用 Three.js 做浏览器游戏的 9 个技能：玩法系统、AAA 级画面、游戏 UI、3D/图像/音频资产生成、调试与性能分析、QA 与发布 |
| [auteur](https://github.com/agiwhitelist/auteur) | ⭐1,018 | 把网页当电影来导：整站从零设计构建，滚动驱动的电影感叙事页，多屏产品（应用/仪表盘/后台/引导/文档）共用一套设计系统 |

<a id="catalog-game"></a>
### 🎮 游戏开发（5 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | ⭐24,399 | 把 Claude Code 变成完整游戏工作室：49 个 AI 智能体 + 72 个工作流技能 + 一套协调系统。仓库含 74 个 SKILL.md |
| [sprite-gen](https://github.com/aldegad/sprite-gen) | ⭐733 | 生成干净的 2D 游戏精灵图与动画图集：状态分行、去除杂边、逐帧对齐的流水线 |
| [novel-to-game](https://github.com/worldwonderer/novel-to-game) | ⭐687 | 把小说变成有据可依、可实际游玩的游戏：7 个技能覆盖小说分析、游戏概念、世界设计、美术指导、构建与 QA |
| [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) | ⭐591 | 游戏开发技能路由：装一次，主路由自动识别引擎（Godot/Unity/Unreal/Bevy/Phaser/PixiJS/three.js/LÖVE/pygame/Roblox）并调用对应技能。含 67 个 SKILL.md |
| [GD-Agentic-Skills](https://github.com/thedivergentai/GD-Agentic-Skills) | ⭐564 | Godot 4.7+ 专用技能库：97 个专家技能 + 27 个指南，覆盖 2D/3D 动画、物理、光照、材质、世界构建、能力系统等 |

---

## 怎么自己写一个 Skill

```
my-skill/
└── SKILL.md          # 必需
    references/       # 可选
```

**一个建议**：写清楚「不做什么」和「能做什么」同样重要。
我们 13 个原创 Skill 都写明了边界——记账不做税务筹划、辅导作业不给答案、
学习教练不替你完成输出、国潮视觉不伪造文物。

推荐用官方 [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 生成。

---

## ⚠️ 安全提醒

Skills 可含**可执行脚本**。装第三方前先看 `SKILL.md` 和 `scripts/` 内容。

---

*本文件由脚本从 `data/skills.json` 自动生成，最后更新 2026-08-22。*
*收录有误或想推荐新 Skill？欢迎 [提 Issue](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues)*
