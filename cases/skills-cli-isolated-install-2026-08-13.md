# skills CLI 1.5.22 隔离安装复测

> 日期：2026-08-13 · 平台：macOS · 范围：CLI 发现、项目级复制安装与文件一致性；**不测试自动触发或任务完成**。

## 为什么重测

未固定版本运行 `npx skills --version` 时，本机命中了旧缓存 `1.5.18`；npm 元数据中的 `latest` 是 `1.5.22`。同时，仓库内容在全局副本安装后发生过更新，因此不能继续用旧副本证明当前安装内容一致。

## 隔离方法

1. 创建系统临时目录并初始化空 Git 项目。
2. 对现有 `~/.agents/skills/*/SKILL.md` 计算 SHA-256 清单。
3. 在临时项目中固定 CLI 版本并使用复制模式安装：

```bash
npx --yes skills@1.5.22 add /path/to/awesome-chinese-ai-tools \
  --skill '*' --agent codex --copy -y
```

4. 将临时项目 `.agents/skills/<name>/SKILL.md` 与仓库 13 个 `skills/<name>/SKILL.md` 逐字节比较。
5. 再次计算全局 Skill 哈希清单，确认隔离测试没有修改用户现有安装。

## 观察结果

| 检查 | 结果 |
|---|---:|
| 固定版本 `--list` 发现 | 13 / 13 |
| 临时项目复制安装 | 13 / 13 |
| 与当前仓库 `SKILL.md` 逐字节一致 | 13 / 13 |
| 全局 Skill 文件前后哈希一致 | 是 |
| 既有全局副本与当前仓库一致 | 0 / 13 |

既有全局副本的修改时间早于当前仓库文件；其中多数差异是后来新增的作者、分类与标签元数据，`chinese-lesson-plan`、`ecommerce-copywriting` 和 `homework-tutor-cn` 另有内容修订。

## 证据边界

- 结果只证明 `skills@1.5.22` 在这次 macOS 临时 Git 项目中的发现、复制安装与文件一致性。
- 没有运行 Claude Code 或 Cursor；Claude 桌面应用的存在不等于 Claude Code 实测。
- 没有证明 Skill 会自动触发，也没有证明任务能够完成。
- `npx` 的缓存和未来 npm 版本可能改变结果；复现时必须记录实际版本。
- 临时目录和本机绝对路径不作为公开证据保存，避免暴露私人环境信息。
