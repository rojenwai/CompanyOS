# DevOps - Playbooks

Situational guides. Each names the trigger and the steps.

### A deploy breaks production

1. Apply the [broken-deployment playbook](../post-launch/playbooks/broken-deployment.md)
2. Roll back to last-good
3. Verify recovery
4. Diagnose in a safe environment
5. Fix forward with a test

### Cloud cost spikes

1. Apply the [high-cloud-cost playbook](../post-launch/playbooks/high-cloud-cost.md)
2. Identify the driver
3. Right-size or cap
4. Verify savings
5. Add a cost alert
