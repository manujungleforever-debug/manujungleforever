import re
import os

files = [
    "www.manujungleforever.com/index.php",
    "www.manujungleforever.com/index.html"
]

testimonials_html = '''<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-top: 20px;">
        <!-- Testimonial 1 -->
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 32px; text-align: left; transition: transform 0.3s; cursor: default;">
            <div style="color: #c9a84c; margin-bottom: 16px; font-size: 1.1rem;">
                <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
            </div>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.7; margin-bottom: 24px;">"An absolutely incredible experience. The guides were deeply knowledgeable and passionate about the rainforest. We saw giant river otters, caimans, and countless macaws. The lodge was rustic but perfectly comfortable. Highly recommend this local agency!"</p>
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 40px; height: 40px; background: rgba(34, 211, 238, 0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #22d3ee; font-weight: bold;">J</div>
                <div>
                    <div style="color: #fff; font-weight: 600; font-size: 0.95rem;">James W.</div>
                    <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">United Kingdom</div>
                </div>
            </div>
        </div>
        
        <!-- Testimonial 2 -->
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 32px; text-align: left; transition: transform 0.3s; cursor: default;">
            <div style="color: #c9a84c; margin-bottom: 16px; font-size: 1.1rem;">
                <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
            </div>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.7; margin-bottom: 24px;">"The highlight of our Peru trip! Going deep into the Amazon with indigenous guides made all the difference. We felt completely safe while being totally immersed in nature. The night walks through the jungle were mind-blowing. Thank you for everything!"</p>
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 40px; height: 40px; background: rgba(34, 211, 238, 0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #22d3ee; font-weight: bold;">S</div>
                <div>
                    <div style="color: #fff; font-weight: 600; font-size: 0.95rem;">Sarah T.</div>
                    <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">United States</div>
                </div>
            </div>
        </div>

        <!-- Testimonial 3 -->
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 32px; text-align: left; transition: transform 0.3s; cursor: default;">
            <div style="color: #c9a84c; margin-bottom: 16px; font-size: 1.1rem;">
                <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
            </div>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.7; margin-bottom: 24px;">"If you want to see untouched wilderness, this is the company to book with. No crowded tourist traps, just pure Amazon. The food was surprisingly fantastic, and seeing a jaguar resting on the riverbank is a memory I will cherish forever."</p>
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 40px; height: 40px; background: rgba(34, 211, 238, 0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #22d3ee; font-weight: bold;">M</div>
                <div>
                    <div style="color: #fff; font-weight: 600; font-size: 0.95rem;">Matteo C.</div>
                    <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">Italy</div>
                </div>
            </div>
        </div>
    </div>'''

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Change the title from "Google Reviews" to "Traveler Testimonials"
        content = content.replace('<h2 class="h2">Google Reviews</h2>', '<h2 class="h2">Traveler Testimonials</h2>')

        # Replace the placeholder with the new testimonials grid
        new_content = re.sub(
            r'<div style="padding: 40px; background: rgba\(255,255,255,0\.05\).*?</div>\s*</div>',
            testimonials_html + '\n    </div>',
            content,
            flags=re.DOTALL
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
