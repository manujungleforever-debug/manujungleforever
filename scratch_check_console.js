const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.log('CONSOLE ERROR:', msg.text());
    }
  });

  page.on('pageerror', error => {
    console.log('PAGE ERROR:', error.message);
  });

  // Since it's protected by auth, we first need to navigate to login and set the session storage
  await page.goto('https://www.manujungleforever.com/admin/index.html');
  
  await page.evaluate(() => {
    sessionStorage.setItem('cms_token', 'test_token');
    sessionStorage.setItem('cms_user', 'test@example.com');
  });

  await page.goto('https://www.manujungleforever.com/admin/panel.html', { waitUntil: 'networkidle' });
  
  await browser.close();
})();
