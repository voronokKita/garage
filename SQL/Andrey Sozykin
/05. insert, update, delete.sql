INSERT INTO superheroes (name, appearances, universe)
VALUES ('Spider-Man', 4043, 'marvel');

UPDATE superheroes
SET name = 'Batman',
    universe = 'dc'
WHERE id = 1;

UPDATE superheroes
SET gender = 'Man'
WHERE gender = 'Male Characters';

DELETE FROM superheroes
WHERE id = 2;

DELETE FROM superheroes;
