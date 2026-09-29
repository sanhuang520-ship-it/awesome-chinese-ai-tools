#!/usr/bin/env python3
"""Generate a prospective compatibility retest queue with no implied results."""

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "retest" / "index.html"
BASE = "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/"


def load_items():
    data = json.loads((ROOT / "data" / "retest-queue.json").read_text(encoding="utf-8"))
    items = data["items"]
    allowed = {"planned", "executed-pass", "executed-fail"}
    if len(items) != 6 or any(item.get("status") not in allowed for item in items):
        raise ValueError("retest queue must contain exactly six prospective items with known statuses")
    for item in items:
        execution = item.get("execution")
        if item["status"] == "planned" and execution is not None:
            raise ValueError(f"planned item cannot contain execution evidence: {item['skill']}")
        if item["status"] != "planned":
            if not execution or execution.get("totalChecks") != len(item["acceptanceZh"]):
                raise ValueError(f"executed item lacks complete evidence: {item['skill']}")
            if not (ROOT / execution.get("case", "")).is_file():
                raise ValueError(f"executed item case is missing: {item['skill']}")
            remediation = execution.get("remediation")
            if remediation:
                if remediation.get("passedChecks") != remediation.get("totalChecks"):
                    raise ValueError(f"remediation must preserve a complete passing result: {item['skill']}")
                if not (ROOT / remediation.get("case", "")).is_file():
                    raise ValueError(f"remediation case is missing: {item['skill']}")
    return items


def render():
    items = load_items()
    executed = sum(item["status"] != "planned" for item in items)
    remaining = len(items) - executed
    executed_skills = "、".join(item["skill"] for item in items if item["status"] != "planned")
    remediation_count = sum(bool(item.get("execution", {}).get("remediation")) for item in items)
    cards = []
    for index, item in enumerate(items, 1):
        prompt = item["promptZh"]
        checks = "".join(f"<li>{html.escape(check)}</li>" for check in item["acceptanceZh"])
        issue = (
            "https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new"
            "?template=compatibility-result.yml"
        )
        if item["status"] == "planned":
            status = "PLANNED · 尚无结果"
            result_link = f'<a class="submit" href="{issue}">提交你的运行结果 →</a>'
        else:
            execution = item["execution"]
            remediation = execution.get("remediation")
            if remediation:
                status = f"初次 {execution['passedChecks']} / {execution['totalChecks']} · 修复后 {remediation['passedChecks']} / {remediation['totalChecks']}"
                result_link = f'<a class="submit" href="../{html.escape(execution["case"])}">初次失败记录</a> · <a class="submit" href="../{html.escape(remediation["case"])}">修复后复测 →</a>'
            else:
                label = "已执行 · 预注册门槛通过" if item["status"] == "executed-pass" else "已执行 · 未通过全部门槛"
                status = f"{label} {execution['passedChecks']} / {execution['totalChecks']}"
                result_link = f'<a class="submit" href="../{html.escape(execution["case"])}">查看执行记录与限制 →</a>'
        cards.append(f'''<article class="queue-card" data-status="{html.escape(item['status'])}"><div class="card-top"><span>{index:02d} · {html.escape(item["skill"])}</span><b>{status}</b></div><h2>{html.escape(item["titleZh"])}</h2><strong>运行前公开的任务</strong><pre>{html.escape(prompt)}</pre><button type="button" data-copy="{html.escape(prompt, quote=True)}">复制任务</button><strong class="gate-title">预注册成功门槛</strong><ul>{checks}</ul>{result_link}</article>''')
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><title>中文 Agent Skills 前瞻复测：6 项执行与 2 项修复闭环</title><meta name="description" content="6 个先公开任务与成功门槛的中文 Agent Skill 兼容性复测已全部执行；初次 4 项通过、2 项失败，针对性修复后两项均以相同任务通过 4/4。"><link rel="canonical" href="{BASE}retest/"><meta property="og:type" content="article"><meta property="og:locale" content="zh_CN"><meta property="og:title" content="中文 Agent Skills 待复测队列"><meta property="og:description" content="先发布任务与成功门槛，再记录初次结果与修复后复测；旧失败不会覆盖。"><meta property="og:url" content="{BASE}retest/"><meta property="og:image" content="{BASE}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="中文 Agent Skills 待复测队列"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="中文 Agent Skills 待复测队列"><meta name="twitter:description" content="先发布任务与成功门槛，再记录初次结果与修复后复测；旧失败不会覆盖。"><meta name="twitter:image" content="{BASE}og.png"><meta name="twitter:image:alt" content="中文 Agent Skills 待复测队列"><script type="application/ld+json">{{"@context":"https://schema.org","@type":"TechArticle","headline":"中文 Agent Skills 待复测队列","description":"运行前公开的兼容性复测任务与验收标准。","inLanguage":"zh-CN","dateModified":"2026-08-13","mainEntityOfPage":"{BASE}retest/","image":"{BASE}og.png","author":{{"@type":"Organization","name":"中文 AI Skills 库"}}}}</script><style>:root{{--paper:#efe9dc;--sheet:#fffaf0;--ink:#1c231f;--muted:#616963;--line:#c5baa6;--red:#a54437;--jade:#28614e;--amber:#a96e1f;--serif:"Songti SC","Noto Serif CJK SC",STSong,serif;--sans:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,monospace}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.72 var(--sans)}}a{{color:var(--jade)}}.wrap{{width:min(1120px,calc(100% - 38px));margin:auto}}.top{{padding:22px 0;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:20px;font-size:13px}}.top a{{text-decoration:none;font-weight:800}}.top span{{font:11px var(--mono);color:var(--muted);letter-spacing:.12em}}.hero{{padding:72px 0 58px;display:grid;grid-template-columns:1.2fr .8fr;gap:50px;align-items:end}}.eyebrow{{font:800 12px var(--mono);color:var(--red);letter-spacing:.15em}}h1,h2{{font-family:var(--serif)}}h1{{font-size:clamp(44px,7vw,78px);line-height:1.06;margin:18px 0 22px;max-width:10em}}.lead{{font-size:20px;color:#465149;max-width:37em}}.warning{{border:1px solid var(--ink);background:var(--sheet);padding:28px;box-shadow:10px 10px 0 rgba(169,110,31,.18)}}.warning b{{font:700 32px var(--serif);color:var(--amber)}}.warning p{{margin:9px 0 0;color:var(--muted)}}.method{{border-block:1px solid var(--line);padding:22px 0;background:rgba(255,250,240,.5)}}.method p{{margin:0}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:17px;padding:64px 0}}.queue-card{{background:var(--sheet);border:1px solid var(--line);padding:25px;min-width:0}}.card-top{{display:flex;justify-content:space-between;gap:14px;font:11px var(--mono);color:var(--muted)}}.card-top b{{color:var(--amber)}}.queue-card h2{{font-size:28px;margin:17px 0 21px}}.queue-card strong{{font-size:13px}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#eee5d5;padding:14px;font:12px/1.65 var(--mono)}}button{{border:1px solid var(--jade);background:transparent;color:var(--jade);padding:8px 11px;font-weight:800;cursor:pointer}}.gate-title{{display:block;margin-top:22px;padding-top:18px;border-top:1px solid var(--line)}}ul{{padding-left:1.25em;color:var(--muted);font-size:13px}}.submit{{font-size:12px;font-weight:800}}.cta{{margin:0 auto 64px;background:var(--red);color:#fff8ed;padding:45px;display:grid;grid-template-columns:1fr auto;gap:25px;align-items:end}}.cta h2{{font-size:34px;margin:0 0 8px}}.cta p{{margin:0;opacity:.86}}.cta a{{color:#fff8ed;border:1px solid;padding:10px 14px;text-decoration:none;font-weight:800}}footer{{padding:0 0 45px;display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;color:var(--muted);font-size:13px}}@media(max-width:760px){{.hero,.grid,.cta{{grid-template-columns:1fr}}}}@media(max-width:460px){{.wrap{{width:calc(100% - 26px)}}.top span{{display:none}}.queue-card{{padding:19px}}.card-top{{flex-direction:column}}}}</style></head><body><header class="wrap top"><a href="../">← 中文 AI Skills 库</a><span>PROSPECTIVE RETEST · {executed} EXECUTED · {remediation_count} REMEDIATED</span></header><main><section class="wrap hero"><div><div class="eyebrow">先定任务与门槛，再看结果</div><h1>6 个全部执行，<br>2 个完成修复闭环。</h1><p class="lead">任务与成功标准在运行前公开。{executed_skills} 均已在隔离 Codex 环境执行；两项初次失败经针对性修复后，用完全相同任务通过 4/4。</p></div><aside class="warning"><b>PREREGISTERED ≠ UNIVERSAL</b><p>修复后通过不抹去初次失败；所有结论只限记录的客户端、任务、Skill 版本和隔离环境。</p></aside></section><section class="method"><div class="wrap"><p><strong>最小记录：</strong>客户端与版本、是否点名 Skill、是否自动读取、最终是否完成、脱敏输出。不要用安装成功代替任务结果。</p></div></section><section class="wrap grid">{''.join(cards)}</section><section class="wrap cta"><div><h2>你可以先跑其中一个。</h2><p>Claude Code、Cursor 或其他 Codex 版本都欢迎；失败结果同样保留。</p></div><a href="https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml">提交结构化结果 →</a></section></main><footer class="wrap"><span><a href="../reproduce/">7 个历史逐字任务</a> · <a href="../compatibility/">兼容性证据</a> · <a href="../fix-agent-skill/">失败后怎么修</a> · <a href="../data/retest-queue.json">机器可读队列</a></span><span><a href="https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools">查看 GitHub 仓库 · 觉得有用再 Star</a></span></footer><script>document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{{try{{await navigator.clipboard.writeText(button.dataset.copy);const old=button.textContent;button.textContent='已复制 ✓';setTimeout(()=>button.textContent=old,1600)}}catch{{button.textContent='复制失败，请手动选择'}}}}));</script></body></html>'''


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
        raise SystemExit("retest/index.html is stale; run scripts/generate_retest_queue.py --write")


if __name__ == "__main__":
    main()
