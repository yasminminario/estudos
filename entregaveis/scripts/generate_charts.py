from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "dados" / "metricas.csv"
CHARTS_DIR = ROOT / "graficos"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["workflow_duration"] = pd.to_numeric(df["workflow_duration"], errors="coerce")
    df["job_duration"] = pd.to_numeric(df["job_duration"], errors="coerce")
    df["test_count"] = pd.to_numeric(df["test_count"], errors="coerce").fillna(0)
    return df


def chart_total_duration(df: pd.DataFrame) -> None:
    runs = (
        df.groupby(["run_id", "variation", "status"], as_index=False)["workflow_duration"]
        .first()
        .sort_values("run_id")
    )
    labels = [f"{row.variation}\n({row.run_id})" for row in runs.itertuples()]
    colors = ["#2ecc71" if status == "success" else "#e74c3c" for status in runs["status"]]

    plt.figure(figsize=(12, 6))
    plt.bar(labels, runs["workflow_duration"], color=colors)
    plt.title("Tempo total do pipeline por execucao")
    plt.ylabel("Segundos")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "01_tempo_total_por_execucao.png", dpi=150)
    plt.close()


def chart_job_duration(df: pd.DataFrame) -> None:
    jobs = df[df["job_name"] != "Collect Metrics"].copy()
    pivot = jobs.pivot_table(
        index="variation",
        columns="job_name",
        values="job_duration",
        aggfunc="mean",
    )

    plt.figure(figsize=(10, 6))
    pivot.plot(kind="bar", ax=plt.gca())
    plt.title("Tempo medio por job em cada variacao")
    plt.ylabel("Segundos")
    plt.xlabel("Variacao")
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="Job")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "02_tempo_por_job.png", dpi=150)
    plt.close()


def chart_success_failure(df: pd.DataFrame) -> None:
    runs = df.groupby(["run_id", "status"], as_index=False).first()
    counts = runs["status"].value_counts()
    labels = counts.index.tolist()
    values = counts.values.tolist()
    colors = ["#2ecc71" if label == "success" else "#e74c3c" for label in labels]

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%1.0f%%", colors=colors, startangle=90)
    plt.title("Taxa de sucesso e falha das execucoes")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "03_taxa_sucesso_falha.png", dpi=150)
    plt.close()


def chart_tests_vs_duration(df: pd.DataFrame) -> None:
    runs = (
        df.groupby("run_id", as_index=False)
        .agg(
            workflow_duration=("workflow_duration", "first"),
            test_count=("test_count", "max"),
            variation=("variation", "first"),
        )
        .query("test_count > 0")
    )

    plt.figure(figsize=(9, 6))
    plt.scatter(runs["test_count"], runs["workflow_duration"], s=100, alpha=0.8)
    for row in runs.itertuples():
        plt.annotate(row.variation, (row.test_count, row.workflow_duration), fontsize=8)
    plt.title("Relacao entre quantidade de testes e duracao do pipeline")
    plt.xlabel("Quantidade de testes")
    plt.ylabel("Duracao total (s)")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "04_testes_vs_duracao.png", dpi=150)
    plt.close()


def main() -> None:
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    chart_total_duration(df)
    chart_job_duration(df)
    chart_success_failure(df)
    chart_tests_vs_duration(df)
    print(f"Graficos salvos em: {CHARTS_DIR}")


if __name__ == "__main__":
    main()
