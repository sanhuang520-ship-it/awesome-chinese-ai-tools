#!/usr/bin/env python3
"""Read-only pre-install audit for one Agent Skill directory.

This scanner reports review indicators. It does not execute the target, follow
symlinks, detect every malicious behavior, or certify that a Skill is safe.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


SCRIPT_SUFFIXES = {".py", ".js", ".mjs", ".cjs", ".sh", ".bash", ".zsh", ".ps1", ".rb", ".pl"}
TEXT_SUFFIXES = SCRIPT_SUFFIXES | {".md", ".txt", ".html", ".css", ".json", ".yaml", ".yml", ".toml"}
MAX_TEXT_BYTES = 1_000_000

RULES = (
    ("high", "pipe-to-shell", re.compile(r"(?:curl|wget)\b[^\n|]{0,500}\|\s*(?:ba)?sh\b", re.I), "下载内容直接交给 shell"),
    ("high", "recursive-delete", re.compile(r"\brm\s+(?:-[A-Za-z]*r[A-Za-z]*f|-rf|-fr)\b", re.I), "递归强制删除命令"),
    ("review", "privilege", re.compile(r"(?:^|\s)sudo\s+", re.M), "提升系统权限"),
    ("review", "process-exec", re.compile(r"\b(?:subprocess\.|os\.system\s*\(|child_process|execSync\s*\(|spawnSync\s*\(|Invoke-Expression\b)"), "启动外部进程或解释命令"),
    ("review", "external-resource", re.compile(r"(?:\b(?:src|href)\s*=\s*['\"]https?://|\burl\(\s*['\"]?https?://|\b(?:import|export)\s+(?:[^;]*?\s+from\s+)?['\"]https?://|<script\b[^>]*type\s*=\s*['\"]importmap['\"][^>]*>[\s\S]*?https?://)", re.I), "加载外部运行时资源"),
    ("review", "network", re.compile(r"\b(?:fetch\s*\(|requests\.|httpx\.|urlopen\s*\(|WebSocket\s*\(|EventSource\s*\(|curl\s+|wget\s+)", re.I), "主动网络访问"),
    ("review", "credential", re.compile(r"\b(?:API[_-]?KEY|ACCESS[_-]?TOKEN|AUTH[_-]?TOKEN|PASSWORD|PRIVATE[_-]?KEY|SECRET[_-]?KEY)\b", re.I), "凭据或密钥相关字段"),
    ("review", "file-mutation", re.compile(r"\b(?:write_text|write_bytes|unlink|rmtree|Remove-Item|Set-Content|Add-Content)\b|\.open\s*\([^\n]{0,120}['\"](?:w|a|x)[bt+]*['\"]", re.I), "写入或删除文件"),
)


def iter_entries(root: Path):
    """Walk without following directory symlinks."""
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in list(dirs):
            path = current_path / name
            if path.is_symlink():
                yield path
                dirs.remove(name)
        for name in files:
            yield current_path / name


def add_finding(findings, severity, rule, path, summary, line=None):
    item = {"severity": severity, "rule": rule, "path": path, "summary": summary}
    if line is not None:
        item["line"] = line
    findings.append(item)


def parse_frontmatter(text: str):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not match:
        return {}
    result = {}
    for key in ("name", "description"):
        field = re.search(rf"^{key}:\s*['\"]?([^'\"\n]+)", match.group(1), re.M)
        if field:
            result[key] = field.group(1).strip()
    return result


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def audit(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError("目标必须是一个存在的 Skill 目录")

    findings = []
    files = []
    skipped_large = []
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        add_finding(findings, "high", "missing-skill-md", "SKILL.md", "缺少必需的 SKILL.md")
        skill_text = ""
    else:
        skill_text = skill_file.read_text(encoding="utf-8", errors="replace")
        metadata = parse_frontmatter(skill_text)
        if not metadata.get("name"):
            add_finding(findings, "review", "missing-name", "SKILL.md", "frontmatter 缺少 name")
        elif metadata["name"] != root.name:
            add_finding(findings, "review", "name-mismatch", "SKILL.md", f"name={metadata['name']} 与目录名不一致")
        if not metadata.get("description"):
            add_finding(findings, "review", "missing-description", "SKILL.md", "frontmatter 缺少 description")

        for link in re.findall(r"\[[^]]*\]\(([^)]+)\)", skill_text):
            if re.match(r"^[a-z]+://", link, re.I) or link.startswith("#"):
                continue
            target = (root / link.split("#", 1)[0]).resolve()
            if root not in (target, *target.parents):
                add_finding(findings, "high", "escaping-reference", "SKILL.md", f"本地引用越出 Skill 目录：{link}")
            elif not target.exists():
                add_finding(findings, "review", "missing-reference", "SKILL.md", f"本地引用不存在：{link}")

    for path in iter_entries(root):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            add_finding(findings, "high", "symlink", relative, "发现符号链接；扫描器未跟随目标")
            continue
        if not path.is_file():
            continue
        files.append(relative)
        if path.suffix.lower() in SCRIPT_SUFFIXES:
            add_finding(findings, "review", "executable-script", relative, "发现可执行脚本类型")
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name != "SKILL.md":
            continue
        if path.stat().st_size > MAX_TEXT_BYTES:
            skipped_large.append(relative)
            add_finding(findings, "review", "large-text-skipped", relative, "文本文件超过 1 MB，未扫描内容")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for severity, rule, pattern, summary in RULES:
            for match in pattern.finditer(text):
                add_finding(findings, severity, rule, relative, summary, line_number(text, match.start()))

    order = {"high": 0, "review": 1, "info": 2}
    findings.sort(key=lambda item: (order[item["severity"]], item["path"], item.get("line", 0), item["rule"]))
    counts = {level: sum(1 for item in findings if item["severity"] == level) for level in order}
    return {
        "scanner": "awesome-chinese-ai-tools/read-only-skill-audit-v1",
        "target": root.name,
        "scope": {
            "readOnly": True,
            "executesTarget": False,
            "followsSymlinks": False,
            "maxTextBytesPerFile": MAX_TEXT_BYTES,
        },
        "summary": {"files": len(files), **counts},
        "findings": findings,
        "limitations": [
            "结果是需要人工复核的静态线索，不是恶意代码检测或安全认证。",
            "动态拼接、混淆代码、外部依赖行为和提示注入可能无法被发现。",
            "没有发现线索不代表 Skill 安全；敏感环境仍应隔离测试并使用最小权限。",
        ],
    }


def render_text(result: dict) -> str:
    summary = result["summary"]
    lines = [
        f"只读审计：{result['target']}",
        f"文件 {summary['files']} · 高关注 {summary['high']} · 需复核 {summary['review']}",
    ]
    for item in result["findings"]:
        location = item["path"] + (f":{item['line']}" if item.get("line") else "")
        lines.append(f"[{item['severity'].upper()}] {location} · {item['summary']} ({item['rule']})")
    if not result["findings"]:
        lines.append("未发现预设规则命中的线索；这不代表安全。")
    lines.extend(["", "边界："] + [f"- {item}" for item in result["limitations"]])
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="只读扫描一个 Agent Skill 目录中的安装前复核线索")
    parser.add_argument("path", type=Path, help="包含 SKILL.md 的目录")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    args = parser.parse_args(argv)
    try:
        result = audit(args.path)
    except (OSError, ValueError) as exc:
        print(f"audit error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render_text(result))
    return 1 if result["summary"]["high"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
