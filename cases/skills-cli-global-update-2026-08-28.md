# `skills update -g` 会静默跳过没有锁条目的 Skill

> 实测日期：**2026-08-28** · CLI：`skills@1.5.23` · 平台：macOS（darwin 25.5.0）
> 作用域：用户级全局安装 `~/.agents/skills/`

## 起因

[Claude Code 实测](claude-code-13-skills-2026-08-26.md)发现本机 13 个全局副本里有 7 个已经漂移，
其中 `guofeng-threejs` 停留在 130 行的旧版，仍在推荐一条本仓库已经推翻的技法。
本轮的目的是更新副本，顺带补上 `COMPATIBILITY.md` 中标注为未验证的场景：
**全局 `update -g`**。

## 观察到的行为

```bash
npx --yes skills@1.5.23 update -g -y
```

```
✓ Updated 22 skill(s)
```

退出码 **0**。输出逐个列出了被更新的 22 个 Skill，**其中没有本仓库的任何一个**，
也没有任何"跳过""未找到来源""无法更新"之类的提示。

更新前后对 13 个目录取哈希（全文件排序后再整体哈希），**13 / 13 完全未变**：

| Skill | 更新前 | 更新后 |
|---|---|---|
| 全部 13 个 | 见下方基线 | 逐一相同 |

也就是说：命令报告成功，实际上一个都没更新，且没有任何迹象表明它们被略过。

## 原因

`~/.agents/.skill-lock.json` 记录每个 Skill 的来源（`source` / `sourceUrl` /
`skillPath` / `skillFolderHash` / `installedAt`）。`update` 只处理锁文件里有条目的 Skill。

实测时锁文件共 40 条，本仓库的 13 个中只有 6 个在内：

| 分组 | 锁条目 | 安装日期 | 与仓库内容 |
|---|:-:|---|---|
| `ai-learning-coach` `book-digest-cn` `chinese-lesson-plan` `chinese-typography` `chinese-work-report` `ecommerce-copywriting` | ✅ 有 | 2026-08-19 | **一致** |
| `bookkeeping-cn` `chinese-design-md` `chinese-web-themes` `github-readme-cn` `guochao-visual-cn` `guofeng-threejs` `homework-tutor-cn` | ❌ 无 | 2026-08-08 | **漂移** |

两组完全对应：**有锁条目的都是最新的，没有锁条目的都是旧的。**
没有锁条目的 Skill 对 `update` 不可见——不报错、不警告、不计入统计。

这 7 个自 2026-08-08 起持续过期 **20 天**，期间每次 `update -g` 都返回成功。

本轮那 6 个有锁条目的也未被改动（`updatedAt` 仍是 08-19）。这部分是正常行为：
它们本来就是最新的，CLI 只列出实际更新过的项。

## 实际后果

不是版本号不齐这种记账问题。`guofeng-threejs` 的旧副本在「其他中式风格」表里
把工笔的关键技法写作 **细线描边（Sobel 后处理）**；本仓库当前版本已改为反向外壳，
原因是实测发现 `fwidth(N)` 法线突变检测在光滑有机形体上基本无效
（没有硬转折，`length(fwidth(N))` 全场趋近 0）。

**使用者运行 update、看到绿勾、继续拿到已被推翻的建议。**

## 修复与验证

`update` 帮不上忙，改用重新安装以补上锁条目。逐个执行——
本仓库此前已实测逗号分隔的 `--skill a,b,c` 不生效：

```bash
for s in bookkeeping-cn chinese-design-md chinese-web-themes \
         github-readme-cn guochao-visual-cn guofeng-threejs homework-tutor-cn; do
  npx --yes skills@1.5.23 add \
    https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools \
    --skill "$s" -g -y
done
```

结果：

- 7 / 7 补上锁条目（锁文件 40 → 47 条，`installedAt` 均为 2026-08-28）
- **13 / 13 与本仓库当前内容逐字节一致**
- `guofeng-threejs` 由 130 行更新为 394 行；`Sobel` 一词仍出现，但性质已变——
  不再是推荐做法，而是权衡表中的对照项（全屏 pass 成本与场景复杂度无关、
  只有它能画内部结构线），并明确写明本实现没有采用它及原因

## 同日补测：有锁条目的路径能正确更新

上面那轮只证明了「没有锁条目会被静默跳过」，没有证明「有锁条目就更新得上」——
6 个有条目的恰好都已是最新，该路径未被触发。同日制造条件补测。

**判定标准在运行前定死**，避免事后找理由：文件行数、是否含新增段落、
文件 sha、锁条目 hash，四项都要变才算通过。

先改动上游的 `github-readme-cn`（新增一段中文搜索实测，176 → 181 行）并推送，
再运行同一条 `npx --yes skills@1.5.23 update -g -y`：

| 判定项 | 更新前 | 更新后 |
|---|---|---|
| 行数 | 176 | **181** |
| 含新增段落 | 否 | **是** |
| 文件 sha | `96812b5f…` | **`5ace90a5…`** |
| 锁条目 hash | `032b0563…` | **`9a9aa9bd…`** |

输出中明确出现 `✓ Updated github-readme-cn`，事后与仓库**逐字节一致**。

**四项全变，通过。**

### 所以这个失败是有条件的

`update -g` 本身没坏：**有锁条目就能正确拉取上游新版，没有锁条目才会被静默跳过。**
这个对比也让「补锁条目」成为一个有依据的修复手段，而不只是碰巧管用。

### ⚠️ 一个未能解释的观察

同一次运行还报告更新了 `guofeng-threejs` 与 `homework-tutor-cn`，
但这两个自 2026-08-28 重装以来**上游并无改动**。而处境完全相同的
`bookkeeping-cn`、`chinese-design-md`（上游同样停在 08-21、同样 08-28 重装）
却未被触及。

内容上无影响：事后 13/13 仍与仓库逐字节一致。

**原因未查明。这里只记录现象，不给解释。** 可能与锁条目里
`skillFolderHash` 的计算方式有关，但没有验证过的推测不写进结论。

## 结论与边界

**已验证（否定结论）**：`skills@1.5.23` 的 `update -g` 不会更新锁文件中没有条目的
Skill，且不提示这些 Skill 的存在。重新安装可以补上锁条目并使内容追平。

**已验证（肯定结论）**：同一命令对**有**锁条目的 Skill 能正确拉取上游新版
（四项预设判定全部通过，内容与仓库逐字节一致）。因此这是个有条件的缺陷，
不是 `update` 整体失效。

**不能外推**：

1. 只测了 `1.5.23` 单个版本、macOS 单个平台、全局单个作用域
2. 未测项目级 `update -p` 在缺锁条目时的行为
3. 未测锁条目存在但来源仓库已改名或删除的情形
4. 有锁条目的路径只在**单个 Skill、单次改动**上验证过，不证明多个同时更新、
   或上游发生删除/改名时的行为
5. 「无上游改动却被报告更新」的原因未查明
