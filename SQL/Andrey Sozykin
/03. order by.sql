SELECT *
FROM superheroes
ORDER BY year DESC;

SELECT *
FROM superheroes
WHERE align == 'Bad Characters'
  AND gender = 'Female Characters'
ORDER BY appearances DESC
LIMIT 5;

SELECT *
FROM superheroes
ORDER BY year, appearances;
