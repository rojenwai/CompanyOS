# Code Review Checklist

For reviewers. The reviewer never assumes the author is correct.

- [ ] **Correctness** — does it do what the acceptance criteria require?
- [ ] **Readability** — could a new engineer follow it?
- [ ] **Naming** — clear, consistent with [conventions](../standards.md)?
- [ ] **Architecture** — fits [boundaries](../organization.md); no unjustified complexity?
- [ ] **Performance** — no obvious inefficiency; measured where it matters?
- [ ] **Security** — input validated, output encoded, no secrets; [standards](../security-standards.md) met?
- [ ] **Testing** — meaningful tests for happy path, edge cases, and failures?
- [ ] **Documentation** — public APIs and non-obvious *why* documented?
- [ ] **Error handling** — errors carry message, code, context, recovery?
- [ ] **Edge cases** — nulls, limits, concurrency, failure modes considered?
- [ ] **Accessibility** — for UI, keyboard/screen-reader/contrast handled?
- [ ] **Maintainability** — will this be easy to change later?
