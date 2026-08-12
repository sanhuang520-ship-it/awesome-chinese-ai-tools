#!/usr/bin/env python3
"""Generate the first-party Skill guide index from repository evidence data."""

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "guides" / "index.html"
BASE = "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/"

COPY = {
    "ai-learning-coach": ("AI 学习教练", "想系统学会一项技能，而不是只收集教程"),
    "book-digest-cn": ("中文拆书", "想把一本书变成问题、论证和自己的判断"),
    "bookkeeping-cn": ("家庭流水整理", "想分类收支、核对金额，同时守住财务边界"),
    "chinese-design-md": ("中式 DESIGN.md", "想让 AI 按统一的中式设计规范生成界面"),
    "chinese-lesson-plan": ("中文中小学教案", "想把核心素养落实到任务、证据和课时"),
    "chinese-typography": ("中文排版", "想修正字体、行高、断行和中英混排问题"),
    "chinese-web-themes": ("中式网页主题", "想直接采用可切换的中国美学 CSS 主题"),
    "chinese-work-report": ("中文职场汇报", "想把工作素材组织成不编数据的周报或述职"),
    "ecommerce-copywriting": ("电商文案校样", "想写商品文案，同时分清事实、待补项与风险宣称"),
    "github-readme-cn": ("GitHub README 审查", "想减少仓库首屏的信息流失，但不迷信涨星公式"),
    "guochao-visual-cn": ("国潮视觉方向", "想把宽泛的中国风收束成可执行的画风与配色"),
    "guofeng-threejs": ("Three.js 水墨渲染", "想实现可运行的水墨 shader，并核对性能边界"),
    "homework-tutor-cn": ("家长辅导作业", "想教家长引导孩子，而不是生成可直接抄的成品"),
}


def load_data():
    skills = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))
    compatibility = json.loads((ROOT / "data" / "compatibility.json").read_text(encoding="utf-8"))
    quality = json.loads((ROOT / "data" / "quality.json").read_text(encoding="utf-8"))
    originals = [item for item in skills["skills"] if item.get("ours")]
    results = compatibility["results"]["codexActivation"]["skillResults"]
    return originals, results, quality["skills"]


def render_card(skill, result, quality):
    name = skill["name"]
    title, scenario = COPY[name]
    outcome = result["outcome"]
    status_class = {"completed": "done", "waiting-input": "wait", "bounded-retest": "partial"}[outcome]
    boundary = quality.get("sensitiveBoundaryZh") or "未标记敏感决策边界；仍需按具体任务核对输出"
    network = quality.get("networkDetailZh") if quality.get("runtimeNetwork") else "Skill 本身不要求运行时联网"
    return f'''<article class="guide-card" data-outcome="{status_class}">
  <div class="card-top"><span class="number">{html.escape(name)}</span><span class="status {status_class}">{html.escape(result["labelZh"])}</span></div>
  <h2><a href="../{html.escape(skill["explainer"])}">{html.escape(title)}</a></h2>
  <p class="scenario">{html.escape(scenario)}</p>
  <div class="evidence"><b>本次记录</b><span>{html.escape(result["summaryZh"])}</span></div>
  <div class="boundary"><b>质量边界</b><span>{html.escape(boundary)}；{html.escape(network)}。</span></div>
  <div class="card-links"><a href="../{html.escape(skill["explainer"])}">看方法与证据</a><a href="https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/blob/main/{html.escape(result["case"])}">看原始案例</a><a href="../skills/{html.escape(name)}/SKILL.md">看 SKILL.md</a></div>
</article>'''


def render():
    originals, results, qualities = load_data()
    if set(COPY) != {item["name"] for item in originals}:
        raise ValueError("guide copy does not match original Skill catalog")
    if set(results) != set(COPY) or set(qualities) != set(COPY):
        raise ValueError("compatibility or quality data does not cover all original Skills")
    cards = "\n".join(render_card(item, results[item["name"]], qualities[item["name"]]) for item in originals)
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>13 个原创中文 Agent Skills：方法、实测与安全边界总览</title>
<meta name="description" content="按使用场景比较 13 个原创中文 Agent Skills。每项公开方法说明、Codex 自动触发结果、失败或等待状态、质量与安全边界。">
<link rel="canonical" href="{BASE}guides/">
<meta property="og:type" content="website"><meta property="og:locale" content="zh_CN">
<meta property="og:title" content="13 个原创中文 Agent Skills 方法与证据总览">
<meta property="og:description" content="不是只列名称：按场景比较方法、实测状态、原始案例和安全边界。">
<meta property="og:url" content="{BASE}guides/">
<meta property="og:image" content="{BASE}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="13 个原创中文 Agent Skills 方法与证据总览">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="13 个原创中文 Agent Skills 方法与证据总览"><meta name="twitter:description" content="按场景比较方法、实测状态、原始案例和安全边界。"><meta name="twitter:image" content="{BASE}og.png"><meta name="twitter:image:alt" content="13 个原创中文 Agent Skills 方法与证据总览">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"13 个原创中文 Agent Skills 方法与证据总览","description":"按场景比较本站原创 Agent Skills 的方法、实测结果与质量边界。","inLanguage":"zh-CN","dateModified":"2026-08-12","url":"{BASE}guides/","image":"{BASE}og.png","isPartOf":{{"@type":"WebSite","name":"中文 AI Skills 库","url":"{BASE}"}},"numberOfItems":13}}</script>
<style>
:root{{--paper:#eee8dc;--sheet:#fbf8ef;--ink:#1a211d;--muted:#5f6963;--line:#c4baa8;--red:#a54136;--jade:#285f4d;--gold:#b77d27;--blue:#355f74;--sans:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;--serif:"Songti SC","Noto Serif CJK SC",STSong,serif;--mono:ui-monospace,SFMono-Regular,Menlo,monospace}}*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.72 var(--sans);background-image:radial-gradient(rgba(50,40,30,.06) .7px,transparent .7px);background-size:8px 8px}}a{{color:var(--jade)}}.wrap{{width:min(1180px,calc(100% - 38px));margin:auto}}.top{{padding:22px 0;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:20px;font-size:13px}}.top a{{text-decoration:none;font-weight:800}}.top span{{font:11px var(--mono);letter-spacing:.12em;color:var(--muted)}}.hero{{padding:72px 0 54px;display:grid;grid-template-columns:1.2fr .8fr;gap:54px;align-items:end}}.eyebrow{{font:800 12px var(--mono);letter-spacing:.16em;color:var(--red)}}h1,h2{{font-family:var(--serif)}}h1{{font-size:clamp(44px,7vw,80px);line-height:1.06;margin:18px 0 22px;max-width:10em}}.lead{{font-size:clamp(18px,2vw,22px);color:#465149;max-width:36em}}.legend{{background:var(--sheet);border:1px solid var(--ink);padding:28px;box-shadow:10px 10px 0 rgba(165,65,54,.18)}}.legend h2{{font-size:25px;margin:0 0 14px}}.legend p{{margin:8px 0;font-size:13px;color:var(--muted)}}.dot{{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:8px}}.dot.done{{background:var(--jade)}}.dot.wait{{background:var(--blue)}}.dot.partial{{background:var(--gold)}}.proof-strip{{border-block:1px solid var(--line);background:rgba(251,248,239,.55)}}.proof-strip .wrap{{display:grid;grid-template-columns:repeat(4,1fr)}}.proof{{padding:22px}}.proof+.proof{{border-left:1px solid var(--line)}}.proof b{{display:block;font:700 29px var(--serif);color:var(--jade)}}.proof span{{font-size:12px;color:var(--muted)}}.intro{{padding:58px 0 22px}}.intro h2{{font-size:clamp(30px,5vw,50px);margin:0 0 8px}}.intro p{{color:var(--muted);max-width:50em}}.filters{{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}}.filters button{{border:1px solid var(--line);background:var(--sheet);padding:9px 13px;color:var(--ink);font-weight:800;cursor:pointer}}.filters button[aria-pressed="true"]{{background:var(--ink);color:var(--sheet);border-color:var(--ink)}}.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;padding:18px 0 70px}}.guide-card{{background:var(--sheet);border:1px solid var(--line);padding:25px;display:flex;flex-direction:column;min-height:390px}}.guide-card[hidden]{{display:none}}.card-top{{display:flex;justify-content:space-between;gap:15px;align-items:center}}.number{{font:11px var(--mono);color:var(--muted)}}.status{{font:800 11px var(--mono);padding:6px 8px;border:1px solid}}.status.done{{color:var(--jade)}}.status.wait{{color:var(--blue)}}.status.partial{{color:#875b18}}.guide-card h2{{font-size:29px;margin:17px 0 4px}}.guide-card h2 a{{color:var(--ink);text-decoration:none}}.scenario{{font-size:15px;color:var(--muted);margin:0 0 19px}}.evidence,.boundary{{display:grid;grid-template-columns:72px 1fr;gap:12px;padding:13px 0;border-top:1px solid var(--line);font-size:13px}}.evidence b{{color:var(--jade)}}.boundary b{{color:var(--red)}}.card-links{{margin-top:auto;padding-top:18px;display:flex;gap:13px;flex-wrap:wrap}}.card-links a{{font-size:12px;font-weight:800}}.method{{padding:55px 0;border-top:1px solid var(--line);display:grid;grid-template-columns:.75fr 1.25fr;gap:50px}}.method h2{{font-size:39px;margin:0}}.method p{{margin:0;color:var(--muted)}}.cta{{margin:0 auto 65px;background:var(--red);color:#fff7e9;padding:clamp(30px,6vw,58px);display:grid;grid-template-columns:1fr auto;gap:28px;align-items:end}}.cta h2{{font-size:36px;margin:0 0 8px}}.cta p{{margin:0;opacity:.86}}.cta a{{color:#fff7e9;border:1px solid;padding:10px 15px;text-decoration:none;font-weight:800}}footer{{padding:0 0 45px;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;color:var(--muted);font-size:13px}}@media(max-width:760px){{.hero,.method,.cta{{grid-template-columns:1fr}}.proof-strip .wrap{{grid-template-columns:1fr 1fr}}.proof:nth-child(3){{border-left:0;border-top:1px solid var(--line)}}.proof:nth-child(4){{border-top:1px solid var(--line)}}.grid{{grid-template-columns:1fr}}}}@media(max-width:470px){{.wrap{{width:calc(100% - 26px)}}.top span{{display:none}}.proof-strip .wrap{{grid-template-columns:1fr}}.proof+.proof{{border-left:0;border-top:1px solid var(--line)}}.evidence,.boundary{{grid-template-columns:1fr;gap:3px}}}}
</style></head>
<body><header class="wrap top"><a href="../">← 中文 AI Skills 库</a><span>FIRST-PARTY GUIDES · EVIDENCE INDEX</span></header>
<main><section class="wrap hero"><div><div class="eyebrow">13 个本站原创 · 方法与证据</div><h1>先按问题选，<br>再看它做到了哪一步。</h1><p class="lead">这里不是把 13 个名称再列一遍。每张卡都连接方法说明、原始实测和质量边界，帮助你判断哪个 Skill 适合当前任务。</p></div><aside class="legend"><h2>三种任务状态</h2><p><span class="dot done"></span><b>当次任务完成</b>：记录中的交付已完成。</p><p><span class="dot wait"></span><b>校准完成，待输入</b>：按流程先问必要信息。</p><p><span class="dot partial"></span><b>缩小复测通过</b>：大任务未完成，较小任务通过。</p></aside></section>
<section class="proof-strip"><div class="wrap"><div class="proof"><b>13 / 13</b><span>Codex 单任务中观察到自动触发</span></div><div class="proof"><b>10</b><span>记录中的当次任务完成</span></div><div class="proof"><b>1</b><span>按设计停在校准提问</span></div><div class="proof"><b>2</b><span>大任务失败后缩小复测通过</span></div></div></section>
<section class="wrap intro"><h2>你现在想解决什么？</h2><p>筛选只改变当前页面显示，不改变证据。所有结论限定于记录的客户端版本和任务原文，不代表跨版本准确率或官方认证。</p><div class="filters" role="group" aria-label="按实测状态筛选"><button type="button" data-filter="all" aria-pressed="true">全部 13 个</button><button type="button" data-filter="done" aria-pressed="false">当次完成</button><button type="button" data-filter="wait" aria-pressed="false">等待输入</button><button type="button" data-filter="partial" aria-pressed="false">缩小复测</button></div></section>
<section class="wrap grid" id="guide-grid">{cards}</section>
<section class="wrap method"><h2>证据怎么读</h2><p>“能发现”“已安装”“自动触发”“完成任务”是四件事。这里的状态来自 <a href="../data/compatibility.json">compatibility.json</a>，文件构成、联网行为与敏感边界来自 <a href="../data/quality.json">quality.json</a>。第三方目录收录、安装次数或单次运行都不等于质量认证。</p></section>
<section class="wrap cta"><div><h2>先装一个当前真需要的。</h2><p>从小任务开始，保留客户端版本、原始任务和实际输出。成功与失败都可以提交为可复现证据。</p></div><a href="../install/">看安装与排错 →</a></section></main>
<footer class="wrap"><span><a href="../compatibility/">兼容性实测</a> · <a href="../QUALITY.md">质量与安全标签</a> · <a href="../cases/README.md">全部案例</a></span><span><a href="https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools">查看 GitHub 仓库 · 觉得有用再 Star</a></span></footer>
<script>document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{{const value=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(item=>item.setAttribute('aria-pressed',item===button?'true':'false'));document.querySelectorAll('.guide-card').forEach(card=>card.hidden=value!=='all'&&card.dataset.outcome!==value);}}));</script></body></html>'''


def sync_explainer_links(write=False):
    originals, _, _ = load_data()
    changed = []
    marker = '<a href="../guides/">13 个原创 Skill 总览</a>'
    for skill in originals:
        path = ROOT / skill["explainer"] / "index.html"
        body = path.read_text(encoding="utf-8")
        if marker in body:
            continue
        footer = body.rfind("</footer>")
        if footer < 0:
            raise ValueError(f"missing footer: {path}")
        updated = body[:footer] + f'<span>{marker}</span>' + body[footer:]
        changed.append(path.relative_to(ROOT).as_posix())
        if write:
            path.write_text(updated, encoding="utf-8")
    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    expected = render()
    current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
    stale = current != expected
    link_changes = sync_explainer_links(write=args.write)
    if args.write:
        OUTPUT.parent.mkdir(exist_ok=True)
        OUTPUT.write_text(expected, encoding="utf-8")
        return
    problems = ([OUTPUT.relative_to(ROOT).as_posix()] if stale else []) + link_changes
    if problems:
        raise SystemExit("stale generated guide files: " + ", ".join(problems))


if __name__ == "__main__":
    main()
