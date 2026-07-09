# Security Policy

Company OS is a documentation framework, so most "security" concerns are about the guidance it gives.
We still take reports seriously.

## Reporting a vulnerability

If you find a security issue — in this repository (e.g. a leaked secret, a malicious link, an unsafe CI
workflow) **or** unsafe advice in the guidance (e.g. a standard or playbook that could lead adopters to
an insecure practice):

1. **Do not open a public issue** for anything sensitive.
2. Use GitHub's **[private vulnerability reporting](https://github.com/rojenwai/CompanyOS/security/advisories/new)**
   (Security → Advisories → Report a vulnerability), or contact the maintainer privately.
3. Include: what you found, where (file/path), and the potential impact.

## What to expect

- Acknowledgement of your report.
- An assessment and, if valid, a fix or corrected guidance.
- Credit for the report, if you'd like it.

## Scope

- ✅ In scope: leaked credentials in the repo, unsafe CI workflows, malicious links, guidance that
  recommends insecure practices.
- ❌ Out of scope: vulnerabilities in *your own* company built with this framework — use the framework's
  own [security standards](../handbook/departments/engineering/security-standards.md) and
  [incident response](../handbook/departments/post-launch/incident-response.md) for those.

## For companies built on Company OS

Your product's security is governed by the framework itself:
[engineering/security-standards.md](../handbook/departments/engineering/security-standards.md),
[ai/ai-security.md](../handbook/departments/ai-engineering/ai-security.md), the [Security Reviewer](../ai/orchestration/security-reviewer.md),
and the [security-breach playbook](../handbook/departments/post-launch/playbooks/security-breach.md).
