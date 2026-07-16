-- Top 10 States by Customer Base and Average Order Value (AOV)
SELECT 
    c.customer_state,
    COUNT(DISTINCT c.customer_unique_id) AS total_unique_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(i.price) AS total_revenue,
    SUM(i.price) / COUNT(DISTINCT o.order_id) AS average_order_value
FROM dim_customers c
JOIN dim_orders o ON c.customer_id = o.customer_id
JOIN fact_order_items i ON o.order_id = i.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC
LIMIT 10;
