SELECT p.id, p.name, p.price, s.quantity,
       p.price * s.quantity AS total
FROM products AS p JOIN sales AS s
ON p.id = s.product_id
WHERE s.order_id = 2;


SELECT products.id, products.name, products.price, sales.quantity,
       products.price * sales.quantity AS total
FROM products JOIN sales
ON products.id = sales.product_id JOIN orders
  ON orders.id = sales.order_id
WHERE orders.customer_id = 1;
