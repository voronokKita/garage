CREATE TABLE superheroes(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  align VARCHAR(30),
  eye VARCHAR(30),
  hair VARCHAR(30),
  gender VARCHAR(30),
  appearances INT,
  year INT,
  universe VARCHAR(10)
);

ALTER TABLE superheroes
ADD COLUMN alive BOOLEAN;

ALTER TABLE superheroes
DROP COLUMN year;

ALTER TABLE superheroes
RENAME COLUMN name TO hero_name;

ALTER TABLE superheroes RENAME TO comic_characters;
