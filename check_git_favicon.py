import subprocess

r = subprocess.run(['git','show','HEAD:www.manujungleforever.com/index.html'], capture_output=True, text=True, cwd=r'g:\Git\MANUJUNGLEFOREVER')
c = r.stdout
idx = c.find('rel="icon"')
print("Favicon in last commit:", c[idx:idx+80])
print("favicon2 in last commit:", 'favicon2' in c)
