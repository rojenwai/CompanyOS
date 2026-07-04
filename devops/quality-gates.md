# DevOps - Quality Gates

Work does not progress until the relevant gate passes. These implement the company
[quality gates](../governance/quality-gates.md).

| Gate | Must pass |
|---|---|
| Pipeline gate | Tests, coverage, and security scans pass; gates non-bypassable |
| Infra gate | Change is code-reviewed and plan-approved |
| Deploy gate | Tested rollback exists; canary healthy |
| Post-deploy gate | Error rate, latency, and saturation green |
