fetch('https://www.manujungleforever.com/api/booking', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
  },
  body: JSON.stringify({
    name: 'Prueba Logo',
    email: 'test@manujungleforever.com',
    phone: '+51999999999',
    tour: 'Tour de Prueba',
    travelers: '2',
    date: '2026-12-01',
    contact: 'Email',
    notes: 'Prueba del nuevo diseño de correo con logo grande.'
  })
})
.then(res => res.json())
.then(data => console.log('Success:', data))
.catch(err => console.error('Error:', err));
