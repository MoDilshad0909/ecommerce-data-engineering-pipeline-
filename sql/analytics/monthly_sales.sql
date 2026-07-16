-- Monthly Sales Trends over time
SELECT 
    DATE_TRUNC('month', o.order_purchase_timestamp) AS sales_month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(i.price) AS total_sales,
    SUM(i.freight_value) AS total_freight
FROM dim_orders o
JOIN fact_order_items i ON o.order_id = i.order_id
WHERE o.order_status = 'delivered'
GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp)
ORDER BY sales_month ASC;
