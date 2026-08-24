PRAGMA foreign_keys = OFF;
DELETE FROM departures WHERE id = '012';
UPDATE departures SET id = UPPER(id) WHERE id LIKE 'dep-%';
UPDATE passengers SET departure_id = UPPER(departure_id) WHERE departure_id LIKE 'dep-%';
PRAGMA foreign_keys = ON;
