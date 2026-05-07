# Incident Response Playbook Mapping

This document maps ZeroDaySentinel synthetic detection rules to safe defensive response actions.

## Mapping Table

| Rule ID | Rule Name | Response ID | First Defensive Action |
|---|---|---|---|
| ZDS-001 | Authentication Anomaly Burst | IR-AUTH-001 | Review identity logs, account context, and recent access patterns. |
| ZDS-002 | Unexpected Execution Context | IR-ENDPOINT-001 | Review process lineage, host role, and endpoint telemetry. |
| ZDS-003 | Unusual Outbound Pattern | IR-NETWORK-001 | Review network destination rarity, source host, and communication frequency. |
| ZDS-004 | Sensitive Access Pattern | IR-DATA-001 | Review access authorization, resource sensitivity, and user role. |
| ZDS-005 | Rare Privileged Operation | IR-PRIV-001 | Review privileged activity approval, administrator context, and change records. |
| ZDS-006 | Abnormal API Frequency | IR-APP-001 | Review request volume, endpoint usage, and application behavior baseline. |

## Defensive Workflow

1. Confirm the alert source.
2. Review the matched rule and risk score.
3. Check whether the behavior is expected for the user, host, and service.
4. Correlate with nearby synthetic telemetry.
5. Assign a response owner.
6. Document the triage outcome.
7. Close as expected activity or escalate for deeper defensive review.

## Safety Boundary

This playbook does not provide exploitation steps, bypass guidance, persistence methods, evasion methods, or unauthorized testing procedures. It is limited to defensive triage and response planning.
