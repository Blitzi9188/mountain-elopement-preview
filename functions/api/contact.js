// Cloudflare Pages Function — POST /api/contact
// Verschickt die Anfrage als saubere, normale E-Mail via Resend an hello@mountain-elopement.com.
// Antworten geht direkt an den Absender (Reply-To = Kundenadresse).
// Botschutz: Honeypot-Feld (_honey). Kein CAPTCHA. Antwortet IMMER als JSON und haengt nie (fetch-Timeout).
//
// Benoetigte Umgebungsvariablen (Cloudflare Pages → Settings → Environment variables):
//   RESEND_API_KEY  — API-Key von https://resend.com
//   FROM_EMAIL      — verifizierter Absender, z. B. "Mountain Elopement <noreply@mountain-elopement.com>"

const TO_EMAIL = 'hello@mountain-elopement.com';

export async function onRequestPost({ request, env }) {
  try {
    const form = await request.formData();

    // Honeypot — von Bots ausgefuellt, von Menschen leer.
    if ((form.get('_honey') || '').toString().trim() !== '') return json({ ok: true });

    const name = (form.get('name') || '').toString().trim();
    const email = (form.get('email') || '').toString().trim();
    const date = (form.get('date') || '').toString().trim();
    const interests = (form.get('interests') || '').toString().trim();
    const message = (form.get('message') || '').toString().trim();
    const language = (form.get('language') || '').toString().trim();

    if (!name || !email || !message) return json({ ok: false, error: 'Bitte Name, E-Mail und Nachricht ausfüllen.' }, 400);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ ok: false, error: 'Bitte eine gültige E-Mail-Adresse angeben.' }, 400);
    if (!env.RESEND_API_KEY || !env.FROM_EMAIL) return json({ ok: false, error: 'E-Mail-Versand ist nicht konfiguriert.' }, 500);

    const rows = [
      ['Name', name],
      ['E-Mail', email],
      ['Datum', date || '—'],
      ['Interesse', interests || '—'],
      ['Sprache', language || '—'],
    ].map(([k, v]) => `<tr><td style="padding:6px 12px;border:1px solid #e5e5e5;font-weight:600">${esc(k)}</td><td style="padding:6px 12px;border:1px solid #e5e5e5">${esc(v)}</td></tr>`).join('');
    const html =
      `<div style="font-family:Arial,Helvetica,sans-serif;color:#222;max-width:560px">` +
      `<h2 style="font-weight:400">Neue Anfrage über mountain-elopement.com</h2>` +
      `<table style="border-collapse:collapse;font-size:14px">${rows}</table>` +
      `<p style="font-size:14px;margin-top:16px"><strong>Nachricht:</strong><br>${esc(message).replace(/\n/g, '<br>')}</p>` +
      `<p style="font-size:12px;color:#888;margin-top:20px">Antworten geht direkt an ${esc(email)}.</p></div>`;

    // Resend-Aufruf mit hartem Timeout → kann den Worker nie haengen lassen (kein 502).
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 8000);
    let send;
    try {
      send = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'content-type': 'application/json' },
        body: JSON.stringify({
          from: env.FROM_EMAIL,
          to: [TO_EMAIL],
          reply_to: email,
          subject: `Neue Anfrage — ${name}`,
          html,
        }),
        signal: controller.signal,
      });
    } catch (e) {
      clearTimeout(timer);
      return json({ ok: false, error: 'E-Mail-Dienst hat zu lange gebraucht. Bitte schreibt uns direkt.' }, 502);
    }
    clearTimeout(timer);

    if (!send.ok) {
      const detail = await send.text().catch(() => '');
      console.log('Resend error', send.status, detail);
      return json({ ok: false, error: 'Konnte gerade nicht senden. Bitte schreibt uns direkt.' }, 502);
    }
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: 'Unerwarteter Fehler. Bitte erneut versuchen.' }, 500);
  }
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json' } });
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}
