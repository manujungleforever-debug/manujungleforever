file_path = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\contact\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    c = f.read()

# Remove 'r' class from the LEFT and RIGHT contact grid columns
# so they don't start with opacity:0 and invisible
old_left = '      <!-- LEFT: Contact Info -->\n      <div class="r">'
new_left = '      <!-- LEFT: Contact Info -->\n      <div>'
old_right = '      <!-- RIGHT: Inquiry Form -->\n      <div class="r">'
new_right = '      <!-- RIGHT: Inquiry Form -->\n      <div>'

c = c.replace(old_left, new_left)
c = c.replace(old_right, new_right)

# Also fix the WA CTA message (remove "Anna" reference)
c = c.replace("Message Anna on WhatsApp for instant answers about tours, dates and availability.",
              "Message us on WhatsApp for instant answers about tours, dates and availability.")

# Fix WA number in contact info card (line 131 area)
c = c.replace("+51 923 289 231 (Anna's WhatsApp)", "+51 901 525 679")
c = c.replace("phone=51923289231", "phone=51901525679")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed contact page visibility")
