-- Arquitetura Medalhao: Camada SILVER
SET timezone = 'America/Sao_Paulo';

CREATE SCHEMA IF NOT EXISTS silver;

-- Sprint 2 - Silver (Olist)
DROP TABLE IF EXISTS silver.fact_sales_olist CASCADE;

CREATE TABLE silver.fact_sales_olist (
    -- Identificadores
    order_id VARCHAR(32) NOT NULL,
    order_item_id INTEGER NOT NULL,
    customer_id VARCHAR(32),
    customer_unique_id VARCHAR(32),
    product_id VARCHAR(32),
    seller_id VARCHAR(32),

    -- Eventos (timestamp)
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    shipping_limit_date TIMESTAMP,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,

    -- Datas derivadas
    purchase_date DATE,
    purchase_year INTEGER,
    purchase_month INTEGER,
    purchase_year_month VARCHAR(7),
    purchase_quarter INTEGER,
    purchase_weekday VARCHAR(16),
    delivery_days INTEGER,
    estimated_delivery_days INTEGER,
    delivery_delay_days INTEGER,

    -- Comerciais e pedido
    order_status VARCHAR(32),
    price NUMERIC(12,2),
    freight_value NUMERIC(12,2),
    payment_value_total NUMERIC(12,2),
    payment_installments_max INTEGER,
    payment_methods_count INTEGER,
    payment_type_main VARCHAR(32),
    has_payment BOOLEAN,
    has_multiple_payment_methods BOOLEAN,
    total_sale NUMERIC(12,2),
    total_freight NUMERIC(12,2),
    total_item_value NUMERIC(12,2),
    total_order_payment NUMERIC(12,2),

    -- Cliente e vendedor
    customer_zip_code_prefix VARCHAR(10),
    customer_city VARCHAR(255),
    customer_state VARCHAR(2),
    seller_zip_code_prefix VARCHAR(10),
    seller_city VARCHAR(255),
    seller_state VARCHAR(2),

    -- Produto
    product_category_name VARCHAR(255),
    product_category_name_english VARCHAR(255),
    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,
    product_weight_g NUMERIC(12,2),
    product_length_cm NUMERIC(10,2),
    product_height_cm NUMERIC(10,2),
    product_width_cm NUMERIC(10,2),

    -- Review
    review_score NUMERIC(5,2),
    review_count INTEGER,

    -- Flags
    is_completed BOOLEAN,
    is_delivered BOOLEAN,
    is_late BOOLEAN,

    CONSTRAINT pk_fact_sales_olist PRIMARY KEY (order_id, order_item_id)
);

CREATE INDEX idx_silver_fact_sales_olist_order_id ON silver.fact_sales_olist(order_id);
CREATE INDEX idx_silver_fact_sales_olist_purchase_ts ON silver.fact_sales_olist(order_purchase_timestamp);
CREATE INDEX idx_silver_fact_sales_olist_status ON silver.fact_sales_olist(order_status);
CREATE INDEX idx_silver_fact_sales_olist_customer ON silver.fact_sales_olist(customer_id);
CREATE INDEX idx_silver_fact_sales_olist_seller ON silver.fact_sales_olist(seller_id);
CREATE INDEX idx_silver_fact_sales_olist_category ON silver.fact_sales_olist(product_category_name_english);
CREATE INDEX idx_silver_fact_sales_olist_state ON silver.fact_sales_olist(customer_state);
CREATE INDEX idx_silver_fact_sales_olist_payment_type ON silver.fact_sales_olist(payment_type_main);

-- Sprint 3 - Silver (E-commerce Moderno)
DROP TABLE IF EXISTS silver.fact_sales_modern CASCADE;

CREATE TABLE silver.fact_sales_modern (
    -- Identificadores
    order_id VARCHAR(32) NOT NULL,
    order_item_id INTEGER NOT NULL,
    sku VARCHAR(80),
    asin VARCHAR(32),

    -- Eventos (timestamp)
    order_date TIMESTAMP,

    -- Datas derivadas
    order_year INTEGER,
    order_month INTEGER,
    order_year_month VARCHAR(7),

    -- Comerciais
    order_status VARCHAR(64),
    courier_status VARCHAR(64),
    fulfillment VARCHAR(64),
    sales_channel VARCHAR(64),
    ship_service_level VARCHAR(64),
    category VARCHAR(64),
    style VARCHAR(64),
    size VARCHAR(16),
    color VARCHAR(32),
    quantity INTEGER,
    unit_price NUMERIC(12,2),
    gross_revenue NUMERIC(14,2),
    currency VARCHAR(8),
    promotion_ids TEXT,
    is_b2b BOOLEAN,
    fulfilled_by VARCHAR(64),
    stock_available NUMERIC(12,2),

    -- Logistica
    ship_city VARCHAR(255),
    ship_state VARCHAR(64),
    ship_postal_code VARCHAR(10),
    ship_country VARCHAR(8),

    -- Flags
    is_cancelled BOOLEAN,
    is_returned BOOLEAN,
    is_delivered BOOLEAN,

    CONSTRAINT pk_fact_sales_modern PRIMARY KEY (order_id, order_item_id)
);

CREATE INDEX idx_silver_fact_sales_modern_order_id ON silver.fact_sales_modern(order_id);
CREATE INDEX idx_silver_fact_sales_modern_order_date ON silver.fact_sales_modern(order_date);
CREATE INDEX idx_silver_fact_sales_modern_status ON silver.fact_sales_modern(order_status);
CREATE INDEX idx_silver_fact_sales_modern_channel ON silver.fact_sales_modern(sales_channel);
CREATE INDEX idx_silver_fact_sales_modern_category ON silver.fact_sales_modern(category);
CREATE INDEX idx_silver_fact_sales_modern_state ON silver.fact_sales_modern(ship_state);

-- Sprint 4 - Silver Integrada
-- A tabela silver.fact_sales sera criada na Sprint 4 a partir da uniao padronizada de:
--   1) silver.fact_sales_olist
--   2) silver.fact_sales_modern

DO $$
BEGIN
    RAISE NOTICE 'Schema SILVER criado com sucesso!';
    RAISE NOTICE '   - Tabela silver.fact_sales_olist';
    RAISE NOTICE '   - Tabela silver.fact_sales_modern';
    RAISE NOTICE '   - Indices criados';
    RAISE NOTICE '';
    RAISE NOTICE 'PROXIMO PASSO: Executar ETLs para popular fact_sales_olist e fact_sales_modern';
END $$;
