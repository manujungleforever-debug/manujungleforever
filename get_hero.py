import urllib.request
import re

url = "https://www.hiddenjunglecusco.com/about-2/"
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    # Find all post-*.css urls
    css_links = re.findall(r'href=["\'](.*?/css/post-.*?\.css.*?)["\']', html)
    for link in css_links:
        link = link.split('?')[0]
        print("CSS Link:", link)
        req_css = urllib.request.Request(link, headers=headers)
        with urllib.request.urlopen(req_css) as resp_css:
            css_content = resp_css.read().decode('utf-8')
            # Look for 5131a13e background image
            matches = re.findall(r'5131a13e.*?background-image:url\((.*?)\)', css_content)
            if matches:
                print("Found match:", matches)
except Exception as e:
    print("Error:", e)
