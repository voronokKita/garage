SELECT hair, COUNT(*)
FROM superheroes
WHERE gender = 'Female Characters'
GROUP BY hair
HAVING COUNT(*) > 10;

SELECT hair, COUNT(*)
FROM superheroes
WHERE gender = 'Female Characters'
GROUP BY hair
HAVING COUNT(*) BETWEEN 50 AND 300;
