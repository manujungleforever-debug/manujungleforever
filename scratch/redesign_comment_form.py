import glob
import re

NEW_COMMENT_SECTION = '''<!-- COMMENT FORM -->
<section class="comment-section-area" style="background:var(--k, #F5F0E8); padding:80px 0 100px;">
<div class="cx">
<div class="comment-card-modern" style="max-width:860px; margin:0 auto; background:#FFFFFF; border:1px solid rgba(13,38,28,0.08); border-radius:24px; padding:48px 52px; box-shadow:0 16px 45px -10px rgba(7,24,17,0.07), 0 2px 8px rgba(7,24,17,0.03); position:relative; overflow:hidden;">
  <div style="position:absolute; top:0; left:0; right:0; height:4px; background:linear-gradient(90deg, #2dd4bf 0%, #0d9488 50%, #065f46 100%);"></div>
  <div style="margin-bottom:32px;">
    <div style="display:inline-flex; align-items:center; gap:8px; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:#0d9488; background:rgba(13,148,136,0.08); border:1px solid rgba(13,148,136,0.2); padding:5px 14px; border-radius:20px; margin-bottom:14px;">
      <i class="fas fa-comments"></i> Community &amp; Travelers
    </div>
    <h2 style="font-family:'Syne',sans-serif; font-size:clamp(1.6rem, 2.5vw, 2.1rem); font-weight:800; color:#071811; margin:0 0 10px; letter-spacing:-0.02em;">
      Leave a Comment
    </h2>
    <p style="color:#64748B; margin:0; font-size:0.98rem; line-height:1.6; max-width:640px;">
      We'd love to hear your thoughts! Share your questions, impressions, or travel experiences in Manu National Park.
    </p>
  </div>
  <form id="comment-form" onsubmit="submitComment(event)" style="display:flex; flex-direction:column; gap:22px;">
    <div class="comment-grid-2" style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
      <div>
        <label for="cf-name" style="display:block; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.06em; color:#0B241C; font-weight:700; margin-bottom:8px;">
          Your Name <span style="color:#0d9488;">*</span>
        </label>
        <div style="position:relative;">
          <input id="cf-name" name="name" placeholder="e.g. Maria Garcia" required="" type="text"
            style="width:100%; background:#F8FAF9; border:1.5px solid #E2E8F0; border-radius:12px; padding:14px 16px 14px 42px; color:#0F172A; font-size:0.95rem; font-family:inherit; outline:none; transition:all 0.25s ease; box-sizing:border-box;"
            onfocus="this.style.borderColor='#0d9488'; this.style.background='#FFFFFF'; this.style.boxShadow='0 0 0 4px rgba(13,148,136,0.12)';"
            onblur="this.style.borderColor='#E2E8F0'; this.style.background='#F8FAF9'; this.style.boxShadow='none';" />
          <i class="fas fa-user" style="position:absolute; left:15px; top:50%; transform:translateY(-50%); color:#94A3B8; font-size:0.9rem; pointer-events:none;"></i>
        </div>
      </div>
      <div>
        <label for="cf-email" style="display:block; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.06em; color:#0B241C; font-weight:700; margin-bottom:8px;">
          Email Address <span style="color:#0d9488;">*</span>
        </label>
        <div style="position:relative;">
          <input id="cf-email" name="email" placeholder="your@email.com" required="" type="email"
            style="width:100%; background:#F8FAF9; border:1.5px solid #E2E8F0; border-radius:12px; padding:14px 16px 14px 42px; color:#0F172A; font-size:0.95rem; font-family:inherit; outline:none; transition:all 0.25s ease; box-sizing:border-box;"
            onfocus="this.style.borderColor='#0d9488'; this.style.background='#FFFFFF'; this.style.boxShadow='0 0 0 4px rgba(13,148,136,0.12)';"
            onblur="this.style.borderColor='#E2E8F0'; this.style.background='#F8FAF9'; this.style.boxShadow='none';" />
          <i class="fas fa-envelope" style="position:absolute; left:15px; top:50%; transform:translateY(-50%); color:#94A3B8; font-size:0.9rem; pointer-events:none;"></i>
        </div>
      </div>
    </div>
    <div>
      <label for="cf-comment" style="display:block; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.06em; color:#0B241C; font-weight:700; margin-bottom:8px;">
        Comment <span style="color:#0d9488;">*</span>
      </label>
      <div style="position:relative;">
        <textarea id="cf-comment" name="comment" placeholder="Share your thoughts, questions or experiences..." required="" rows="5"
          style="width:100%; background:#F8FAF9; border:1.5px solid #E2E8F0; border-radius:12px; padding:14px 16px 14px 42px; color:#0F172A; font-size:0.95rem; font-family:inherit; outline:none; resize:vertical; min-height:130px; line-height:1.6; transition:all 0.25s ease; box-sizing:border-box;"
          onfocus="this.style.borderColor='#0d9488'; this.style.background='#FFFFFF'; this.style.boxShadow='0 0 0 4px rgba(13,148,136,0.12)';"
          onblur="this.style.borderColor='#E2E8F0'; this.style.background='#F8FAF9'; this.style.boxShadow='none';"></textarea>
        <i class="fas fa-pen-nib" style="position:absolute; left:15px; top:18px; color:#94A3B8; font-size:0.9rem; pointer-events:none;"></i>
      </div>
    </div>
    <div style="display:flex; flex-direction:column; align-items:flex-start; gap:14px; margin-top:4px;">
      <button class="comment-submit-btn" type="submit"
        style="background:linear-gradient(135deg, #0d9488 0%, #065f46 100%); color:#FFFFFF; font-weight:700; font-size:1rem; border-radius:50px; border:none; padding:15px 36px; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; gap:10px; box-shadow:0 8px 20px rgba(13,148,136,0.25); transition:all 0.25s ease; font-family:inherit;"
        onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 12px 26px rgba(13,148,136,0.35)';"
        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 20px rgba(13,148,136,0.25)';">
        <i class="fas fa-paper-plane" style="font-size:0.95rem;"></i> Post Comment
      </button>
      <div style="display:flex; align-items:center; gap:8px; color:#64748B; font-size:0.83rem;">
        <i class="fas fa-shield-halved" style="color:#0d9488; font-size:0.9rem;"></i>
        <span>Your email address will remain private and will not be published. Required fields marked with <strong style="color:#0d9488;">*</strong></span>
      </div>
    </div>
  </form>
  <div id="comment-sent" style="display:none; background:rgba(16,185,129,0.08); border:1.5px solid rgba(16,185,129,0.3); border-radius:14px; padding:22px 26px; color:#065f46; margin-top:24px; align-items:center; gap:14px; font-weight:600; font-size:0.98rem;">
    <i class="fas fa-circle-check" style="font-size:1.6rem; color:#10b981; flex-shrink:0;"></i>
    <div>
      <div style="color:#047857; font-weight:700; font-size:1.05rem; margin-bottom:2px;">Thank you for your comment!</div>
      <div style="color:#475569; font-weight:400; font-size:0.9rem;">We appreciate you sharing your thoughts. Our team will review and publish it shortly.</div>
    </div>
  </div>
</div>
</div>
</section>'''

pattern = re.compile(r'<!-- COMMENT FORM -->\s*<section[\s\S]*?</section>', re.MULTILINE)

target_files = glob.glob('www.manujungleforever.com/**/*.html', recursive=True)
updated = []

for fpath in target_files:
    if 'admin' in fpath or 'wp-content' in fpath:
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<!-- COMMENT FORM -->' in content:
        new_content, count = pattern.subn(NEW_COMMENT_SECTION, content)
        if count > 0:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated.append(fpath)

print(f"Updated {len(updated)} files:")
for u in updated:
    print(f" - {u}")
