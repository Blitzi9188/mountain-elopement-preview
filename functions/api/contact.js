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

    // 1b) Turnstile-Token MUSS vorhanden sein — blockiert Direkt-POST-Bots auch dann,
    //     wenn TURNSTILE_SECRET_KEY (noch) nicht gesetzt ist (echte Nutzer bekommen das
    //     Token automatisch vom Managed-Widget).
    if (!(form.get('cf-turnstile-response') || '').toString().trim()) {
      return json({ ok: true }); // kein Widget-Token => Bot, stillschweigend verwerfen
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

    // 3b) Inhaltsfilter — offensichtlichen SEO-/Marketing-Spam stillschweigend verwerfen.
    //     Blockt bei 2+ Links oder typischen Spam-Begriffen (Wortgrenzen -> keine Fehltreffer
    //     bei Namen wie "Frank"/"Sloane"). Echte Paare mit einem einzelnen Link kommen durch.
    const blob = `${name} ${message} ${interests}`;
    const urlCount = (blob.match(/https?:\/\/|www\.[a-z0-9-]+\.[a-z]{2,}/gi) || []).length;
    const spamRe = /\b(seo|backlink|guest post|link building|rank your|crypto|bitcoin|casino|viagra|cialis|payday|web design|digital marketing|b2b leads|marketing services|escort|gambling|search engine optimi|increase (your )?traffic|web hosting|cpanel|vps|rdp|openvz|softaculous|reseller hosting|dedicated server|windows vps|use code|promo code|free ssl)/i;
    if (urlCount >= 2 || spamRe.test(blob)) {
      return json({ ok: true }); // sieht für den Absender wie Erfolg aus, landet aber im Nichts
    }

    // 4) E-Mail via Resend senden
    const html = `
      <h2>Neue Anfrage &uuml;ber mountain-elopement.com</h2>
      <p><strong>Name:</strong> ${esc(name)}</p>
      <p><strong>E-Mail:</strong> ${esc(email)}</p>
      <p><strong>Datum:</strong> ${esc(date) || '&mdash;'}</p>
      <p><strong>Interesse:</strong> ${esc(interests) || '&mdash;'}</p>
      <p><strong>Sprache:</strong> ${esc(language) || '&mdash;'}</p>
      <p><strong>Nachricht:</strong><br>${esc(message).replace(/\n/g, '<br>')}</p>`;

    const send = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        from: env.FROM_EMAIL,
        to: [env.TO_EMAIL],
        reply_to: email,
        subject: `Neue Anfrage — ${name}`,
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
