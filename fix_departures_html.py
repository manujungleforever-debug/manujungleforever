import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\departures\index.html'

with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

new_departures_html = """
    <div class="departures-container">
      <div class="dep-intro">
        <h2 class="h2">Upcoming Departures</h2>
        <p>Please contact us for information about coordinating a departure date! We can plan any of our pre-determined itineraries, customize a private trip, or organize an independant visit to Nuevo Eden.</p>
        <p>To plan your trip and get a price quote, please reach out to us and we’ll be happy to coordinate!</p>
      </div>

      <div class="dep-grid">
        <!-- May -->
        <div class="dep-card">
          <div class="dep-img" style="background-image: url('../assets/media_to_upload/photos/placeholder.jpg');"></div>
          <div class="dep-content">
            <h3>May 2026</h3>
            <ul class="dep-list">
              <li><i class="fas fa-calendar-alt"></i> <span><strong>5 Days Nuevo Eden:</strong> May 19 – 23</span></li>
            </ul>
          </div>
        </div>

        <!-- June -->
        <div class="dep-card">
          <div class="dep-img" style="background-image: url('../assets/media_to_upload/photos/placeholder.jpg');"></div>
          <div class="dep-content">
            <h3>June 2026</h3>
            <ul class="dep-list">
              <li><i class="fas fa-calendar-alt"></i> <span><strong>3 Days Machu Wasi:</strong> June 1 – 3</span></li>
              <li><i class="fas fa-calendar-alt"></i> <span><strong>4 Days (TBC):</strong> June 29 – July 2</span></li>
            </ul>
          </div>
        </div>

        <!-- July -->
        <div class="dep-card">
          <div class="dep-img" style="background-image: url('../assets/media_to_upload/photos/placeholder.jpg');"></div>
          <div class="dep-content">
            <h3>July 2026</h3>
            <ul class="dep-list">
              <li><i class="fas fa-calendar-alt"></i> <span><strong>3 Days Machu Wasi:</strong> July 16 – 18</span></li>
              <li><i class="fas fa-calendar-alt"></i> <span><strong>4 Days Nuevo Eden:</strong> July 22 – 25</span></li>
            </ul>
          </div>
        </div>

        <!-- August -->
        <div class="dep-card">
          <div class="dep-img" style="background-image: url('../assets/media_to_upload/photos/placeholder.jpg');"></div>
          <div class="dep-content">
            <h3>August 2026</h3>
            <ul class="dep-list">
              <li><i class="fas fa-calendar-alt"></i> <span><strong>6 Days Reserved Zone (TBC):</strong> Aug 2 – 7</span></li>
              <li><i class="fas fa-calendar-alt"></i> <span><strong>4/5 Days (TBC):</strong> Aug 6</span></li>
              <li><i class="fas fa-calendar-alt"></i> <span><strong>4 Days:</strong> Aug 12 – 15</span></li>
              <li><i class="fas fa-calendar-alt"></i> <span><strong>6 Days Reserved Zone:</strong> Aug 14 – 19</span></li>
            </ul>
          </div>
        </div>

        <!-- September -->
        <div class="dep-card">
          <div class="dep-img" style="background-image: url('../assets/media_to_upload/photos/placeholder.jpg');"></div>
          <div class="dep-content">
            <h3>September 2026</h3>
            <ul class="dep-list">
              <li><i class="fas fa-calendar-alt"></i> <span><strong>5 Days Nuevo Eden:</strong> Sept 17 – 21</span></li>
            </ul>
          </div>
        </div>

        <!-- October -->
        <div class="dep-card">
          <div class="dep-img" style="background-image: url('../assets/media_to_upload/photos/placeholder.jpg');"></div>
          <div class="dep-content">
            <h3>October 2026</h3>
            <ul class="dep-list">
              <li><i class="fas fa-calendar-alt"></i> <span><strong>5 Days Nuevo Eden:</strong> Oct 26 – 30</span></li>
            </ul>
          </div>
        </div>
      </div>

      <div class="dep-cta">
        <h4>To join a trip, or inquire about new dates, please fill out our inquiry form. Vamos a la selva!</h4>
        <a href="https://forms.gle/e8sNMmNh1HvtUYgu7" class="btn ba" target="_blank"><i class="fas fa-envelope"></i> JOIN A TRIP - INQUIRE TODAY!</a>
      </div>
    </div>
"""

# Replace the content of the <div class="article-w"...> ... </div> with the new HTML.
# We'll use regex to find <div class="article-w" ...> up to the end of its enclosing section.
pattern = re.compile(r'<div class="article-w".*?</div>\s*</div>\s*</section>', re.DOTALL)

replacement = f"{new_departures_html}\n    </div>\n  </section>"

if pattern.search(html):
    html = pattern.sub(replacement, html)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Departures HTML rewritten.")
else:
    print("Could not find article-w block in departures.")
