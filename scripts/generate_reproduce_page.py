#!/usr/bin/env python3
"""Generate a replay page only from verbatim task evidence preserved in cases."""

import argparse
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reproduce" / "index.html"
BASE = "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/"
TITLES = {
    "ai-learning-coach": "两周 SQL 学习前校准",
    "bookkeeping-cn": "家庭流水与越界请求",
    "chinese-typography": "中文网页 CSS 审查",
    "chinese-work-report": "不编数据的中文周报",
    "ecommerce-copywriting": "面霜功效宣称校样",
    "github-readme-cn": "GitHub 仓库首屏审查",
    "homework-tutor-cn": "家长辅导作业边界",
}


def load_records():
    evidence = json.loads((ROOT / "data" / "task-evidence.json").read_text(encoding="utf-8"))
    compatibility = json.loads((ROOT / "data" / "compatibility.json").read_text(encoding="utf-8"))
    return evidence["records"], compatibility["results"]["codexActivation"]["skillResults"]


def original_task(case_path: Path):
    body = case_path.read_text(encoding="utf-8")
    section = re.search(r"^## 原始任务\s*$([\s\S]*?)(?=^## |\Z)", body, re.M)
    if not section:
        return None
    match = re.search(r"```text\n(.*?)\n```", section.group(1), re.S)
    return match.group(1).strip() if match else None


def validate_records(records):
    verbatim = []
    summary = []
    for name, record in records.items():
        path = ROOT / record["case"]
        task = original_task(path)
        if record["level"] == "verbatim":
            if not task:
                raise ValueError(f"verbatim record lacks original task block: {name}")
            verbatim.append((name, record, task))
        elif record["level"] == "summary-only":
            if task:
                raise ValueError(f"summary-only record contains an original task block: {name}")
            summary.append((name, record))
        else:
            raise ValueError(f"unknown evidence level: {name}")
    if len(verbatim) != 7 or len(summary) != 6:
        raise ValueError(f"expected 7 verbatim and 6 summary-only records, got {len(verbatim)} and {len(summary)}")
    return verbatim, summary


def render():
    records, results = load_records()
    verbatim, summaries = validate_records(records)
    cards = []
    for name, record, task in verbatim:
        install = f"npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill {name} -g"
        result = results[name]
        cards.append(f'''<article class="task-card">
  <div class="card-head"><span>{html.escape(name)}</span><b>{html.escape(result["labelZh"])}</b></div>
  <h2>{html.escape(TITLES[name])}</h2>
  <div class="step"><i>01</i><div><strong>安装</strong><code>{html.escape(install)}</code><button type="button" data-copy="{html.escape(install, quote=True)}">复制安装命令</button></div></div>
  <div class="step"><i>02</i><div><strong>逐字任务原文</strong><pre>{html.escape(task)}</pre><button type="button" data-copy="{html.escape(task, quote=True)}">复制任务</button></div></div>
  <div class="step result"><i>03</i><div><strong>仓库记录</strong><p>{html.escape(result["summaryZh"])}</p><a href="https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/blob/main/{html.escape(record["case"])}">查看完整案例与限制 →</a></div></div>
</article>''')
    summary_items = "".join(
        f'<li><code>{html.escape(name)}</code><a href="https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/blob/main/{html.escape(record["case"])}">查看任务摘要</a></li>'
        for name, record in summaries
    )
    return f'''<!doctype html><html lang="zh-CN"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow">
<title>7 个可逐字复现的中文 Agent Skill 测试任务</title>
<meta name="description" content="复制安装命令和逐字任务原文，复现 7 个中文 Agent Skills 的 Codex 自动触发与边界测试；另外 6 项仅保留摘要，不反向编造提示词。">
<link rel="canonical" href="{BASE}reproduce/"><meta property="og:type" content="article"><meta property="og:locale" content="zh_CN"><meta property="og:title" content="7 个可逐字复现的中文 Agent Skill 测试任务"><meta property="og:description" content="安装、复制任务、对照原始案例；逐字原文与任务摘要严格分开。"><meta property="og:url" content="{BASE}reproduce/"><meta property="og:image" content="{BASE}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="7 个可逐字复现的中文 Agent Skill 测试任务"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="7 个可逐字复现的中文 Agent Skill 测试任务"><meta name="twitter:description" content="安装、复制任务、对照原始案例；逐字原文与任务摘要严格分开。"><meta name="twitter:image" content="{BASE}og.png"><meta name="twitter:image:alt" content="7 个可逐字复现的中文 Agent Skill 测试任务">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"TechArticle","headline":"7 个可逐字复现的中文 Agent Skill 测试任务","description":"从仓库案例中提取的逐字任务原文与复现入口。","inLanguage":"zh-CN","dateModified":"2026-08-12","mainEntityOfPage":"{BASE}reproduce/","image":"{BASE}og.png","author":{{"@type":"Organization","name":"中文 AI Skills 库"}}}}</script>
<style>:root{{--paper:#eee9de;--sheet:#fffaf0;--ink:#1b221e;--muted:#606963;--line:#c5baa6;--red:#a44336;--jade:#28614e;--gold:#b77e29;--serif:"Songti SC","Noto Serif CJK SC",STSong,serif;--sans:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,monospace}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.72 var(--sans)}}a{{color:var(--jade)}}.wrap{{width:min(1120px,calc(100% - 38px));margin:auto}}.top{{padding:22px 0;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:20px;font-size:13px}}.top a{{font-weight:800;text-decoration:none}}.top span{{font:11px var(--mono);color:var(--muted);letter-spacing:.12em}}.hero{{padding:70px 0 58px;display:grid;grid-template-columns:1.2fr .8fr;gap:50px;align-items:end}}.eyebrow{{font:800 12px var(--mono);color:var(--red);letter-spacing:.14em}}h1,h2{{font-family:var(--serif)}}h1{{font-size:clamp(44px,7vw,78px);line-height:1.06;margin:18px 0 22px;max-width:10em}}.lead{{font-size:20px;color:#465149;max-width:36em}}.stamp{{border:1px solid var(--ink);background:var(--sheet);padding:28px;box-shadow:10px 10px 0 rgba(164,67,54,.16)}}.stamp b{{display:block;font:700 52px var(--serif);color:var(--jade)}}.stamp p{{margin:8px 0 0;color:var(--muted)}}.notice{{border-block:1px solid var(--line);background:rgba(255,250,240,.5);padding:22px 0}}.notice p{{margin:0}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:17px;padding:64px 0}}.task-card{{background:var(--sheet);border:1px solid var(--line);padding:25px;min-width:0}}.card-head{{display:flex;justify-content:space-between;gap:15px;font:11px var(--mono);color:var(--muted)}}.card-head b{{color:var(--jade)}}.task-card h2{{font-size:28px;margin:16px 0 20px}}.step{{display:grid;grid-template-columns:32px 1fr;gap:11px;padding:17px 0;border-top:1px solid var(--line);min-width:0}}.step i{{font:800 11px var(--mono);font-style:normal;color:var(--red)}}.step strong{{display:block;margin-bottom:8px}}code,pre{{font:12px/1.6 var(--mono)}}code{{display:block;background:#202722;color:#f6f0e4;padding:11px;overflow-wrap:anywhere}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#eee5d5;padding:14px;margin:0}}button{{margin-top:8px;border:1px solid var(--jade);background:transparent;color:var(--jade);padding:8px 11px;font-weight:800;cursor:pointer}}.result p{{color:var(--muted);font-size:13px}}.result a{{font-size:12px;font-weight:800}}.missing{{padding:54px 0;border-top:1px solid var(--line);display:grid;grid-template-columns:.85fr 1.15fr;gap:48px}}.missing h2{{font-size:38px;margin:0}}.missing p{{color:var(--muted)}}.missing ul{{list-style:none;margin:18px 0 0;padding:0;border:1px solid var(--line)}}.missing li{{padding:12px 15px;background:var(--sheet);display:flex;justify-content:space-between;gap:12px}}.missing li+li{{border-top:1px solid var(--line)}}.missing li code{{display:inline;background:none;color:var(--ink);padding:0}}.missing li a{{font-size:12px}}.cta{{margin:60px auto;background:var(--red);color:#fff8ed;padding:45px;display:grid;grid-template-columns:1fr auto;gap:25px;align-items:end}}.cta h2{{font-size:34px;margin:0 0 8px}}.cta p{{margin:0;opacity:.86}}.cta a{{color:#fff8ed;border:1px solid;padding:10px 14px;text-decoration:none;font-weight:800}}footer{{padding:0 0 45px;display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;color:var(--muted);font-size:13px}}@media(max-width:760px){{.hero,.grid,.missing,.cta{{grid-template-columns:1fr}}}}@media(max-width:460px){{.wrap{{width:calc(100% - 26px)}}.top span{{display:none}}.task-card{{padding:19px}}.missing li{{flex-direction:column}}}}</style></head>
<body><header class="wrap top"><a href="../">← 中文 AI Skills 库</a><span>VERBATIM TASK LAB · 7 / 13</span></header><main><section class="wrap hero"><div><div class="eyebrow">安装 · 复制 · 对照证据</div><h1>7 个任务，<br>可以逐字重放。</h1><p class="lead">这些任务直接取自案例中保存的原始代码块。你可以在自己的客户端重放，并把结果与仓库记录对照。</p></div><aside class="stamp"><b>7 / 13</b><p>7 条逐字任务原文；6 条只有任务摘要。没有保存下来的措辞，不根据结果倒推补写。</p></aside></section><section class="notice"><div class="wrap"><p><strong>怎样使用：</strong>先安装单个 Skill，重启客户端，再复制任务。任务里没有写 Skill 名称，目的是观察客户端是否自动选择它。请勿在含私人数据的真实环境中直接复用合成测试内容。</p></div></section><section class="wrap grid">{''.join(cards)}</section><section class="wrap missing"><div><h2>另外 6 项，为什么不能放复制按钮？</h2><p>它们保留了任务主题与观察结果，但没有保存逐字提示。根据摘要重新写一条“看起来一样”的任务，会把重构内容误装成原始证据。</p></div><div><strong>仅有任务摘要</strong><ul>{summary_items}</ul></div></section><section class="wrap cta"><div><h2>重放后，提交成功或反例。</h2><p>请记录客户端版本、是否自动触发、是否完成和脱敏输出；不要只写“好用”。</p></div><a href="https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml">提交兼容性实测 →</a></section></main><footer class="wrap"><span><a href="../guides/">13 个原创 Skill 总览</a> · <a href="../compatibility/">兼容性证据</a> · <a href="../data/task-evidence.json">任务证据数据</a></span><span><a href="https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools">查看 GitHub 仓库 · 觉得有用再 Star</a></span></footer><script>document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{{try{{await navigator.clipboard.writeText(button.dataset.copy);const old=button.textContent;button.textContent='已复制 ✓';setTimeout(()=>button.textContent=old,1600)}}catch{{button.textContent='复制失败，请手动选择'}}}}));</script></body></html>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    expected = render()
    current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
    if args.write:
        OUTPUT.parent.mkdir(exist_ok=True)
        OUTPUT.write_text(expected, encoding="utf-8")
    elif current != expected:
        raise SystemExit("reproduce/index.html is stale; run scripts/generate_reproduce_page.py --write")


if __name__ == "__main__":
    main()
