import os

def clean_mojibake(content):
    # Standard Spanish mojibake replacements caused by UTF-8 to CP1252 / ISO-8859-1 conversion
    mapping = [
        ('N┬░', 'N°'),
        ('┬░', '°'),
        ('C├│digo', 'Código'),
        ('Protecci├│n', 'Protección'),
        ('Raz├│n', 'Razón'),
        ('Direcci├│n', 'Dirección'),
        ('Per├║', 'Perú'),
        ('├í', 'á'),
        ('├®', 'é'),
        ('├¡', 'í'),
        ('├│', 'ó'),
        ('├║', 'ú'),
        ('├▒', 'ñ'),
        ('├æ', 'Ñ'),
        ('├ü', 'Á'),
        ('├ë', 'É'),
        ('├Í', 'Í'),
        ('├ô', 'Ó'),
        ('├Ü', 'Ú'),
        ('┬┐', '¿'),
        ('┬í', '¡')
    ]
    for k, v in mapping:
        content = content.replace(k, v)
    return content

# Clean original_libro.html if present
if os.path.exists('original_libro.html'):
    with open('original_libro.html', 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    c = clean_mojibake(c)
    with open('original_libro.html', 'w', encoding='utf-8', newline='\n') as f:
        f.write(c)
    print("original_libro.html cleaned.")
