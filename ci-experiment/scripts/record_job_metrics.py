import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    job_name = sys.argv[1]
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    job_start = float(os.environ.get("JOB_START", time.time()))
    job_duration = round(time.time() - job_start, 2)

    metrics = {
        "job_name": job_name,
        "job_duration": job_duration,
        "test_count": 0,
        "test_failures": 0,
        "test_duration_avg": 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if job_name == "Test":
        report_path = artifacts_dir / "pytest-report.json"
        if report_path.exists():
            report = json.loads(report_path.read_text(encoding="utf-8"))
            summary = report.get("summary", {})
            tests = report.get("tests", [])
            metrics["test_count"] = summary.get("total", len(tests))
            metrics["test_failures"] = summary.get("failed", 0) + summary.get("error", 0)
            durations = [t.get("duration", 0) for t in tests if t.get("duration") is not None]
            if durations:
                metrics["test_duration_avg"] = round(sum(durations) / len(durations), 4)

    workflow_start = os.environ.get("WORKFLOW_START")
    if workflow_start and job_name == "Lint":
        start_file = artifacts_dir / "workflow-start.txt"
        start_file.write_text(workflow_start, encoding="utf-8")

    output_path = artifacts_dir / f"job-{job_name.lower()}.json"
    output_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
