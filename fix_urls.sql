
UPDATE users 
SET foto = REPLACE(foto, 'https://pub-2e90c74b49be4b3eb0b9aeb69c6fc38f.r2.dev', '/api/media/file')
WHERE foto LIKE '%pub-2e90c74b49be4b3eb0b9aeb69c6fc38f.r2.dev%';

UPDATE blog 
SET cover = REPLACE(cover, 'https://pub-2e90c74b49be4b3eb0b9aeb69c6fc38f.r2.dev', '/api/media/file')
WHERE cover LIKE '%pub-2e90c74b49be4b3eb0b9aeb69c6fc38f.r2.dev%';

UPDATE blog 
SET contenido = REPLACE(contenido, 'https://pub-2e90c74b49be4b3eb0b9aeb69c6fc38f.r2.dev', '/api/media/file')
WHERE contenido LIKE '%pub-2e90c74b49be4b3eb0b9aeb69c6fc38f.r2.dev%';
