-- Example DML for inserting a new dimension record explicitly (if not using Python bulk load)
INSERT INTO dim_customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
VALUES ('test_cust_id_001', 'test_unique_id_001', 12345, 'sao paulo', 'SP')
ON CONFLICT (customer_id) DO UPDATE 
SET customer_city = EXCLUDED.customer_city,
    customer_state = EXCLUDED.customer_state;

-- Upserting Fact Orders
INSERT INTO dim_orders (order_id, customer_id, order_status, order_purchase_timestamp)
VALUES ('test_order_001', 'test_cust_id_001', 'delivered', CURRENT_TIMESTAMP)
ON CONFLICT (order_id) DO NOTHING;
