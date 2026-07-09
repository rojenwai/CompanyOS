# Example - Threat Model (excerpt)

> Worked example - illustrative, not a live record.

**System:** Public file-upload endpoint.

| Threat (STRIDE) | Vector | Risk | Control |
|---|---|---|---|
| Tampering | Malicious file content | High | Type/size validation, sandboxed scanning |
| Info disclosure | Path traversal in filename | High | Server-generated names, no user paths |
| DoS | Large/zip-bomb uploads | Medium | Size limits, rate limits, async processing |
| Elevation | Executable upload + serve | Critical | Store off-web-root, never execute, content-type pinning |

**Decision:** Critical and high controls are release-blocking; the endpoint ships only once all are implemented and tested.
