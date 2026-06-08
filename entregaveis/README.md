# Entregáveis — Experimento CI/CD

| Arquivo / Pasta | Descrição | Status |
|-----------------|-----------|--------|
| `dados/metricas.csv` | Base de dados coletada | Concluído |
| `dados/metricas.json` | Versão JSON das métricas | Concluído |
| `graficos/01_tempo_total_por_execucao.png` | Tempo total do pipeline por execução | Concluído |
| `graficos/02_tempo_por_job.png` | Tempo por job ou etapa | Concluído |
| `graficos/03_taxa_sucesso_falha.png` | Taxa de sucesso e falha | Concluído |
| `graficos/04_testes_vs_duracao.png` | Relação entre quantidade de testes e duração | Concluído |
| `scripts/collect_metrics.py` | Script de coleta via API GitHub | Concluído |
| `scripts/generate_charts.py` | Script de geração dos gráficos | Concluído |
| `scripts/requirements.txt` | Dependências dos scripts | Concluído |
| `workflow.yml` | Cópia do YAML do GitHub Actions | Concluído |
| `relatorio.md` | Relatório técnico completo | Concluído |
| `reproducao.md` | Como reproduzir o experimento | Concluído |

## Repositório

- GitHub (este fork): https://github.com/yasminminario/estudos
- Workflow: https://github.com/yasminminario/estudos/blob/master/.github/workflows/ci.yml
- Actions: https://github.com/yasminminario/estudos/actions

## Repositório original

O código-base deste repositório foi obtido a partir do projeto original:

- **Autor:** [W8jonas](https://github.com/W8jonas)
- **Repositório:** https://github.com/W8jonas/estudos
- **Descrição:** Repositório contendo projetos, algoritmos e apps realizados com fins de estudo
- **Licença:** MIT

O experimento de CI/CD (`ci-experiment/` e `entregaveis/`) foi desenvolvido sobre este repositório.

## Execuções documentadas

10 execuções instrumentadas com Run IDs reais + 2 execuções de setup = 12 runs no GitHub Actions.
