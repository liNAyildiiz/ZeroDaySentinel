# Detection Rules

This directory contains defensive detection engineering material for ZeroDaySentinel.

## Current Rule Catalog

The current catalog is stored in:

- `detection/rules/catalog.json`

The catalog includes synthetic defensive rules for:

- authentication anomaly bursts,
- unexpected execution context,
- unusual outbound patterns,
- sensitive access patterns,
- rare privileged operations,
- abnormal API frequency.

## Safety Boundary

The rules are defensive and synthetic. They do not include exploit code, payloads, bypass techniques, persistence logic, evasion logic, or unauthorized testing instructions.

## Intended Use

The catalog is intended for:

- defensive detection engineering practice,
- blue-team learning,
- alert triage modeling,
- incident response mapping,
- safe zero-day readiness simulation.
