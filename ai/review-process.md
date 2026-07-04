# AI Engineering - Review Process

AI work is reviewed on evaluation results (does it meet the quality, safety, latency, and cost bar?), grounding (is it retrieving rather than guessing?), and versioning (can we roll back?). The AI Evaluation Agent is a hard release gate.

Reviews are independent - the [Reviewer](../orchestration/reviewer.md) never assumes the author is
correct. Security-sensitive work also requires the
[Security Reviewer](../orchestration/security-reviewer.md).
