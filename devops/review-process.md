# DevOps - Review Process

DevOps changes are reviewed as code (peer review on IaC and pipelines), with special attention to gate integrity (can quality/security checks be bypassed?) and reversibility (is there a tested rollback?). Security reviews infrastructure hardening.

Reviews are independent - the [Reviewer](../orchestration/reviewer.md) never assumes the author is
correct. Security-sensitive work also requires the
[Security Reviewer](../orchestration/security-reviewer.md).
