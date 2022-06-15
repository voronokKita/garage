SELECT products.name, product_types.type_name
FROM products JOIN product_types
ON products.type_id = product_types.id;

SELECT p.name, t.type_name
FROM products AS p JOIN product_types AS t
ON p.type_id = t.id;


SELECT p.name AS product_name,
       t.type_name AS product_type,
       p.price AS product_price
FROM products AS p JOIN product_types AS t
ON p.type_id = t.id
WHERE t.type_name = 'Онлайн-курс'
ORDER BY p.price DESC;


SELECT p.name AS product_name,
       t.type_name AS product_type,
       p.price AS product_price
FROM products AS p JOIN product_types AS t
ON p.type_id = t.id
WHERE t.type_name = 'Вебинар' AND p.price = 0;
