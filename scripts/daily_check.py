#!/usr/bin/env python3
"""Maintain verifiable repository data: link health, Skill status and generated indexes."""

import json
import re
import base64
import urllib.request
import urllib.error
import datetime
import os
import ssl
try:
    import certifi
    _CAFILE = certifi.where()
except ImportError:
    _CAFILE = None
import time

from check_catalog_claims import find_claim_violations
from sync_public_metadata import CAT_ORDER, sync_public_metadata
from check_internal_links import ROOT as SITE_ROOT, missing_links, published_pages
from render_static_catalog import render_catalog
from generate_social_preview import build_preview_stats, render_svg

# ── 配置 ──────────────────────────────────────────────────
# token 从环境变量读取。GitHub Actions 里用自带的 GITHUB_TOKEN，无需配置密钥；
# 本地跑： export GITHUB_TOKEN=xxx && python3 scripts/daily_check.py
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
if not GITHUB_TOKEN:
    raise SystemExit("缺少环境变量 GITHUB_TOKEN")
REPO     = os.environ.get("GITHUB_REPOSITORY", "sanhuang520-ship-it/awesome-chinese-ai-tools")
API_BASE = "https://api.github.com"
# ──────────────────────────────────────────────────────────

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


def should_persist_tool_check(changed, previous_checked_at, today_str):
    """状态变化或新检测日期尚未落盘时，必须持久化结果。"""
    return changed > 0 or previous_checked_at != today_str


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
        raise RuntimeError("[链接检测] 无法读取 data/tools.json")

    raw = base64.b64decode(existing["content"]).decode("utf-8")
    data = json.loads(raw)
    sha  = existing["sha"]
    tools = data.get("tools", [])
    previous_checked_at = data.get("meta", {}).get("linkCheckedAt")

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

    # 4. 状态有变化，或当天检测日期尚未落盘时写回 GitHub。
    # 不能只看状态变化：否则每天确实执行了请求，但公开证据日期会永久停在旧值。
    date_changed = previous_checked_at != today_str
    if not should_persist_tool_check(changed, previous_checked_at, today_str):
        print(f"[链接检测] 状态和检测日期均无变化，跳过写入")
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
        detail = '; '.join(summary) or ("状态无变化，已记录当天检测日期" if date_changed else "全部正常")
        print(f"[链接检测] ✅ 已更新 tools.json — {detail}")
    else:
        raise RuntimeError(f"[链接检测] 写入失败: {result.get('message', result)}")

    # 把新发现的失效写入动态时间线
    prepend_updates(tl_events)



# ── Skill 健康复检 ─────────────────────────────────────────
def github_repo_name(url):
    """从 GitHub URL 提取 owner/repo；子目录链接仍归到同一个来源仓库。"""
    m = re.match(r"https://github\.com/([^/]+)/([^/#?]+)", url or "")
    if not m:
        return None
    return f"{m.group(1)}/{m.group(2).removesuffix('.git')}"


def unique_skill_repositories(skills):
    return {repo.lower() for item in skills if (repo := github_repo_name(item.get("url", "")))}


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
        raise RuntimeError("[Skill 复检] 无法读取 skills.json")
    data = json.loads(base64.b64decode(info["content"]).decode("utf-8"))
    sha = info["sha"]

    skills = data.get("skills", [])
    repo_results = {}
    for s in skills:
        if s.get("ours"):
            continue
        full = github_repo_name(s.get("url", ""))
        if full and full.lower() not in repo_results:
            repo_results[full.lower()] = github_api("GET", f"/repos/{full}")
            time.sleep(0.05)

    dead, alive, star_moved, changed = [], 0, 0, 0
    for s in skills:
        if s.get("ours"):
            s["skillOk"] = True
            s["skillCheckedAt"] = today_str
            continue
        full = github_repo_name(s.get("url", ""))
        if not full:
            continue
        r = repo_results[full.lower()]
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

    data["skillsCheckedAt"] = today_str
    claim_violations = find_claim_violations(data)
    if claim_violations:
        raise RuntimeError("[Skill 复检] 目录声明门槛未通过，拒绝写回：\n           "
                           + "\n           ".join(claim_violations))
    result = github_api("PUT", f"/repos/{REPO}/contents/{path}", {
        "message": f"chore: {today_str} skill 复检 — {len(dead)} 失效 / {star_moved} 个星数更新",
        "content": base64.b64encode(
            json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")).decode("ascii"),
        "sha": sha,
        "committer": {"name": "sanhuang520-ship-it", "email": "noreply@github.com"},
    })
    ok = "content" in result
    total_repos = len(unique_skill_repositories(skills))
    print(f"[Skill 复检] {'✅' if ok else '❌'} 来源仓库 {total_repos} | 存活条目 {alive + sum(bool(s.get('ours')) for s in skills)} | 失效条目 {len(dead)} | 星数更新 {star_moved}")
    if dead:
        print(f"           失效：{', '.join(dead)}")
        prepend_updates([{
            "date": today_str, "type": "alert",
            "title": f"{len(dead)} 个 Skill 仓库已失效",
            "desc": "、".join(dead[:3]) + ("…" if len(dead) > 3 else "") + " —— 已在站内标记",
        }])



# ── SKILLS.md 自动生成 ─────────────────────────────────────
def catalog_quality_label(quality):
    scripts = "发现独立可执行脚本，安装前需人工复核" if quality.get("executableScripts") else "无独立可执行脚本"
    network = quality.get("networkDetailZh") if quality.get("runtimeNetwork") else "未发现运行时联网"
    boundary = quality.get("sensitiveBoundaryZh") or "未标记敏感决策边界，仍需核对输出"
    return f"{quality['filesZh']}；{scripts}；{network}；**边界：**{boundary}"


def build_skills_md():
    """
    从 data/skills.json 重新生成 SKILLS.md。
    手写会过时（曾出现清单写 114 个、实际 116 个），改为每天自动重建。
    """
    info = github_api("GET", f"/repos/{REPO}/contents/data/skills.json")
    if "content" not in info:
        raise RuntimeError("[SKILLS.md] 读不到 skills.json")
    d = json.loads(base64.b64decode(info["content"]).decode("utf-8"))
    quality_info = github_api("GET", f"/repos/{REPO}/contents/data/quality.json")
    if "content" not in quality_info:
        raise RuntimeError("[SKILLS.md] 读不到 quality.json，拒绝生成以免丢失安装前标签")
    quality_data = json.loads(base64.b64decode(quality_info["content"]).decode("utf-8"))
    S = d.get("skills", [])
    claim_violations = find_claim_violations(d)
    if claim_violations:
        raise RuntimeError("[SKILLS.md] 目录声明门槛未通过，跳过生成：\n            "
                           + "\n            ".join(claim_violations))
    cats = d.get("categories", {})
    checked = d.get("skillsCheckedAt", "—")

    ours = [s for s in S if s.get("ours")]
    qualities = quality_data.get("skills", {})
    if {s["name"] for s in ours} != set(qualities):
        only_ours = {s["name"] for s in ours} - set(qualities)
        only_tags = set(qualities) - {s["name"] for s in ours}
        raise RuntimeError(
            "[SKILLS.md] 原创 Skill 与质量标签范围不一致，"
            "data/quality.json 需与 skills.json 里 ours=true 的条目一一对应；"
            f"缺标签={sorted(only_ours)} 多余标签={sorted(only_tags)}")
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
    L.append(f"> **{len(S)} 个 Skill 条目｜{cn_n} 个中文条目｜✍️ {len(ours)} 个本站原创**<br>")
    L.append("> 来源仓库经 GitHub API 核验真实存在；第三方说明来自上游资料或维护者摘要，不等于逐项功能实测<br>")
    L.append(f"> 🔄 最近自动复检：**{checked}**（复检仓库是否还在、星数是否变化；超半年没更新的标 🕰）\n")
    L.append("🧪 **[Codex 13/13 自动触发实测 → COMPATIBILITY.md](COMPATIBILITY.md)**　"
             "🧰 [4 组开箱组合](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/bundles/)　"
             "📋 [原创 Skill 输出示例](EXAMPLES.md)　"
             "🔎 [按场景找 Skill](#skill-catalog)　"
             "🌐 [在线浏览（可搜索/筛选）](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)\n")
    L.append("🛡️ **[安装第三方 Skill 前：运行只读本地审计器](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/audit-skill/)**"
             "（检查脚本、联网、凭据词与高风险命令；不执行目标，0 项命中不等于安全）\n")
    L.append("> 兼容性边界：当前只有 Codex 的任务级实测；Claude Code 与 Cursor 待测。"
             "成功、失败或未触发均可通过[结构化表单提交](https://github.com/"
             f"{REPO}/issues/new?template=compatibility-result.yml)。\n")
    L.append("---\n")
    L.append("## 什么是 Skills\n")
    L.append("**一句话：Skills 是给 AI 助手加的「专业技能包」。**\n")
    L.append("一个文件夹 + 一份 `SKILL.md` 说明书，告诉 AI 什么时候该用、按什么步骤做。"
             "支持 Skills 的客户端可以按任务自动激活；是否触发取决于客户端、版本、安装位置和任务措辞，需分别实测。\n")
    L.append("| | 是什么 | 解决什么 |")
    L.append("|---|--------|---------|")
    L.append("| **Skills** | 一份工作说明书（Markdown + 可选脚本） | 教 AI **怎么做**某类任务 |")
    L.append("| **MCP** | 一个后台服务 | 让 AI **连上**外部系统（数据库、浏览器） |")
    L.append("| **插件** | 打包分发的组合 | 把 skills + MCP 打包一键装 |\n")
    L.append("---\n")
    L.append("## 怎么安装\n")
    L.append("```bash")
    L.append(f"npx skills add https://github.com/{REPO} --list          # 先看有哪些")
    L.append(f"npx skills add https://github.com/{REPO} --skill guochao-visual-cn -g   # -g = 全局安装")
    L.append(f"npx skills add https://github.com/{REPO} --skill '*' -g          # 全部")
    L.append("```\n")
    L.append("> ⚠️ **实测提醒（CLI 1.5.23，2026-08-19 复测）**：`npx skills add` **默认是项目级**，")
    L.append("> 把文件装进**你当前所在的目录**（`./.agents/skills/`），不是家目录；")
    L.append("> 加 `-g` 才装到用户级的 `~/.agents/skills/`。CLI 帮助原文：")
    L.append("> `-g, --global  Install skill globally (user-level) instead of project-level`。")
    L.append("> 两种情况都会在同级的 `.claude/skills/` 建符号链接，所以两处能看到同一份文件；")
    L.append("> 这只证明安装结果，本轮尚未运行 Claude Code。")
    L.append("> 而部分教程（包括 7 万星仓库）写的 `~/.config/claude-code/skills/`，本机实测**并不存在**。\n")
    L.append("> 📌 本页此前写的是「装到 `~/.agents/skills/`」，不准确——当初那次实测在家目录下跑，")
    L.append("> 把「当前目录恰好是家目录」当成了工具行为。2026-08-19 换目录交叉验证后更正。\n")
    L.append("装好后重启你使用的客户端，用一个**不点名 Skill 名称**的自然任务测试是否自动触发。不同客户端与版本的行为可能不同；当前只有 Codex 的任务级实测。"
             "遇到问题先看[安装与排错页](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/install/)。\n")
    L.append("安装第三方 Skill 前，可先运行 `python3 scripts/audit_skill.py /path/to/skill` 做只读静态扫描；"
             "它只提供人工复核线索，不是恶意代码检测或安全认证。\n")
    L.append("### 30 秒选一个真实任务\n")
    L.append("只装当前需要的一项，重启客户端，再复制自然任务。任务中不点名 Skill，才能观察客户端是否会主动选择它。\n")
    L.append("| 需求 | 安装 | 复制给 AI | 本仓库记录 |")
    L.append("|---|---|---|---|")
    L.append(f"| 审查中文网页排版 | `npx skills add https://github.com/{REPO} --skill chinese-typography -g` | `请检查这段 CSS 的中文字体、行高、断词和两端对齐问题，只审查，不修改文件。` | [Codex 单任务实测](cases/chinese-typography-codex.md) |")
    L.append(f"| 整理不编数据的周报 | `npx skills add https://github.com/{REPO} --skill chinese-work-report -g` | `把这些工作素材整理成给老板看的周报；结果数据没有提供，不要编造。` | [Codex 单任务实测](cases/chinese-work-report-codex.md) |")
    L.append(f"| 校对商品文案事实边界 | `npx skills add https://github.com/{REPO} --skill ecommerce-copywriting -g` | `根据已知参数整理可写、待补和不应发布的信息；没有的参数、认证和功效不要编。` | [Codex 单任务实测](cases/ecommerce-copywriting-codex.md) |")
    L.append(f"| 制定能动手练习的学习计划 | `npx skills add https://github.com/{REPO} --skill ai-learning-coach -g` | `我想两周入门 SQL。先了解目标和基础，再制定有练习、输出和复盘的计划。` | [Codex 校准实测](cases/ai-learning-coach-codex.md) |\n")
    L.append("**[→ 查看全部 13 个单项安装命令与可复制首次任务](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/try-agent-skills/)**：7 条历史逐字原文与 6 条前瞻任务严格分开；前瞻任务 6 条均已执行。\n")
    L.append("这些链接只记录一次特定 Codex 版本与任务的结果，不保证其他客户端、版本或措辞得到相同结果。\n")
    L.append("---\n")
    L.append('<a id="skill-catalog"></a>')
    L.append("## Skill 清单\n")
    L.append("### 按场景直达\n")
    L.append("| 场景 | 条目数 | 跳转 |")
    L.append("|---|---:|---|")
    L.append(f"| ✍️ 本站原创 | {len(ours)} | [查看](#catalog-original) |")
    for c in CAT_ORDER:
        grp = [s for s in rest if s.get("cat") == c]
        if not grp:
            continue
        label = "🇨🇳 其他中文条目" if c == "cn" else cats.get(c, {}).get("label", c)
        L.append(f"| {label} | {len(grp)} | [查看](#catalog-{c}) |")
    L.append("")

    # 本站原创单列在最前
    if ours:
        L.append('<a id="catalog-original"></a>')
        L.append(f"### ✍️ 本站原创（{len(ours)} 个）\n")
        L.append("> 我们自己编写维护，每个都写明「不做什么」。以下是安装前静态检查标签，不是安全认证；完整方法见 [QUALITY.md](QUALITY.md)。\n")
        L.append("| Skill | 做什么 | 安装前标签 |")
        L.append("|-------|--------|------------|")
        for s in sorted(ours, key=lambda x: x["name"]):
            quality = qualities[s["name"]]
            page = f"https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/{s['explainer']}"
            L.append(
                f"| [{s['name']}]({page}) · [源码]({s['url']}) | {s.get('desc','')} | "
                f"{catalog_quality_label(quality)} |"
            )
        L.append("")

    for c in CAT_ORDER:
        grp = [s for s in rest if s.get("cat") == c]
        if not grp:
            continue
        label = "🇨🇳 其他中文条目" if c == "cn" else cats.get(c, {}).get("label", c)
        L.append(f'<a id="catalog-{c}"></a>')
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
    L.append(f"*本文件由脚本从 `data/skills.json` 自动生成，最后更新 {datetime.date.today()}。*")
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


def _repo_json_text(path):
    """按路径取仓库里的文本内容，取不到就抛错（不静默跳过）。"""
    info = github_api("GET", f"/repos/{REPO}/contents/{path}")
    if "content" not in info:
        raise RuntimeError(f"读不到 {path}：{info.get('message', info)}")
    return base64.b64decode(info["content"]).decode("utf-8")


def sync_static_catalog():
    """
    从 data/skills.json 重渲染 catalog/index.html（无 JS 版可爬取目录）。

    render_static_catalog.py 本身设计成本地文件 + git commit 跑；
    这里改用同一套 github_api 读写，跟 build_skills_md 保持一个模式，
    避免"数据改了、这个静态页没人跟着更新"再发生一次（08-13 已经踩过）。
    """
    info = github_api("GET", f"/repos/{REPO}/contents/data/skills.json")
    if "content" not in info:
        raise RuntimeError("[catalog] 读不到 skills.json")
    data = json.loads(base64.b64decode(info["content"]).decode("utf-8"))

    claim_violations = find_claim_violations(data)
    if claim_violations:
        raise RuntimeError("[catalog] 目录声明门槛未通过，跳过生成：\n           "
                           + "\n           ".join(claim_violations))

    rendered = render_catalog(data)

    path = "catalog/index.html"
    cur = github_api("GET", f"/repos/{REPO}/contents/{path}")
    current = base64.b64decode(cur["content"]).decode("utf-8") if "content" in cur else ""
    if current == rendered:
        print(f"[catalog] 无变化，跳过写入")
        return

    res = github_api("PUT", f"/repos/{REPO}/contents/{path}", {
        "message": f"chore: 自动重渲染 catalog/index.html — {len(data.get('skills', []))} 个 skill",
        "content": base64.b64encode(rendered.encode("utf-8")).decode("ascii"),
        "sha": cur.get("sha"),
        "committer": {"name": "sanhuang520-ship-it", "email": "noreply@github.com"},
    })
    if "content" not in res:
        raise RuntimeError(f"[catalog] 写入失败: {res.get('message', res)}")
    print(f"[catalog] ✅ 已重渲染 — {len(data.get('skills', []))} 个 skill")

def sync_social_preview():
    """
    从数据重渲染 og.svg（社交预览图）。

    generate_social_preview.py 原本只能本地跑 + git commit，不在这套 API 流程里，
    结果每次增删 Skill 都要人工记得跑一遍 `--write --png`，08-14 和 08-17 各漏过一次，
    靠 Tests CI 事后报红才发现。这里用跟 build_skills_md / sync_static_catalog
    完全一样的「读 → 比对 → 有变化才写」接进 STEPS。

    ⚠️ 只同步 og.svg。og.png 需要 rsvg-convert 二进制，runner 上默认没有，
    仍需本地跑 `python3 scripts/generate_social_preview.py --write --png` 后提交。
    """
    catalog = json.loads(_repo_json_text("data/skills.json"))
    tools = json.loads(_repo_json_text("data/tools.json"))
    compatibility = json.loads(_repo_json_text("data/compatibility.json"))

    rendered = render_svg(build_preview_stats(catalog, tools, compatibility))

    path = "og.svg"
    cur = github_api("GET", f"/repos/{REPO}/contents/{path}")
    current = base64.b64decode(cur["content"]).decode("utf-8") if "content" in cur else ""
    if current == rendered:
        print("[og.svg] 无变化，跳过写入")
        return

    res = github_api("PUT", f"/repos/{REPO}/contents/{path}", {
        "message": f"chore: 自动重渲染 og.svg — {len(catalog.get('skills', []))} 个 skill",
        "content": base64.b64encode(rendered.encode("utf-8")).decode("ascii"),
        "sha": cur.get("sha"),
        "committer": {"name": "sanhuang520-ship-it", "email": "noreply@github.com"},
    })
    if "content" not in res:
        raise RuntimeError(f"[og.svg] 写入失败: {res.get('message', res)}")
    print("[og.svg] ✅ 已重渲染（og.png 仍需本地生成）")

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
        raise RuntimeError("[信源导航] 找不到 SOURCES.md")
    body = base64.b64decode(info["content"]).decode("utf-8")

    # 已知误报：这些域名从 runner 访问会失败，但站点本身是好的 —— 都手动 curl 复核过，
    # 别让它们天天误报。加新条目前必须先本机复核，不要凭超时就往这里加。
    #
    # ai.meta.com    整个域名从本机网络返回 400（含首页），IP/地区层拦截
    # www.zhipuai.cn 2026-08-20 runner 报 timeout，但本机两种 UA 实测均 HTTP 200，
    #                DNS 解析到 kunluncan CDN（223.95.60.x）——国内 CDN 对海外 IP 的
    #                常见表现，不是站点失效
    SKIP = ("ai.meta.com", "zhipuai.cn")

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
    if "content" not in res:
        raise RuntimeError(f"[信源导航] 写回失败: {res.get('message', res)}")
    print("[信源导航] ✅ 已更新核对日期")


if __name__ == "__main__":
    # 每步独立 try/except —— 任何一步失败都不影响后面的步骤。
    # （2026-08-09 之前是串行调用，check_tool_links 一次 SSL 抖动就让当天
    #   的 skill 复检和 SKILLS.md 重建全部没跑。）
    import traceback

    def check_published_links():
        failures = missing_links(SITE_ROOT)
        if failures:
            raise RuntimeError("站内断链：" + "；".join(failures))
        print(f"[站内链接] ✅ {len(published_pages(SITE_ROOT))} 个 HTML 页面")

    STEPS = [
        ("站内链接体检",   check_published_links),
        ("核对官方信源",   check_source_nav),
        ("工具链接实测",   check_tool_links),
        ("Skill 仓库复检", check_skills),
        ("重建 SKILLS.md", build_skills_md),
        ("重渲染目录页", sync_static_catalog),
        ("重渲染社交预览图", sync_social_preview),
        ("同步公开统计", lambda: sync_public_metadata(github_api, REPO)),
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
        # 必须非零退出：README 对外承诺「运行记录公开可查」，
        # 绿勾就得真的代表六步都写回了，不能让静默跳过冒充成功。
        raise SystemExit(1)
    else:
        print(f"\n===== {stamp} {len(STEPS)} 步全部完成 =====")
