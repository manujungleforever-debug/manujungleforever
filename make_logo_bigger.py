from PIL import Image
import os
import re

# 1. Crop logo to remove transparent padding
img_path = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\img\logo.png"
if os.path.exists(img_path):
    img = Image.open(img_path).convert("RGBA")
    # Get bounding box of non-transparent pixels
    bbox = img.getbbox()
    if bbox:
        # Crop to the bounding box
        cropped_img = img.crop(bbox)
        cropped_img.save(img_path, "PNG")
        print("Logo cropped successfully!")
    else:
        print("Logo was completely empty/transparent?")

# 2. Update new.css to make the logo larger
css_file = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\css\new.css"
if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()
    
    # Increase logo height
    css = re.sub(r'\.nl img\{height:\d+px;', '.nl img{height:80px;', css)
    
    # Decrease padding on .nl so the nav bar doesn't get too thick
    css = re.sub(r'\.nl\{.*?\}', '.nl{position:relative;display:flex;align-items:center;justify-content:center;padding:2px 10px;transition:all 0.4s ease;}', css, flags=re.DOTALL)
    
    with open(css_file, "w", encoding="utf-8") as f:
        f.write(css)
    print("CSS updated successfully!")
