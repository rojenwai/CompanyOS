# API Standards

REST or GraphQL, and only when justified. Owned by the [API Architect](../agents/engineering/api-architect.md).

## Every endpoint defines

- Purpose
- Method and route
- Authentication and authorization
- Validation
- Request and response schemas
- Error codes
- Rate limits
- Version
- OpenAPI documentation

## Rules

- Version explicitly; never break a published contract without a version bump and migration path.
- Validate all input; encode all output.
- Document with OpenAPI; the [Documentation Reviewer](../orchestration/documentation-reviewer.md) gates it.
- Backward compatibility is monitored post-release by the [API Compatibility Agent](../agents/post-launch/api-compatibility-agent.md).
