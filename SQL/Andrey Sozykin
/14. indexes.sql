CREATE INDEX superheroes_name_idx
ON superheroes(name);

SELECT name, appearances, eye, hair
FROM superheroes
WHERE name = 'Iron Man (Anthony \"Tony\" Stark)';

CREATE INDEX superheroes_appearances_index
ON superheroes(appearances DESC);

SELECT *
FROM superheroes
ORDER BY appearances DESC;

CREATE INDEX person_name_index
ON person(last_name, first_name);

-- index works for both or for the first one
SELECT *
FROM person
WHERE last_name = 'Sozykin' AND first_name = 'Andrey';

DROP INDEX person_name_index;
