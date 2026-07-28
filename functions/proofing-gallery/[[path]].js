// Stillgelegte private Kundengalerie: echtes "410 Gone", damit die URLs
// zügig aus dem Google-Index fallen. Cloudflare Pages unterstützt 410
// nicht in _redirects, deshalb als Function.
export async function onRequest() {
  const html = `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="robots" content="noindex"><title>Gone — Mountain Elopement</title></head>
<body><h1>This gallery is no longer available</h1>
<p>This private client gallery has been retired. <a href="/">Back to the homepage</a></p>
</body></html>`;
  return new Response(html, { status: 410, headers: { 'content-type': 'text/html; charset=utf-8' } });
}
