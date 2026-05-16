# ZeroDaySentinel Defensive Detection Report

This report summarizes the latest synthetic defensive telemetry run and triage analytics output.

## Executive Summary

- Total synthetic events: `120`
- Total generated alerts: `25`
- Alert rate: `0.2083`
- Triage pressure score: `2.88`

The triage pressure score is a defensive prioritization metric derived from generated synthetic alert priorities. It helps reviewers quickly understand whether the latest local run produced a low, moderate, or high triage load.

## Alert Priority Distribution

| Priority | Count |
|---|---|
| critical | 22 |
| high | 3 |

## Top Observed Hosts

| Host | Alerts |
|---|---|
| build-runner-01 | 9 |
| win-endpoint-01 | 5 |
| k8s-node-03 | 5 |
| db-gateway-01 | 4 |
| linux-api-02 | 2 |

## Top Observed Users

| User | Alerts |
|---|---|
| david.ops | 6 |
| service.backup | 6 |
| bob.admin | 5 |
| alice.research | 5 |
| carol.engineering | 3 |

## Rule Hit Summary

| Rule | Hits |
|---|---|
| {'rule_id': 'ZDS-003', 'name': 'Unusual Outbound Pattern', 'description': 'Detects synthetic rare outbound communication behavior.'} | 7 |
| {'rule_id': 'ZDS-001', 'name': 'Authentication Anomaly Burst', 'description': 'Detects synthetic bursts of failed authentication behavior.'} | 4 |
| {'rule_id': 'ZDS-006', 'name': 'Abnormal API Frequency', 'description': 'Detects synthetic high-frequency API behavior.'} | 4 |
| {'rule_id': 'ZDS-004', 'name': 'Sensitive Access Pattern', 'description': 'Detects synthetic access behavior involving sensitive areas.'} | 4 |
| {'rule_id': 'ZDS-005', 'name': 'Rare Privileged Operation', 'description': 'Detects synthetic rare administrative activity.'} | 3 |
| {'rule_id': 'ZDS-002', 'name': 'Unexpected Execution Context', 'description': 'Detects synthetic process-tree behavior that deviates from normal baselines.'} | 3 |

## Recommended Defensive Actions

| Action | Count |
|---|---|
| triage_required | 25 |

## Defensive Interpretation

This report is designed for local blue-team review. It summarizes which synthetic hosts, users, event types, and rules should receive attention first during a defensive triage exercise.

## Safety Boundary

ZeroDaySentinel remains defensive, synthetic, and non-weaponized. This report is generated only from local synthetic telemetry and defensive alert metadata. It does not include exploit code, payloads, bypass techniques, persistence logic, evasion logic, unauthorized testing instructions, or internet-wide scanning tools.
