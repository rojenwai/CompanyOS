# Versioning & Version Lifecycle

## Versioning scheme

Semantic versioning: **MAJOR.MINOR.PATCH**.

- **MAJOR** — breaking changes (requires migration; coordinated with the [API Compatibility Agent](../../../ai/agents/post-launch/api-compatibility-agent.md)).
- **MINOR** — backward-compatible features.
- **PATCH** — backward-compatible fixes.

## Version lifecycle

Every version moves through:

```
Planning → Development → Testing → Release → Maintenance
→ Support Window → Security Support → Deprecation → End of Life → Archive
```

| Stage | Meaning |
|---|---|
| Maintenance | Actively fixed and improved |
| Support window | Bug fixes provided |
| Security support | Security fixes only |
| [Deprecation](deprecation-policy.md) | Announced sunset; migration guidance published |
| [End of Life](end-of-life.md) | No support; retired |
| Archive | Read-only historical record |

LTS versions get an extended support and security window. Version state is tracked so customers always
know where their version stands.
