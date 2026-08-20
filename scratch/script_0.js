
window.addEventListener('error', function(e) {
  const mc = document.getElementById('mc') || document.body;
  if(mc) {
    mc.innerHTML = '<div style="padding:40px;max-width:600px;margin:40px auto;background:#fff;border-radius:12px;box-shadow:0 10px 25px rgba(0,0,0,0.1);text-align:center"><h2 style="color:#ef4444;margin-bottom:10px">❌ Error Crítico del Panel</h2><p style="color:#64748b;margin-bottom:20px">El sistema no pudo renderizar esta vista debido a un error interno.</p><div style="text-align:left;background:#0f172a;color:#cbd5e1;padding:15px;border-radius:8px;font-family:monospace;font-size:12px;overflow-x:auto;margin-bottom:20px">' + (e.error ? e.error.stack : e.message) + '</div><button onclick="location.reload()" style="background:#0d9488;color:#fff;border:none;padding:10px 20px;border-radius:8px;cursor:pointer;font-weight:600">Recargar Panel</button></div>';
  }
});
