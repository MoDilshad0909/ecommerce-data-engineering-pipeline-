-- Top 10 Best Selling Products by Revenue
SELECT 
    p.product_category_name,
    COUNT(i.order_item_id) AS total_units_sold,
    SUM(i.price) AS total_revenue
FROM fact_order_items i
JOIN dim_products p ON i.product_id = p.product_id
JOIN dim_orders o ON i.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;
