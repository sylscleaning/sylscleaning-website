"""Builds the Syl's Cleaning static website into ./dist."""
import os, re, json, shutil, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
import badge as B

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')
SITE = 'https://sylscleaning.com'
PHONE = '262-338-0783'
TEL = 'tel:+12623380783'
GADS_ID = 'AW-18568144859'                      # Google Ads tag
GADS_CONV = 'AW-18568144859/62vlCKq1vLYdENvP_ZVF'  # "Contact" conversion action
EMAIL = 'info@sylscleaning.com'
FACEBOOK = 'https://www.facebook.com/sylscleaning/'
LINKEDIN = 'https://www.linkedin.com/company/sylscleaning'
PLACE_ID = 'ChIJuaOfLJBfBIgRh1MwdoSoQuU'
GMAPS = f'https://www.google.com/maps/place/?q=place_id:{PLACE_ID}'
REVIEW_URL = f'https://search.google.com/local/writereview?placeid={PLACE_ID}'
RATING, REVIEWS = '4.9', '34'
HOURS = 'Mon&ndash;Fri 8 AM&ndash;5 PM'
HOURS_NOTE = 'Saturday &amp; evening appointments available'
# About page photo: swap for the owner & crew photo when it's ready
ABOUT_IMG = 'syls-carpet.jpg'
ABOUT_ALT = 'Syl&rsquo;s technician deep-cleaning a living room carpet'
AREA = 'Washington, Ozaukee, Waukesha and Dodge Counties'
COUNTIES = ['Washington County', 'Ozaukee County', 'Waukesha County', 'Dodge County']
AREA_LINKS = [('/service-areas/' + c.lower().replace(' ', '-') + '/', c) for c in COUNTIES]

P = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/brand/wordmark_path.txt')).read()
P = re.sub(r'(\d+\.\d)\d', r'\1', P)
VB = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/brand/wordmark_vb.txt')).read()

def wordmark(h, color='#2A4C9E'):
    return (f'<svg viewBox="{VB}" aria-hidden="true" style="height:{h}px;width:auto;display:block">'
            f'<path fill="{color}" fill-rule="evenodd" d="{P}"/></svg>')

NAV = [
    ('carpet', 'Carpet &amp; Upholstery', '/carpet-upholstery/'),
    ('tile', 'Tile &amp; Grout', '/tile-grout/'),
    ('floor', 'Floor Care', '/floor-care/'),
    ('rugs', 'Area Rugs', '/area-rugs/'),
    ('commercial', 'Commercial', '/commercial/'),
]

def svg(paths, size=28, stroke='#2A4C9E', sw=1.8):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')

ICON = {
    'commercial': '<path d="M3 21h18"/><path d="M5 21V5a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v16"/><path d="M15 9h3a1 1 0 0 1 1 1v11"/><path d="M8 8h1M11 8h1M8 12h1M11 12h1M8 16h1M11 16h1"/>',
    'carpet': '<path d="M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3"/><path d="M2 13a2 2 0 0 1 4 0v2h12v-2a2 2 0 0 1 4 0v4a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1z"/><path d="M5 18v2M19 18v2"/>',
    'tile': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>',
    'floor': '<path d="M11 3l1.8 4.2L17 9l-4.2 1.8L11 15l-1.8-4.2L5 9l4.2-1.8z"/><path d="M18.5 14l.8 1.9 1.9.8-1.9.8-.8 1.9-.8-1.9-1.9-.8 1.9-.8z"/><path d="M3 21h18"/>',
    'rugs': '<rect x="5" y="5" width="14" height="14" rx="1"/><rect x="9" y="9" width="6" height="6"/><path d="M5 8H3M5 12H3M5 16H3M19 8h2M19 12h2M19 16h2"/>',
}
FB_IC = '<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.5H16l.4-3H13.5V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.3H8v3h2.5V21z"/></svg>'
LI_IC = '<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5 3.5a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM3.3 9h3.4v11.5H3.3zM9 9h3.3v1.6h.1c.5-.9 1.6-1.9 3.4-1.9 3.6 0 4.2 2.4 4.2 5.4v6.4h-3.4v-5.7c0-1.4 0-3.1-1.9-3.1s-2.2 1.5-2.2 3v5.8H9z"/></svg>'
CHECK = svg('<path d="M5 12l5 5L20 7"/>', 22, sw=2.4)
MAIL_IC = svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>', 26)
PIN_IC = svg('<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>', 26)
CLOCK_IC = svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>', 26)
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
    "slogan": "Reliability in Professional Cleaning",
    "description": "Locally owned and operated carpet, upholstery, tile & grout, floor care (strip and wax) and area rug cleaning since 1977.",
    "address": {"@type": "PostalAddress", "streetAddress": "3750 S River Rd", "addressLocality": "West Bend", "addressRegion": "WI", "postalCode": "53095", "addressCountry": "US"},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:00"}],
    "hasMap": "https://www.google.com/maps/place/?q=place_id:ChIJuaOfLJBfBIgRh1MwdoSoQuU",
    "sameAs": ["https://www.facebook.com/sylscleaning/", "https://www.linkedin.com/company/sylscleaning"],
    "areaServed": [{"@type": "AdministrativeArea", "name": c + ", WI"} for c in COUNTIES],
    "hasOfferCatalog": {
        "@type": "OfferCatalog", "name": "Cleaning services",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in
            ["Carpet cleaning", "Commercial carpet cleaning", "Post-construction carpet and floor cleaning", "Upholstery cleaning", "Tile and grout cleaning", "Floor stripping and waxing", "Area rug cleaning"]
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
<meta name="theme-color" content="#2A4C9E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css">
{ld}
<script async src="https://www.googletagmanager.com/gtag/js?id={GADS_ID}"></script>
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('js',new Date());gtag('config','{GADS_ID}');
(function(){{var sent={{}};function conv(kind){{if(sent[kind])return;sent[kind]=1;gtag('event','conversion',{{send_to:'{GADS_CONV}',event_label:kind}});}}
document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('a');if(!a)return;var h=a.getAttribute('href')||'';
if(h.indexOf('tel:')===0)conv('call');else if(h.indexOf('clienthub.getjobber.com')>-1)conv('quote_form');}},true);
window.addEventListener('blur',function(){{setTimeout(function(){{var f=document.activeElement;if(f&&f.tagName==='IFRAME'&&f.closest('.jobber'))conv('quote_form');}},0);}});
}})();
</script>
</head>
<body>"""

def header(active):
    svc_keys = [k for k, _, _ in NAV if k != 'commercial']
    svc_links = ''.join(
        f'<a href="{href}"{" aria-current=\"page\"" if k == active else ""}>{label}</a>' for k, label, href in NAV if k != 'commercial')
    svc_cur = ' aria-current="true"' if active in svc_keys else ''
    top = ''.join(
        f'<a href="{href}"{" aria-current=\"page\"" if k == active else ""}>{label}</a>'
        for k, label, href in [('commercial', 'Commercial', '/commercial/'), ('about', 'About', '/about/'), ('contact', 'Contact', '/contact/')])
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="wrap hdr">
<a class="brand" href="/" aria-label="Syl's Cleaning home">{wordmark(52)}</a>
<nav class="nav" aria-label="Main">
<a href="/"{' aria-current="page"' if active == 'home' else ''}>Home</a>
<details class="dd"><summary{svc_cur}>Services <span class="caret" aria-hidden="true">&#9662;</span></summary><div class="dd-menu">{svc_links}</div></details>
{top}
</nav>
<div class="hdr-cta">
<a class="hdr-phone" href="{TEL}">{PHONE_IC}<span>{PHONE}</span></a>
<a class="btn btn-b btn-sm" href="/contact/">Request a Quote</a>
</div>
</div>
</header>
<script>document.addEventListener('click',function(e){{document.querySelectorAll('details.dd[open]').forEach(function(d){{if(!d.contains(e.target))d.removeAttribute('open');}});}});document.addEventListener('keydown',function(e){{if(e.key==='Escape')document.querySelectorAll('details.dd[open]').forEach(function(d){{d.removeAttribute('open');}});}});</script>
<main id="main">"""

def footer():
    svc = ''.join(f'<a href="{h}">{l}</a>' for _, l, h in NAV)
    areas = ''.join(f'<a href="{h}">{n}</a>' for h, n in AREA_LINKS)
    return f"""</main>
<footer class="site-footer">
<div class="wrap foot">
<div class="foot-brand">{B.badge(132)}<p class="foot-slogan">Reliability in Professional Cleaning</p><p>Locally owned &amp; operated since 1977. Serving {AREA}.</p></div>
<div class="foot-col"><h2>Services</h2>{svc}</div>
<div class="foot-col"><h2>Service areas</h2>{areas}</div>
<div class="foot-col"><h2>Contact</h2><a href="{TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>3750 S River Rd, West Bend, WI 53095</span><span>{HOURS}<br>{HOURS_NOTE}</span><a class="strong" href="/contact/">Request a free quote &rarr;</a><a href="/about/">About us</a><a href="/about/#reviews">Customer reviews</a><a class="strong" href="{REVIEW_URL}" target="_blank" rel="noopener">&#9733; Leave us a Google review</a><div class="social"><a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Syl&rsquo;s Cleaning on Facebook">{FB_IC}</a><a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="Syl&rsquo;s Cleaning on LinkedIn">{LI_IC}</a></div></div>
</div>
<div class="wrap foot-bottom"><span>&copy; <span id="yr">2026</span> Syl&rsquo;s Carpet &amp; Upholstery Cleaning</span><span>sylscleaning.com</span></div>
</footer>
<script>document.getElementById('yr').textContent=new Date().getFullYear();</script>
</body>
</html>
"""

def btns():
    return (f'<div class="btns"><a class="btn btn-w" href="/contact/">Request a free quote</a>'
            f'<a class="btn btn-o" href="{TEL}">{PHONE_IC}<span>{PHONE}</span></a></div>'
            f'<a class="rev" href="{GMAPS}" target="_blank" rel="noopener"><span class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span> <strong>{RATING}</strong> from {REVIEWS} Google reviews</a>')

def cta(title, sub=None):
    s = f'<p>{sub}</p>' if sub else ''
    return (f'<section class="wrap"><div class="cta"><div class="cta-txt"><h2>{title}</h2>{s}</div>'
            f'<div class="btns"><a class="btn btn-w" href="/contact/">Request a free quote</a>'
            f'<a class="btn btn-o" href="{TEL}">Call {PHONE}</a></div></div></section>')

def pic(name, alt, extra=''):
    base = name.rsplit('.', 1)[0]
    return (f'<picture><source type="image/webp" srcset="/assets/{base}-800.webp 800w, /assets/{base}-1400.webp 1400w" '
            f'sizes="(max-width: 860px) 100vw, 600px">'
            f'<img src="/assets/{name}" alt="{alt}" width="1400" height="1046" fetchpriority="high" decoding="async"{extra}></picture>')

def write(path, html):
    out = os.path.join(DIST, path.strip('/'), 'index.html') if path != '/' else os.path.join(DIST, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(html)


# Real Google reviews (verbatim; "..." marks shortened text). First name + last initial only.
REVIEW_LIST = [
    ('Marianne S.', 'Whole-home carpet before a sale', 'Mike and Carson were on time, polite and professional. They did an amazing job cleaning the carpets in my entire home to get it ready for sale, even getting out tough stains and pet accidents. Very reasonably priced too - I highly recommend them!'),
    ('Todd W.', 'Church &amp; home carpet', 'Everything about Syl&rsquo;s is top notch. I was referred to them by our pastor where they did the carpet cleaning at our church in West Bend. &hellip; The crew that came to my house was courteous, professional and very accommodating. &hellip; Everything looks great; all spots removed and the carpet looks like new.'),
    ('Norma J.', 'Carpet cleaning', 'Always on time and does an awesome job. Some carpets look like there&rsquo;s no hope for them but the guys surprise me and the carpet looks fantastic. I would recommend Syl&rsquo;s to anyone that needs a good company to clean their carpets.'),
    ('Janet E.', 'Area rug', 'Terrific service with great pricing. Left my 9x12 area rug literally looking like new in less than 30 minutes. &hellip; I highly recommend Syl&rsquo;s and will use them again if I need furniture or carpets cleaned.'),
    ('Marissa H.', 'New home carpet &amp; rugs', 'Professional, effective, affordable. I used them to clean the carpets in a house I just bought and I was so satisfied that I brought my area rugs to them to be cleaned as well!'),
    ('David C.', 'Carpet cleaning', '2 years in a row I&rsquo;ve used them, very friendly and does a great job. So nice that they move the furniture, my wife is expecting and can&rsquo;t do these things when I&rsquo;m away. Very happy with their service. 5 stars all day.'),
    ('Marilynn G.', 'Upholstery', 'Excellent work. So clean. Another upholstery cleaner could not get it clean.'),
    ('OBrian O.', 'Carpet cleaning', 'Very professional service. Great price! Very pleasant! Outstanding service. No fuss no muss! Carpet looks new and smells great!'),
    ('Karen H.', 'Area rug', 'Cleaned a 5 x 8 ft. area rug beautifully and fair price.'),
]
def review_cards(items):
    return ''.join(f'<figure class="review"><div class="stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
                   f'<blockquote>&ldquo;{t}&rdquo;</blockquote><figcaption><strong>{n}</strong><span>{j}</span></figcaption></figure>'
                   for n, j, t in items)

# ---------------- HOME ----------------
cards = [
    ('carpet', 'Carpet &amp; Upholstery', 'Deep-cleaned carpet, sofas, chairs and mattresses.', '/carpet-upholstery/'),
    ('tile', 'Tile &amp; Grout', 'Grime lifted from tile and grout lines, back to bright.', '/tile-grout/'),
    ('floor', 'Floor Care', 'Strip &amp; wax that brings hard floors back to a shine.', '/floor-care/'),
    ('rugs', 'Area Rugs', 'Gentle, thorough cleaning for the rugs you love.', '/area-rugs/'),
    ('commercial', 'Commercial Cleaning', 'Offices, apartment communities, churches and more.', '/commercial/'),
]
cards_html = ''.join(
    f'<a class="card" href="{h}"><span class="ic">{svg(ICON[k])}</span><h3>{t}</h3><p>{d}</p><span class="more">Learn more &rarr;</span></a>'
    for k, t, d, h in cards)
steps = [('1', 'Send a request', 'Tell us what needs cleaning. It takes about a minute.'),
         ('2', 'We reach out to schedule', 'We&rsquo;ll confirm the details and find a time that works for you.'),
         ('3', 'Enjoy the fresh clean', 'Our trained technicians handle the work, and you come home to fresh carpet, furniture and floors.')]
steps_html = ''.join(f'<div class="step"><span class="step-n">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, t, d in steps)
area_html = ''.join(f'<li><a href="{h}">{n}</a></li>' for h, n in AREA_LINKS)

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
<div class="photo">{pic("syls-carpet.jpg", "Syl&rsquo;s technician deep-cleaning a living room carpet")}<div class="seal">{B.badge(150)}</div></div>
</div></section>
<section class="wrap slogan"><p>Reliability in Professional Cleaning</p></section>
<section class="wrap s"><h2>What we clean</h2><p class="sub">One call covers every surface in your home or building.</p><div class="grid">{cards_html}</div></section>
<section class="wrap s"><h2>What our customers say</h2><p class="sub">Rated {RATING} stars from {REVIEWS} Google reviews.</p><div class="reviews">{review_cards(REVIEW_LIST[:3])}</div><p class="more-link"><a href="/about/#reviews">Read more reviews &rarr;</a></p></section>
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
<div class="photo">{pic(img, alt)}</div>
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
    [('How do you clean carpet?', 'We use truck-mounted hot water extraction. The powerful equipment stays in our van, so we can lift deep-down dirt and rinse it away without bringing loud machines into your home.'),
     ('How long does carpet take to dry?', 'Usually just a few hours. Drying time varies with the carpet, humidity and airflow, and opening windows or running fans helps it dry faster.'),
     ('Is it safe for kids and pets?', 'Yes. Our cleaning products are safe for kids and pets once dry, and we treat pet stains and odors.'),
     ('How much does a cleaning cost?', 'Every job is different, so pricing depends on the size, the number of rooms or pieces and their condition. Request a free quote and we&rsquo;ll give you a clear price before any work starts.'),
     ('What areas do you serve?', f'We clean homes, businesses and apartment communities across {AREA_SHORT} in Wisconsin.'),
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
     ('How much does a cleaning cost?', 'Every job is different, so pricing depends on the size, the number of rooms or pieces and their condition. Request a free quote and we&rsquo;ll give you a clear price before any work starts.'),
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
     ('How much does a cleaning cost?', 'Every job is different, so pricing depends on the size, the number of rooms or pieces and their condition. Request a free quote and we&rsquo;ll give you a clear price before any work starts.'),
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
     ('Can you get pet odors out of rugs?', 'We treat pet stains and odors in area rugs, and our products are safe for kids and pets once dry.'),
     ('How much does a cleaning cost?', 'Every job is different, so pricing depends on the size, the number of rooms or pieces and their condition. Request a free quote and we&rsquo;ll give you a clear price before any work starts.'),
     ('How do I get a quote?', f'Send a request on our Request a Quote page or call {PHONE}.')])

# ---------------- COUNTY / SERVICE-AREA PAGES ----------------
AREAS = [
    ('washington-county', 'Washington County',
     ['West Bend', 'Hartford', 'Germantown', 'Jackson', 'Slinger', 'Kewaskum', 'Richfield', 'Hubertus'],
     'From family homes in West Bend and Hartford to offices and apartment buildings in Germantown, we keep Washington County carpets, furniture and floors looking their best.'),
    ('ozaukee-county', 'Ozaukee County',
     ['Mequon', 'Cedarburg', 'Grafton', 'Port Washington', 'Thiensville', 'Saukville', 'Fredonia', 'Belgium'],
     'From lakeshore homes in Port Washington and Mequon to shops and offices in Cedarburg and Grafton, we bring careful, reliable cleaning to Ozaukee County.'),
    ('waukesha-county', 'Waukesha County',
     ['Waukesha', 'Brookfield', 'New Berlin', 'Menomonee Falls', 'Oconomowoc', 'Pewaukee', 'Delafield', 'Hartland', 'Sussex', 'Muskego', 'Elm Grove', 'Mukwonago'],
     'From lake homes in Oconomowoc and Pewaukee to apartment communities and offices in Brookfield and Waukesha, we clean carpet, tile and floors across Waukesha County.'),
    ('dodge-county', 'Dodge County',
     ['Beaver Dam', 'Mayville', 'Horicon', 'Juneau', 'Hustisford', 'Lomira', 'Fox Lake', 'Theresa'],
     'From homes in Beaver Dam and Mayville to businesses in Horicon and Juneau, Dodge County families and businesses count on us for a thorough clean.'),
]
SVC_LINKS = [('Carpet &amp; Upholstery Cleaning', '/carpet-upholstery/', 'Carpet, sofas, sectionals, chairs and mattresses.'),
             ('Tile &amp; Grout Cleaning', '/tile-grout/', 'Kitchens, bathrooms, showers and entryways.'),
             ('Floor Care (Strip &amp; Wax)', '/floor-care/', 'Vinyl and VCT floors, hallways, lobbies and offices.'),
             ('Area Rug Cleaning', '/area-rugs/', 'Everyday area rugs and oriental rugs.'),
             ('Commercial Cleaning', '/commercial/', 'Offices, apartment communities, churches and businesses.')]

for slug, name, towns, intro in AREAS:
    path = f'/service-areas/{slug}/'
    town_list = ', '.join(towns[:-1]) + ' and ' + towns[-1]
    svc_html = ''.join(f'<a class="card" href="{h}"><h3>{t}</h3><p>{d}</p><span class="more">Learn more &rarr;</span></a>' for t, h, d in SVC_LINKS)
    towns_html = ''.join(f'<li>{t}</li>' for t in towns)
    others = ' &middot; '.join(f'<a href="{h}">{n}</a>' for h, n in AREA_LINKS if n != name)
    faq = [(f'Do you serve all of {name}?', f'Yes. We clean homes, businesses and apartment communities throughout {name}, including {town_list}. Not sure if we reach you? Just call {PHONE}.'),
           (f'What do you clean in {name}?', 'Carpet and upholstery (including sofas, chairs and mattresses), tile and grout, hard floors with strip and wax, and area rugs, including oriental rugs.'),
           ('How do I get a quote?', f'Send a request on our Request a Quote page or call {PHONE}. We&rsquo;ll reach out to schedule a time that works for you.')]
    faq_html = ''.join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    clean = lambda s: re.sub('&amp;', '&', re.sub('&rsquo;', "'", s))
    extra = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": f"Carpet, upholstery, tile and floor cleaning in {name}, WI",
         "provider": {"@id": SITE + "/#business"},
         "areaServed": [{"@type": "City", "name": t + ", WI"} for t in towns]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in faq]}]}
    html = head(f"Carpet & Tile Cleaning in {name}, WI | Syl's Cleaning",
                f"Carpet, upholstery, tile & grout, floor strip & wax and area rug cleaning in {town_list} and all of {name}, WI. Locally owned since 1977.",
                path, extra_schema=extra) + header('') + f"""
<section class="wrap hero-wrap"><div class="hero">
<div class="hero-txt">
<p class="eyebrow">Service area</p>
<h1>Carpet &amp; Floor Cleaning in {name}</h1>
<p class="lead">{intro}</p>
{btns()}
</div>
<div class="photo">{pic("syls-carpet.jpg", f"Syl&rsquo;s technician cleaning carpet in a {name} home")}<div class="seal">{B.badge(150)}</div></div>
</div></section>
<section class="wrap s"><h2>Services in {name}</h2><p class="sub">Locally owned &amp; operated since 1977. Reliability in professional cleaning.</p><div class="grid">{svc_html}</div></section>
<section class="wrap s area"><div><h2>Communities we serve</h2><p class="sub">Homes, businesses and apartment communities in and around:</p></div><ul class="area-list">{towns_html}</ul></section>
<section class="wrap s"><h2>Common questions</h2><div class="faqs">{faq_html}</div><p class="sub" style="margin-top:22px">We also serve {others}.</p></section>
{cta(f'Ready for a cleaner space in {name}?', 'Send us a quick request and we&rsquo;ll reach out to schedule.')}
""" + footer()
    write(path, html)

# ---------------- COMMERCIAL ----------------
BUILDINGS = [
    ('Offices', 'Carpeted work areas, conference rooms, lobbies and office chairs.'),
    ('Apartment communities', 'Hallways, common areas, and units between tenants.'),
    ('Churches', 'Sanctuaries, fellowship halls, classrooms and entryways.'),
    ('Retail shops &amp; showrooms', 'High-traffic floors that need to look sharp for customers.'),
    ('Medical &amp; dental offices', 'Waiting rooms, hallways and upholstered seating.'),
    ('Schools &amp; daycares', 'Classrooms, hallways and gyms, scheduled around your calendar.'),
    ('Salons &amp; spas', 'Tile, grout and hard floors in wet and busy areas.'),
    ('Rental &amp; move-out turnovers', 'Carpet and floors ready for the next tenant or buyer.'),
    ('New builds &amp; remodels', 'New homes, additions and remodeled spaces cleaned after the contractors finish.'),
]
COMM_ITEMS = ['Post-construction carpet &amp; floor cleaning', 'Commercial carpet &amp; walk-off areas', 'Hallway &amp; common-area carpet', 'Lobby furniture &amp; office chairs',
              'Restroom &amp; kitchen tile and grout', 'Floor strip &amp; wax (VCT &amp; vinyl)', 'Area rugs &amp; entry rugs']
WHY = [('Scheduled around you', f'Evening and Saturday appointments are available, so your doors stay open and your team keeps working.'),
       ('One-time or recurring', 'Book a single deep clean or set up a regular schedule for carpet and floor care.'),
       ('Truck-mounted equipment', 'The powerful machines stay in our van outside, so the work is thorough without loud equipment in your building.'),
       ('One call, every surface', 'Carpet, upholstery, tile and grout, and hard floors, handled by one local company since 1977.')]
comm_faq = [
    ('Do you clean after construction or remodeling?', 'Yes. We deep-clean carpet, tile and grout, and hard floors after new construction, remodels and contractor work, removing drywall dust, sawdust, footprints and grime so the space is ready to move into or show.'),
    ('Can you clean after hours?', 'Yes. Weekday service runs Monday through Friday, 8 AM to 5 PM, and evening and Saturday appointments are available so cleaning doesn&rsquo;t interrupt your business.'),
    ('Do you offer recurring service?', 'Yes. We can set up a recurring schedule for carpet cleaning or floor strip and wax, or come out for a one-time deep clean.'),
    ('Do you clean apartments between tenants?', 'Yes. We clean carpet and floors in units between tenants, plus hallways and common areas for apartment communities.'),
    ('How do I get a commercial quote?', f'Send a request on our Request a Quote page or call {PHONE}. We&rsquo;ll go over your space and give you a clear price before any work starts.')]
clean_txt = lambda s: re.sub('&amp;', '&', re.sub('&rsquo;', "'", s))
comm_schema = {"@context": "https://schema.org", "@graph": [
    {"@type": "Service", "name": "Commercial carpet, upholstery, tile and floor cleaning", "serviceType": "Commercial cleaning",
     "provider": {"@id": SITE + "/#business"}, "areaServed": [{"@type": "AdministrativeArea", "name": c + ", WI"} for c in COUNTIES]},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": clean_txt(q), "acceptedAnswer": {"@type": "Answer", "text": clean_txt(a)}} for q, a in comm_faq]}]}
COMM_PROJECTS = [
    ('commercial', 'Post-construction cleanup', 'New carpet and floors cleaned of construction dust and footprints before move-in or the final walkthrough.'),
    ('commercial', 'Church carpet', 'Sanctuaries, fellowship halls and classrooms cleaned between services and events.'),
    ('commercial', 'Office carpet &amp; chairs', 'Work areas, conference rooms and upholstered office chairs refreshed after hours.'),
    ('floor', 'Hallway &amp; lobby strip and wax', 'Worn finish stripped away and fresh wax applied on vinyl and VCT floors.'),
    ('carpet', 'Apartment turnovers', 'Carpet in units cleaned between tenants, plus hallway and common-area carpet.'),
    ('tile', 'Restroom &amp; kitchen tile', 'Grout lines in high-traffic restrooms, break rooms and kitchens brought back to bright.'),
    ('rugs', 'Lobby &amp; entry rugs', 'Entry and lobby rugs cleaned to keep the first thing visitors see looking sharp.'),
]
comm_proj_html = ''.join(f'<div class="card"><span class="ic">{svg(ICON[k])}</span><h3>{t}</h3><p>{d}</p></div>' for k, t, d in COMM_PROJECTS)
bld_html = ''.join(f'<div class="card"><span class="ic">{svg(ICON["commercial"])}</span><h3>{t}</h3><p>{d}</p></div>' for t, d in BUILDINGS)
why_html = ''.join(f'<div class="step"><span class="step-n">{CHECK.replace("#2A4C9E", "#fff")}</span><h3>{t}</h3><p>{d}</p></div>' for t, d in WHY)
comm_checks = ''.join(f'<li class="check">{CHECK}<span>{i}</span></li>' for i in COMM_ITEMS)
comm_faq_html = ''.join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in comm_faq)
commercial = head(
    "Commercial Carpet & Floor Cleaning | Syl's Cleaning, WI",
    f"Commercial and post-construction carpet, tile & grout and floor cleaning for offices, apartments, churches, new homes and remodels in {AREA_SHORT}. After-hours available.",
    '/commercial/', 'syls-floor.jpg', comm_schema) + header('commercial') + f"""
<section class="wrap hero-wrap"><div class="hero">
<div class="hero-txt">
<p class="eyebrow">Commercial cleaning</p>
<h1>Commercial Carpet &amp; Floor Cleaning</h1>
<p class="lead">Clean carpet and floors make a strong first impression. We keep offices, apartment communities, churches and businesses looking their best, on a schedule that works around you.</p>
{btns()}
</div>
<div class="photo">{pic("syls-floor.jpg", "Freshly cleaned commercial hallway floor")}</div>
</div></section>
<section class="wrap s"><h2>What we clean for businesses</h2><ul class="checks">{comm_checks}</ul></section>
<section class="wrap s" id="post-construction"><div class="split">
<div><p class="eyebrow-d">New homes &middot; Remodels &middot; Contractor work</p><h2>Post-construction cleaning</h2>
<p class="sub">Construction leaves more behind than you can see. Drywall dust, sawdust and grit settle deep into new carpet and grout lines, and work boots track it across every floor. Before anyone moves in, or before the final walkthrough, we deep-clean the carpet and floors so the space looks as new as it is.</p></div>
<ul class="checks one-col">{''.join(f'<li class="check">{CHECK}<span>{i}</span></li>' for i in ['New homes before move-in', 'Remodels, additions &amp; basement finishes', 'Offices &amp; storefronts after a build-out', 'Apartment units after renovation', 'Drywall dust, sawdust &amp; footprints removed', 'Carpet, tile &amp; grout and hard floors'])}</ul>
</div><p class="sub" style="margin-top:22px"><strong>Builders, contractors &amp; property managers:</strong> we&rsquo;re glad to be your go-to for final carpet and floor cleaning. Call <a href="{TEL}">{PHONE}</a> to set up your next project.</p></section>

<section class="wrap s"><h2>Buildings we clean</h2><p class="sub">From a single office to a full apartment community.</p><div class="grid">{bld_html}</div></section>
<section class="wrap s"><h2>Why businesses choose Syl&rsquo;s</h2><div class="grid">{why_html}</div></section>
<section class="wrap s"><h2>Commercial projects we do</h2><p class="sub">The jobs businesses call us for most.</p><div class="grid">{comm_proj_html}</div></section>
<section class="wrap s"><div class="reviews one">{review_cards([REVIEW_LIST[1]])}</div></section>
<section class="wrap s"><h2>Common questions</h2><div class="faqs">{comm_faq_html}</div></section>
{cta('Need a cleaner building?', 'Tell us about your space and we&rsquo;ll put together a free quote.')}
""" + footer()
write('/commercial/', commercial)

# ---------------- ABOUT & REVIEWS ----------------
PROJECTS = [
    ('carpet', 'Whole-home carpet before a sale', 'Every room deep-cleaned, tough stains and pet accidents treated, so the home shows its best.'),
    ('carpet', 'Move-in cleaning for a new home', 'Fresh, clean carpet before the furniture arrives in a home you just bought.'),
    ('carpet', 'Sofas, chairs &amp; mattresses', 'Upholstery cleaned deep, including pieces other cleaners couldn&rsquo;t get clean.'),
    ('rugs', 'Area &amp; oriental rugs', 'Everyday rugs and specialty rugs cleaned with care to bring back color and softness.'),
    ('tile', 'Kitchen &amp; bathroom tile', 'Grime lifted out of grout lines so tile floors and showers look bright again.'),
    ('commercial', 'Churches, offices &amp; apartments', 'High-traffic carpet and floors for businesses, scheduled around your hours.'),
]
proj_html = ''.join(f'<div class="card"><span class="ic">{svg(ICON[k])}</span><h3>{t}</h3><p>{d}</p></div>' for k, t, d in PROJECTS)
VALUES = [('Locally owned', 'Owned and run from our shop at 3750 S River Rd in West Bend, by people who live and work here.'),
          ('Since 1977', 'Nearly 50 years of cleaning carpet, furniture and floors across southeastern Wisconsin.'),
          ('Reliability in professional cleaning', 'We show up on time, treat your home or building with care, and stand behind the work.')]
values_html = ''.join(f'<div class="step"><span class="step-n">{CHECK.replace("#2A4C9E", "#fff")}</span><h3>{t}</h3><p>{d}</p></div>' for t, d in VALUES)
about = head(
    "About Us & Reviews | Syl's Cleaning, West Bend WI",
    f"Syl's Cleaning is locally owned and operated in West Bend, WI since 1977. Rated {RATING} stars from {REVIEWS} Google reviews. Carpet, upholstery, rug, tile and floor cleaning.",
    '/about/', ABOUT_IMG) + header('about') + f"""
<section class="wrap hero-wrap"><div class="hero">
<div class="hero-txt">
<p class="eyebrow">About Syl&rsquo;s</p>
<h1>Locally owned. Locally trusted.</h1>
<p class="lead">Syl&rsquo;s has been cleaning carpet, furniture and floors for families and businesses in southeastern Wisconsin since 1977. Today Syl&rsquo;s is owned by Ben Seaman and run from our shop in West Bend, with a crew that takes pride in doing the job right.</p>
{btns()}
</div>
<div class="photo">{pic(ABOUT_IMG, ABOUT_ALT)}<div class="seal">{B.badge(150)}</div></div>
</div></section>
<section class="wrap s"><div class="grid">{values_html}</div></section>
<section class="wrap s" id="reviews"><h2>What our customers say</h2><p class="sub"><span class="stars-inline" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span> {RATING} stars from {REVIEWS} Google reviews</p><div class="reviews">{review_cards(REVIEW_LIST)}</div><p class="more-link"><a href="{GMAPS}" target="_blank" rel="noopener">Read all {REVIEWS} reviews on Google &rarr;</a> &nbsp;&middot;&nbsp; <a href="{REVIEW_URL}" target="_blank" rel="noopener">Leave a review &rarr;</a></p></section>
<section class="wrap s"><h2>Projects we do</h2><p class="sub">The jobs our customers call us for most.</p><div class="grid">{proj_html}</div></section>
{cta('Ready for a cleaner space?', 'Send us a quick request and we&rsquo;ll reach out to schedule.')}
""" + footer()
write('/about/', about)

# ---------------- REQUEST A QUOTE ----------------
quote = head(
    "Contact Us & Free Quotes | Syl's Cleaning, West Bend WI",
    f"Contact Syl's Cleaning: call {PHONE}, email {EMAIL}, or request a free quote online. Shop at 3750 S River Rd, West Bend, WI. Serving {AREA_SHORT}.",
    '/contact/') + header('contact') + f"""
<section class="wrap contact-top">
<p class="eyebrow-d">Contact us</p>
<h1>Let&rsquo;s get you a free quote</h1>
<p class="sub">Send a request, give us a call or send an email. We&rsquo;ll get back to you to schedule.</p>
<div class="contact-cards">
<a class="ccard" href="{TEL}">{PHONE_IC}<strong>Call us</strong><span>{PHONE}</span></a>
<a class="ccard" href="mailto:{EMAIL}">{MAIL_IC}<strong>Email</strong><span>info@<wbr>sylscleaning.com</span></a>
<a class="ccard" href="{GMAPS}" target="_blank" rel="noopener">{PIN_IC}<strong>Our shop</strong><span>3750 S River Rd, West Bend, WI 53095</span></a>
<div class="ccard">{CLOCK_IC}<strong>Hours</strong><span>{HOURS}<br>{HOURS_NOTE}</span></div>
</div>
</section>
<section class="wrap quote">
<div class="quote-main">
<h2>Request a free quote</h2>
<p class="sub">Tell us a little about what you need. It takes about a minute.</p>
<div class="jobber">
<!-- JOBBER_FORM -->
<div id="ba537b6b-99e0-4482-b46a-1a8b75f7292a-5279390"></div><link rel="stylesheet" href="https://d3ey4dbjkt2f6s.cloudfront.net/assets/external/work_request_embed.css" media="screen" /><script src="https://d3ey4dbjkt2f6s.cloudfront.net/assets/static_link/work_request_embed_snippet.js" clienthub_id="ba537b6b-99e0-4482-b46a-1a8b75f7292a-5279390" form_url="https://clienthub.getjobber.com/client_hubs/ba537b6b-99e0-4482-b46a-1a8b75f7292a/public/work_request/embedded_work_request_form?form_id=5279390"></script>
<noscript><p><a class="btn btn-b" href="https://clienthub.getjobber.com/hubs/ba537b6b-99e0-4482-b46a-1a8b75f7292a/public/requests/5279390/new">Open the request form</a></p></noscript>
<p class="form-note">Having trouble with the form? <a href="https://clienthub.getjobber.com/hubs/ba537b6b-99e0-4482-b46a-1a8b75f7292a/public/requests/5279390/new">Open it in a new page</a> or call <a href="{TEL}">{PHONE}</a>.</p>
<!-- /JOBBER_FORM -->
</div>
</div>
<aside class="quote-side">
<div class="map map-lg"><iframe title="Map to Syl&rsquo;s Cleaning, 3750 S River Rd, West Bend" src="https://www.google.com/maps?q=3750+S+River+Rd,+West+Bend,+WI+53095&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe><a href="{GMAPS}" target="_blank" rel="noopener">3750 S River Rd, West Bend &middot; Get directions &rarr;</a></div>
<div class="info"><div><strong>Service area</strong><span>{AREA_SHORT}</span></div><div><strong>We serve</strong><span>Homes, businesses &amp; apartment communities</span></div><div><strong>Follow us</strong><span><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a> &middot; <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></span></div></div>
</aside>
</section>
""" + footer()
write('/contact/', quote)

# ---------------- 404 ----------------
nf = head("Page not found | Syl's Cleaning", "Sorry, that page doesn't exist.", '/404.html') + header('') + f"""
<section class="wrap s" style="text-align:center;padding-bottom:40px"><h1 style="font-size:44px">Page not found</h1><p class="sub">Sorry, we couldn&rsquo;t find that page.</p><div class="btns" style="justify-content:center"><a class="btn btn-b" href="/">Go to the home page</a></div></section>
""" + footer()
open(os.path.join(DIST, '404.html'), 'w').write(nf.replace('<link rel="canonical" href="https://sylscleaning.com/404.html">\n', '').replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1))

# ---------------- assets, sitemap, robots ----------------
A = os.path.join(DIST, 'assets'); os.makedirs(A, exist_ok=True)
shutil.copy(os.path.join(ROOT, 'styles.css'), A)
from PIL import Image
for f in os.listdir(os.path.join(ROOT, 'src/photos')):
    src = os.path.join(ROOT, 'src/photos', f)
    if not f.endswith('.jpg'):
        shutil.copy(src, A); continue
    im = Image.open(src).convert('RGB')
    im.save(os.path.join(A, f), 'JPEG', quality=78, optimize=True, progressive=True)
    base = f[:-4]
    for w in (800, 1400):
        r = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(os.path.join(A, f'{base}-{w}.webp'), 'WEBP', quality=72, method=6)
open(os.path.join(A, 'favicon.svg'), 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#2A4C9E"/>'
    f'<svg x="6" y="12" width="52" height="40" viewBox="{VB}"><path fill="#FFFFFF" fill-rule="evenodd" d="{P}"/></svg></svg>')
pages = ['/', '/carpet-upholstery/', '/tile-grout/', '/floor-care/', '/area-rugs/', '/commercial/', '/about/', '/contact/'] + [h for h, _ in AREA_LINKS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
     ''.join(f'  <url><loc>{SITE}{p}</loc></url>\n' for p in pages) + '</urlset>\n'
open(os.path.join(DIST, 'sitemap.xml'), 'w').write(sm)
open(os.path.join(DIST, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
# Netlify handles www -> sylscleaning.com (primary domain) automatically
open(os.path.join(DIST, '_redirects'), 'w').write('')
# llms.txt: plain-language summary for AI assistants
llms = f"""# Syl's Cleaning (Syl's Carpet & Upholstery Cleaning)

> Locally owned and operated professional cleaning company in southeastern Wisconsin, serving homes, businesses and apartment communities since 1977. Slogan: Reliability in Professional Cleaning.

- Phone: {PHONE}
- Email: {EMAIL}
- Website: {SITE}/
- Service area: {', '.join(n for _, n, _, _ in AREAS)}, Wisconsin
- Towns served include: {', '.join(t for _, _, ts, _ in AREAS for t in ts)}

## Services
- [Carpet & Upholstery Cleaning]({SITE}/carpet-upholstery/): wall-to-wall carpet, spot and stain treatment, sofas, sectionals, chairs, mattresses, vehicle seats, carpet repair
- [Tile & Grout Cleaning]({SITE}/tile-grout/): ceramic and porcelain tile, grout lines, kitchens, bathrooms, showers, entryways, commercial tile
- [Floor Care (Strip & Wax)]({SITE}/floor-care/): stripping and waxing vinyl, VCT and other hard floors; apartment hallways, lobbies, offices; one-time or recurring
- [Area Rug Cleaning]({SITE}/area-rugs/): everyday area rugs and oriental rugs
- [Commercial Cleaning]({SITE}/commercial/): offices, apartment communities, churches, retail, medical and dental offices, schools, salons and rental turnovers; post-construction carpet and floor cleaning for new homes, remodels and contractor work; evening and Saturday appointments; one-time or recurring

## Reviews
- Rated {RATING} stars from {REVIEWS} Google reviews: [about us and customer reviews]({SITE}/about/)
- Facebook: {FACEBOOK}
- LinkedIn: {LINKEDIN}

## Service areas
""" + ''.join(f"- [{n}]({SITE}/service-areas/{sl}/): {', '.join(ts)}\n" for sl, n, ts, _ in AREAS) + f"""
## Get a quote
- [Request a free quote]({SITE}/contact/) or call {PHONE}
"""
open(os.path.join(DIST, 'llms.txt'), 'w').write(llms)
print('built', pages)
