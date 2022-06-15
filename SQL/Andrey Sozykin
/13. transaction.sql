START TRANSACTION;

UPDATE accounts
SET balance = balance - 15000
WHERE account_number = 1234567;

UPDATE accounts
SET balance = balance + 15000
WHERE account_number = 9876543;

COMMIT; --or ROLLBACK
