import os

files = [
    "www.manujungleforever.com/index.php",
    "www.manujungleforever.com/index.html",
    "www.manujungleforever.com/about-2/index.html"
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace full name with just the first name
        new_content = content.replace("Jordy Leonidas Llaqui Chusi", "Jordy")

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
