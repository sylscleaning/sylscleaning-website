"""Builds the Syl's Cleaning static website into ./dist."""
import os, re, json, shutil, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
import badge as B

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')
SITE = 'https://www.sylscleaning.com'
PHONE = '262-338-0783'
TEL = 'tel:+12623380783'
EMAIL = 'info@sylscleaning.com'
AREA = 'Washington, Ozaukee, Waukesha and Dodge Counties'
COUNTIES = ['Washington County', 'Ozaukee County', 'Waukesha County', 'Dodge County']

P = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/brand/wordmark_path.txt')).read()
P = re.sub(r'(\d+\.\d)\d', r'\1', P)
VB = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/brand/wordmark_vb.txt')).read()

def wordmark(h, color='#3D3C8A'):
    return (f'<svg viewBox="{VB}" aria-hidden="true" style="height:{h}px;width:auto;display:block">'
            f'<path fill="{color}" fill-rule="evenodd" d="{P}"/></svg>')

NAV = [
    ('carpet', 'Carpet &amp; Upholstery', '/carpet-upholstery/'),
    ('tile', 'Tile &amp; Grout', '/tile-grout/'),
    ('floor', 'Floor Care', '/floor-care/'),
    ('rugs', 'Area Rugs', '/area-rugs/'),
]

def svg(paths, size=28, stroke='#3D3C8A', sw=1.8):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')

ICON = {
    'carpet': '<path d="M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3"/><path d="M2 13a2 2 0 0 1 4 0v2h12v-2a2 2 0 0 1 4 0v4a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1z"/><path d="M5 18v2M19 18v2"/>',
    'tile': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>',
    'floor': '<path d="M11 3l1.8 4.2L17 9l-4.2 1.8L11 15l-1.8-4.2L5 9l4.2-1.8z"/><path d="M18.5 14l.8 1.9 1.9.8-1.9.8-.8 1.9-.8-1.9-1.9-.8 1.9-.8z"/><path d="M3 21h18"/>',
    'rugs': '<rect x="5" y="5" width="14" height="14" rx="1"/><rect x="9" y="9" width="6" height="6"/><path d="M5 8H3M5 12H3M5 16H3M19 8h2M19 12h2M19 16h2"/>',
}
CHECK = svg('<path d="M5 12l5 5L20 7"/>', 22, sw=2.4)
PHONE_IC = svg('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>', 18, 'currentColor', 2)

SCHEMA = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": SITE + "/#business",
    "name": "Syl's Cleaning",
    "alternateName": "Syl's Carpet & Upholstery Cleaning",
    "url": SITE + "/",
    "logo": SITE + "/assets/syls-logo.png",
    "image": SITE + "/assets/syls-carpet.jpg",
    "telephone": "+1-262-338-0783",
    "email": EMAIL,
    "foundingDate": "1977",
    "description": "Locally owned and operated carpet, upholstery, tile & grout, floor care (strip and wax) and area rug cleaning since 1977.",
    "address": {"@type": "PostalAddress", "addressRegion": "WI", "addressCountry": "US"},
    "areaServed": [{"@type": "AdministrativeArea", "name": c + ", WI"} for c in COUNTIES],
    "hasOfferCatalog": {
        "@type": "OfferCatalog", "name": "Cleaning services",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in
            ["Carpet cleaning", "Upholstery cleaning", "Tile and grout cleaning", "Floor stripping and waxing", "Area rug cleaning"]
        ]
    },
}

def head(title, desc, path, img='syls-carpet.jpg', extra_schema=None):
    url = SITE + path
    schemas = [SCHEMA] + ([extra_schema] if extra_schema else [])
    ld = '\n'.join(f'<script type="application/ld+json">{json.dumps(s, separators=(",", ":"))}</script>' for s in schemas)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Syl's Cleaning">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/{img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#3D3C8A">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css">
{ld}
</head>
<body>"""

def header(active):
    links = ''.join(
        f'<a href="{href}"{" aria-current=\"page\"" if k == active else ""}>{label}</a>' for k, label, href in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="wrap hdr">
<a class="brand" href="/" aria-label="Syl's Cleaning home">{wordmark(52)}</a>
<nav class="nav" aria-label="Main">{links}</nav>
<div class="hdr-cta">
<a class="hdr-phone" href="{TEL}">{PHONE_IC}<span>{PHONE}</span></a>
<a class="btn btn-b btn-sm" href="/contact/">Request a Quote</a>
</div>
</div>
</header>
<main id="main">"""

def footer():
    svc = ''.join(f'<a href="{h}">{l}</a>' for _, l, h in NAV)
    return f"""</main>
<footer class="site-footer">
<div class="wrap foot">
<div class="foot-brand">{B.badge(132)}<p>Locally owned &amp; operated since 1977. Serving {AREA}.</p></div>
<div class="foot-col"><h2>Services</h2>{svc}</div>
<div class="foot-col"><h2>Contact</h2><a href="{TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a class="strong" href="/contact/">Request a free quote &rarr;</a></div>
</div>
<div class="wrap foot-bottom"><span>&copy; <span id="yr">2026</span> Syl&rsquo;s Carpet &amp; Upholstery Cleaning</span><span>sylscleaning.com</span></div>
</footer>
<script>document.getElementById('yr').textContent=new Date().getFullYear();</script>
</body>
</html>
"""

def btns():
    return (f'<div class="btns"><a class="btn btn-w" href="/contact/">Request a free quote</a>'
            f'<a class="btn btn-o" href="{TEL}">{PHONE_IC}<span>{PHONE}</span></a></div>')

def cta(title, sub=None):
    s = f'<p>{sub}</p>' if sub else ''
    return (f'<section class="wrap"><div class="cta"><div class="cta-txt"><h2>{title}</h2>{s}</div>'
            f'<div class="btns"><a class="btn btn-w" href="/contact/">Request a free quote</a>'
            f'<a class="btn btn-o" href="{TEL}">Call {PHONE}</a></div></div></section>')

def write(path, html):
    out = os.path.join(DIST, path.strip('/'), 'index.html') if path != '/' else os.path.join(DIST, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(html)

# ---------------- HOME ----------------
cards = [
    ('carpet', 'Carpet &amp; Upholstery', 'Deep-cleaned carpet, sofas, chairs and mattresses.', '/carpet-upholstery/'),
    ('tile', 'Tile &amp; Grout', 'Grime lifted from tile and grout lines, back to bright.', '/tile-grout/'),
    ('floor', 'Floor Care', 'Strip &amp; wax that brings hard floors back to a shine.', '/floor-care/'),
    ('rugs', 'Area Rugs', 'Gentle, thorough cleaning for the rugs you love.', '/area-rugs/'),
]
cards_html = ''.join(
    f'<a class="card" href="{h}"><span class="ic">{svg(ICON[k])}</span><h3>{t}</h3><p>{d}</p><span class="more">Learn more &rarr;</span></a>'
    for k, t, d, h in cards)
steps = [('1', 'Send a request', 'Tell us what needs cleaning. It takes about a minute.'),
         ('2', 'We reach out to schedule', 'We&rsquo;ll confirm the details and find a time that works for you.'),
         ('3', 'Enjoy the difference', 'Our trained technicians do the work. You enjoy a cleaner space.')]
steps_html = ''.join(f'<div class="step"><span class="step-n">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, t, d in steps)
area_html = ''.join(f'<li>{c}</li>' for c in COUNTIES)

home = head(
    "Carpet, Upholstery & Tile Cleaning | Syl's Cleaning, Wisconsin",
    f"Locally owned since 1977. Carpet, upholstery, tile & grout, floor strip & wax and area rug cleaning for homes, businesses and apartments in {AREA}.",
    '/') + header('home') + f"""
<section class="wrap hero-wrap"><div class="hero">
<div class="hero-txt">
<p class="pill">Locally owned &amp; operated &middot; Since 1977</p>
<h1>Cleaner floors. Fresher furniture. Done right.</h1>
<p class="lead">Carpet, upholstery, tile and floor care for homes, businesses and apartment communities across {AREA}.</p>
{btns()}
</div>
<div class="photo"><img src="/assets/syls-carpet.jpg" alt="Syl&rsquo;s technician deep-cleaning a living room carpet" width="1400" height="1046" fetchpriority="high"><div class="seal">{B.badge(150)}</div></div>
</div></section>
<section class="wrap s"><h2>What we clean</h2><p class="sub">One call covers every surface in your home or building.</p><div class="grid">{cards_html}</div></section>
<section class="wrap s"><h2>Getting a cleaning is easy</h2><div class="grid">{steps_html}</div></section>
<section class="wrap s area"><div><h2>Proudly serving southeastern Wisconsin</h2><p class="sub">Homes, businesses and apartment communities throughout:</p></div><ul class="area-list">{area_html}</ul></section>
{cta('Ready for a cleaner space?', 'Send us a quick request and we&rsquo;ll reach out to schedule.')}
""" + footer()
write('/', home)

# ---------------- SERVICE PAGES ----------------
def service(path, key, title, h1, desc, intro, img, alt, items, great, cta_title, faq, items_heading='What we clean'):
    checks = ''.join(f'<li class="check">{CHECK}<span>{i}</span></li>' for i in items)
    chips = ''
    if great:
        chips = '<div class="chips"><strong>Great for:</strong>' + ''.join(f'<span class="chip">{g}</span>' for g in great) + '</div>'
    faq_html = ''.join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": re.sub('&amp;', '&', q), "acceptedAnswer": {"@type": "Answer", "text": re.sub('&amp;', '&', re.sub('&rsquo;', "'", a))}}
        for q, a in faq]}
    html = head(title, desc, path, img, faq_schema) + header(key) + f"""
<section class="wrap hero-wrap"><div class="hero">
<div class="hero-txt">
<p class="eyebrow">Our services</p>
<h1>{h1}</h1>
<p class="lead">{intro}</p>
{btns()}
</div>
<div class="photo"><img src="/assets/{img}" alt="{alt}" width="1400" height="1046" fetchpriority="high"></div>
</div></section>
<section class="wrap s"><h2>{items_heading}</h2><ul class="checks">{checks}</ul>{chips}</section>
<section class="wrap s"><h2>Common questions</h2><div class="faqs">{faq_html}</div></section>
{cta(cta_title)}
""" + footer()
    write(path, html)

AREA_SHORT = 'Washington, Ozaukee, Waukesha and Dodge Counties'
service('/carpet-upholstery/', 'carpet',
    "Carpet & Upholstery Cleaning | Syl's Cleaning, WI",
    'Carpet &amp; Upholstery Cleaning',
    f"Professional carpet and upholstery cleaning for homes, apartments and offices in {AREA_SHORT}. Sofas, mattresses, stains and more. Request a free quote.",
    'We lift out the dirt, stains and odors that vacuuming leaves behind, so your carpet and furniture look and feel fresh again.',
    'syls-upholstery.jpg', 'Syl&rsquo;s technician cleaning a gray fabric sofa',
    ['Wall-to-wall carpet', 'Spot &amp; stain treatment', 'Sofas, sectionals &amp; chairs', 'Mattresses', 'Vehicle seats &amp; carpet', 'Carpet repair'],
    ['Homes', 'Apartment communities', 'Offices', 'Move-in / move-out'],
    'Ready for fresher carpet and furniture?',
    [('What areas do you serve?', f'We clean homes, businesses and apartment communities across {AREA_SHORT} in Wisconsin.'),
     ('Do you clean furniture as well as carpet?', 'Yes. We clean sofas, sectionals, chairs and mattresses, plus vehicle seats and carpet.'),
     ('How do I get a quote?', f'Send a request on our Request a Quote page or call {PHONE}. We&rsquo;ll reach out to schedule.')])

service('/tile-grout/', 'tile',
    "Tile & Grout Cleaning | Syl's Cleaning, WI",
    'Tile &amp; Grout Cleaning',
    f"Deep tile and grout cleaning for kitchens, bathrooms, entryways and commercial spaces in {AREA_SHORT}. Bring dull grout back to bright. Free quotes.",
    'Mopping can&rsquo;t reach the grime built up in grout lines. We deep-clean tile and grout so your floors look bright again.',
    'syls-tile.jpg', 'Grout lines being scrubbed clean on a tile kitchen floor',
    ['Ceramic &amp; porcelain tile', 'Grout line deep cleaning', 'Kitchen &amp; bathroom floors', 'Showers &amp; tiled walls', 'Entryways &amp; mudrooms'],
    ['Kitchens', 'Bathrooms', 'Entryways', 'Spas &amp; commercial spaces'],
    'Ready for brighter tile and grout?',
    [('Why doesn&rsquo;t mopping get my grout clean?', 'Grout is porous, so dirt settles below the surface where a mop can&rsquo;t reach. Professional deep cleaning lifts it back out.'),
     ('Do you clean commercial tile floors?', 'Yes. We clean tile for homes as well as spas, offices and other commercial spaces.'),
     ('How do I get a quote?', f'Send a request on our Request a Quote page or call {PHONE}.')])

service('/floor-care/', 'floor',
    "Floor Strip & Wax Services | Syl's Cleaning, WI",
    'Floor Care: Strip &amp; Wax',
    f"Commercial and residential floor stripping and waxing for vinyl, VCT and other hard floors in {AREA_SHORT}. Apartment hallways, lobbies, offices.",
    'We strip away dull, worn finish and lay down fresh wax, so hard floors shine and stay protected longer.',
    'syls-floor.jpg', 'Freshly stripped and waxed hallway floor with a floor machine',
    ['Stripping old, worn finish', 'Fresh wax / floor finish', 'Vinyl &amp; VCT floors', 'Other hard surfaces', 'One-time or recurring service'],
    ['Apartment hallways', 'Lobbies', 'Offices', 'Kitchens &amp; laundry rooms'],
    'Ready to bring your floors back to a shine?',
    [('What does strip and wax mean?', 'We remove the old, worn floor finish down to the surface, then apply fresh coats of wax so the floor shines and is protected.'),
     ('Do you offer recurring floor care?', 'Yes. We can do a one-time strip and wax or set up recurring service for apartment buildings and businesses.'),
     ('How do I get a quote?', f'Send a request on our Request a Quote page or call {PHONE}.')],
    items_heading='What&rsquo;s included')

service('/area-rugs/', 'rugs',
    "Area Rug Cleaning | Syl's Cleaning, WI",
    'Area Rug Cleaning',
    f"Careful cleaning for everyday area rugs and oriental rugs in {AREA_SHORT}. Spot, stain and odor treatment. Request a free quote.",
    'From everyday rugs to oriental rugs, we clean with care to bring back their color and softness.',
    'syls-rugs.jpg', 'Clean patterned area rug in a sunny living room',
    ['Everyday area rugs', 'Oriental &amp; specialty rugs', 'Spot, stain &amp; odor treatment'],
    None, 'Have a rug that needs some love?',
    [('Do you clean oriental rugs?', 'Yes. We clean oriental and specialty rugs as well as everyday area rugs.'),
     ('How do I get a quote?', f'Send a request on our Request a Quote page or call {PHONE}.')])

# ---------------- REQUEST A QUOTE ----------------
quote = head(
    "Request a Free Quote | Syl's Cleaning",
    f"Request a free cleaning quote from Syl's Cleaning. Carpet, upholstery, tile & grout, floor care and area rugs in {AREA_SHORT}. Call {PHONE}.",
    '/contact/') + header('contact') + f"""
<section class="wrap quote">
<div class="quote-main">
<h1>Request a free quote</h1>
<p class="sub">Tell us a little about what you need. We&rsquo;ll reach out to schedule.</p>
<div class="jobber">
<!-- JOBBER_FORM -->
<div id="ba537b6b-99e0-4482-b46a-1a8b75f7292a-5279390"></div><link rel="stylesheet" href="https://d3ey4dbjkt2f6s.cloudfront.net/assets/external/work_request_embed.css" media="screen" /><script src="https://d3ey4dbjkt2f6s.cloudfront.net/assets/static_link/work_request_embed_snippet.js" clienthub_id="ba537b6b-99e0-4482-b46a-1a8b75f7292a-5279390" form_url="https://clienthub.getjobber.com/client_hubs/ba537b6b-99e0-4482-b46a-1a8b75f7292a/public/work_request/embedded_work_request_form?form_id=5279390"></script>
<noscript><p><a class="btn btn-b" href="https://clienthub.getjobber.com/hubs/ba537b6b-99e0-4482-b46a-1a8b75f7292a/public/requests/5279390/new">Open the request form</a></p></noscript>
<p class="form-note">Having trouble with the form? <a href="https://clienthub.getjobber.com/hubs/ba537b6b-99e0-4482-b46a-1a8b75f7292a/public/requests/5279390/new">Open it in a new page</a> or call <a href="{TEL}">{PHONE}</a>.</p>
<!-- /JOBBER_FORM -->
</div>
</div>
<aside class="quote-side">
<div class="talk"><p class="label">Prefer to talk?</p><a class="big" href="{TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
<div class="info"><div><strong>Service area</strong><span>{AREA_SHORT}</span></div><div><strong>We serve</strong><span>Homes, businesses &amp; apartment communities</span></div></div>
</aside>
</section>
""" + footer()
write('/contact/', quote)

# ---------------- 404 ----------------
nf = head("Page not found | Syl's Cleaning", "Sorry, that page doesn't exist.", '/404.html') + header('') + f"""
<section class="wrap s" style="text-align:center;padding-bottom:40px"><h1 style="font-size:44px">Page not found</h1><p class="sub">Sorry, we couldn&rsquo;t find that page.</p><div class="btns" style="justify-content:center"><a class="btn btn-b" href="/">Go to the home page</a></div></section>
""" + footer()
open(os.path.join(DIST, '404.html'), 'w').write(nf.replace('<link rel="canonical" href="https://www.sylscleaning.com/404.html">\n', '').replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1))

# ---------------- assets, sitemap, robots ----------------
A = os.path.join(DIST, 'assets'); os.makedirs(A, exist_ok=True)
shutil.copy(os.path.join(ROOT, 'styles.css'), A)
for f in os.listdir(os.path.join(ROOT, 'src/photos')):
    shutil.copy(os.path.join(os.path.join(ROOT, 'src/photos'), f), A)
open(os.path.join(A, 'favicon.svg'), 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#3D3C8A"/>'
    f'<svg x="6" y="12" width="52" height="40" viewBox="{VB}"><path fill="#FFFFFF" fill-rule="evenodd" d="{P}"/></svg></svg>')
pages = ['/', '/carpet-upholstery/', '/tile-grout/', '/floor-care/', '/area-rugs/', '/contact/']
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
     ''.join(f'  <url><loc>{SITE}{p}</loc></url>\n' for p in pages) + '</urlset>\n'
open(os.path.join(DIST, 'sitemap.xml'), 'w').write(sm)
open(os.path.join(DIST, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
open(os.path.join(DIST, '_redirects'), 'w').write('https://sylscleaning.com/* https://www.sylscleaning.com/:splat 301!\n')
print('built', pages)
