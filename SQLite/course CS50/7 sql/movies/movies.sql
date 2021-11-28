/*  CS50 PSet 7: Movies
    Write SQLite3 queries to answer questions about a database of movies from IMDb. */


/* Query 1: lists the titles of all movies released in 2008. */
SELECT title FROM movies WHERE year = 2008;


/* Query 2: determine the birth year of Emma Stone. */
SELECT birth FROM people WHERE name = "Emma Stone";


/* Query 3: lists the titles of all movies with a
   release date on or after 2018, in alphabetical order. */
SELECT title FROM movies WHERE year >= 2018 ORDER BY title ASC;


/* Query 4: determine the number of movies with an IMDb rating of 10.0. */
SELECT COUNT(*) FROM ratings WHERE rating = 10.0;


/* Query 5: lists the titles and release years of all
   Harry Potter movies, in chronological order. */
SELECT title, year FROM movies WHERE title LIKE "Harry Potter%" ORDER BY year ASC;


/* Query 6: determine the average rating of all movies released in 2012. */
SELECT AVG(rating) FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE year = 2012;


/* Query 7: lists all movies released in 2010 and their ratings, in descending order by rating.
   For movies with the same rating, order them alphabetically by title. */
SELECT title, rating FROM movies
INNER JOIN ratings ON movies.id = ratings.movie_id
WHERE year = 2010
ORDER BY rating DESC, title ASC;


/* Query 8: lists the names of all people who starred in Toy Story. */
SELECT name FROM stars
JOIN movies ON stars.movie_id = movies.id
JOIN people ON stars.person_id = people.id
WHERE title = "Toy Story";


/* Query 9: lists the names of all people who
   starred in a movie released in 2004, ordered by birth year. */
SELECT DISTINCT name FROM stars
JOIN movies ON stars.movie_id = movies.id
JOIN people ON stars.person_id = people.id
WHERE year = 2004
ORDER BY birth;


/* Query 10: lists the names of all people who have
   directed a movie that received a rating of at least 9.0. */
SELECT DISTINCT name FROM directors
JOIN movies ON directors.movie_id = movies.id
JOIN ratings ON directors.movie_id = ratings.movie_id
JOIN people ON directors.person_id = people.id
WHERE rating >= 9.0;


/* Query 11: lists the titles of the five highest rated movies (in order) that
   Chadwick Boseman starred in, starting with the highest rated. */
SELECT title FROM stars
JOIN movies ON stars.movie_id = movies.id
JOIN ratings ON stars.movie_id = ratings.movie_id
JOIN people ON stars.person_id = people.id
WHERE name = "Chadwick Boseman"
ORDER BY rating DESC
LIMIT 5;


/* Query 12: lists the titles of all movies in which
   both Johnny Depp and Helena Bonham Carter starred. */
SELECT title FROM stars
JOIN movies ON stars.movie_id = movies.id
JOIN people ON stars.person_id = people.id
WHERE name = "Johnny Depp"
INTERSECT
SELECT title FROM stars
JOIN movies ON stars.movie_id = movies.id
JOIN people ON stars.person_id = people.id
WHERE name = "Helena Bonham Carter";


/* Query 13: lists the names of all people who
   starred in a movie in which Kevin Bacon also starred. */
SELECT DISTINCT name FROM stars
JOIN movies ON stars.movie_id = movies.id
JOIN people ON stars.person_id = people.id
WHERE title IN (
    SELECT DISTINCT title FROM stars
    JOIN movies ON stars.movie_id = movies.id
    JOIN people ON stars.person_id = people.id
    WHERE name = "Kevin Bacon" AND birth = 1958
) AND name != "Kevin Bacon";
