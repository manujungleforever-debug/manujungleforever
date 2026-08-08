import re
import os

# Update index.php and index.html
files = [
    "www.manujungleforever.com/index.php",
    "www.manujungleforever.com/index.html"
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Update testimonial 1
        content = content.replace(
            "The guides were deeply knowledgeable and passionate",
            "Our lead guide, Jordy Leonidas Llaqui Chusi, was deeply knowledgeable and passionate"
        )
        # Update testimonial 2
        content = content.replace(
            "with indigenous guides made all the difference",
            "with Jordy made all the difference"
        )
        
        # Update footer or intro if it exists
        content = content.replace(
            "Founded by indigenous experts who have spent their entire lives",
            "Founded by Jordy Leonidas Llaqui Chusi and our team of indigenous experts who have spent their entire lives"
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

# Update about-2/index.html
about_file = "www.manujungleforever.com/about-2/index.html"
if os.path.exists(about_file):
    with open(about_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Update About page text
    content = content.replace(
        "We are a dedicated local family",
        "Led by owner and head guide Jordy Leonidas Llaqui Chusi, we are a dedicated local family"
    )

    content = content.replace(
        "Our guides are born and raised in the jungle.",
        "Our team, directed by Jordy Leonidas Llaqui Chusi, is born and raised in the jungle."
    )

    with open(about_file, "w", encoding="utf-8") as f:
        f.write(content)
