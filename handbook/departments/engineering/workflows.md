# Engineering Workflows

The repeatable processes for shipping code: repository layout, branching, commits, and pull requests.
These plug into the company [SDLC](../../workflows/sdlc.md) (development phases 12–17).

## Repository structure

```
project/
├── docs/            ├── architecture/   ├── research/     ├── product/
├── apps/            ├── services/        ├── packages/     ├── firmware/
├── hardware/        ├── ai/              ├── models/       ├── datasets/
├── infrastructure/  ├── deployment/      ├── tests/        ├── benchmarks/
├── scripts/         ├── tools/           ├── assets/       ├── examples/
├── configs/         ├── monitoring/      ├── security/     ├── .github/
├── README.md        ├── CHANGELOG.md     ├── LICENSE       └── CLAUDE.md
```

## Branch strategy

| Purpose | Branch |
|---|---|
| Protected | `main` |
| Development | `develop` |
| Features | `feature/user-auth`, `feature/payment` |
| Bug fixes | `bugfix/login`, `bugfix/cache` |
| Releases | `release/v2.1` |
| Hotfix | `hotfix/security` |

**No direct commits to `main`.**

## Git commit convention

Conventional Commits: `feat:` `fix:` `docs:` `style:` `refactor:` `perf:` `test:` `build:` `ci:` `chore:` `revert:`

```
feat(auth): implement OAuth2 login
fix(api): resolve token expiration
refactor(database): normalize schema
perf(search): reduce query latency
docs(api): update OpenAPI specification
```

## Pull request rules

Every PR includes: Summary · Problem · Solution · Testing · Screenshots (if UI) · Performance Impact ·
Security Impact · Breaking Changes · Checklist.

- Minimum reviewers: **2**
- Critical infrastructure: **3**

Review is governed by [review-process.md](review-process.md). PRs must pass the
[quality gates](quality-gates.md) before merge.

## Development rules

Small commits · descriptive messages · feature branches · code review required · no direct commits
to `main` · every feature includes tests. A task may only start once it meets the
[Definition of Ready](definition-of-ready.md) and is done only when it meets the
[Definition of Done](quality-gates.md).
