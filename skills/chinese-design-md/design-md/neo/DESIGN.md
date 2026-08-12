---
version: 1.0
name: Neo-Chinese-chinese-design
description: "木色与暖灰，低饱和，线条简洁。最百搭的一套，适合家居、生活方式、品牌官网。 Wood tones and warm greys, low saturation, clean lines. The most versatile set."

colors:
  primary: "#8C6E4A"
  primary-weak: "#C9B79E"
  canvas: "#FAF8F5"
  surface: "#F0EBE3"
  hairline: "#DFD6C9"
  ink: "#413B33"
  ink-strong: "#221E19"
  ink-soft: "#756C60"

typography:
  font-sans: "PingFang SC / Microsoft YaHei / Noto Sans CJK SC"
  font-serif: "Songti SC / SimSun / Noto Serif SC"
  body-size: 17px
  line-height: 1.75
  measure: 38em
---

# 新中式 · Neo-Chinese

## Overview

木色与暖灰，低饱和，线条简洁。最百搭的一套，适合家居、生活方式、品牌官网。

**出处**：新中式：传统比例 + 现代材质，克制的东方感。

这是一套**为中文内容设计**的系统。它和多数设计系统最大的不同不在配色，
而在排版——中文的行高、断行、标点、强调方式都和西文不一样，
这些规则写在下面的 Typography 一节里。

## Colors

### Brand & Accent

| Token | 值 | 用途 |
|---|---|---|
| `primary` | `#8C6E4A` | 主行动点、链接、关键强调。**一屏不超过 2–3 处** |
| `primary-weak` | `#C9B79E` | 强调色的浅版，用于背景高亮、选中态、边框 |

### Surface

| Token | 值 | 用途 |
|---|---|---|
| `canvas` | `#FAF8F5` | 页面底色 |
| `surface` | `#F0EBE3` | 卡片、引用块、代码块底 |
| `hairline` | `#DFD6C9` | 分割线、边框。**只用 1px** |

### Text

| Token | 值 | 用途 |
|---|---|---|
| `ink-strong` | `#221E19` | 标题 |
| `ink` | `#413B33` | 正文 |
| `ink-soft` | `#756C60` | 辅助文字、说明、时间戳 |

### 对比度实测

用 WCAG 相对亮度公式实算的，不是估计：

| 组合 | 对比度 | AA (4.5:1) |
|---|---|---|
| 正文 / 底色 | **10.44:1** | ✅ |
| 标题 / 底色 | **15.63:1** | ✅ |
| 辅助文字 / 底色 | 4.87:1 | ✅ |
| 主色 / 底色 | 4.46:1 | ⚠️ 未达标 |

> ⚠️ **主色作为文字色未达 AA（4.46:1）**。这套的主色适合做
> 色块底、边框、图标和 24px 以上大字，**不要拿它写正文或小字**。


[8 套主题的真实渲染截图在这里](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/shots/)。

## Typography

### Font Family

```css
--font-sans:  -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
              "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
              "Source Han Sans SC", "Noto Sans CJK SC", sans-serif;
--font-serif: "Songti SC", "SimSun", "Source Han Serif SC",
              "Noto Serif SC", Georgia, "Times New Roman", serif;
```

**为什么这样排**：`PingFang SC` 覆盖 macOS/iOS，`Microsoft YaHei` 覆盖 Windows，
`Noto Sans CJK SC` 覆盖 Linux 与 Android。缺了任何一个，都会有一大批用户看到系统默认字体。

### Chinese Typography Rules（这一节是西文设计系统没有的）

| 项 | 值 | 为什么 |
|---|---|---|
| `line-height` | **1.75** | 中文字面率高、没有 x-height 起伏，行高比西文需要更大。1.5 会挤 |
| `max-width` | **38em** | 中文每行 30–40 字最舒服。西文常用的 65ch 换算成中文太长 |
| `letter-spacing` | **0.01em** | 极小的字距能让中文更透气，但超过 0.05em 就散了 |
| `text-align` | **left** | ⚠️ 不要用 `justify`。中文没有词间空格，两端对齐会拉出难看的字距 |
| `line-break` | **strict** | 让浏览器执行 CJK 避头尾：`。，、）」` 不出现在行首，`（「` 不出现在行尾 |
| 强调 | `text-emphasis: dot` | ⚠️ **中文不用斜体**。宋体、黑体没有真正的意大利体，浏览器会做机械倾斜，很丑。用着重号 |
| 中英间距 | 手动或用工具加 | 「使用 AI 工具」比「使用AI工具」易读——这叫**盘古之白** |

```css
body {
  font-family: var(--font-sans);
  font-size: 17px;
  line-height: 1.75;
  letter-spacing: 0.01em;
  max-width: 38em;
  line-break: strict;
  text-align: left;          /* 不要 justify */
}
em {
  font-style: normal;                    /* 关掉斜体 */
  text-emphasis: dot;                    /* 换成着重号 */
  -webkit-text-emphasis: dot;
}
```

### Hierarchy

| 层级 | 字号 | 字重 | 字体 | 行高 |
|---|---|---|---|---|
| Display | 40–56px | 700 | serif | 1.25 |
| H1 | 32px | 700 | serif | 1.3 |
| H2 | 24px | 700 | serif | 1.4 |
| H3 | 19px | 600 | sans | 1.5 |
| Body | 17px | 400 | sans | **1.75** |
| Caption | 13px | 400 | sans | 1.6 |

**衬线用在标题、无衬线用在正文** —— 这是中文网页最稳的组合。
反过来（黑体标题 + 宋体正文）在屏幕上正文会发虚。

### Note on Font Substitutes

本设计系统**不依赖任何商业字体**。全部使用系统自带中文字体，
所以不存在「设计稿好看、上线糊掉」的问题——这是与多数西文设计系统的一个关键差异。


## Layout

### Spacing System

以 4px 为基数：`4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96`

### Grid & Container

- 正文容器 **38em**（约 30–40 个中文字/行）
- 宽内容（表格、代码、图）可突破到 **56em**
- 页面左右留白至少 20px（移动端）/ 48px（桌面）

### Whitespace Philosophy

**留白是内容的一部分，不是没画完。**

这套系统里，层次优先靠**间距**表达，其次才是分割线，最后才是颜色。
如果你发现自己在加第三条分割线，通常说明间距没拉开。

## Elevation & Depth

这套系统**几乎不用阴影**。层级靠底色差（canvas → surface）和 1px 分隔线表达。

需要浮层时（弹窗、下拉），用：

```css
box-shadow: 0 8px 32px rgba(0, 0, 0, .08);
```

## Shapes

### Border Radius Scale

| 用途 | 值 |
|---|---|
| 小元素（标签、徽章） | 6px |
| 按钮、输入框 | 8px |
| 卡片、面板 | 12px |
| 圆形（头像） | 50% |



## Components

### Buttons

```css
.btn-primary {
  background: #8C6E4A;
  color: #FAF8F5;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  letter-spacing: 0.02em;   /* 按钮里的中文加一点字距更清晰 */
}
.btn-ghost {
  background: transparent;
  color: #413B33;
  border: 1px solid #DFD6C9;
}
```

⚠️ **中文按钮文案控制在 2–6 个字**。「立即开始使用我们的服务」这种会撑破布局。

### Cards

```css
.card {
  background: #F0EBE3;
  border: 1px solid #DFD6C9;
  border-radius: 12px;
  padding: 20px 24px;
}
```

### Inputs

```css
input {
  background: #FAF8F5;
  border: 1px solid #DFD6C9;
  border-radius: 8px;
  padding: 10px 14px;
  color: #413B33;
}
input:focus {
  border-color: #8C6E4A;
  outline: 2px solid #C9B79E;
}
```

⚠️ **placeholder 用 `ink-soft`（#756C60）**，不要更浅——中文笔画密，太浅会糊。

## Do's and Don'ts

### Do

- 用木色（#8C6E4A）做主强调，温润不刺眼
- 圆角适中（8–12px），介于传统方正与现代圆润之间
- 留白比例大一些，现代感来自空间不是装饰
- 行高保持 1.75，这是中文可读性的底线
- 强调用着重号，不用斜体

### Don't

- 别堆传统纹样，一个足够
- 别用高对比黑白，这套是中间调
- 别配冷色，整套是暖的
- **不要用 `text-align: justify`** —— 中文没有词间空格，两端对齐会拉出难看的字距
- **不要用斜体强调中文** —— 系统中文字体没有真正的意大利体，浏览器机械倾斜很丑
- 不要在中英文之间省略空格 —— 「使用 AI 工具」比「使用AI工具」易读

## Responsive Behavior

### Breakpoints

`520px`（手机）· `768px`（平板）· `1024px`（桌面）

### 中文特有的响应式注意

- **正文字号在手机上不要小于 15px** —— 中文笔画密，比西文更早糊
- 表格在手机上用 `overflow-x: auto` 横向滚动，**不要**换行——中文表头换行后极难读
- 标题在手机上降一档字号即可，行高保持不变

## Iteration Guide

想在这套基础上做自己的品牌：

1. **先只换 `primary`** —— 其余 7 个 token 是配套调过对比度的，动了要重新验证
2. 换色后跑一遍对比度：正文/底色 ≥ 4.5:1，大字 ≥ 3:1
3. **不要动 `line-height` 和 `measure`** —— 那两个是中文排版的地基，不是风格选择

## Known Gaps

- 色值提取自本设计系统自己的实现，**不代表任何传统绘画的权威标准**——
  传统色本身在不同文献里就有出入
- 没有覆盖数据可视化配色（图表用色需要另一套规则）
- 没有覆盖繁体中文场景（台标/港标字形与断行规则略有不同）
- 深色模式仅 `night` 一套；其余 7 套是浅色系统

---

*来自 [中文 AI Skills 库](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools) ·
生成于 2026-08-12 · MIT ·
[8 套主题的真实渲染截图](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/shots/)*
