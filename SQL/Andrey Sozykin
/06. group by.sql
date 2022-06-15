SELECT gender, COUNT(*)
FROM superheroes
GROUP BY gender;

SELECT align, COUNT(*)
FROM superheroes
GROUP BY align;

SELECT universe, align, COUNT(*)
FROM superheroes
GROUP BY universe, align;

SELECT hair, COUNT(*)
FROM superheroes
WHERE gender = 'Female Characters'
GROUP BY hair
ORDER BY COUNT(*) DESC
LIMIT 5;
