-- Total Revenue by Payment Type
SELECT 
    p.payment_type,
    COUNT(p.order_id) AS total_transactions,
    SUM(p.payment_value) AS total_revenue,
    AVG(p.payment_value) AS avg_transaction_value
FROM fact_payments p
JOIN dim_orders o ON p.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.payment_type
ORDER BY total_revenue DESC;
