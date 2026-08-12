# Chinese AI Agent Skills Directory

An evidence-first directory of **184 Agent Skill entries from 141 source repositories**, focused on Chinese-language workflows. This repository also maintains 13 first-party Skills and 46 AI tool links.

[中文 README](README.md) · [Browsable directory](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/) · [Compatibility evidence](COMPATIBILITY.md) · [Quality labels](QUALITY.md) · [Security policy](SECURITY.md)

## What is different here?

- **13 first-party Skills:** maintained in this repository instead of only linking elsewhere.
- **Reproducible compatibility evidence:** all 13 first-party Skills activated once in the tested Codex environment. Eleven completed on the first task; two large tasks failed and later passed reduced-scope retests. The original failures remain documented.
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

The repository is also [indexed by skills.sh](https://skills.sh/sanhuang520-ship-it/awesome-chinese-ai-tools). Its aggregated install count comes from skills CLI telemetry and may include maintainer verification runs; it is not a unique-user count, usage outcome, or quality certification.

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
- Report stale links or factual errors through the [problem report form](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=report-problem.yml).
- Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing catalog data.

Remove tokens, private paths, email addresses, and unpublished business data before posting logs. Third-party inclusion is not a security audit or endorsement.

## License

[MIT](LICENSE)
