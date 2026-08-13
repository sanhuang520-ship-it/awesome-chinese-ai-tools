#!/usr/bin/env python3
"""Generate one first-use page from preserved and prospective task evidence."""

import argparse
import html
import json
from pathlib import Path

from generate_reproduce_page import TITLES, original_task, validate_records


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "try-agent-skills" / "index.html"
BASE = "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/"
ISSUE = "https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml"


def load_tasks():
    evidence = json.loads((ROOT / "data" / "task-evidence.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "data" / "compatibility.json").read_text(encoding="utf-8"))["results"]["codexActivation"]["skillResults"]
    queue = json.loads((ROOT / "data" / "retest-queue.json").read_text(encoding="utf-8"))["items"]
    verbatim, summaries = validate_records(evidence["records"])
    if {name for name, _ in summaries} != {item["skill"] for item in queue}:
        raise ValueError("prospective tasks must exactly cover summary-only evidence")
    historical = [
        {
            "skill": name,
            "title": TITLES[name],
            "prompt": task,
            "kind": "historical",
            "status": results[name]["labelZh"],
            "summary": results[name]["summaryZh"],
            "case": record["case"],
        }
        for name, record, task in verbatim
    ]
    prospective = [
        {
            "skill": item["skill"],
            "title": item["titleZh"],
            "prompt": item["promptZh"],
            "kind": "prospective",
            "status": (
                "PLANNED · 尚无结果"
                if item["status"] == "planned"
                else f"已执行 · {'预注册门槛通过' if item['status'] == 'executed-pass' else '未通过全部门槛'} {item['execution']['passedChecks']} / {item['execution']['totalChecks']}"
            ),
            "checks": item["acceptanceZh"],
            "execution": item.get("execution"),
        }
        for item in queue
    ]
    return historical, prospective


def render_card(item):
    install = f"npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill {item['skill']}"
    if item["kind"] == "historical":
        evidence = f'''<strong>已有记录（只限当时版本与任务）</strong><p>{html.escape(item["summary"])}</p><a href="https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/blob/main/{html.escape(item["case"])}">查看原始案例与限制 →</a>'''
        badge = "历史逐字原文"
    else:
        checks = "".join(f"<li>{html.escape(check)}</li>" for check in item["checks"])
        if item.get("execution"):
            evidence_link = f'<a href="../{html.escape(item["execution"]["case"])}">查看执行记录与限制 →</a>'
            heading = "预注册门槛（已执行）"
        else:
            evidence_link = f'<a href="{ISSUE}">提交成功、失败或未触发结果 →</a>'
            heading = "成功门槛（尚未执行）"
        evidence = f'''<strong>{heading}</strong><ul>{checks}</ul>{evidence_link}'''
        badge = "前瞻任务"
    return f'''<article class="task" data-kind="{item['kind']}"><div class="head"><span>{html.escape(item['skill'])}</span><b>{badge}</b></div><h2>{html.escape(item['title'])}</h2><div class="step"><i>01</i><div><strong>安装单项</strong><code>{html.escape(install)}</code><button type="button" data-copy="{html.escape(install, quote=True)}">复制安装命令</button></div></div><div class="step"><i>02</i><div><strong>重启客户端后复制自然任务</strong><pre>{html.escape(item['prompt'])}</pre><button type="button" data-copy="{html.escape(item['prompt'], quote=True)}">复制任务</button></div></div><div class="step proof"><i>03</i><div><span class="status">{html.escape(item['status'])}</span>{evidence}</div></div></article>'''


def render():
    historical, prospective = load_tasks()
    if len(historical) != 7 or len(prospective) != 6:
        raise ValueError("expected 7 historical and 6 prospective tasks")
    executed = sum(item.get("execution") is not None for item in prospective)
    remaining = len(prospective) - executed
    cards = "".join(render_card(item) for item in historical + prospective)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><title>13 个中文 Agent Skills 首次试用任务：安装、复制、验证</title><meta name="description" content="13 个原创中文 Agent Skills 的单项安装命令、可复制自然任务与验证入口；7 条来自历史逐字原文，6 条为运行前公开的前瞻任务，其中 {executed} 条已执行、{remaining} 条仍待测。"><link rel="canonical" href="{BASE}try-agent-skills/"><meta property="og:type" content="article"><meta property="og:locale" content="zh_CN"><meta property="og:title" content="13 个中文 Agent Skills 首次试用任务"><meta property="og:description" content="安装一个、复制自然任务、对照证据或成功门槛；历史原文与前瞻任务严格分开。"><meta property="og:url" content="{BASE}try-agent-skills/"><meta property="og:image" content="{BASE}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="13 个中文 Agent Skills 首次试用任务"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="13 个中文 Agent Skills 首次试用任务"><meta name="twitter:description" content="安装一个、复制自然任务、对照证据或成功门槛。"><meta name="twitter:image" content="{BASE}og.png"><script type="application/ld+json">{{"@context":"https://schema.org","@type":"TechArticle","headline":"13 个中文 Agent Skills 首次试用任务","description":"单项安装、自然任务与证据边界。","inLanguage":"zh-CN","dateModified":"2026-08-13","mainEntityOfPage":"{BASE}try-agent-skills/","image":"{BASE}og.png","author":{{"@type":"Organization","name":"中文 AI Skills 库"}}}}</script><style>:root{{--paper:#eee8dc;--sheet:#fffaf0;--ink:#1b221e;--muted:#606963;--line:#c4b9a5;--red:#a44336;--jade:#28614e;--amber:#9b681f;--sans:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;--serif:"Songti SC","Noto Serif CJK SC",STSong,serif;--mono:ui-monospace,SFMono-Regular,Menlo,monospace}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.72 var(--sans)}}a{{color:var(--jade)}}.wrap{{width:min(1160px,calc(100% - 38px));margin:auto}}.top{{padding:22px 0;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;font-size:13px}}.top a{{font-weight:800;text-decoration:none}}.top span,.head{{font:11px var(--mono);color:var(--muted)}}.hero{{padding:70px 0 50px;display:grid;grid-template-columns:1.2fr .8fr;gap:48px;align-items:end}}h1,h2{{font-family:var(--serif)}}h1{{font-size:clamp(44px,7vw,78px);line-height:1.06;margin:16px 0 20px;max-width:10em}}.eyebrow{{font:800 12px var(--mono);color:var(--red);letter-spacing:.14em}}.lead{{font-size:20px;color:#465149}}.legend{{background:var(--sheet);border:1px solid var(--ink);padding:26px;box-shadow:10px 10px 0 rgba(164,67,54,.15)}}.legend p{{margin:9px 0;color:var(--muted)}}.legend b{{color:var(--jade)}}.method{{border-block:1px solid var(--line);background:rgba(255,250,240,.5);padding:21px 0}}.method p{{margin:0}}.filters{{display:flex;gap:8px;padding-top:42px;flex-wrap:wrap}}.filters button{{margin:0}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:17px;padding:18px 0 65px}}.task{{background:var(--sheet);border:1px solid var(--line);padding:24px;min-width:0}}.task[hidden]{{display:none}}.head{{display:flex;justify-content:space-between;gap:12px}}.head b{{color:var(--red)}}.task h2{{font-size:27px;margin:15px 0 20px}}.step{{display:grid;grid-template-columns:30px 1fr;gap:10px;padding:16px 0;border-top:1px solid var(--line);min-width:0}}.step i{{font:800 11px var(--mono);font-style:normal;color:var(--red)}}.step strong{{display:block;margin-bottom:7px}}code,pre{{font:12px/1.6 var(--mono);overflow-wrap:anywhere}}code{{display:block;background:#202722;color:#f7f0e4;padding:10px}}pre{{white-space:pre-wrap;background:#eee5d5;padding:13px;margin:0}}button{{margin-top:8px;border:1px solid var(--jade);background:transparent;color:var(--jade);padding:8px 11px;font-weight:800;cursor:pointer}}.proof p,.proof ul{{font-size:13px;color:var(--muted)}}.proof ul{{padding-left:1.2em}}.proof a{{font-size:12px;font-weight:800}}.status{{display:block;font:800 11px var(--mono);color:var(--amber);margin-bottom:8px}}footer{{padding:0 0 45px;display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;color:var(--muted);font-size:13px}}@media(max-width:760px){{.hero,.grid{{grid-template-columns:1fr}}}}@media(max-width:460px){{.wrap{{width:calc(100% - 26px)}}.top span{{display:none}}.task{{padding:18px}}}}</style></head><body><header class="wrap top"><a href="../">← 中文 AI Skills 库</a><span>FIRST USE LAB · 13 TASKS</span></header><main><section class="wrap hero"><div><div class="eyebrow">安装一个 · 复制任务 · 核对结果</div><h1>别先装全部，<br>先完成一个真任务。</h1><p class="lead">每张卡给出单项安装、未点名 Skill 的自然任务，以及可以核对的历史记录或前瞻成功门槛。</p></div><aside class="legend"><p><b>7 条历史逐字原文</b>：可与仓库当时记录对照，但不保证其他版本相同。</p><p><b>6 条前瞻任务</b>：在执行前公开成功门槛；{executed} 条已执行，{remaining} 条仍为 planned。</p></aside></section><section class="method"><div class="wrap"><p><strong>使用顺序：</strong>安装一个 Skill → 重启客户端 → 复制自然任务 → 记录客户端版本、是否自动触发与最终结果。先移除 Token、邮箱、私人路径和未公开数据。</p></div></section><section class="wrap filters" aria-label="任务类型筛选"><button type="button" data-filter="all" aria-pressed="true">全部 13 条</button><button type="button" data-filter="historical" aria-pressed="false">7 条历史原文</button><button type="button" data-filter="prospective" aria-pressed="false">6 条前瞻任务（{executed} 已执行）</button></section><section class="wrap grid">{cards}</section></main><footer class="wrap"><span><a href="../guides/">方法与证据总览</a> · <a href="../reproduce/">历史逐字任务</a> · <a href="../retest/">前瞻复测队列</a></span><span><a href="{ISSUE}">提交一次真实结果</a> · <a href="https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools">查看 GitHub 仓库 · 觉得有用再 Star</a></span></footer><script>document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{{try{{await navigator.clipboard.writeText(button.dataset.copy);const old=button.textContent;button.textContent='已复制 ✓';setTimeout(()=>button.textContent=old,1600)}}catch{{button.textContent='复制失败，请手动选择'}}}}));document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{{const value=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(item=>item.setAttribute('aria-pressed',item===button?'true':'false'));document.querySelectorAll('.task').forEach(card=>card.hidden=value!=='all'&&card.dataset.kind!==value);}}));</script></body></html>'''


def sync_explainer_links(write=False):
    skills = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))["skills"]
    marker = '<a href="../try-agent-skills/">复制首次试用任务</a>'
    changed = []
    for skill in (item for item in skills if item.get("ours")):
        path = ROOT / skill["explainer"] / "index.html"
        body = path.read_text(encoding="utf-8")
        if marker in body:
            continue
        footer = body.rfind("</footer>")
        if footer < 0:
            raise ValueError(f"missing footer: {path}")
        changed.append(path.relative_to(ROOT).as_posix())
        if write:
            path.write_text(body[:footer] + f"<span>{marker}</span>" + body[footer:], encoding="utf-8")
    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    expected = render()
    current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
    link_changes = sync_explainer_links(write=args.write)
    if args.write:
        OUTPUT.parent.mkdir(exist_ok=True)
        OUTPUT.write_text(expected, encoding="utf-8")
    elif current != expected or link_changes:
        raise SystemExit("stale first-use page or explainer links")


if __name__ == "__main__":
    main()
