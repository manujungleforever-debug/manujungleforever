import re

file_path = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\about-2\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace mentions of Moises and Anna in the story intro
content = content.replace("where Moises and his 5 sisters all grew up.", "where Jordy and his family grew up.")
content = content.replace("Moises has been a professional tour guide", "Jordy has been a professional tour guide")
content = content.replace("Anna’s enthusiasm for travel, they started this project together.", "Gloria’s dedication to conservation, they operate this project together.")
content = content.replace("Anna?Ts enthusiasm for travel, they started this project together.", "Gloria's dedication to conservation, they operate this project together.")
content = content.replace("When Anna first visited Nuevo Eden, she had already traveled to Manu as a tourist.", "When Gloria joined the project, she brought her deep knowledge of the region to every itinerary.")
content = content.replace("Whereas her trip as a tourist was strictly nature-focused,\n                  this trip was a complete immersion into a totally different life. Yet, she was in the same little slice\n                  of paradise in the Peruvian Amazon. When she experienced exactly what the jungle entails, and witnessed\n                  what an incredible experience could be crafted for visitors, the project was born.", "Her focus on genuine immersion creates a truly unforgettable experience for visitors.")
content = content.replace("Tour guide Moises Llaqui teaches", "Tour guide Jordy teaches")


# Let's find the start of the first team member
start_first = content.find('<!-- Team Member')
if start_first != -1:
    # Find the end of the team section (which is before the <hr> and Destinations)
    end_last = content.find('<hr style=\'border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 60px 0;\'>\n          <h2 class=\'h2 r r-up\' style=\'text-align:center; margin-bottom:60px;\'>Destinations</h2>', start_first)
    
    if end_last != -1:
        new_team_html = """<!-- Team Member (Jordy) -->
          <div class="split-row team-row r r-up"
            style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 60px; margin-bottom: 80px; align-items: start;">
            <div class="split-left rl">
              <img src='../assets/img/hero.png'
                alt='Tour Guide Jordy teaches travelers about the jungle' class='anim-img'
                style='width:100%; border-radius:24px; box-shadow: 0 15px 35px rgba(0,0,0,0.4);'>
            </div>
            <div class="split-right rr">
              <h3 class='h3' style='margin-bottom:4px;'>Jordy Leonidas LLaqui</h3>
              <span class='role'
                style='display:block; color:var(--a); font-weight:600; text-transform:uppercase; font-size:0.85rem; letter-spacing:0.05em; margin-bottom:16px;'>Principal Tour Guide</span>
              <div class='tour-rich-text' style='font-size:0.95rem;'>
                <p>He was born on August 1994 and grew up in the Manu National Park. He and his family used the abundant
                  resources around them to live and prosper in the jungle, embracing the nature around them, and learning
                  how to navigate the challenges as well. He went to primary school in the area, then moved to Cusco
                  where he studied Tourism at the Instituto Americana de Turismo. As a jungle specialist, Jordy is very
                  knowledgeable about the many species of birds in Peru, animals, plants, insects, and all wildlife. His
                  goal is help to conserve and preserve the jungle and is passionate about sharing and teaching people
                  about nature and the world in Manu National Park.</p>
              </div>
            </div>
          </div>

          <!-- Team Member (Gloria) -->
          <div class="split-row team-row r r-up"
            style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 60px; margin-bottom: 80px; align-items: start;">
            <div class="split-left rl">
              <img src='../assets/img/hero.png'
                alt='Gloria, Administration and Coordination' class='anim-img'
                style='width:100%; border-radius:24px; box-shadow: 0 15px 35px rgba(0,0,0,0.4);'>
            </div>
            <div class="split-right rr">
              <h3 class='h3' style='margin-bottom:4px;'>Gloria</h3>
              <span class='role'
                style='display:block; color:var(--a); font-weight:600; text-transform:uppercase; font-size:0.85rem; letter-spacing:0.05em; margin-bottom:16px;'>Administration & Adventure Coordinator</span>
              <div class='tour-rich-text' style='font-size:0.95rem;'>
                <p>Gloria is a passionate advocate for the Peruvian Amazon, deeply connected to the natural wonders of the Manu region. Growing up surrounded by the rich biodiversity of the cloud forest, she developed an early love for nature and a strong commitment to its preservation.</p>
                <p>With years of experience in eco-tourism, Gloria now coordinates all adventures for Manu Jungle Forever. Her meticulous planning ensures that every traveler enjoys a safe, seamless, and authentic experience while respecting the delicate balance of the rainforest. She believes that tourism, when done right, is the ultimate tool for conservation.</p>
              </div>
            </div>
          </div>
          """
        content = content[:start_first] + new_team_html + content[end_last:]
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated team members successfully!")
    else:
        print("Could not find Destinations section to end replacement.")
else:
    print("Could not find Team Member section.")
