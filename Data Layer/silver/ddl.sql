-- Arquitetura Medalhao: Camada SILVER
-- Configuracoes iniciais
SET timezone = 'America/Sao_Paulo';

CREATE SCHEMA IF NOT EXISTS silver;

-- Drop da tabela se existir
DROP TABLE IF EXISTS silver.fact_sales CASCADE;

-- Esta tabela integra os dados tratados da camada RAW em uma unica estrutura de fatos
CREATE TABLE silver.fact_sales (

	-- IDENTIFICADORES
	order_id VARCHAR(32) NOT NULL,
	order_item_id INTEGER NOT NULL,
	product_id VARCHAR(32),
	seller_id VARCHAR(32),
	customer_id VARCHAR(32),

	-- DADOS TEMPORAIS
	shipping_limit_date TIMESTAMP,
	order_purchase_timestamp TIMESTAMP,
	order_approved_at TIMESTAMP,
	order_delivered_carrier_date TIMESTAMP,
	order_delivered_customer_date TIMESTAMP,
	order_estimated_delivery_date DATE,
	last_review_answer_at TIMESTAMP,

	-- DADOS COMERCIAIS E PEDIDO
	order_status VARCHAR(32),
	price NUMERIC(12,2),
	freight_value NUMERIC(12,2),
	total_payment_value NUMERIC(12,2),
	mean_payment_value NUMERIC(12,2),
	n_payment_events INTEGER,
	max_installments INTEGER,
	main_payment_type VARCHAR(32),

	-- DADOS DO CLIENTE
	customer_unique_id VARCHAR(32),
	customer_zip_code_prefix INTEGER,
	customer_city VARCHAR(255),
	customer_state VARCHAR(2),
	customer_geolocation_zip_code_prefix INTEGER,
	customer_geolocation_lat NUMERIC(10,6),
	customer_geolocation_lng NUMERIC(10,6),
	customer_geolocation_city VARCHAR(255),
	customer_geolocation_state VARCHAR(2),

	-- DADOS DO VENDEDOR
	seller_zip_code_prefix INTEGER,
	seller_city VARCHAR(255),
	seller_state VARCHAR(2),
	seller_geolocation_zip_code_prefix INTEGER,
	seller_geolocation_lat NUMERIC(10,6),
	seller_geolocation_lng NUMERIC(10,6),
	seller_geolocation_city VARCHAR(255),
	seller_geolocation_state VARCHAR(2),

	-- DADOS DO PRODUTO
	product_category_name VARCHAR(255),
	product_category_name_english VARCHAR(255),
	product_name_lenght NUMERIC(10,2),
	product_description_lenght NUMERIC(10,2),
	product_photos_qty NUMERIC(10,2),
	product_weight_g NUMERIC(12,2),
	product_length_cm NUMERIC(10,2),
	product_height_cm NUMERIC(10,2),
	product_width_cm NUMERIC(10,2),

	-- DADOS DE REVIEW
	review_score_mean NUMERIC(5,2),
	review_score_min NUMERIC(5,2),
	review_score_max NUMERIC(5,2),
	n_reviews INTEGER,
	has_comment BOOLEAN,

	CONSTRAINT pk_fact_sales PRIMARY KEY (order_id, order_item_id)
);

-- INDICES PARA PERFORMANCE
CREATE INDEX idx_silver_fact_sales_order_id ON silver.fact_sales(order_id);
CREATE INDEX idx_silver_fact_sales_purchase_ts ON silver.fact_sales(order_purchase_timestamp);
CREATE INDEX idx_silver_fact_sales_status ON silver.fact_sales(order_status);
CREATE INDEX idx_silver_fact_sales_customer ON silver.fact_sales(customer_id);
CREATE INDEX idx_silver_fact_sales_seller ON silver.fact_sales(seller_id);
CREATE INDEX idx_silver_fact_sales_category ON silver.fact_sales(product_category_name_english);
CREATE INDEX idx_silver_fact_sales_state ON silver.fact_sales(customer_state);
CREATE INDEX idx_silver_fact_sales_payment_type ON silver.fact_sales(main_payment_type);

-- MENSAGEM DE SUCESSO
DO $$
BEGIN
	RAISE NOTICE 'Schema SILVER criado com sucesso!';
	RAISE NOTICE '   - Tabela silver.fact_sales';
	RAISE NOTICE '   - Indices criados';
	RAISE NOTICE '';
	RAISE NOTICE 'PROXIMO PASSO: Executar ETL para popular a tabela silver';
END $$;
