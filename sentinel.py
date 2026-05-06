from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
GENERATOR = ROOT_DIR / "lab" / "log-generator" / "generate_logs.py"
DETECTOR = ROOT_DIR / "lab" / "detector" / "detector.py"
SUMMARY_FILE = ROOT_DIR / "reports" / "summary.json"


def run_python_script(script_path: Path) -> None:
    if not script_path.exists():
        raise FileNotFoundError(f"Required script not found: {script_path}")

    subprocess.run([sys.executable, str(script_path)], check=True)


def run_demo() -> None:
    print("[ZeroDaySentinel] Starting safe local demo...")
    run_python_script(GENERATOR)
    run_python_script(DETECTOR)
    print("[ZeroDaySentinel] Demo completed.")


def show_summary() -> None:
    if not SUMMARY_FILE.exists():
        print("[ZeroDaySentinel] No summary found. Run: python sentinel.py --demo")
        return

    with SUMMARY_FILE.open("r", encoding="utf-8") as file:
        summary = json.load(file)

    print(json.dumps(summary, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ZeroDaySentinel",
        description="Defensive zero-day readiness and synthetic telemetry lab.",
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the safe synthetic telemetry generator and defensive detector.",
    )

    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print the latest generated detection summary.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    if args.summary:
        show_summary()
        return

    parser.print_help()


if __name__ == "__main__":
    main()
