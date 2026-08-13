# Codex Skill 搜索型文章：分发素材

> 准备日期：2026-08-12。仓库内文章已经上线；本文件只准备文案，不代表已经发布到外部平台。

## 发布顺序

优先发“不自动触发排查”，因为问题更具体，正文包含可执行命令和判断树。至少观察一天评论，再决定是否发布“创建 Skill”教程；不要同一小时铺到多个社区。

## 主题一：安装了却不自动触发

文章：https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/codex-skill-not-triggering/

### V2EX / Linux.do 标题

Codex Skill 明明安装了却不触发？我把排查过程拆成了 5 层

### 正文

最近在逐个复测中文 Agent Skills 时，我发现“Skill 不能用”通常混了 5 种不同问题：

1. CLI 根本没有发现它
2. 安装命令结束了，但文件没有落盘
3. 文件存在，但 Codex 没有自动读取
4. Codex 读对了 Skill，但任务没有完成
5. 模型开始前就被账户、网络或平台阻断

这五种情况的修法不同，也不能都记成 Skill 失败。

我整理了一棵可以照着走的诊断树，包含 `--list`、文件检查、不点名 Skill 的自然任务测试，以及“环境阻断为什么不能归因给 Skill”：

https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/codex-skill-not-triggering/

文中的通过案例来自 Codex CLI 0.147.0-alpha.6.5 的单任务记录；它不是所有版本或提示词的兼容保证。遇到不同结果，成功或失败都欢迎提交。

### 掘金 / 知乎开头

Codex Skill 的文件已经在 `~/.agents/skills/`，为什么任务里还是没有出现？

最容易犯的错误，是一看到“不触发”就反复重装。安装只是第二层证据：在它之前还有 CLI 发现，在它之后还有客户端自动选择、任务完成和环境状态。

### 短帖

“Codex Skill 不能用”至少可能是 5 件不同的事：发现失败 / 文件未落盘 / 未自动读取 / 读到了但没完成 / 模型开始前环境阻断。

我把排查顺序、命令和真实案例整理成了一棵诊断树：
https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/codex-skill-not-triggering/

单任务实测，不是跨版本保证。

## 主题二：创建自己的 Codex Skill

文章：https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/create-codex-skill/

### V2EX / Linux.do 标题

写 Codex Skill 不该从长 Prompt 开始：一个最小 SKILL.md 的完整例子

### 正文

我在维护 13 个中文 Skill 后，越来越确定一件事：一个好 Skill 不是“更长的 Prompt”，而是一个已经跑通过、能验收的重复工作流。

OpenAI 当前文档里，最小 Skill 是一个含 `SKILL.md` 的目录，`name` 和 `description` 必填。Codex 先根据名称和描述判断是否选择，选中后才读取完整说明。

所以真正难写的不是正文，而是 description：它必须让客户端知道“什么时候选我”和“什么时候别选我”。

我用一个真实中文排版 Skill 拆了最小结构、description 正反例、按需拆分 scripts/references/assets，以及安装、自动触发和最终交付的三层测试：

https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/create-codex-skill/

容易变化的格式与行为均链接 OpenAI 官方文档；安装路径和触发结果则单独标为仓库实测。

### 短帖

写 Codex Skill，别从长 Prompt 开始。先找一次已经成功、以后会重复、而且能验收的任务；再写最小 SKILL.md，把“何时使用”和“不做什么”放进 description 前部。

真实中文排版 Skill 的结构、触发描述与三层验证：
https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/create-codex-skill/

## 主题三：Agent Skill 测试失败后怎么修

文章：https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/fix-agent-skill/

### V2EX / Linux.do 标题

Agent Skill 测试失败后，我为什么坚持用同一道题复测

### 正文

测试失败后，最容易让数字变好看的做法，是改一道更容易的题、删掉没满足的门槛，或者只保留修复后的结果。这样无法证明原问题已经关闭。

这次我保留了两条预注册失败：一个中文网页主题 Skill 漏掉授权检查，记为 3/4；一个国风 Three.js Skill 超过 300 字限制，408 个 Unicode 字符，也记为 3/4。

修复只改通用指令：前者补齐六项上线检查，后者增加短答模板和字符计数。然后重放完全相同的原任务，分别达到 4/4 和 294 个 Unicode 字符；初次失败仍公开保留。

完整任务、门槛、前后输出和证据边界：
https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/fix-agent-skill/

这只是所记录 Codex 环境中的两条任务结果，不是总体准确率或跨客户端保证。

### 短帖

Agent Skill 测试失败后，不改题、不降门槛、不覆盖旧失败。先定位最小指令缺口，再用完全相同的任务复测。

两条真实 3/4 → 4/4 的完整记录：
https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/fix-agent-skill/

## 发布后记录

每个平台一次只发一篇，记录平台、发布 URL、发布时间、标题版本，以及 24 小时和 72 小时后的独立访客、引荐来源、Star 与事实纠错。变化只能写“发布后观察到”，不能直接归因于文章。不得互 Star、买量、群发私信或主动索要 Star。
