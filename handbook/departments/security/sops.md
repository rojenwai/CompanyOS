# Security - Standard Operating Procedures

### SOP-01 - Run a security review

1. Confirm scope and threat model
2. Review architecture and code against standards
3. Run automated scans
4. Document findings by severity
5. Gate the release on criticals

### SOP-02 - Rotate a compromised secret

1. Revoke the exposed secret immediately
2. Issue a new secret in the vault
3. Redeploy affected services
4. Audit for misuse
5. Record the incident
