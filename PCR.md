# 📋 PCR — Evolução do E-commerce Brasileiro

## 1. Visão Geral

### Objetivo

Desenvolver um projeto completo de Engenharia de Dados utilizando a Arquitetura Medalhão (Raw → Silver → Gold), integrando diferentes fontes de dados do comércio eletrônico brasileiro para construir uma plataforma analítica moderna, escalável e orientada à tomada de decisão.

O projeto utiliza como base principal o dataset histórico da Olist (2016–2018) e será enriquecido com um dataset moderno de e-commerce (2022–2024), permitindo comparar a evolução do mercado brasileiro em diferentes períodos.

Ao final, os dados serão disponibilizados em uma camada Gold otimizada para consumo pelo Power BI, possibilitando a construção de dashboards executivos com indicadores estratégicos de negócio.

---

# 2. Objetivos Técnicos

Durante o desenvolvimento serão aplicados conceitos de:

- Arquitetura Medalhão
- Engenharia de Dados
- ETL
- Modelagem Analítica
- Integração de múltiplas fontes
- Qualidade de Dados
- Pandas
- PyArrow
- SQL
- Power BI
- Git e GitHub

---

# 3. Arquitetura do Projeto

```
RAW
│
├── Olist
├── E-commerce Moderno
├── Marketing
└── Navegação
        │
        ▼
SILVER
│
├── fact_sales_olist
├── fact_sales_modern
└── fact_sales
        │
        ▼
GOLD
│
├── KPIs
├── Tabelas Analíticas
└── Dashboard Power BI
```

---

# 4. Roadmap de Desenvolvimento

---

# ✅ Sprint 1 — Camada RAW

## Objetivo

Organizar todas as fontes de dados sem realizar transformações, garantindo rastreabilidade e integridade dos arquivos originais.

### Atividades

- Organização da estrutura de pastas
- Importação dos datasets
- Inventário dos arquivos
- Validação de existência dos CSVs
- Verificação de duplicidades
- Identificação de inconsistências
- Notebook de exploração inicial
- Script de validação da camada RAW

### Entregáveis

- analytics.ipynb
- raw_validation.py
- CSVs organizados
- Relatório de validação

### Status

✅ Concluído

---

# ✅ Sprint 2 — Silver (Olist)

## Objetivo

Construir a primeira Big Table analítica (`fact_sales_olist`) utilizando exclusivamente os dados históricos da Olist.

### Atividades

### ETL

- Leitura dos datasets
- Conversão de tipos
- Tratamento de valores nulos
- Remoção de duplicidades
- Tratamento de datas

### Transformações

Criação das tabelas intermediárias:

- products_enriched
- payments_agg
- reviews_agg

### Integração

Construção da Big Table:

```
fact_sales_olist
```

Integrando:

- Orders
- Customers
- Order Items
- Payments
- Reviews
- Sellers
- Products
- Category Translation

### Exportação

- CSV
- Parquet

### Analytics

- Estatísticas
- Integridade
- Valores nulos
- Duplicidades
- Qualidade dos dados

### DDL

Criação do script SQL da tabela.

### Entregáveis

- etl_silver_olist.py
- analytics_olist.ipynb
- ddl.sql
- fact_sales_olist.csv
- fact_sales_olist.parquet

### Status

✅ Concluído

---

# 🚧 Sprint 3 — Silver (E-commerce Moderno)

## Objetivo

Construir uma segunda Big Table (`fact_sales_modern`) utilizando exclusivamente o dataset moderno de e-commerce (2022–2024).

Esta etapa será desenvolvida de forma independente da Olist para preservar a modelagem de cada fonte de dados.

### Atividades

### Estudo dos datasets

- Identificação do modelo relacional
- Dicionário de dados
- Definição da granularidade

### ETL

- Conversão de tipos
- Limpeza
- Tratamento de nulos
- Remoção de duplicidades
- Padronização

### Construção da Big Table

```
fact_sales_modern
```

### Exportação

- CSV
- Parquet

### Analytics

- Estatísticas
- Integridade
- Qualidade

### DDL

Script SQL da nova tabela.

### Gate de conclusão da Sprint 3

Antes de marcar como concluída, validar obrigatoriamente:

- Granularidade definida e documentada
- Chave lógica definida e testada
- Joins validados sem perda/duplicação indevida
- ETL reproduzível com exportações CSV/Parquet
- Analytics final com estatísticas de qualidade
- DDL aderente ao schema final da Big Table

### Sequência de execução (padrão Sprint 2)

RAW -> Analytics inicial -> Tratamento -> Big Table -> ETL -> CSV/Parquet -> Analytics final -> DDL

### Entregáveis

- etl_silver_modern.py
- analytics_modern.ipynb
- ddl.sql
- fact_sales_modern.csv
- fact_sales_modern.parquet

### Status

🚧 Em andamento (aguardando validação formal de modelagem, ETL, analytics e DDL)

---

# 🚧 Sprint 4 — Silver Integrada

## Objetivo

Unificar as duas Big Tables construídas nas sprints anteriores em uma única tabela analítica consolidada.

Entrada

```
fact_sales_olist
```

+

```
fact_sales_modern
```

↓

Saída

```
fact_sales
```

### Atividades

- Padronização de colunas
- Padronização de tipos
- Padronização de categorias
- Padronização temporal
- União dos datasets
- Criação do ETL de integração
- Atualização do Analytics
- Atualização do DDL

### Entregáveis

- etl_silver.py
- analytics.ipynb
- ddl.sql
- fact_sales.csv
- fact_sales.parquet

### Status

⬜ Não iniciado

---

# 🚧 Sprint 5 — Silver (Marketing e Navegação)

## Objetivo

Enriquecer a Big Table consolidada com dados simulados de campanhas de marketing e comportamento de navegação dos usuários.

### Atividades

Integração de:

- Sessões
- Campanhas
- Origem do tráfego
- Canal de aquisição
- Dispositivo
- Conversão

Atualização da fact_sales.

### Entregáveis

- ETL atualizado
- Analytics atualizado
- Nova fact_sales

### Status

⬜ Não iniciado

---

# 🚧 Sprint 6 — Camada Gold

## Objetivo

Transformar a Big Table da Silver em tabelas analíticas orientadas ao negócio.

### KPIs

- Receita Total
- Receita Mensal
- Ticket Médio
- Clientes Ativos
- Produtos Mais Vendidos
- Categorias
- Market Share
- Sellers
- Logística
- Entregas
- Marketing
- Conversão

### ETL

Construção das tabelas Gold.

### Analytics

Validação dos indicadores.

### DDL

Scripts SQL.

### Entregáveis

- etl_gold.py
- analytics.ipynb
- ddl.sql
- Tabelas Gold

### Status

⬜ Não iniciado

---

# 🚧 Sprint 7 — Dashboard Executivo

## Objetivo

Construir um dashboard executivo no Power BI consumindo exclusivamente a camada Gold.

### Dashboards

- Visão Geral
- Receita
- Clientes
- Produtos
- Logística
- Marketing
- Comparativo Histórico
- Evolução do Mercado

### Entregáveis

- dashboard.pbix
- Layout final

### Status

⬜ Não iniciado

---

# 🚧 Sprint 8 — Publicação

## Objetivo

Preparar o projeto para publicação como portfólio profissional.

### Atividades

- README completo
- Documentação da arquitetura
- Fluxograma
- Prints
- GIFs
- Organização do GitHub
- Publicação no LinkedIn

### Status

⬜ Não iniciado

---

# 5. Progresso Geral

| Sprint | Descrição | Status |
|----------|-------------------------------|---------|
| Sprint 1 | Camada RAW | ✅ |
| Sprint 2 | Silver Olist | ✅ |
| Sprint 3 | Silver E-commerce Moderno | 🚧 |
| Sprint 4 | Silver Integrada | ⬜ |
| Sprint 5 | Marketing e Navegação | ⬜ |
| Sprint 6 | Camada Gold | ⬜ |
| Sprint 7 | Dashboard Executivo | ⬜ |
| Sprint 8 | Publicação | ⬜ |

---

# 6. Resultado Esperado

Ao término do projeto será entregue uma solução completa de Engenharia de Dados contendo:

- Arquitetura Medalhão completa.
- ETLs independentes para cada camada.
- Integração de múltiplas fontes de dados.
- Big Tables consolidadas.
- Camada Gold orientada à análise.
- Dashboard executivo no Power BI.
- Documentação técnica.
- Projeto pronto para portfólio profissional e demonstração de competências em Engenharia de Dados.