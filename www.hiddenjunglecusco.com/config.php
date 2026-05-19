<?php
/**
 * Hidden Jungle Cusco – Site Configuration
 * Deploy on Hostinger: set SMTP credentials in Hostinger's control panel
 * or fill in the values below before uploading.
 */

// ─── Site Identity ────────────────────────────────────────────────
define('SITE_NAME',  'Hidden Jungle Cusco');
define('SITE_URL',   'https://www.hiddenjunglecusco.com');
define('SITE_EMAIL', 'discover@hiddenjunglecusco.com');
define('SITE_PHONE', '+51 979 808 013 / +51 923 289 231');
define('WHATSAPP_NUMBER', '51923289231');
define('SITE_ADDRESS', 'Hidden Jungle Cusco – La Casa Escondida 17800, Nuevo Eden, Peru');

// ─── SMTP (Hostinger → hPanel → Email → SMTP) ─────────────────────
define('SMTP_HOST',     'smtp.hostinger.com');     // Hostinger SMTP
define('SMTP_PORT',     587);
define('SMTP_SECURE',   'tls');
define('SMTP_USER',     'discover@hiddenjunglecusco.com'); // your email
define('SMTP_PASS',     'YOUR_EMAIL_PASSWORD_HERE');        // set before deploy

// ─── Social Links ─────────────────────────────────────────────────
define('SOCIAL_FACEBOOK',    'https://www.facebook.com/hiddenjunglecusco');
define('SOCIAL_INSTAGRAM',   'https://www.instagram.com/hiddenjunglecusco/?hl=en');
define('SOCIAL_TRIPADVISOR', 'https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html?m=19905');
define('SOCIAL_AIRBNB',      'https://abnb.me/Ri8XQWoA19');
define('SOCIAL_WHATSAPP',    'https://wa.me/51923289231');
define('SOCIAL_TIKTOK',      'https://www.tiktok.com/@hidden.jungle.cus');

// ─── Analytics ────────────────────────────────────────────────────
define('GTM_ID',     'GTM-5476BC9');
define('GA_ID',      'GT-NS9ZNKJP');
define('GOOGLE_MAP', 'https://www.google.com/maps/d/embed?mid=1CkYt9KUrq9Jjp9tgxChYmOYvyNaLZnxF');

// ─── Environment ──────────────────────────────────────────────────
define('APP_ENV', 'production'); // 'development' | 'production'

if (APP_ENV === 'development') {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}

// ─── CSRF helper ──────────────────────────────────────────────────
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}
function csrf_token(): string {
    return $_SESSION['csrf_token'];
}
function verify_csrf(string $token): bool {
    return hash_equals($_SESSION['csrf_token'] ?? '', $token);
}
