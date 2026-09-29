# Codex 自动触发实测：中文网页排版审查

> 实测日期：**2026-08-12** · Skill：[`chinese-typography`](../skills/chinese-typography/) · 客户端：Codex CLI `0.147.0-alpha.6.5`

## 要验证什么

用户只描述中文排版任务，**不在提示中点名 Skill**，观察 Codex 是否会自行选择并读取 `chinese-typography`，以及输出是否覆盖输入中的主要问题。

## 原始任务

```text
请检查下面这段网页 CSS 的中文排版问题，只做审查，不修改文件。明确列出问题、理由和建议值：
body { font-family: Arial, sans-serif; font-size: 14px; line-height: 1.35; text-align: justify; word-break: break-all; }
article { max-width: 80em; }
em { font-style: italic; }
```

运行方式：

```bash
codex exec --ephemeral --sandbox read-only -C . '<上面的任务>'
```

## 观察结果

### 1. 自动触发：通过

Codex 在执行前明确说明：

> 我会用「chinese-typography」规范做纯审查。

随后读取了已安装的：

```text
~/.agents/skills/chinese-typography/SKILL.md
```

提示词没有出现 `chinese-typography`，因此这次记录可以证明：**在这个任务、客户端版本和已安装 Skill 集合下发生了自动触发。** 它不能证明所有版本或所有相似措辞都会触发。

### 2. 主要问题识别：9 项

输出识别了以下问题，并给出理由和建议值：

| 输入中的问题 | 输出建议 |
|---|---|
| Arial 缺少中文字形 | 补充系统中文字体栈 |
| `14px` 正文偏小 | 最低 `16px`，推荐 `17px` |
| `line-height: 1.35` 拥挤 | 推荐 `1.75` |
| 全局 `text-align: justify` | 默认改为 `start`；确需两端对齐时缩小作用域 |
| `word-break: break-all` | 改为 `normal`，补 `overflow-wrap` 与 `line-break` |
| `max-width: 80em` 过宽 | 推荐 `38em` |
| 中文使用伪斜体 | 改用着重号或加粗 |
| 版心没有居中 | 增加 `margin-inline: auto` |
| 缺少段间距 | 为段落增加下间距 |

最终还给出了可直接替换的 CSS 示例，并把字号、行高、断词和行宽列为最高优先级。

## 已知限制

- 本次是**审查任务**，没有修改真实页面，也没有做浏览器视觉验收。
- 本次没有独立评分器，表中的“识别 9 项”只是对输出内容的记录，不是准确率指标。
- Codex 同时报告：已安装 Skill 较多，部分 description 为适应上下文预算而被缩短。虽然本次仍正确触发，但这可能影响其他 Skill 的发现，后续测试需要继续记录。
- 没有测试 Claude Code 或 Cursor，不能把本结果外推到其他客户端。

## 可复现结论

在 Codex CLI `0.147.0-alpha.6.5`、当前已安装 Skill 集合和上述原始任务下，`chinese-typography` **完成自动触发并产出结构化审查结果**。结论强度限定为单任务、单客户端版本的一次通过。
