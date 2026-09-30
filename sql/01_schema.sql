DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;


CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    email VARCHAR(150)
);


CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    price NUMERIC(10, 2) NOT NULL
);


CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL,
    order_date DATE NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,

    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

CREATE INDEX idx_orders_customer
ON orders(customer_id);


CREATE INDEX idx_orders_product
ON orders(product_id);


CREATE INDEX idx_orders_date
ON orders(order_date);


CREATE OR REPLACE VIEW order_analytics AS

SELECT
    o.order_id,
    o.order_date,

    c.customer_id,
    c.name AS customer_name,
    c.city,

    p.product_id,
    p.product_name,
    p.category,

    o.quantity,
    o.price,
    o.total_amount

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

JOIN products p
    ON o.product_id = p.product_id;