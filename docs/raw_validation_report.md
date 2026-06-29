# Relatorio de Validacao da RAW

Gerado em: `2026-06-29 14:48:45`

## Resumo

- Datasets esperados: 16
- Datasets encontrados: 16
- Total de registros carregados: 1729327
- Memoria estimada em pandas: 504.93 MB
- Datasets ausentes: 0
- Datasets inesperados: 0

## Existencia dos datasets

Todos os datasets esperados foram encontrados.

## Datasets inesperados

Nenhum dataset inesperado foi encontrado.

## Quantidade de registros, colunas e duplicidades

| dataset | registros | colunas | linhas duplicadas | memoria_mb |
| --- | --- | --- | --- | --- |
| ecommerce_2024/Amazon Sale Report.csv | 128975 | 24 | 0 | 173.69 |
| ecommerce_2024/Cloud Warehouse Compersion Chart.csv | 50 | 4 | 0 | 0.01 |
| ecommerce_2024/Expense IIGF.csv | 17 | 5 | 0 | 0.00 |
| ecommerce_2024/International sale Report.csv | 37432 | 10 | 0 | 18.35 |
| ecommerce_2024/May-2022.csv | 1330 | 17 | 0 | 1.10 |
| ecommerce_2024/P  L March 2021.csv | 1330 | 18 | 0 | 1.17 |
| ecommerce_2024/Sale Report.csv | 9271 | 7 | 0 | 2.59 |
| olist/olist_customers_dataset.csv | 99441 | 5 | 0 | 26.59 |
| olist/olist_geolocation_dataset.csv | 1000163 | 5 | 261831 | 130.26 |
| olist/olist_order_items_dataset.csv | 112650 | 7 | 0 | 35.99 |
| olist/olist_order_payments_dataset.csv | 103886 | 5 | 0 | 16.23 |
| olist/olist_order_reviews_dataset.csv | 99224 | 7 | 0 | 39.12 |
| olist/olist_orders_dataset.csv | 99441 | 8 | 0 | 52.94 |
| olist/olist_products_dataset.csv | 32951 | 9 | 0 | 6.30 |
| olist/olist_sellers_dataset.csv | 3095 | 4 | 0 | 0.59 |
| olist/product_category_name_translation.csv | 71 | 2 | 0 | 0.01 |

## Chaves de relacionamento

| relacionamento | status | chaves ausentes | % ausente | amostra ausente |
| --- | --- | --- | --- | --- |
| orders.customer_id -> customers.customer_id | ok | 0 | 0.0000% |  |
| order_items.order_id -> orders.order_id | ok | 0 | 0.0000% |  |
| order_payments.order_id -> orders.order_id | ok | 0 | 0.0000% |  |
| order_reviews.order_id -> orders.order_id | ok | 0 | 0.0000% |  |
| order_items.product_id -> products.product_id | ok | 0 | 0.0000% |  |
| order_items.seller_id -> sellers.seller_id | ok | 0 | 0.0000% |  |
| products.product_category_name -> translation.product_category_name | failed | 13 | 0.0402% | pc_gamer, portateis_cozinha_e_preparadores_de_alimentos |

## ecommerce_2024/Amazon Sale Report.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| ASIN | str |
| Amount | float64 |
| B2B | bool |
| Category | str |
| Courier Status | str |
| Date | str |
| Fulfilment | str |
| Order ID | str |
| Qty | int64 |
| SKU | str |
| Sales Channel  | str |
| Size | str |
| Status | str |
| Style | str |
| Unnamed: 22 | object |
| currency | str |
| fulfilled-by | str |
| index | int64 |
| promotion-ids | str |
| ship-city | str |
| ship-country | str |
| ship-postal-code | float64 |
| ship-service-level | str |
| ship-state | str |

### Valores nulos

| coluna | nulos | % |
| --- | --- | --- |
| fulfilled-by | 89698 | 69.55% |
| promotion-ids | 49153 | 38.11% |
| Unnamed: 22 | 49050 | 38.03% |
| currency | 7795 | 6.04% |
| Amount | 7795 | 6.04% |
| Courier Status | 6872 | 5.33% |
| ship-city | 33 | 0.03% |
| ship-state | 33 | 0.03% |
| ship-postal-code | 33 | 0.03% |
| ship-country | 33 | 0.03% |

## ecommerce_2024/Cloud Warehouse Compersion Chart.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| INCREFF | str |
| Shiprocket | str |
| Unnamed: 1 | str |
| index | int64 |

### Valores nulos

| coluna | nulos | % |
| --- | --- | --- |
| Shiprocket | 29 | 58.00% |
| INCREFF | 22 | 44.00% |
| Unnamed: 1 | 9 | 18.00% |

## ecommerce_2024/Expense IIGF.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| Expance | str |
| Recived Amount | str |
| Unnamed: 1 | str |
| Unnamed: 3 | str |
| index | int64 |

### Valores nulos

| coluna | nulos | % |
| --- | --- | --- |
| Recived Amount | 11 | 64.71% |
| Unnamed: 1 | 11 | 64.71% |
| Expance | 2 | 11.76% |

## ecommerce_2024/International sale Report.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| CUSTOMER | str |
| DATE | str |
| GROSS AMT | str |
| Months | str |
| PCS | str |
| RATE | str |
| SKU | str |
| Size | str |
| Style | str |
| index | int64 |

### Valores nulos

| coluna | nulos | % |
| --- | --- | --- |
| SKU | 2474 | 6.61% |
| CUSTOMER | 1040 | 2.78% |
| Style | 1040 | 2.78% |
| Size | 1040 | 2.78% |
| PCS | 1040 | 2.78% |
| RATE | 1040 | 2.78% |
| GROSS AMT | 1040 | 2.78% |
| Months | 25 | 0.07% |
| DATE | 1 | 0.00% |

## ecommerce_2024/May-2022.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| Ajio MRP | str |
| Amazon FBA MRP | str |
| Amazon MRP | str |
| Catalog | str |
| Category | str |
| Final MRP Old | str |
| Flipkart MRP | str |
| Limeroad MRP | str |
| MRP Old | str |
| Myntra MRP | str |
| Paytm MRP | str |
| Sku | str |
| Snapdeal MRP | str |
| Style Id | str |
| TP | str |
| Weight | str |
| index | int64 |

### Valores nulos

Nenhum valor nulo identificado.

## ecommerce_2024/P  L March 2021.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| Ajio MRP | str |
| Amazon FBA MRP | str |
| Amazon MRP | str |
| Catalog | str |
| Category | str |
| Final MRP Old | str |
| Flipkart MRP | str |
| Limeroad MRP | str |
| MRP Old | str |
| Myntra MRP | str |
| Paytm MRP | str |
| Sku | str |
| Snapdeal MRP | str |
| Style Id | str |
| TP 1 | str |
| TP 2 | str |
| Weight | str |
| index | int64 |

### Valores nulos

Nenhum valor nulo identificado.

## ecommerce_2024/Sale Report.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| Category | str |
| Color | str |
| Design No. | str |
| SKU Code | str |
| Size | str |
| Stock | float64 |
| index | int64 |

### Valores nulos

| coluna | nulos | % |
| --- | --- | --- |
| SKU Code | 83 | 0.90% |
| Category | 45 | 0.49% |
| Color | 45 | 0.49% |
| Design No. | 36 | 0.39% |
| Stock | 36 | 0.39% |
| Size | 36 | 0.39% |

## olist/olist_customers_dataset.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| customer_city | str |
| customer_id | str |
| customer_state | str |
| customer_unique_id | str |
| customer_zip_code_prefix | int64 |

### Valores nulos

Nenhum valor nulo identificado.

## olist/olist_geolocation_dataset.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| geolocation_city | str |
| geolocation_lat | float64 |
| geolocation_lng | float64 |
| geolocation_state | str |
| geolocation_zip_code_prefix | int64 |

### Valores nulos

Nenhum valor nulo identificado.

## olist/olist_order_items_dataset.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| freight_value | float64 |
| order_id | str |
| order_item_id | int64 |
| price | float64 |
| product_id | str |
| seller_id | str |
| shipping_limit_date | str |

### Valores nulos

Nenhum valor nulo identificado.

## olist/olist_order_payments_dataset.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| order_id | str |
| payment_installments | int64 |
| payment_sequential | int64 |
| payment_type | str |
| payment_value | float64 |

### Valores nulos

Nenhum valor nulo identificado.

## olist/olist_order_reviews_dataset.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| order_id | str |
| review_answer_timestamp | str |
| review_comment_message | str |
| review_comment_title | str |
| review_creation_date | str |
| review_id | str |
| review_score | int64 |

### Valores nulos

| coluna | nulos | % |
| --- | --- | --- |
| review_comment_title | 87656 | 88.34% |
| review_comment_message | 58247 | 58.70% |

## olist/olist_orders_dataset.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| customer_id | str |
| order_approved_at | str |
| order_delivered_carrier_date | str |
| order_delivered_customer_date | str |
| order_estimated_delivery_date | str |
| order_id | str |
| order_purchase_timestamp | str |
| order_status | str |

### Valores nulos

| coluna | nulos | % |
| --- | --- | --- |
| order_delivered_customer_date | 2965 | 2.98% |
| order_delivered_carrier_date | 1783 | 1.79% |
| order_approved_at | 160 | 0.16% |

## olist/olist_products_dataset.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| product_category_name | str |
| product_description_lenght | float64 |
| product_height_cm | float64 |
| product_id | str |
| product_length_cm | float64 |
| product_name_lenght | float64 |
| product_photos_qty | float64 |
| product_weight_g | float64 |
| product_width_cm | float64 |

### Valores nulos

| coluna | nulos | % |
| --- | --- | --- |
| product_category_name | 610 | 1.85% |
| product_name_lenght | 610 | 1.85% |
| product_description_lenght | 610 | 1.85% |
| product_photos_qty | 610 | 1.85% |
| product_weight_g | 2 | 0.01% |
| product_length_cm | 2 | 0.01% |
| product_height_cm | 2 | 0.01% |
| product_width_cm | 2 | 0.01% |

## olist/olist_sellers_dataset.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| seller_city | str |
| seller_id | str |
| seller_state | str |
| seller_zip_code_prefix | int64 |

### Valores nulos

Nenhum valor nulo identificado.

## olist/product_category_name_translation.csv

### Tipos das colunas

| coluna | tipo |
| --- | --- |
| product_category_name | str |
| product_category_name_english | str |

### Valores nulos

Nenhum valor nulo identificado.
