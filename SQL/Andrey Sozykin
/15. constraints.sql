CREATE TABLE superheroes(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  align VARCHAR(30),
  eye VARCHAR(30),
  hair VARCHAR(30),
  gender VARCHAR(30),
  appearances INT NOT NULL,
  year INT NOT NULL,
  universe VARCHAR(10)
);

CREATE TABLE sales(
  product_id INT,
  order_id INT,
  quantity INT,
  PRIMARY KEY(product_id, order_id)
);

CREATE TABLE products(
  id PRIMARY KEY,
  name VARCHAR(100),
  type_id INT,
  price INT CHECK (price >= 0)
);

CREATE TABLE products(
  id PRIMARY KEY,
  name VARCHAR(100),
  type_id INT,
  price INT CONSTRAINT positive_price
            CHECK (price >= 0)
);

CREATE TABLE products(
  id PRIMARY KEY,
  name VARCHAR(100),
  type_id INT,
  CONSTRAINT positive_price CHECK (price >= 0)
);

CREATE TABLE products(
  id PRIMARY KEY,
  name VARCHAR(100),
  type_id INT REFERENCES product_types(id)
              ON DELETE RESTRICT
              ON UPDATE CASCADE,
  price INT
);

CREATE TABLE products(
  id PRIMARY KEY,
  name VARCHAR(100),
  type_id INT,
  price INT,
  FOREIGN KEY(type_id) REFERENCES product_types(id)
);

CREATE TABLE sales(
  product_id INT REFERENCES products(id),
  order_id INT REFERENCES orders(id),
  quantity INT,
  PRIMARY KEY(product_id, order_id)
);
