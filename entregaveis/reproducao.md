# Como reproduzir o experimento

## Repositório original

O código-base foi obtido de https://github.com/W8jonas/estudos (autor: [W8jonas](https://github.com/W8jonas), licença MIT). Este experimento foi desenvolvido no fork https://github.com/yasminminario/estudos.

## 1. Pré-requisitos

- Conta GitHub com repositório clonado
- Python 3.12+
- Token GitHub com escopo `repo` (para coleta via API)

## 2. Execução local do projeto

```bash
cd ci-experiment
pip install -r requirements.txt
ruff check src tests
pytest tests/ -v
```

## 3. Disparar o pipeline

Cada commit na branch `master` que altere `ci-experiment/` ou `.github/workflows/` dispara o workflow `CI Pipeline Experiment`.

```bash
git push origin master
```

Acompanhe em: https://github.com/yasminminario/estudos/actions

## 4. Baixar métricas de uma execução

1. Abra a execução no GitHub Actions
2. Na seção **Artifacts**, baixe `pipeline-results`
3. Extraia `pipeline-metrics.csv`

## 5. Coletar métricas via API (obrigatório)

```bash
cd entregaveis/scripts
pip install -r requirements.txt

set GITHUB_TOKEN=seu_token_aqui
set GITHUB_REPOSITORY_OWNER=yasminminario
set GITHUB_REPOSITORY_NAME=estudos

python collect_metrics.py
```

Saída: `entregaveis/dados/metricas.csv` e `entregaveis/dados/metricas.json`

## 6. Gerar gráficos

```bash
cd entregaveis/scripts
python generate_charts.py
```

Saída em `entregaveis/graficos/`:

- `01_tempo_total_por_execucao.png`
- `02_tempo_por_job.png`
- `03_taxa_sucesso_falha.png`
- `04_testes_vs_duracao.png`

## 7. Variações do experimento

| Commit | Variação | O que muda |
|--------|----------|------------|
| experiment(01) | 01-baseline-passing | Todos os testes passando |
| experiment(02) | 02-failing-test | Teste falhando |
| experiment(03) | 03-more-tests | 48 testes parametrizados |
| experiment(04) | 04-slow-test | sleep(3) em um teste |
| experiment(05) | 05-cache-on | cache pip habilitado |
| experiment(06) | 06-cache-off | cache pip desabilitado |
| experiment(07) | 07-sequential | Install → Lint → Test |
| experiment(08) | 08-parallel | Lint \|\| Test |
| experiment(10) | 10-final-collection | Scripts e relatório final |
