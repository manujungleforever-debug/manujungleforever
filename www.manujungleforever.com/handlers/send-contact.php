<?php
/**
 * Contact Form Handler – Manu Jungle Forever
 * POST: name, email, phone, message, subject, csrf_token
 */
header('Content-Type: application/json; charset=UTF-8');
require_once __DIR__ . '/../config.php';

// ─── Only POST ─────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok'=>false,'message'=>'Method not allowed.']);
    exit;
}

// ─── CSRF ───────────────────────────────────────────────────────
if (!verify_csrf($_POST['csrf_token'] ?? '')) {
    http_response_code(403);
    echo json_encode(['ok'=>false,'message'=>'Security token mismatch. Please reload the page.']);
    exit;
}

// ─── Validate ───────────────────────────────────────────────────
$name    = trim(strip_tags($_POST['name']    ?? ''));
$email   = trim($_POST['email']   ?? '');
$phone   = trim(strip_tags($_POST['phone']   ?? ''));
$subject = trim(strip_tags($_POST['subject'] ?? 'New Contact – Manu Jungle Forever'));
$message = trim(strip_tags($_POST['message'] ?? ''));

$errors = [];
if (strlen($name) < 2)              $errors[] = 'Please provide your name.';
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'Please provide a valid email address.';
if (strlen($message) < 10)         $errors[] = 'Message is too short.';

if ($errors) {
    echo json_encode(['ok'=>false,'message'=>implode(' ', $errors)]);
    exit;
}

// ─── Build email ────────────────────────────────────────────────
$to      = SITE_EMAIL;
$subj    = '[HJC Contact] ' . $subject;
$body    = "You have a new contact message from the Manu Jungle Forever website.\n\n";
$body   .= "Name:    $name\n";
$body   .= "Email:   $email\n";
$body   .= "Phone:   " . ($phone ?: 'Not provided') . "\n";
$body   .= "Subject: $subject\n\n";
$body   .= "Message:\n$message\n\n";
$body   .= "---\nSent via manujungleforever.com contact form.";

$headers  = "From: " . SITE_NAME . " <" . SITE_EMAIL . ">\r\n";
$headers .= "Reply-To: $name <$email>\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

// ─── Send ───────────────────────────────────────────────────────
// Hostinger supports PHP mail() natively on shared hosting.
// For more reliability, swap this block for PHPMailer + SMTP.
$sent = mail($to, $subj, $body, $headers);

if ($sent) {
    // Auto-reply to traveler
    $arSubj = "We received your message – " . SITE_NAME;
    $arBody  = "Hello $name,\n\n";
    $arBody .= "Thank you for contacting Manu Jungle Forever!\n";
    $arBody .= "We will get back to you within 24 hours.\n\n";
    $arBody .= "In the meantime, feel free to reach us on WhatsApp:\n";
    $arBody .= "https://wa.me/" . WHATSAPP_NUMBER . "\n\n";
    $arBody .= "Best regards,\nThe Manu Jungle Forever Team\n";
    $arBody .= "www.manujungleforever.com\n";
    $arHeaders = "From: " . SITE_NAME . " <" . SITE_EMAIL . ">\r\n";
    $arHeaders .= "Content-Type: text/plain; charset=UTF-8\r\n";
    @mail($email, $arSubj, $arBody, $arHeaders);

    echo json_encode(['ok'=>true,'message'=>'Thank you! Your message has been sent. We\'ll be in touch soon.']);
} else {
    error_log('[HJC] mail() failed for contact from: ' . $email);
    echo json_encode(['ok'=>false,'message'=>'Could not send your message right now. Please email us directly at discover@manujungleforever.com']);
}
