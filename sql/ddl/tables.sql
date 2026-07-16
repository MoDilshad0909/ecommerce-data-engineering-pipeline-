-- Dimension Table: Customers
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50) NOT NULL,
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

-- Dimension Table: Products
CREATE TABLE IF NOT EXISTS dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght FLOAT,
    product_description_lenght FLOAT,
    product_photos_qty FLOAT,
    product_weight_g FLOAT,
    product_length_cm FLOAT,
    product_height_cm FLOAT,
    product_width_cm FLOAT
);

-- Dimension Table: Sellers
CREATE TABLE IF NOT EXISTS dim_sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
);

-- Dimension Table: Orders (Can act as a degenerate dimension)
CREATE TABLE IF NOT EXISTS dim_orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) REFERENCES dim_customers(customer_id),
    order_status VARCHAR(20),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

-- Fact Table: Order Items
CREATE TABLE IF NOT EXISTS fact_order_items (
    order_id VARCHAR(50) REFERENCES dim_orders(order_id),
    order_item_id INT,
    product_id VARCHAR(50) REFERENCES dim_products(product_id),
    seller_id VARCHAR(50) REFERENCES dim_sellers(seller_id),
    shipping_limit_date TIMESTAMP,
    price NUMERIC(10, 2),
    freight_value NUMERIC(10, 2),
    PRIMARY KEY (order_id, order_item_id)
);

-- Fact Table: Payments
CREATE TABLE IF NOT EXISTS fact_payments (
    order_id VARCHAR(50) REFERENCES dim_orders(order_id),
    payment_sequential INT,
    payment_type VARCHAR(50),
    payment_installments INT,
    payment_value NUMERIC(10, 2),
    PRIMARY KEY (order_id, payment_sequential)
);
