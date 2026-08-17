import codecs

path = r'g:\Git\MANUJUNGLEFOREVER\functions\api\reclamo.js'
with codecs.open(path, 'r', 'utf-8') as f:
    js = f.read()

old_snippet = '''        <p style="text-align:center;margin-top:20px;font-size:12px;color:#777;">El documento PDF oficial se encuentra adjunto.</p>
      </div>`;'''

new_snippet = '''        <div style="text-align:center;margin-top:30px;margin-bottom:10px;">
          <a href="https://www.manujungleforever.com/admin/gestionar-reclamos" style="background-color:#10b981;color:#ffffff;text-decoration:none;padding:14px 28px;border-radius:6px;font-weight:bold;display:inline-block;font-size:14px;">Responder / Auditar Reclamo</a>
        </div>
        <p style="text-align:center;margin-top:20px;font-size:12px;color:#777;">El documento PDF oficial se encuentra adjunto.</p>
      </div>`;'''

js = js.replace(old_snippet, new_snippet)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(js)
