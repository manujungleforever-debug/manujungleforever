UPDATE tours SET nombre = REPLACE(nombre, '  -  ', ' - ');
UPDATE departures SET tour_nombre = REPLACE(tour_nombre, '  -  ', ' - ');
UPDATE testimonials SET tour_nombre = REPLACE(tour_nombre, '  -  ', ' - ');
