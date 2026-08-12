# Agent Skill 安装前只读审计器：分发素材

> 准备日期：2026-08-13。状态：**未发布**。工具、源码、测试与说明页均已上线；本文件只准备可核验文案，不代表已发布到任何外部平台。Linux.do 不使用本稿。

工具页：https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/audit-skill/

源码：https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/blob/main/scripts/audit_skill.py

## 推荐标题

安装 Agent Skill 前，我写了一个不会执行目标的只读检查器

## V2EX / 掘金 / 知乎正文

Agent Skill 不一定只有一份 `SKILL.md`，还可能带 Python、Shell、JavaScript、浏览器 Demo 和外部依赖。安装前靠肉眼检查整个目录很容易漏项，但“自动扫描通过”也不能等同于安全。

我给自己的中文 Agent Skills 仓库加了一个只依赖 Python 标准库的只读检查器：

```bash
python3 scripts/audit_skill.py /path/to/skill
python3 scripts/audit_skill.py /path/to/skill --json
```

它会列出需要人工复核的线索：

- 可执行脚本和符号链接
- 外部运行时资源与主动网络访问
- 凭据相关字段
- 文件写入、追加或删除调用
- `sudo`、下载后管道执行、递归强制删除等高关注命令

扫描器不会导入、安装或运行目标 Skill，不跟随符号链接，也不会上传文件内容。高关注项返回退出码 1，JSON 输出可接入自己的检查流程。

我用仓库里已有的 `guofeng-threejs` 做了实际核对：它准确报告两个 HTML Demo 中的 `unpkg` importmap 外部资源，与此前人工质量标签一致。

边界也写在输出里：这是规则驱动的静态线索，不是病毒查杀、沙箱、提示注入检测或安全认证。动态拼接、混淆代码和外部依赖行为可能漏掉；0 项命中绝不等于安全。

工具、规则和限制：
https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/audit-skill/

如果你有能最小复现的误报或漏报，欢迎提交规则和脱敏样例；不要上传真实 Token、私人路径或未公开业务代码。

## 短帖

安装 Agent Skill 前，至少该知道目录里有没有脚本、符号链接、联网、凭据访问、写删文件和高风险命令。

我开源了一个只依赖 Python 标准库的只读检查器：不执行目标、不跟随符号链接，支持 JSON 和 CI 退出码。

它只报告人工复核线索，不做“安全认证”；0 项命中不等于安全：
https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/audit-skill/

## 发布与判断规则

1. 一次只选一个平台，发布操作需用户当时确认；不群发、不互 Star、不私信陌生人。
2. Linux.do 不使用 AI 生成或润色正文，由用户本人按社区规则撰写。
3. 发布前重新运行 `python3 scripts/audit_skill.py skills/guofeng-threejs --json`，确认仍报告两个外部资源；若结果变化先更新文案。
4. 记录发布 URL、时间和标题版本；24 小时、72 小时后采集聚合 Traffic 快照。
5. 只描述发布后的变化，不声称因果；Clone 不能称为用户，也不能计算 Star 转化率。
