#!/usr/bin/env python3
"""
每天自动给 awesome-chinese-ai-tools 仓库提交一条"今日工具推荐"
并检测所有收录工具的链接健康状态，挂掉的工具自动在 data/tools.json 中打标。
运行方式：由 launchd 每天 09:00 自动触发
"""

import json
import re
import base64
import urllib.request
import urllib.error
import datetime
import random
import os
import ssl
try:
    import certifi
    _CAFILE = certifi.where()
except ImportError:
    _CAFILE = None
import time

# ── 配置 ──────────────────────────────────────────────────
# token 从环境变量读取。GitHub Actions 里用自带的 GITHUB_TOKEN，无需配置密钥；
# 本地跑： export GITHUB_TOKEN=xxx && python3 scripts/daily_check.py
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
if not GITHUB_TOKEN:
    raise SystemExit("缺少环境变量 GITHUB_TOKEN")
REPO     = os.environ.get("GITHUB_REPOSITORY", "sanhuang520-ship-it/awesome-chinese-ai-tools")
API_BASE = "https://api.github.com"
# ──────────────────────────────────────────────────────────

TOOL_SPOTLIGHTS = [
    ("DeepSeek-R1", "https://chat.deepseek.com", "深度求索开源推理模型，数学和代码能力比肩 o1，API 价格极低，国产之光。"),
    ("秘塔搜索", "https://metaso.cn", "国内最好用的 AI 搜索引擎，无广告，支持深度模式和学术模式，完全免费。"),
    ("沉浸式翻译", "https://immersivetranslate.com", "浏览器双语对照翻译神器，支持 PDF、字幕、网页，免费版已非常够用。"),
    ("通义灵码", "https://lingma.aliyun.com", "阿里出品的免费 AI 编程插件，支持 VS Code 和 JetBrains，对国内开发者最友好。"),
    ("即梦 AI", "https://jimeng.jianying.com", "字节出品的图像/视频生成工具，中文提示词理解极佳，每日免费额度充足。"),
    ("Kimi", "https://kimi.moonshot.cn", "月之暗面出品，200k 超长上下文，适合分析长文档、合同、论文，网页版免费。"),
    ("可灵 AI", "https://klingai.kuaishou.com", "快手出品的视频生成工具，720p 高质量，运动流畅度领先，每日免费积分可用。"),
    ("FastGPT", "https://fastgpt.in", "开源知识库问答平台，支持私有部署，RAG 效果好，中文支持完善。"),
    ("Dify", "https://dify.ai", "国产开源 LLMOps 平台，可视化编排 Agent 工作流，GitHub 30k+ stars。"),
    ("豆包", "https://www.doubao.com", "字节跳动出品，多模态支持，联网搜索，日常对话和创作场景表现均衡。"),
    ("LiblibAI", "https://www.liblib.art", "国内最大的 Stable Diffusion 模型社区，每日免费算力，国风/二次元模型丰富。"),
    ("Coze", "https://coze.cn", "字节出品的 Agent 搭建平台，国内版免费，插件生态丰富，适合搭建个人 AI 助手。"),
    ("WPS AI", "https://ai.wps.cn", "Office 场景下的 AI 助手，文档摘要、公式生成、PPT 美化，对中文文档处理最优。"),
    ("海螺视频", "https://hailuoai.video", "MiniMax 出品的视频生成工具，人物运动流畅，每日免费次数可用。"),
    ("Fish Audio", "https://fish.audio", "支持中文方言的 TTS 平台，音色克隆效果好，每月有免费额度。"),
    ("Windsurf", "https://codeium.com/windsurf", "Codeium 出品的免费 AI IDE，功能与 Cursor 相近，完全免费是最大优势。"),
    ("智谱清言", "https://chatglm.cn", "清华技术背景，GLM-4 模型，支持 Agent 和代码解释器，API 有免费额度。"),
    ("秘塔写作猫", "https://xiezuocat.com", "国内老牌中文写作助手，语法检查、改写润色、AI 续写，基础功能免费。"),
    ("Gamma", "https://gamma.app", "AI 一键生成 PPT 和文档，模板精美，适合快速出提案和汇报，每月有免费积分。"),
    ("天工 AI 搜索", "https://search.tiangong.cn", "昆仑万维出品，完全免费，中文资讯和时事查询效果好，支持多轮追问。"),
    ("Qwen3", "https://tongyi.aliyun.com", "阿里最新旗舰模型，235B 参数，思维链推理强，API 有免费额度，性价比高。"),
    ("MarsCode", "https://www.marscode.cn", "字节出品的在线云 IDE，内置 AI 编程助手，免费版功能够用，无需本地配置。"),
    ("彩云小译", "https://caiyunapp.com", "日语翻译效果国内最佳，支持实时字幕翻译，适合追番和看日语技术文档。"),
    ("讯飞配音", "https://peiyin.xunfei.cn", "科大讯飞出品，国内 TTS 标杆，音色最丰富，每日有免费字符额度。"),
    ("Perplexity", "https://perplexity.ai", "AI 搜索引擎国际标杆，引用来源准确，学术和技术查询效果最佳，每日免费次数。"),
]

# ── GitHub API 封装 ────────────────────────────────────────
def github_api(method, path, data=None, retries=3):
    """
    调 GitHub API。

    2026-08-09 修：原来只捕 HTTPError，网络层异常（SSLEOFError / URLError）会直接抛出来，
    导致整个脚本崩溃、当天后面的步骤全不执行。现在网络错误重试 3 次（指数退避），
    仍失败则返回 {"_neterr": ...} 让调用方自己判断，而不是炸掉进程。
    """
    url = f"{API_BASE}{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "daily-ai-update-bot"
    }
    body = json.dumps(data).encode() if data else None
    ctx = ssl.create_default_context(cafile=_CAFILE)

    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=45) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            # 5xx 和 429 值得重试，4xx 直接返回让调用方看错误内容
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                last = f"http_{e.code}"
                time.sleep(2 ** attempt)
                continue
            try:
                return json.loads(e.read())
            except Exception:
                return {"_neterr": f"http_{e.code}"}
        except (urllib.error.URLError, ssl.SSLError, OSError) as e:
            last = repr(e)
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
    print(f"[github_api] ⚠️ {method} {path} 网络失败 {retries} 次：{last}")
    return {"_neterr": last}

# ── 本周动态时间线 ─────────────────────────────────────────
def prepend_updates(new_events):
    """把新事件插到 data/updates.json 顶部，去重，最多保留 20 条。"""
    if not new_events:
        return
    path = "data/updates.json"
    info = github_api("GET", f"/repos/{REPO}/contents/{path}")
    if "content" not in info:
        return  # 文件不存在则跳过，避免误创建覆盖
    sha  = info["sha"]
    data = json.loads(base64.b64decode(info["content"]).decode("utf-8"))
    events   = data.get("events", [])
    existing = {(e.get("date"), e.get("title")) for e in events}
    added    = [e for e in new_events if (e.get("date"), e.get("title")) not in existing]
    if not added:
        return
    data["events"]  = (added + events)[:20]
    data["updated"] = datetime.date.today().strftime("%Y-%m-%d")
    payload = {
        "message": f"chore: {data['updated']} 动态时间线 +{len(added)} 条",
        "content": base64.b64encode(
            json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")).decode("ascii"),
        "sha": sha,
        "committer": {"name": "sanhuang520-ship-it", "email": "noreply@github.com"}
    }
    res = github_api("PUT", f"/repos/{REPO}/contents/{path}", payload)
    print(f"[动态时间线] {'✅ 新增 ' + str(len(added)) + ' 条' if 'content' in res else '❌ ' + str(res.get('message', res))}")

# ── 链接健康检测 ───────────────────────────────────────────
def check_url(url, timeout=9):
    """
    检测 URL 是否可访问。
    策略：先发 HEAD，若返回 405 / 501 再发 GET（只读 1 字节）。
    返回 (ok: bool, status: int | None, note: str)
    """
    ctx = ssl.create_default_context(cafile=_CAFILE)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,*/*",
    }

    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=headers, method=method)
            with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
                code = resp.status
                if code < 400:
                    return True, code, "ok"
                return False, code, f"http_{code}"
        except urllib.error.HTTPError as e:
            if e.code in (405, 501) and method == "HEAD":
                continue          # HEAD 不被允许，改用 GET 重试
            # 403/401 = 站点存在但拦截机器人，视为可访问
            if e.code in (403, 401, 429):
                return True, e.code, "ok_bot_blocked"
            return False, e.code, f"http_{e.code}"
        except urllib.error.URLError as e:
            reason = str(e.reason)
            if "timed out" in reason.lower() or "timeout" in reason.lower():
                return False, None, "timeout"
            return False, None, f"url_error"
        except OSError:
            return False, None, "connection_error"
    return False, None, "unknown"


def check_tool_links():
    """
    读取 data/tools.json → 检测每个工具 URL → 写回更新后的 JSON。
    新增字段：
      linkOk        bool | null   — true=可访问 / false=异常 / null=未检测
      linkStatus    str           — "ok" | "http_4xx" | "timeout" | ...
      linkCheckedAt str           — YYYY-MM-DD
      linkFailCount int           — 连续失败次数（≥2 才在网站展示警告）
    """
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    # 已知误报白名单：urllib 检测易失败但实际可访问的域名（curl 验证 200）
    # 跳过这些工具的自动检测，避免反复误报和动态时间线垃圾事件
    # 反复误报的域名：手动 curl 复核确认站点正常，但检测端拿到 403/超时。
    # midjourney.com = Cloudflare 机器人防护，日志里已「异常↔恢复」横跳 76 次。
    SKIP_DOMAINS = {"azure.microsoft.com", "midjourney.com"}
    print(f"\n[链接检测] 开始 — {today_str}")

    # 1. 从 GitHub 拉取 tools.json
    file_path = "data/tools.json"
    existing = github_api("GET", f"/repos/{REPO}/contents/{file_path}")
    if "content" not in existing:
        print("[链接检测] ❌ 无法读取 data/tools.json，跳过检测")
        return

    raw = base64.b64decode(existing["content"]).decode("utf-8")
    data = json.loads(raw)
    sha  = existing["sha"]
    tools = data.get("tools", [])

    # 2. 逐一检测（顺序+间隔，避免被视为扫描器）
    changed     = 0
    dead_names  = []
    recovered   = []
    tl_events   = []

    for t in tools:
        url = t.get("url", "")
        if not url:
            continue

        prev_ok         = t.get("linkOk")
        prev_fail_count = t.get("linkFailCount", 0)

        # 已知误报域名直接跳过（标记为正常，不实际请求）
        if any(d in url for d in SKIP_DOMAINS):
            ok, code, note = True, 200, "ok_whitelisted"
        else:
            ok, code, note = check_url(url)
            if not ok:
                time.sleep(2)
                ok, code, note = check_url(url)  # 重试一次，避免瞬时抖动/反爬误报
        fail_count = 0 if ok else (prev_fail_count + 1)

        # 只在状态发生变化时标记 changed
        if ok != prev_ok or t.get("linkStatus") != note or fail_count != prev_fail_count:
            changed += 1

        t["linkOk"]        = ok
        t["linkStatus"]    = note
        t["linkCheckedAt"] = today_str
        t["linkFailCount"] = fail_count

        icon = "✅" if ok else f"❌(×{fail_count})"
        print(f"  {icon} {t['name']:18s}  {code or '—':>5}  {note}")

        if not ok:
            dead_names.append(t["name"])
        if ok and prev_ok is False:
            recovered.append(t["name"])
        # 刚跨过失效阈值（连续 2 次失败）→ 记入动态时间线
        if not ok and fail_count == 2:
            tl_events.append({
                "date": today_str, "type": "alert",
                "title": f"{t['name']} 链接异常",
                "desc": "已连续检测失败，访问前请留意，或改用同类工具"
            })

        time.sleep(0.4)   # 礼貌间隔

    # 3. 更新 meta
    data["meta"]["updated"]       = today_str
    data["meta"]["linkCheckedAt"] = today_str
    data["meta"]["linkDeadCount"] = len(dead_names)

    # 4. 如果有变化，写回 GitHub
    if changed == 0:
        print(f"[链接检测] 无变化，跳过写入")
        return

    new_content = json.dumps(data, ensure_ascii=False, indent=2)
    payload = {
        "message": f"chore: {today_str} 链接检测 — {len(dead_names)} 个异常",
        "content": base64.b64encode(new_content.encode("utf-8")).decode("ascii"),
        "sha": sha,
        "committer": {"name": "sanhuang520-ship-it", "email": "noreply@github.com"}
    }
    result = github_api("PUT", f"/repos/{REPO}/contents/{file_path}", payload)

    if "content" in result:
        summary = []
        if dead_names:
            summary.append(f"异常: {', '.join(dead_names)}")
        if recovered:
            summary.append(f"恢复: {', '.join(recovered)}")
        print(f"[链接检测] ✅ 已更新 tools.json — {'; '.join(summary) or '全部正常'}")
    else:
        print(f"[链接检测] ❌ 写入失败: {result.get('message', result)}")

    # 把新发现的失效写入动态时间线
    prepend_updates(tl_events)



# ── Skill 健康复检 ─────────────────────────────────────────
def check_skills():
    """
    复检 data/skills.json 里每个 skill 的仓库是否还存在，
    顺带刷新星数和最后更新时间。本站原创跳过（自己维护的）。
    新增字段：skillOk / skillStatus / lastPush / skillCheckedAt
    """
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    print(f"\n[Skill 复检] 开始 — {today_str}")

    path = "data/skills.json"
    info = github_api("GET", f"/repos/{REPO}/contents/{path}")
    if "content" not in info:
        print("[Skill 复检] ❌ 无法读取 skills.json，跳过")
        return
    data = json.loads(base64.b64decode(info["content"]).decode("utf-8"))
    sha = info["sha"]

    dead, alive, star_moved, changed = [], 0, 0, 0
    for s in data.get("skills", []):
        if s.get("ours"):
            s["skillOk"] = True
            s["skillCheckedAt"] = today_str
            continue
        m = re.match(r"https://github\.com/([^/]+)/([^/#?]+)", s.get("url", ""))
        if not m:
            continue
        full = f"{m.group(1)}/{m.group(2).replace('.git','')}"
        r = github_api("GET", f"/repos/{full}")
        prev_ok = s.get("skillOk")
        if "stargazers_count" in r:
            alive += 1
            s["skillOk"] = True
            s["skillStatus"] = "ok"
            s["lastPush"] = r["pushed_at"][:10]
            if s.get("stars") and r["stargazers_count"] != s["stars"]:
                s["stars"] = r["stargazers_count"]
                star_moved += 1
        else:
            dead.append(s["name"])
            s["skillOk"] = False
            s["skillStatus"] = "gone"
        if s.get("skillOk") != prev_ok:
            changed += 1
        s["skillCheckedAt"] = today_str
        time.sleep(0.05)

    data["skillsCheckedAt"] = today_str
    result = github_api("PUT", f"/repos/{REPO}/contents/{path}", {
        "message": f"chore: {today_str} skill 复检 — {len(dead)} 失效 / {star_moved} 个星数更新",
        "content": base64.b64encode(
            json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")).decode("ascii"),
        "sha": sha,
        "committer": {"name": "sanhuang520-ship-it", "email": "noreply@github.com"},
    })
    ok = "content" in result
    print(f"[Skill 复检] {'✅' if ok else '❌'} 存活 {alive} | 失效 {len(dead)} | 星数更新 {star_moved}")
    if dead:
        print(f"           失效：{', '.join(dead)}")
        prepend_updates([{
            "date": today_str, "type": "alert",
            "title": f"{len(dead)} 个 Skill 仓库已失效",
            "desc": "、".join(dead[:3]) + ("…" if len(dead) > 3 else "") + " —— 已在站内标记",
        }])



# ── SKILLS.md 自动生成 ─────────────────────────────────────
CAT_ORDER = ["cn", "doc", "dev", "design", "biz", "data", "sec"]

def build_skills_md():
    """
    从 data/skills.json 重新生成 SKILLS.md。
    手写会过时（曾出现清单写 114 个、实际 116 个），改为每天自动重建。
    """
    info = github_api("GET", f"/repos/{REPO}/contents/data/skills.json")
    if "content" not in info:
        print("[SKILLS.md] ❌ 读不到 skills.json，跳过")
        return
    d = json.loads(base64.b64decode(info["content"]).decode("utf-8"))
    S = d.get("skills", [])
    cats = d.get("categories", {})
    checked = d.get("skillsCheckedAt", "—")

    ours = [s for s in S if s.get("ours")]
    rest = [s for s in S if not s.get("ours")]
    cn_n = sum(1 for s in S if s.get("cat") == "cn")

    def src_col(s):
        if s.get("official"):
            return "官方"
        st = s.get("stars")
        return f"⭐{st:,}" if st else "—"

    def stale_mark(s):
        lp = s.get("lastPush")
        if not lp:
            return ""
        try:
            days = (datetime.date.today() - datetime.date.fromisoformat(lp)).days
        except ValueError:
            return ""
        return f" 🕰<sub>{lp} 后未更新</sub>" if days > 180 else ""

    def row(s):
        return f"| [{s['name']}]({s['url']}) | {src_col(s)} | {s.get('desc','')}{stale_mark(s)} |"

    L = []
    L.append("# 🧩 AI Agent Skills 中文合集\n")
    L.append(f"> **{len(S)} 个 Skill｜{cn_n} 个中文原创｜✍️ {len(ours)} 个本站原创**  ")
    L.append("> 每一个都经 GitHub API 验证仓库真实存在  ")
    L.append(f"> 🔄 最近自动复检：**{checked}**（复检仓库是否还在、星数是否变化；超半年没更新的标 🕰）\n")
    L.append("📋 **[看原创 Skill 实际输出什么 → EXAMPLES.md](EXAMPLES.md)**　"
             "🌐 [在线浏览（可搜索/筛选）](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)\n")
    L.append("---\n")
    L.append("## 什么是 Skills\n")
    L.append("**一句话：Skills 是给 AI 助手加的「专业技能包」。**\n")
    L.append("一个文件夹 + 一份 `SKILL.md` 说明书，告诉 AI 什么时候该用、按什么步骤做。AI 自动判断何时激活。\n")
    L.append("| | 是什么 | 解决什么 |")
    L.append("|---|--------|---------|")
    L.append("| **Skills** | 一份工作说明书（Markdown + 可选脚本） | 教 AI **怎么做**某类任务 |")
    L.append("| **MCP** | 一个后台服务 | 让 AI **连上**外部系统（数据库、浏览器） |")
    L.append("| **插件** | 打包分发的组合 | 把 skills + MCP 打包一键装 |\n")
    L.append("---\n")
    L.append("## 怎么安装\n")
    L.append("```bash")
    L.append(f"npx skills add https://github.com/{REPO} --list          # 先看有哪些")
    L.append(f"npx skills add https://github.com/{REPO} --skill guochao-visual-cn")
    L.append(f"npx skills add https://github.com/{REPO} --skill '*'             # 全部")
    L.append("```\n")
    L.append("> ⚠️ **实测提醒（CLI 1.5.22）**：`npx skills add` 把文件装到 `~/.agents/skills/`（多家 agent 共用），")
    L.append("> 再在 `~/.claude/skills/` 建符号链接指过去 —— Claude Code 读的是后者，两处都能看到。")
    L.append("> 而部分教程（包括 7 万星仓库）写的 `~/.config/claude-code/skills/`，本机实测**并不存在**。\n")
    L.append("装好后重启 Claude Code，**无需手动调用**——描述任务，AI 自动激活。\n")
    L.append("---\n")
    L.append("## Skill 清单\n")

    # 本站原创单列在最前
    if ours:
        L.append(f"### ✍️ 本站原创（{len(ours)} 个）\n")
        L.append("> 我们自己编写维护，每个都写明「不做什么」。可直接 `npx skills add` 安装。\n")
        L.append("| Skill | 说明 |")
        L.append("|-------|------|")
        for s in sorted(ours, key=lambda x: x["name"]):
            L.append(f"| [{s['name']}]({s['url']}) | {s.get('desc','')} |")
        L.append("")

    for c in CAT_ORDER:
        grp = [s for s in rest if s.get("cat") == c]
        if not grp:
            continue
        label = cats.get(c, {}).get("label", c)
        L.append(f"### {label}（{len(grp)} 个）\n")
        L.append("| Skill | 来源 | 说明 |")
        L.append("|-------|------|------|")
        grp.sort(key=lambda s: (0 if s.get("official") else 1, -(s.get("stars") or 0)))
        L.extend(row(s) for s in grp)
        L.append("")

    L.append("---\n")
    L.append("## 怎么自己写一个 Skill\n")
    L.append("```")
    L.append("my-skill/")
    L.append("└── SKILL.md          # 必需")
    L.append("    references/       # 可选")
    L.append("```\n")
    L.append("**一个建议**：写清楚「不做什么」和「能做什么」同样重要。")
    L.append(f"我们 {len(ours)} 个原创 Skill 都写明了边界——记账不做税务筹划、辅导作业不给答案、")
    L.append("学习教练不替你完成输出、国潮视觉不伪造文物。\n")
    L.append("推荐用官方 [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 生成。\n")
    L.append("---\n")
    L.append("## ⚠️ 安全提醒\n")
    L.append("Skills 可含**可执行脚本**。装第三方前先看 `SKILL.md` 和 `scripts/` 内容。\n")
    L.append("---\n")
    L.append(f"*本文件由脚本从 `data/skills.json` 自动生成，最后更新 {datetime.date.today()}。*  ")
    L.append(f"*收录有误或想推荐新 Skill？欢迎 [提 Issue](https://github.com/{REPO}/issues)*")

    body = "\n".join(L) + "\n"

    cur = github_api("GET", f"/repos/{REPO}/contents/SKILLS.md")
    if "content" in cur and base64.b64decode(cur["content"]).decode("utf-8") == body:
        print("[SKILLS.md] 无变化，跳过")
        return
    res = github_api("PUT", f"/repos/{REPO}/contents/SKILLS.md", {
        "message": f"docs: 自动重建 SKILLS.md — {len(S)} 个 skill / {len(ours)} 原创",
        "content": base64.b64encode(body.encode("utf-8")).decode("ascii"),
        "sha": cur.get("sha"),
        "committer": {"name": "sanhuang520-ship-it", "email": "noreply@github.com"},
    })
    print(f"[SKILLS.md] {'✅' if 'content' in res else '❌'} {len(S)} 个 skill / {len(ours)} 原创 / {cn_n} 中文")


# ── 今日推荐 Spotlight ─────────────────────────────────────
def main():
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    month_str = today.strftime("%Y-%m")

    random.seed(today.toordinal())
    tool_name, tool_url, tool_desc = random.choice(TOOL_SPOTLIGHTS)

    new_entry = f"\n## {date_str}\n\n**今日推荐：[{tool_name}]({tool_url})**\n\n{tool_desc}\n"
    file_path = f"spotlights/{month_str}.md"

    existing = github_api("GET", f"/repos/{REPO}/contents/{file_path}")

    if "content" in existing:
        current_content = base64.b64decode(existing["content"]).decode("utf-8")
        if date_str in current_content:
            print(f"[{date_str}] 今天已提交过，跳过。")
            return
        new_content = current_content + new_entry
        sha = existing["sha"]
    else:
        header = f"# 工具推荐日志 {month_str}\n\n每日一个精选 AI 工具，持续更新。\n"
        new_content = header + new_entry
        sha = None

    payload = {
        "message": f"daily: {date_str} 推荐 {tool_name}",
        "content": base64.b64encode(new_content.encode("utf-8")).decode("ascii"),
        "committer": {"name": "sanhuang520-ship-it", "email": "noreply@github.com"}
    }
    if sha:
        payload["sha"] = sha

    result = github_api("PUT", f"/repos/{REPO}/contents/{file_path}", payload)
    if "content" in result:
        print(f"[{date_str}] ✅ 已提交：{tool_name}")
    else:
        print(f"[{date_str}] ❌ 失败：{result.get('message', result)}")


# ── 日报模板 ───────────────────────────────────────────────
def check_source_nav():
    """
    核对根目录 信源导航.md 里的官方链接是否还可访问。

    以前这里是 create_news_template()，每天新建一个 news/YYYY-MM-DD.md。
    问题是这些文件内容完全相同，只有标题日期不同 —— 两个月堆了 8 份重复文件，
    再往前还有 58 篇早期的转述新闻（已归档到 archive/news-2026/）。
    现在改成：只维护一个常青页，每天核对里面的链接还活着没有。
    """
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    path = "SOURCES.md"
    info = github_api("GET", f"/repos/{REPO}/contents/{path}")
    if "content" not in info:
        print("[信源导航] ❌ 找不到 SOURCES.md，跳过")
        return
    body = base64.b64decode(info["content"]).decode("utf-8")

    # 已知误报：整个域名从本机网络返回 400（含首页），属于 IP/地区层拦截，
    # 不是站点失效 —— 手动 curl 复核过，别让它天天误报。
    SKIP = ("ai.meta.com",)

    urls = sorted(set(re.findall(r"\]\((https?://[^)]+)\)", body)))
    dead, skipped = [], 0
    for u in urls:
        if any(d in u for d in SKIP):
            skipped += 1
            continue
        ok, code, note = check_url(u)
        if not ok:
            dead.append((u, note))
        time.sleep(0.15)

    print(f"[信源导航] 核对 {len(urls)-skipped}/{len(urls)} 个官方链接 — 异常 {len(dead)} 个"
          + (f"（跳过已知误报 {skipped} 个）" if skipped else ""))
    for u, note in dead:
        print(f"           ⚠️ {u} ({note})")

    # 只更新页脚的核对日期，正文不动
    updated = re.sub(r"最后核对 \d{4}-\d{2}-\d{2}", f"最后核对 {today_str}", body)
    if updated == body:
        return
    res = github_api("PUT", f"/repos/{REPO}/contents/{path}", {
        "message": f"chore: {today_str} 核对官方信源链接（{len(urls)} 个，异常 {len(dead)}）",
        "content": base64.b64encode(updated.encode("utf-8")).decode("ascii"),
        "sha": info["sha"],
        "committer": {"name": "sanhuang520-ship-it", "email": "noreply@github.com"},
    })
    print(f"[信源导航] {'✅ 已更新核对日期' if 'content' in res else '❌ 写回失败'}")


if __name__ == "__main__":
    # 每步独立 try/except —— 任何一步失败都不影响后面的步骤。
    # （2026-08-09 之前是串行调用，check_tool_links 一次 SSL 抖动就让当天
    #   的 skill 复检和 SKILLS.md 重建全部没跑。）
    import traceback
    STEPS = [
        ("今日工具推荐",   main),
        ("核对官方信源",   check_source_nav),
        ("工具链接实测",   check_tool_links),
        ("Skill 仓库复检", check_skills),
        ("重建 SKILLS.md", build_skills_md),
    ]
    failed = []
    for name, fn in STEPS:
        try:
            fn()
        except Exception:
            failed.append(name)
            print(f"\n[!] 步骤「{name}」失败，继续执行后面的步骤：")
            traceback.print_exc()
            print()
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if failed:
        print(f"\n===== {stamp} 完成 {len(STEPS)-len(failed)}/{len(STEPS)} 步，"
              f"失败：{'、'.join(failed)} =====")
    else:
        print(f"\n===== {stamp} 五步全部完成 =====")
