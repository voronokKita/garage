SELECT products.name, product_types.type_name
FROM products LEFT OUTER JOIN product_types
ON products.type_id = product_types.id;

SELECT products.name, product_types.type_name
FROM products RIGHT OUTER JOIN product_types
ON products.type_id = product_types.id;

SELECT products.name, product_types.type_name
FROM products FULL OUTER JOIN product_types
ON products.type_id = product_types.id;

SELECT products.name, product_types.type_name
FROM products CROSS JOIN product_types;
