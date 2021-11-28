/*  CS50 PSet 7: Fiftyville
    Write SQL queries to solve a mystery. */
/*
 *  The CS50 Duck has been stolen! The town of Fiftyville has called upon you to
 *  solve the mystery of the stolen duck. Authorities believe that the thief stole the duck and then,
 *  shortly afterwards, took a flight out of town with the help of an accomplice.
 *  Your goal is to identify:
 *      Who the thief is,
 *      What city the thief escaped to, and
 *      Who the thief’s accomplice is who helped them escape
 *  All you know is that the theft took place on July 28, 2020 and that it took place on Chamberlin Street.
 *
 *  Keep a log of any SQL queries you execute as you solve the mystery.
 */


.table
.schema crime_scene_reports
SELECT * FROM crime_scene_reports
WHERE year = 2020 and month = 7 and day = 28 and street = "Chamberlin Street";

/* 295: Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
Interviews were conducted today with three witnesses who were present at the time —
each of their interview transcripts mentions the courthouse. */

.schema interviews
SELECT * FROM interviews
WHERE year = 2020 and month = 7 and day = 28 and transcript LIKE '%courthouse%';

/* 161 Ruth: Sometime within ten minutes of the theft, I saw the thief get into a car in
the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot,
you might want to look for cars that left the parking lot in that time frame. */

.schema courthouse_security_logs
SELECT * FROM courthouse_security_logs
WHERE year = 2020 and month = 7 and day = 28 and hour = 10 and minute BETWEEN 15 and 25;
/*
license_plate
5P2BI95
94KL13X
6P58WS2
4328GD8
G412CB7
L93JTIZ
322W7JE
0NTHK55
*/

/* 162 Eugene: I don't know the thief's name, but it was someone I recognized.
Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on
Fifer Street and saw the thief there withdrawing some money. */

.schema atm_transactions
SELECT * FROM atm_transactions WHERE year = 2020 and month = 7 and day = 28
and atm_location = 'Fifer Street' and transaction_type = 'withdraw';
/*
account_number
28500762
28296815
76054385
49610011
16153065
25506511
81061156
26013199
*/

.schema bank_accounts
SELECT * FROM bank_accounts WHERE account_number IN (
    SELECT account_number FROM atm_transactions WHERE year = 2020 and month = 7 and day = 28
    and atm_location = 'Fifer Street' and transaction_type = 'withdraw'
);
/*
account_number | person_id
28500762       | 467400
28296815       | 395717
76054385       | 449774
49610011       | 686048
16153065       | 458378
25506511       | 396669
81061156       | 438727
26013199       | 514354
*/

/* 163 Raymond: As the thief was leaving the courthouse, they called someone who talked to them
for less than a minute. In the call, I heard the thief say that they were planning to take the
earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone
to purchase the flight ticket. */

.schema phone_calls
SELECT * FROM phone_calls WHERE year = 2020 and month = 7 and day = 28 and duration <= 60;
/*
caller         | receiver
(130) 555-0289 | (996) 555-8899
(499) 555-9472 | (892) 555-8872
(367) 555-5533 | (375) 555-8161
(609) 555-5876 | (389) 555-5198
(499) 555-9472 | (717) 555-1342
(286) 555-6063 | (676) 555-6554
(770) 555-1861 | (725) 555-3243
(031) 555-6622 | (910) 555-3251
(826) 555-1652 | (066) 555-9701
(338) 555-6650 | (704) 555-2131
*/

.schema flights
SELECT * FROM flights WHERE year = 2020 and month = 7 and day = 29 ORDER BY hour, minute;
/*
id | origin_airport_id | destination_airport_id
36 | 8                 | 4
*/
.schema airports
SELECT * FROM airports WHERE id = 4;
/*
id | abbreviation | full_name        | city
4  | LHR          | Heathrow Airport | London
*/

.schema passengers
SELECT * FROM passengers WHERE flight_id = 36;
/*
passport_number
7214083635
1695452385
5773159633
1540955065
8294398571
1988161715
9878712108
8496433585
*/

.schema people

SELECT * FROM people WHERE
license_plate IN (
    SELECT license_plate FROM courthouse_security_logs
    WHERE year = 2020 and month = 7 and day = 28 and hour = 10 and minute BETWEEN 15 and 25
) and
id IN (
    SELECT person_id FROM bank_accounts
    JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
    WHERE year = 2020 and month = 7 and day = 28
    and atm_location = 'Fifer Street' and transaction_type = 'withdraw'
) and
phone_number IN (
    SELECT caller FROM phone_calls WHERE year = 2020 and month = 7 and day = 28 and duration <= 60
) and
passport_number IN (
    SELECT passport_number FROM passengers WHERE flight_id = 36
);
/*
id     | name   | phone_number   | passport_number | license_plate
686048 | Ernest | (367) 555-5533 | 5773159633      | 94KL13X
*/

SELECT * FROM people WHERE phone_number = '(375) 555-8161';
/*
id     | name     | phone_number   | passport_number | license_plate
864400 | Berthold | (375) 555-8161 |                 | 4V16VO0
*/
