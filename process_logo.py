from PIL import Image
import os

img_path = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\img\logo.png"

if os.path.exists(img_path):
    img = Image.open(img_path).convert("RGBA")
    data = img.getdata()
    
    new_data = []
    for item in data:
        # item is (R, G, B, A)
        
        # If the pixel is very close to white, make it fully transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        # If the pixel is very dark (like black text), make it white so it shows on dark background
        elif item[0] < 50 and item[1] < 50 and item[2] < 50:
            new_data.append((255, 255, 255, item[3]))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(img_path, "PNG")
    print("Logo processed successfully!")
else:
    print("Logo not found.")
