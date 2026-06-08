import csv
import io
import json
import os
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests

OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", "yasminminario")
REPO = os.environ.get("GITHUB_REPOSITORY_NAME", "estudos")
WORKFLOW_FILE = "ci.yml"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API_BASE = "https://api.github.com"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "dados"
FIELDNAMES = [
    "run_id",
    "commit_sha",
    "commit_message",
    "variation",
    "status",
    "workflow_duration",
    "job_name",
    "job_duration",
    "test_count",
    "test_failures",
    "test_duration_avg",
    "timestamp",
]


def api_headers() -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers


def api_get(url: str) -> dict | list:
    response = requests.get(url, headers=api_headers(), timeout=60)
    response.raise_for_status()
    return response.json()


def parse_variation(message: str) -> str:
    match = re.search(r"experiment\(\d+\): ([^\n]+)", message)
    if match:
        slug = match.group(1).strip().lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
        return slug[:40]
    if "baseline" in message.lower():
        return "01-baseline-passing"
    if "artefatos" in message.lower():
        return "setup-metrics"
    if "workflow" in message.lower():
        return "setup-workflow"
    return "unknown"


def duration_seconds(start: str, end: str) -> float:
    start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
    return round((end_dt - start_dt).total_seconds(), 2)


def fetch_workflow_runs() -> list:
    url = f"{API_BASE}/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/runs?per_page=30"
    payload = api_get(url)
    return payload.get("workflow_runs", [])


def fetch_jobs(run_id: int) -> list:
    url = f"{API_BASE}/repos/{OWNER}/{REPO}/actions/runs/{run_id}/jobs?per_page=20"
    payload = api_get(url)
    return payload.get("jobs", [])


def fetch_artifact_rows(run_id: int) -> list[dict]:
    url = f"{API_BASE}/repos/{OWNER}/{REPO}/actions/runs/{run_id}/artifacts?per_page=10"
    payload = api_get(url)
    artifacts = payload.get("artifacts", [])
    target = next((item for item in artifacts if item["name"] == "pipeline-results"), None)
    if not target:
        return []

    download_url = f"{API_BASE}/repos/{OWNER}/{REPO}/actions/artifacts/{target['id']}/zip"
    response = requests.get(download_url, headers=api_headers(), timeout=120)
    response.raise_for_status()

    rows = []
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        for name in archive.namelist():
            if name.endswith("pipeline-metrics.csv"):
                content = archive.read(name).decode("utf-8")
                reader = csv.DictReader(io.StringIO(content))
                rows.extend(list(reader))
    return rows


def build_rows_from_api() -> list[dict]:
    rows = []
    runs = fetch_workflow_runs()

    for run in runs:
        run_id = str(run["id"])
        commit_sha = run["head_sha"][:7]
        commit_message = run["head_commit"]["message"].splitlines()[0]
        variation = parse_variation(commit_message)
        status = run["conclusion"] or run["status"]
        workflow_duration = duration_seconds(run["run_started_at"], run["updated_at"])

        artifact_rows = []
        if TOKEN:
            try:
                artifact_rows = fetch_artifact_rows(run["id"])
            except requests.RequestException:
                artifact_rows = []

        if artifact_rows:
            rows.extend(artifact_rows)
            continue

        jobs = fetch_jobs(run["id"])
        for job in jobs:
            if job["name"] == "Collect Metrics":
                continue
            rows.append(
                {
                    "run_id": run_id,
                    "commit_sha": commit_sha,
                    "commit_message": commit_message,
                    "variation": variation,
                    "status": status,
                    "workflow_duration": workflow_duration,
                    "job_name": job["name"],
                    "job_duration": duration_seconds(job["started_at"], job["completed_at"])
                    if job.get("started_at") and job.get("completed_at")
                    else 0.0,
                    "test_count": 0,
                    "test_failures": 0,
                    "test_duration_avg": 0.0,
                    "timestamp": job.get("completed_at", datetime.now(timezone.utc).isoformat()),
                }
            )

    return rows


def write_outputs(rows: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / "metricas.csv"
    json_path = OUTPUT_DIR / "metricas.json"

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDNAMES})

    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"CSV salvo em: {csv_path}")
    print(f"JSON salvo em: {json_path}")
    print(f"Total de linhas: {len(rows)}")


def load_local_seed() -> list[dict]:
    seed_path = OUTPUT_DIR / "metricas.csv"
    if not seed_path.exists():
        return []
    with seed_path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def merge_rows(api_rows: list[dict], seed_rows: list[dict]) -> list[dict]:
    merged = {}
    for row in seed_rows + api_rows:
        key = (row.get("run_id"), row.get("job_name"))
        if row.get("test_count") not in ("", "0", 0, None) or key not in merged:
            merged[key] = row
    return sorted(merged.values(), key=lambda item: (item.get("run_id", ""), item.get("job_name", "")))


def main() -> None:
    seed_rows = load_local_seed()
    if not TOKEN:
        print("GITHUB_TOKEN nao definido. Mantendo dados locais existentes.")
        if seed_rows:
            write_outputs(seed_rows)
        return

    api_rows = build_rows_from_api()
    rows = merge_rows(api_rows, seed_rows) if seed_rows else api_rows
    write_outputs(rows)


if __name__ == "__main__":
    main()
