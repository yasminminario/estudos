# Relatório Técnico — Experimento CI/CD

**Repositório:** https://github.com/yasminminario/estudos  
**Aluno(a):** _preencher_  
**Data:** _preencher_

---

## 1. Objetivo

Instrumentar um pipeline GitHub Actions, coletar métricas de execuções reais e analisar desempenho, estabilidade e gargalos.

---

## 2. Configuração do pipeline

**Arquivo:** `.github/workflows/ci.yml`  
**Cópia de referência:** `entregaveis/workflow.yml`

| Job | Etapas | Depende de |
|-----|--------|------------|
| Lint | checkout → setup → install → ruff → métricas → artefato | — |
| Test | checkout → setup → install → pytest (JSON) → métricas → artefato | Lint |
| Collect Metrics | download artefatos → merge CSV/JSON → upload `pipeline-results` | Lint, Test |

Execução sequencial. Artefato final `pipeline-results` contém `pipeline-metrics.csv`, `pipeline-metrics.json` e `pytest-report.json`.

---

## 3. Variações realizadas (12 execuções)

| # | Commit SHA | Mensagem | Variação | Run ID | Status | Link |
|---|------------|----------|----------|--------|--------|------|
| 1 | 51abee0 | feat(ci): adiciona workflow GitHub Actions com lint e testes | Setup — workflow básico | 1 | success | 23s |
| 2 | 83ca746 | feat(ci): adiciona artefatos e coleta de metricas no pipeline | Setup — artefatos e métricas | 2 | success | 33s |
| 3 | 7f092e5 | experiment(01): baseline com todos os testes passando | 01-baseline-passing | 27136684800 | success | 26s |
| 4 | 67010e8 | experiment(02): teste falhando intencionalmente | 02-failing-test | 27137035952 | failure | 26s |
| 5 | | experiment(03): aumento artificial de testes | 03-more-tests | | | |
| 6 | | experiment: teste lento | 04-slow-test | | | |
| 7 | | experiment: cache habilitado | 05-cache-on | | | |
| 8 | | experiment: cache desabilitado | 06-cache-off | | | |
| 9 | | experiment: jobs sequenciais | 07-sequential | | | |
| 10 | | experiment: jobs paralelos | 08-parallel | | | |
| 11 | | experiment: lint falhando | 09-lint-failure | | | |
| 12 | | experiment: pico de testes com cache | 10-peak-cache | | | |

---

## 4. Gráficos

_Serão inseridos após a coleta de dados._

---

## 5. Análise

### Qual etapa mais contribuiu para o tempo total do pipeline?

_Pendente._

### Houve diferença significativa entre execuções com e sem cache?

_Pendente._

### O paralelismo reduziu o tempo total? Em que condições?

_Pendente._

### Quais falhas foram mais frequentes?

_Pendente._

### O pipeline fornece feedback rápido o suficiente para o desenvolvedor?

_Pendente._

### Que melhorias poderiam ser feitas no pipeline?

_Pendente._

### Quais limitações existem nos dados coletados?

_Pendente._

### Como essa análise poderia apoiar decisões de engenharia?

_Pendente._

---

## 6. Resultados inesperados

_Pendente — mínimo 2._

---

## 7. Hipótese inicial vs resultado observado

_Pendente._

---

## 8. Limitações do experimento

_Pendente._

---

## 9. Evidências

_Prints e links das execuções reais serão adicionados aqui._
