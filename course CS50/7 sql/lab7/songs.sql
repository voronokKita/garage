/*  CS50 Lab 7: Songs
    Write SQLite3 queries to answer questions about a database of songs from Spotify. */


/* Query 1: lists the names of all songs in the database. */
SELECT name FROM songs;


/* Query 2: lists the names of all songs in increasing order of tempo. */
SELECT name FROM songs ORDER BY tempo;


/* Query 3: lists the names of the top 5 longest songs, in descending order of length. */
SELECT name FROM songs ORDER BY duration_ms DESC LIMIT 5;


/* Query 4: lists the names of any songs that have
   danceability, energy, and valence greater than 0.75. */
SELECT name FROM songs WHERE danceability > 0.75 AND energy > 0.75 AND valence > 0.75;


/* Query 5: returns the average energy of all the songs. */
SELECT AVG(energy) FROM songs;


/* Query 6: lists the names of songs that are by Post Malone. */
SELECT name FROM songs WHERE artist_id = (
    SELECT id FROM artists WHERE name = 'Post Malone');


/* Query 7: returns the average energy of songs that are by Drake. */
SELECT AVG(energy) FROM songs WHERE artist_id = (
    SELECT id FROM artists WHERE name = 'Drake');


/* Query 8: lists the names of the songs that feature other artists. */
SELECT name FROM songs WHERE name LIKE '%feat.%';
