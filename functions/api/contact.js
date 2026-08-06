// Cloudflare Pages Function — behandelt POST /api/contact
// Prüft Honeypot + Cloudflare Turnstile und versendet die Anfrage per Resend.
//
// Benötigte Umgebungsvariablen (Cloudflare Pages → Settings → Environment variables):
//   TURNSTILE_SECRET_KEY  — Secret-Key des Turnstile-Widgets
//   RESEND_API_KEY        — API-Key von https://resend.com
//   FROM_EMAIL            — verifizierter Absender, z. B. "Mountain Elopement <info@mountain-elopement.com>"
//   TO_EMAIL              — Empfängeradresse für Anfragen

export async function onRequestPost({ request, env }) {
  try {
    const form = await request.formData();

    // 1) Honeypot — das alte Netlify-Feld "bot-field" dient weiter als Spam-Falle
    if ((form.get('bot-field') || '').toString().trim() !== '') {
      return json({ ok: true }); // Bots stillschweigend verwerfen
    }

    // 2) Turnstile prüfen (nur wenn ein Secret hinterlegt ist)
    if (env.TURNSTILE_SECRET_KEY) {
      const token = (form.get('cf-turnstile-response') || '').toString();
      const ip = request.headers.get('CF-Connecting-IP') || '';
      const verify = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ secret: env.TURNSTILE_SECRET_KEY, response: token, remoteip: ip }),
      });
      const outcome = await verify.json();
      if (!outcome.success) {
        return json({ ok: false, error: 'Spam check failed. Please reload the page and try again.' }, 400);
      }
    }

    // 3) Felder lesen + validieren
    const name = (form.get('name') || '').toString().trim();
    const email = (form.get('email') || '').toString().trim();
    const date = (form.get('date') || '').toString().trim();
    const interests = (form.get('interests') || '').toString().trim();
    const message = (form.get('message') || '').toString().trim();
    const language = (form.get('language') || '').toString().trim();

    if (!name || !email || !message) {
      return json({ ok: false, error: 'Please fill in name, email and message.' }, 400);
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return json({ ok: false, error: 'Please enter a valid email address.' }, 400);
    }

    // 4) E-Mail via Resend senden
    // TO_EMAIL darf mehrere Adressen kommagetrennt enthalten (Backup-Postfach),
    // damit ein einzelnes volles/gesperrtes Postfach nie alle Anfragen verschluckt.
    // Anfragen gehen an info@mountain-elopement.com (fest gesetzt auf Wunsch).
    // Optional via Env TO_EMAIL erweiterbar (kommagetrennt) fuer weitere Backup-Postfaecher.
    const recipients = Array.from(new Set([
      'info@mountain-elopement.com',
      'foto@blitzkneisser.com',
      ...(env.TO_EMAIL || '').split(',').map((s) => s.trim()).filter(Boolean),
    ]));
    const html = `
      <h2>New elopement enquiry</h2>
      <p><strong>Name:</strong> ${esc(name)}</p>
      <p><strong>Email:</strong> ${esc(email)}</p>
      <p><strong>Date:</strong> ${esc(date) || '&mdash;'}</p>
      <p><strong>Interests:</strong> ${esc(interests) || '&mdash;'}</p>
      <p><strong>Language:</strong> ${esc(language) || '&mdash;'}</p>
      <p><strong>Message:</strong><br>${esc(message).replace(/\n/g, '<br>')}</p>`;

    const send = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        from: env.FROM_EMAIL,
        to: recipients,
        reply_to: email,
        subject: `New enquiry — ${name}`,
        html,
      }),
    });

    if (!send.ok) {
      const detail = await send.text();
      console.log('Resend error', send.status, detail);
      return json({ ok: false, error: 'Could not send right now. Please email us directly.' }, 502);
    }
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: 'Unexpected error. Please try again.' }, 500);
  }
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'content-type': 'application/json' },
  });
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}
