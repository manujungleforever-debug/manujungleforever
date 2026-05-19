import zipfile

z = zipfile.ZipFile('hts-cache/new.zip', 'r')
matches = []
for name in z.namelist():
    try:
        content = z.read(name)
        if b'sustainable industry for the rainforest' in content.lower():
            matches.append(name)
    except Exception:
        pass

print("Files containing 'sustainable industry for the rainforest':", matches)
