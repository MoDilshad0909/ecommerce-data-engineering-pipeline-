-- Indexes for Fact Orders (dim_orders as base fact)
CREATE INDEX idx_orders_customer_id ON dim_orders(customer_id);
CREATE INDEX idx_orders_purchase_timestamp ON dim_orders(order_purchase_timestamp);

-- Indexes for Fact Order Items
CREATE INDEX idx_order_items_order_id ON fact_order_items(order_id);
CREATE INDEX idx_order_items_product_id ON fact_order_items(product_id);
CREATE INDEX idx_order_items_seller_id ON fact_order_items(seller_id);

-- Indexes for Fact Payments
CREATE INDEX idx_payments_order_id ON fact_payments(order_id);

-- Optimizing text lookups in dimension tables
CREATE INDEX idx_customers_state ON dim_customers(customer_state);
CREATE INDEX idx_sellers_state ON dim_sellers(seller_state);
