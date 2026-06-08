import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> None:
    artifacts_dir = Path("artifacts")
    merged_dir = Path("merged")
    merged_dir.mkdir(exist_ok=True)

    run_id = os.environ.get("GITHUB_RUN_ID", "local")
    commit_sha = os.environ.get("GITHUB_SHA", "local")[:7]
    commit_message = os.environ.get("COMMIT_MESSAGE", "local run")
    workflow_status = os.environ.get("WORKFLOW_STATUS", "success")

    workflow_start = None
    start_file = artifacts_dir / "workflow-start.txt"
    if start_file.exists():
        workflow_start = parse_iso(start_file.read_text(encoding="utf-8").strip())

    workflow_end = datetime.now(timezone.utc)
    workflow_duration = 0.0
    if workflow_start:
        workflow_duration = round((workflow_end - workflow_start).total_seconds(), 2)

    rows = []
    job_files = sorted(artifacts_dir.glob("job-*.json"))

    for job_file in job_files:
        job_data = json.loads(job_file.read_text(encoding="utf-8"))
        rows.append(
            {
                "run_id": run_id,
                "commit_sha": commit_sha,
                "commit_message": commit_message,
                "status": workflow_status,
                "workflow_duration": workflow_duration,
                "job_name": job_data["job_name"],
                "job_duration": job_data["job_duration"],
                "test_count": job_data["test_count"],
                "test_failures": job_data["test_failures"],
                "test_duration_avg": job_data["test_duration_avg"],
                "timestamp": job_data["timestamp"],
            }
        )

    json_path = merged_dir / "pipeline-metrics.json"
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    fieldnames = [
        "run_id",
        "commit_sha",
        "commit_message",
        "status",
        "workflow_duration",
        "job_name",
        "job_duration",
        "test_count",
        "test_failures",
        "test_duration_avg",
        "timestamp",
    ]

    csv_path = merged_dir / "pipeline-metrics.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summary_path = merged_dir / "summary.txt"
    summary_lines = [
        f"run_id={run_id}",
        f"commit_sha={commit_sha}",
        f"commit_message={commit_message}",
        f"status={workflow_status}",
        f"workflow_duration={workflow_duration}s",
        f"jobs={len(rows)}",
    ]
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
