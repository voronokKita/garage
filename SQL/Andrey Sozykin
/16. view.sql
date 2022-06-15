CREATE VIEW customers_view id, name AS
  SELECT id, name
  FROM customers;

CREATE VIEW products_view AS
  SELECT p.id AS id,
         p.name AS poduct_name,
         t.type_name AS product_type,
         p.price AS product_price
  FROM products AS p JOIN product_types AS t
  ON p.type_id = t.id;

CREATE MATERIALIZED VIEW customers_view id, name AS
  SELECT id, name
  FROM customers;

REFRESH MATERIALIZED VIEW customers_view;

DROP MATERIALIZED VIEW customers_view;
