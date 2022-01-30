SELECT id, name, price
FROM products
WHERE price = (
  SELECT MAX(price)
  FROM products
);

SELECT id, name, price
FROM products
WHERE id IN (
  SELECT product_id
  FROM sales
);

UPDATE products
SET price = perice + 500
WHERE type_id = (
  SELECT id
  FROM product_types
  WHERE type_name = 'Книга'
);
