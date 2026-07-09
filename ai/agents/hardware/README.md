# Hardware Agents

The AI agents for the [hardware department](../../../handbook/departments/hardware/README.md). Each follows the
[standard 11-section agent spec](../agent-template.md); the full registry is in
[ai/agents/README.md](../README.md).

| Agent | Mission |
|---|---|
| [Electrical Engineer Agent](electrical-engineer-agent.md) | Design safe, reliable, manufacturable electronics. |
| [Firmware Engineer Agent](firmware-engineer-agent.md) | Build reliable, secure, updatable on-device software. |
| [Hardware Test Agent](hardware-test-agent.md) | Validate hardware against safety, reliability, and environmental requirements before it ships. |
| [Mechanical Engineer Agent](mechanical-engineer-agent.md) | Design enclosures and structures that are durable, manufacturable, and serviceable. |

**Customizing:** keep the agents you'll actually run and delete the rest - they are specs, not code. To add
one, run `python scripts/scaffold.py agent hardware <agent-name>` or copy the
[template](../agent-template.md). See [CUSTOMIZE.md](../../../CUSTOMIZE.md).
