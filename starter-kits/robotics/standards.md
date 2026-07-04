# Robotics - Added Standards

These extend the core [standards](../../standards/README.md) with what this company type specifically requires.

1. Safety is a hard, non-overridable gate ([hardware safety gate](../../hardware/quality-gates.md)); safety-critical paths are fully tested.
2. Perception/control models are evaluated in simulation and hardware-in-the-loop before field deployment ([ai evaluation](../../ai/evaluation-and-testing.md)).
3. Every robot's firmware is OTA-updatable with a recovery path (never brick a unit).
4. Fleet telemetry and health monitoring are mandatory ([post-launch](../../post-launch/monitoring.md)).
