UPDATE tours SET nombre = REPLACE(REPLACE(nombre, 'ÔÇô', ' - '), '–', ' - ');
UPDATE departures SET tour_nombre = REPLACE(REPLACE(tour_nombre, 'ÔÇô', ' - '), '–', ' - ');
UPDATE testimonials SET tour_nombre = REPLACE(REPLACE(tour_nombre, 'ÔÇô', ' - '), '–', ' - '), comentario = REPLACE(REPLACE(comentario, 'ÔÇô', ' - '), '–', ' - ');
UPDATE blog_posts SET titulo = REPLACE(REPLACE(titulo, 'ÔÇô', ' - '), '–', ' - ');
