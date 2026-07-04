# Coding Standards

The baseline standards for all code. Specialized standards live in
[testing](testing-standards.md) · [security](security-standards.md) · [performance](performance-standards.md) ·
[api](api-standards.md) · [database](database-standards.md) · [documentation](documentation-requirements.md).

## Code quality

Readable code · reusable components · no duplicated logic · meaningful names · document public APIs ·
avoid premature optimization. Every public function documents its **purpose, inputs, outputs, errors,
and an example**. Complex algorithms explain **why**, not **what**.

## Naming conventions

| Kind | Example |
|---|---|
| Variables | `userCount`, `totalRevenue` |
| Classes | `PaymentProcessor`, `NotificationService` |
| Interfaces | `PaymentGateway`, `StorageProvider` |
| Constants | `MAX_UPLOAD_SIZE`, `DEFAULT_TIMEOUT` |
| Enums | `OrderStatus`, `PaymentState` |
| Booleans | `isAuthenticated`, `hasPermission`, `canRetry`, `shouldCache` |
| Functions | verb + object: `createUser()`, `calculateRisk()`, `validateEmail()` |

## File naming

Lowercase, hyphen-separated: `user-service.ts`, `payment-api.py`, `image-loader.cpp`.
Avoid: `NewFile.cpp`, `TestFINAL.py`, `myCode.js`.

## Folder rules

Folders represent **domains, not technologies**.
Good: `payments/`, `authentication/`, `notifications/`, `orders/`.
Avoid: `controllers/`, `models/`, `helpers/`, `utils/`.

## Module rules

Every module owns its API · business logic · data access · tests · documentation · configuration.

## Error handling

Never ignore exceptions. Every error contains a **message, code, context, and recovery suggestion**:

```
AUTH_001
Token expired
Re-authentication required
```

## Logging

Levels: TRACE · DEBUG · INFO · WARN · ERROR · FATAL.
**Never log:** passwords · secrets · API keys · credit cards · personal data.

## Configuration

Never hardcode URLs · secrets · credentials · keys · ports · passwords. Everything configurable
belongs in environment variables or configuration files.

## Dependency rules

Before adding a dependency, ask: Can we build it ourselves? Is it maintained and actively developed?
Is it secure? Does it increase bundle size? Does it introduce licensing issues?
