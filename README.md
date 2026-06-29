# Brazilian E-commerce Data Platform

Projeto de Engenharia de Dados para organizar, processar e analisar dados de e-commerce brasileiro em uma arquitetura por camadas.

## Objetivo

Construir uma plataforma de dados local para ingestao, transformacao e analise de dados de e-commerce, separando os artefatos em camadas `raw`, `silver` e `gold`.

## Estrutura

```text
brazilian-ecommerce-data-platform/
├── .agents/
├── .github/
├── Data Layer/
│   ├── raw/
│   ├── silver/
│   └── gold/
├── docs/
├── notebooks/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Camadas de dados

- `raw`: dados brutos, preservados no formato original.
- `silver`: dados tratados, padronizados e prontos para consumo analitico.
- `gold`: dados modelados para analises, consultas e entregaveis finais.

## Notebooks

Os notebooks de ETL e exploracao ficam em `notebooks/`.

## Validacao da RAW

A etapa de ingestao e validacao da camada RAW pode ser executada com:

```bash
python src/raw_validation.py
```

O processo carrega todos os CSVs em `Data Layer/raw/`, valida existencia dos datasets, quantidade de registros, tipos, valores nulos, duplicidades e chaves de relacionamento. O relatorio e gerado em `docs/raw_validation_report.md`.

## Ambiente

O projeto esta preparado para evoluir com ambiente Python, Jupyter e Docker. As dependencias devem ser registradas em `requirements.txt` conforme forem adicionadas.

## Status

Projeto em organizacao inicial para portfolio de Engenharia de Dados.
