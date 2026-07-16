-- Schema Creation (if creating a specific namespace is desired)
CREATE SCHEMA IF NOT EXISTS ecommerce;

-- Note: We often set search_path so tables default to this schema
SET search_path TO ecommerce, public;
