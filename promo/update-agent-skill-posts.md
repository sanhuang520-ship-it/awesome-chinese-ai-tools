# Agent Skill 项目级更新实测：分发素材

> 准备日期：2026-08-13。状态：**未发布**。页面、实验记录与命令均已上线；本文件只准备可核验文案，外部发布需要用户当时确认。

实测页：https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/update-agent-skill/

完整记录：https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/blob/main/cases/skills-cli-isolated-install-2026-08-13.md

## 推荐标题

Agent Skill 安装后不会自动同步：我用 13 个历史夹具实测了 skills update

## V2EX / 掘金 / 知乎正文

我之前把“安装成功”理解得太静态：文件当时复制对了，不代表几天后还和上游仓库一致。

在维护 13 个中文 Agent Skills 时，我重新比较了 8 月 8 日留下的全局副本，结果是 0/13 与当前仓库一致。多数差异来自后来补充的元数据，另有 3 项内容修订。这不表示旧安装失败，只说明安装不是持续同步。

为了验证项目级更新流程，我在临时 Git 项目做了一个受控实验：

1. 从公开仓库安装 13 项，保留 CLI 生成的 `skills-lock.json`
2. 用仓库历史提交中的完整 Skill 文件夹替换项目副本
3. 确认更新前 13/13 与历史夹具一致、且 13/13 与当前仓库不同
4. 运行固定版本命令：

```bash
npx --yes skills@1.5.22 update -p -y
```

5. 更新后比较完整文件夹，而不只比较 `SKILL.md`

结果：CLI 报告 13/13 更新成功；13/13 完整文件夹与当前公开仓库一致；实验前后全局 Skill 文件哈希未变。

边界也很重要：这次只验证了**有 `skills-lock.json` 的项目级复制安装**。历史内容是受控测试夹具，不是保留下来的旧版 CLI 安装现场；没有测试全局 `update -g`、无锁文件更新、自动触发或最终任务完成。

命令、前置条件和逐层验证：
https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/update-agent-skill/

如果你在其他系统或 CLI 版本复现，成功和失败都欢迎，但请保留版本、原始命令和脱敏结果。

## 短帖

Agent Skill 安装后不会自动跟随 GitHub 仓库同步。

我用 13 个受控历史夹具实测 `skills@1.5.22 update -p -y`：更新前 13/13 与当前不同，更新后 13/13 完整文件夹一致；全局 Skill 哈希未变。

只证明有锁文件的项目级更新，不外推到全局或无锁场景：
https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/update-agent-skill/

## 发布与判断规则

1. 首次只选一个与开发者工具相关的平台，发布操作需用户当时确认；不群发、不互 Star、不私信陌生人。
2. 发布前重新打开公开实测页和案例，确认命令仍是 `skills@1.5.22 update -p -y`，页面返回 200。
3. 不把受控历史夹具写成“真实旧版 CLI 安装”，不声称全局更新已通过。
4. 记录发布 URL、时间和标题版本；24 小时、72 小时后采集聚合 Traffic 与 GitHub 搜索快照。
5. 只写“发布后观察到”，不声称因果；Clone 不能称为用户，也不能计算 Star 转化率。
