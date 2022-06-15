SELECT * FROM superheroes;

SELECT name, appearances
FROM superheroes;

-- alias
SELECT name AS hero_name,
       appearances
FROM superheroes;

-- unique values
SELECT DISTINCT(align)
FROM superheroes;

SELECT DISTINCT(hair)
FROM superheroes
LIMIT 10;
