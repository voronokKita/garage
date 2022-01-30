SELECT *
FROM superheroes
WHERE gender = 'Female Characters';

SELECT *
FROM superheroes
WHERE year BETWEEN 2000 AND 2005;

SELECT *
FROM superheroes
WHERE hair IN
  ('Strawberry Blond Hair', 'Red Hair', 'Auburn Hair');

SELECT *
FROM superheroes
WHERE hair LIKE '%Blond%';

SELECT *
FROM superheroes
WHERE gender = 'Female Characters'
  AND align = 'Bad Characters';

SELECT *
FROM superheroes
WHERE hair = 'Red Hair'
   OR hair = 'Strawberry Blond Hair'
   OR hair = 'Auburn Hair';

SELECT *
FROM superheroes
WHERE hair NOT IN
  ('Blond Hair', 'Black Hair', 'Brown Hair', 'Red Hair');
