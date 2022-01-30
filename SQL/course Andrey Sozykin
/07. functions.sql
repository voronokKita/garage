SELECT align, COUNT(*), SUM(appearances)
FROM superheroes
GROUP BY align;

SELECT align, AVG(appearances),
       SUM(appearances)/COUNT(*) AS average
FROM superheroes
GROUP BY align;

SELECT year, MIN(appearances),
       MAX(appearances) AS max_ap
FROM superheroes
GROUP BY year
ORDER BY max_ap DESC
LIMIT 5;

SELECT COUNT(*),
       MIN(appearances),
       MAX(appearances),
       SUM(appearances),
       AVG(appearances)
FROM superheroes;
