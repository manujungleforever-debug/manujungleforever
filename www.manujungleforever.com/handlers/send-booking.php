<?php
/**
 * Booking Enquiry Handler – Manu Jungle Forever
 * POST: traveler_name, email, phone, tour_type, num_travelers, departure_date,
 *       num_days, contact_pref, notes, csrf_token
 */
header('Content-Type: application/json; charset=UTF-8');
require_once __DIR__ . '/../config.php';

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

// ─── Sanitise & validate ─────────────────────────────────────────
$tname    = trim(strip_tags($_POST['traveler_name']  ?? ''));
$email    = trim($_POST['email']         ?? '');
$phone    = trim(strip_tags($_POST['phone']          ?? ''));
$tour     = trim(strip_tags($_POST['tour_type']      ?? ''));
$pax      = (int)($_POST['num_travelers'] ?? 0);
$date     = trim(strip_tags($_POST['departure_date'] ?? ''));
$days     = trim(strip_tags($_POST['num_days']       ?? ''));
$pref     = trim(strip_tags($_POST['contact_pref']   ?? ''));
$notes    = trim(strip_tags($_POST['notes']          ?? ''));

$errors = [];
if (strlen($tname) < 2)                             $errors[] = 'Please provide your name.';
if (!filter_var($email, FILTER_VALIDATE_EMAIL))     $errors[] = 'Please provide a valid email.';
if (strlen($phone) < 7)                             $errors[] = 'Please provide a phone/WhatsApp number.';
if (empty($tour))                                   $errors[] = 'Please select a tour type.';
if ($pax < 1 || $pax > 20)                         $errors[] = 'Please enter a valid number of travelers.';

if ($errors) {
    echo json_encode(['ok'=>false,'message'=>implode(' ', $errors)]);
    exit;
}

// ─── Build notification email (to agency) ───────────────────────
$to   = SITE_EMAIL;
$subj = "[HJC BOOKING] $tour – $pax pax – $date";
$body  = "NEW BOOKING ENQUIRY – Manu Jungle Forever\n";
$body .= str_repeat('=', 50) . "\n\n";
$body .= "Traveler(s):     $tname\n";
$body .= "Email:           $email\n";
$body .= "Phone/WhatsApp:  $phone\n";
$body .= "Tour Type:       $tour\n";
$body .= "No. of Travelers: $pax\n";
$body .= "Departure Date:  " . ($date ?: 'Flexible') . "\n";
$body .= "No. of Days:     " . ($days ?: 'Not specified') . "\n";
$body .= "Preferred Contact: " . ($pref ?: 'Not specified') . "\n";
$body .= "\nAdditional Notes:\n$notes\n\n";
$body .= str_repeat('-', 50) . "\n";
$body .= "Sent via manujungleforever.com booking form.\n";

$hdrs  = "From: " . SITE_NAME . " <" . SITE_EMAIL . ">\r\n";
$hdrs .= "Reply-To: $tname <$email>\r\n";
$hdrs .= "MIME-Version: 1.0\r\n";
$hdrs .= "Content-Type: text/plain; charset=UTF-8\r\n";

$sent = mail($to, $subj, $body, $hdrs);

if ($sent) {
    // Auto-reply to traveler
    $arSubj = "Your booking enquiry – " . SITE_NAME;
    $arBody  = "Hello $tname,\n\n";
    $arBody .= "Thank you for your booking enquiry with Manu Jungle Forever!\n\n";
    $arBody .= "We have received your request for the following tour:\n";
    $arBody .= "  Tour:    $tour\n";
    $arBody .= "  Dates:   " . ($date ?: 'Flexible') . "\n";
    $arBody .= "  Travelers: $pax person(s)\n\n";
    $arBody .= "Our team will contact you within 24 hours to confirm details and pricing.\n\n";
    $arBody .= "For faster assistance, reach us on WhatsApp:\n";
    $arBody .= "https://wa.me/" . WHATSAPP_NUMBER . "\n\n";
    $arBody .= "We look forward to taking you on an unforgettable journey!\n\n";
    $arBody .= "Best regards,\nManu Jungle Forever\n";
    $arBody .= "discover@manujungleforever.com\n";
    $arBody .= "www.manujungleforever.com\n";
    $arHdrs  = "From: " . SITE_NAME . " <" . SITE_EMAIL . ">\r\n";
    $arHdrs .= "Content-Type: text/plain; charset=UTF-8\r\n";
    @mail($email, $arSubj, $arBody, $arHdrs);

    echo json_encode(['ok'=>true,'message'=>'Your enquiry has been sent! We\'ll contact you within 24 hours. Check your email for confirmation.']);
} else {
    error_log('[HJC] booking mail() failed for: ' . $email);
    echo json_encode(['ok'=>false,'message'=>'We could not process your request right now. Please contact us directly at discover@manujungleforever.com or via WhatsApp.']);
}
