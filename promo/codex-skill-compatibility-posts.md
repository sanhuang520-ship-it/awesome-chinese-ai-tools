# Codex Agent Skills 兼容性实测：发布素材

> 事实基线：2026-08-12 · Codex CLI `0.147.0-alpha.6.5` · 13 个本站原创 Skill · 公开页面：<https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/compatibility/>

所有版本都避免“全面兼容”“准确率 100%”“保证涨星”等无法支持的说法。发布前如客户端版本或案例数变化，应同步更新。

## 推荐主帖：Linux.do / V2EX

### 标题

```text
我把 13 个中文 Agent Skills 逐个做了 Codex 自动触发测试，发现“能触发”不等于“能完成”
```

### 正文

```markdown
我在维护一个中文 Agent Skills 库。之前 README 里写“支持 Codex”，但这个说法其实太粗了：

- CLI 能发现
- 文件能安装
- Codex 会自动选择
- 最终任务能完成

这是四件不同的事。

所以我用 Codex CLI `0.147.0-alpha.6.5`，给 13 个本站原创 Skill 各做了一次**不在提示中点名 Skill**的任务测试。

结果：

- 13 / 13 都发生了自动触发
- 10 项当次任务完成
- 1 项按流程先提问，等待用户补充必要信息
- 2 项虽然选对 Skill，但完整任务没有完成
- 把任务输出范围缩小后，这 2 项复测通过

两个失败分别是完整教案和水墨 Three.js 技术审查。后者暴露出 Skill 会读取过多 Demo 源码，于是我修改了流程：只做方案审查时，先给结论，最多核对 Three.js 版本、shader 关键字和性能保护三类证据。

测试还持续出现一个 Codex 告警：安装的 Skill 较多时，部分 description 会因上下文预算被缩短。现有 13 项仍正确触发，但这不代表换一种提示词也一定能触发。

成功、失败、6 条逐字任务原文、7 条任务摘要、客户端版本和限制都放在这里：

https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/compatibility/

目前只实测了 Codex。Claude Code 和 Cursor 仍是待测，格式看起来兼容不能算实际通过。如果有人愿意复现其中一个，成功或失败结果都欢迎。
```

## 知乎 / 掘金短文开头

```markdown
“这个 Skill 支持 Codex”到底是什么意思？

是 `npx skills add` 能看到它，文件进入了 `~/.agents/skills/`，Codex 在合适任务里会主动读取它，还是它最终真的完成了任务？

我以前把这些状态混在一起。于是这次用 13 个中文 Agent Skills 做了一轮逐项测试，结果是：全部自动触发，但两项在选对 Skill 后仍没有完成。
```

后续可直接沿用主帖的四层证据、两个失败和限制部分。不要把文章扩写成 13 项输出流水账；重点是测试方法和反例。

## 微博 / 即刻 / X 中文短帖

```text
刚把 13 个中文 Agent Skills 逐个做了 Codex 自动触发测试：

13/13 会自动选择正确 Skill：10 项当次任务完成，1 项按设计停在必要的校准提问。

另外 2 项“选对了，却没做完”；缩小输出范围后才通过。其中一个还促使我修改了 Skill 的源码审查流程。

所以：能发现 ≠ 能安装 ≠ 会触发 ≠ 能完成。

成功、失败和任务记录都公开；其中 6 条保留逐字原文，7 条只有摘要：
https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/compatibility/

目前只确认 Codex，Claude Code / Cursor 仍待测。
```

## GitHub Discussion 更新回复

```markdown
兼容性实测第一轮已经完成：13 个本站原创 Skill 都在未点名名称的 Codex 任务中发生了自动触发。

但其中 2 个完整任务在首次执行时没有完成，缩小输出范围后复测通过。原始失败没有删除，也促成了 `guofeng-threejs` 审查流程的修订。

完整记录：<https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/compatibility/>

如果你在 Claude Code 或 Cursor 中使用过其中任何一个 Skill，欢迎回复客户端版本、原始任务和脱敏结果。失败结果同样有价值。
```

## 发布与判断规则

1. 一次只发一个社区，至少间隔一天观察真实评论，避免同时铺量后无法判断来源。
2. 优先回复方法、失败原因和复现问题，不主动索要 Star。
3. 有人指出错误时，先核对并更新案例，再回复链接。
4. 记录发布地址、日期、三天后的仓库独立访客和 Star；相关变化不能直接归因于帖子。
5. 不复制到与 Agent Skills 无关的群组，不私信陌生人群发。
