
UPDATE blog_posts 
SET imagen_hero = REPLACE(imagen_hero, 'https://pub-2e90c74b49be4b3eb0b9aeb69c6fc38f.r2.dev', '/api/media/file')
WHERE imagen_hero LIKE '%pub-2e90c74b49be4b3eb0b9aeb69c6fc38f.r2.dev%';

UPDATE blog_posts 
SET contenido = REPLACE(contenido, 'https://pub-2e90c74b49be4b3eb0b9aeb69c6fc38f.r2.dev', '/api/media/file')
WHERE contenido LIKE '%pub-2e90c74b49be4b3eb0b9aeb69c6fc38f.r2.dev%';
