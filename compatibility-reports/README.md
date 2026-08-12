# 机器可读兼容性报告

通过 Pull Request 提交的单次实测 JSON 放在本目录，文件名使用报告中的 `id`，例如：

```text
compatibility-reports/2026-08-12-codex-example.json
```

提交前复制 [`examples/compatibility-result.example.json`](../examples/compatibility-result.example.json)，并运行：

```bash
python3 scripts/check_compatibility_report.py compatibility-reports/<id>.json
python3 scripts/verify.py
```

完整字段见 [`schemas/compatibility-result.schema.json`](../schemas/compatibility-result.schema.json)。维护者会复核原始证据和隐私边界；通过结构校验不等于结果已被独立复现，也不等于跨客户端兼容认证。
