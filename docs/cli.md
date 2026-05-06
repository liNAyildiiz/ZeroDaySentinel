# ZeroDaySentinel CLI

ZeroDaySentinel includes a small command-line entry point for running the safe local demo.

## Run the Demo

From the repository root:

```powershell
python sentinel.py --demo
```

This command runs:

1. `lab/log-generator/generate_logs.py`
2. `lab/detector/detector.py`

## Show Summary

After running the demo:

```powershell
python sentinel.py --summary
```

## Safety

The CLI does not run exploit code, payloads, bypasses, persistence logic, evasion logic, or unauthorized testing logic. It only executes the synthetic telemetry generator and defensive detector.
