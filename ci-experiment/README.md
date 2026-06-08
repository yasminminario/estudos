# Experimento CI/CD — GitHub Actions

Projeto mínimo em Python para medir e analisar o comportamento de um pipeline CI/CD com execuções reais no GitHub Actions.

**Repositório original:** https://github.com/W8jonas/estudos

## Estrutura

```
ci-experiment/
├── src/           # código da aplicação
├── tests/         # testes automatizados (pytest)
├── requirements.txt
└── pyproject.toml

entregaveis/
├── dados/         # CSV/JSON coletados
├── graficos/      # gráficos gerados
├── scripts/       # script Python de coleta de métricas
├── relatorio.md   # relatório técnico
└── workflow.yml   # cópia de referência do pipeline
```

## Execução local

```bash
cd ci-experiment
pip install -r requirements.txt
ruff check src tests
pytest tests/ -v
```

## Experimentos planejados (12 execuções)

| # | Variação |
|---|----------|
| 1 | Baseline — todos os testes passando |
| 2 | Teste falhando |
| 3 | Aumento da quantidade de testes |
| 4 | Teste lento introduzido |
| 5 | Cache de dependências habilitado |
| 6 | Cache de dependências desabilitado |
| 7 | Jobs em ordem sequencial |
| 8 | Jobs em paralelo |
| 9 | Lint com falha |
| 10 | Remoção do teste lento |
| 11 | Pico de testes + cache |
| 12 | Configuração final consolidada |

## Reprodução do experimento

Será documentado em `entregaveis/relatorio.md` após as 12 execuções no GitHub Actions.
