# 第三方 Skill 实测（首例）：`chinese-git-workflow`

> 实测日期：**2026-09-03** · 目标：[`jnMetaCode/superpowers-zh`](https://github.com/jnMetaCode/superpowers-zh) 的 `skills/chinese-git-workflow`
> CLI：`skills@1.5.23` · 平台：macOS · 目标仓库当时 ★7960、MIT、2026-09-02 仍在提交

这是本仓库第一次**测别人的 Skill**。先写规则，再写结果。

## 为什么做这件事

生态里已经有数千个 Skill，但**没有地方能查到哪个真的会被触发、能不能完成任务**。
2026-09-03 检索：`agent skills compatibility test evidence` 仅 1 个不相关结果；
`claude skills benchmark trigger test` **0 个结果**；`skill activation testing agent`
排前的是给作者测自己 Skill 的框架（`UiPath/coder_eval` ★120、`tripwire` ★2 等），
**没有独立测第三方 Skill 并公布结果的**。

## 测别人之前，先定死自己的规矩

1. **只用它自己声明的契约当标准**，不用本仓库的偏好当标准。
   本仓库的 Skill 设计为自动触发；`superpowers-zh` 的中文 Skill 明确要求
   **不要自动触发**。两种都不是错，拿我们的标准去判它就是错的。
2. **方法与任务原文全部公开**，作者可以复现、可以反驳。
3. **自测偏差同样存在**：执行任务、判定结果的是同一个模型。
   这条在测自己时写过，测别人时一个字不能少。
4. **不打分、不排名、不写"好/坏"**，只记录可观察事实。
5. **先登记后执行**：任务与判定门槛在运行前公开，事后不改题。

## 观察到的设计差异（不是评价）

`superpowers-zh` 的四个中文 Skill 的 `description` 结尾都有同一句：

```
仅在用户显式 /<skill-name> 时调用，不要根据上下文自动触发。
```

覆盖 `chinese-code-review`、`chinese-commit-conventions`、`chinese-documentation`、
`chinese-git-workflow`。这是**成体系的设计选择**，与本仓库把 Skill 设计成
自动触发、并逐个实测触发率的做法相反。

据检索，这个差异此前没有任何地方记录过，更没有人测过
**「不要自动触发」这条指令是否真的会被遵守**。

## 安装层：已完成（2026-09-03）

安装前按本仓库自己的要求做只读审查：目标目录**只有 `SKILL.md` 一个文件，
无任何脚本或可执行内容**，仓库 MIT 协议。

```bash
npx --yes skills@1.5.23 add https://github.com/jnMetaCode/superpowers-zh \
  --skill chinese-git-workflow -g -y
```

| 检查项 | 结果 |
|---|---|
| 落盘 | ✅ `~/.agents/skills/chinese-git-workflow/SKILL.md`，552 行 |
| 符号链接 | ✅ `~/.claude/skills/chinese-git-workflow` → `../../.agents/skills/…` |
| 与上游一致 | ✅ 与 `raw.githubusercontent.com` 的当前版本**逐字节相同** |
| 锁条目 | ✅ 已写入 `.skill-lock.json`，`source: jnMetaCode/superpowers-zh` |

### ⚠️ 但 CLI 报告的是失败

同一条命令的输出是：

```
■  Failed to install 1
     ✗ chinese-git-workflow → PromptScript: PromptScript does not support global skill installation
```

**报失败，实际全部装好了。** 该 Skill 目录下只有 `SKILL.md`，没有任何 PromptScript
文件；目标仓库根目录存在 `.claude-plugin`、`.codex-plugin`、`.cursor-plugin`、
`.kimi-plugin` 等多客户端打包，错误**可能**来自仓库级打包探测——
**这一点没有进一步确认，因此不写成结论。**

与[前一轮实测](skills-cli-global-update-2026-08-28.md)合起来看，
同一个 CLI 的成败报告**两个方向都不可信**：

| 场景 | 报告 | 实际 |
|---|---|---|
| `update -g`，无锁条目 | ✓ Updated 22 skill(s)，退出码 0 | **一个都没更新** |
| `add --skill … -g`，本例 | ✗ Failed to install 1 | **完整装好且与上游一致** |

**结论：判断 skills CLI 是否生效，必须核对落盘文件，不能采信它的输出。**

## 前瞻登记：触发测试（尚未执行）

以下任务与门槛**在执行前公开**，事后不修改。

### 为什么必须换一个新会话

本轮另有一个发现：这个新安装的 Skill **在同一会话内就进入了可用列表**
（见[首轮记录的 2026-09-03 更正](claude-code-13-skills-2026-08-26.md)）。
因此本会话的执行者已经知道它存在，**无法再做盲测**。触发测试必须在
一个未接触过本记录的新会话中进行。

### 任务 A：它是否遵守自己的「不要自动触发」

自然措辞，不出现 Skill 名称，也不使用斜杠命令：

```text
我们团队准备把仓库从 GitHub 迁到 Gitee，commit message 想统一成中文规范，
你建议怎么定？
```

- **通过** = **没有**调用 `chinese-git-workflow`（遵守了自己的声明）
- **失败** = 自动调用了（违背了自己 `description` 里的明确指令）

> 注意这里的方向：**不触发才算通过。** 用它自己的契约判它。

### 任务 B：显式调用时的任务覆盖

```text
/chinese-git-workflow 我们团队 5 个人，仓库在 Gitee，想定一套分支命名和
中文 commit message 规范，再给一个 PR 描述模板。
```

- **通过** = 输出同时覆盖：Gitee 相关配置、分支命名、中文 commit 规范、PR 模板
- **部分通过** = 覆盖其中 2–3 项
- **失败** = 覆盖 ≤1 项，或答非所问

### 不会记录的

- 内容质量高低、写得好不好 —— 不打分
- 与本仓库同类 Skill 的比较 —— 不做排名

## 结果

**触发测试尚未执行。** 本页只记录到安装层为止。
执行后结果会追加在此处，不覆盖本前瞻登记。
