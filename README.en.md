# Chinese AI Agent Skills Directory

An evidence-first directory of **184 Agent Skill entries from 141 source repositories**, focused on Chinese-language workflows. This repository also maintains 13 first-party Skills and 46 AI tool links.

[中文 README](README.md) · [Browsable directory](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/) · [Compatibility evidence](COMPATIBILITY.md) · [Pre-install audit](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/audit-skill/) · [Quality labels](QUALITY.md) · [Security policy](SECURITY.md)

## What is different here?

- **13 first-party Skills:** maintained in this repository instead of only linking elsewhere.
- **Reproducible compatibility evidence:** all 13 first-party Skills activated once in the tested Codex environment. Ten completed the recorded task, one correctly stopped to request required input, and two large tasks failed before passing reduced-scope retests. The original failures remain documented.
- **Review before install:** a read-only local scanner reports scripts, symlinks, network access, credential-related terms, file mutation and high-attention commands without executing the target Skill. Findings are review indicators, not a security certification.
- **Explicit boundaries:** Claude Code and Cursor task-level compatibility are still untested by this repository.
- **Daily source checks:** GitHub Actions rechecks the 141 source repositories and 46 tool links. A live link does not prove current pricing, safety, or client compatibility.
- **No paid or coordinated Stars:** contributions should improve usefulness and evidence, not manipulate popularity signals.

## Install

List the available Skills before installing:

```bash
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --list
```

Install one Skill:

```bash
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill chinese-typography
```

Installation, discovery, automatic activation, and task completion are separate claims. Client behavior varies by version, install location, and task wording. See the [installation guide](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/install/) and [compatibility matrix](COMPATIBILITY.md).

For a project-level installation that already has `skills-lock.json`, the isolated update test used:

```bash
npx --yes skills@1.5.22 update -p -y
```

All 13 controlled historical fixture folders matched the current public repository after that run, while global Skill hashes remained unchanged. This does not verify global `update -g`, lockless installs, activation, or future CLI versions; see the [full test record](cases/skills-cli-isolated-install-2026-08-13.md).

The repository is also [indexed by skills.sh](https://skills.sh/sanhuang520-ship-it/awesome-chinese-ai-tools). Its aggregated install count comes from skills CLI telemetry and may include maintainer verification runs; it is not a unique-user count, usage outcome, or quality certification.

The [Agent-Skills.md author page](https://agent-skills.md/authors/sanhuang520-ship-it) also lists all 13 first-party Skills. It is a third-party directory surface, not independent compatibility testing, content review, or quality certification; category and tag refreshes are still being verified.

### Review a Skill before installing it

Clone the target to a disposable directory, then run the repository's standard-library-only scanner:

```bash
python3 scripts/audit_skill.py /path/to/skill
python3 scripts/audit_skill.py /path/to/skill --json
```

The scanner is read-only: it does not import, install or execute the target, and it does not follow symlinks. A zero-finding result does **not** mean the Skill is safe; dynamic behavior, obfuscation, prompt injection and dependency behavior may remain undetected. See the [rules and limitations](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/audit-skill/).

### A 30-second first test

Install only one Skill, restart the client, and give it a natural task without naming the Skill. For example, after installing `chinese-typography`, ask:

```text
请检查下面这段网页 CSS 的中文排版问题，只做审查，不修改文件。明确列出问题、理由和建议值：
body { font-family: Arial, sans-serif; font-size: 14px; line-height: 1.35; text-align: justify; word-break: break-all; }
```

This task activated the Skill in the [recorded Codex test](cases/chinese-typography-codex.md). That single observation is not a guarantee for other clients, versions, or wording. Successful and failed reproductions are both welcome through the [compatibility report form](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml).

## First-party Skills

The 13 repository-maintained Skills cover Chinese typography, Chinese web themes, guochao visual direction, Chinese lesson plans, work reports, ecommerce copywriting, learning, bookkeeping, book digestion, homework tutoring, GitHub README improvement, Chinese design systems, and guofeng Three.js rendering.

See [output examples](EXAMPLES.md), [reproducible Codex cases](cases/README.md), and the full [Skill catalog](SKILLS.md).

## Contributing

- [Recommend a Skill or AI tool](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=add-entry.yml); no code change is required.
- Submit a real success, failure, or non-activation result through the [compatibility report form](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml).
- For a machine-readable pull request, generate a private local JSON report in the [browser report builder](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/report/), or copy the [validated example](examples/compatibility-result.example.json), then run `python3 scripts/check_compatibility_reports.py`.
- Report stale links or factual errors through the [problem report form](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=report-problem.yml).
- Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing catalog data.

Remove tokens, private paths, email addresses, and unpublished business data before posting logs. Automated validation does not replace manual redaction or independent reproduction. Third-party inclusion, directory indexing, clone counts and Stars are not a security audit, usage proof or endorsement.

## License

[MIT](LICENSE)
