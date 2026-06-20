import os

def update_colors(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    # Replace colors
    new_content = new_content.replace('#39ff6a', '#4aa18e')
    new_content = new_content.replace('#39FF6A', '#4aa18e')
    new_content = new_content.replace('rgba(57,255,106', 'rgba(74,161,142')
    new_content = new_content.replace('rgba(57, 255, 106', 'rgba(74, 161, 142')
    new_content = new_content.replace('#0a1a0f', '#002e24')
    new_content = new_content.replace('#0A1A0F', '#002e24')
    new_content = new_content.replace('#030805', '#001c16')
    new_content = new_content.replace('rgba(3,8,5', 'rgba(0,28,22')
    new_content = new_content.replace('rgba(3, 8, 5', 'rgba(0, 28, 22')

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

def main():
    root_dir = r"g:\Git\HiddenJungleCusco\www.hiddenjunglecusco.com"
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                update_colors(os.path.join(subdir, file))

if __name__ == '__main__':
    main()
