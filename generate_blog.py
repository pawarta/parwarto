#!/usr/bin/env python3
"""Generator blog otomatis PAWARTA.

Nggawe kanggo saben rubrik (69 rubrik x 30 artikel):
    /<rubrik>/index.html, /<rubrik>/artikel1.html ... artikel30.html,
    /<rubrik>/sitemap.html, /<rubrik>/sitemap.xml, /<rubrik>/sitemap.txt
Lan file global: /kategori.html, /arsip.html, /search.json, /sitemap-index.xml,
    /terima-kasih.html, /assets/blog.css, /assets/blog.js

Panganggone:
    python3 generate_blog.py                       # nulis langsung ing root repo (GitHub Pages)
    python3 generate_blog.py --out dist --copy-static   # kanggo Netlify (publish dist)

Variabel lingkungan:
    SITE_URL   URL dhasar kanggo canonical/og/sitemap (default: URL Netlify utawa https://pawarta.github.io)
    NETLIFY    yen "true", gambar dilewati Netlify Image CDN (otomatis ing build Netlify)
"""
import argparse
import hashlib
import html
import json
import os
import random
import re
import shutil
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

from blog_content import (AUTHORS, CATEGORIES, FAQS, GROUPS, MANNERS, OBJECTS, OPENERS, PLACES, PURPOSES,
                          REGION_PLACES, SECTIONS, SENTENCES, TABLE_IMPACT, TABLE_NEXT, TABLE_NOW, TABLE_ROWS,
                          TIPS, TITLE_ANGLES, VERBS)

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTICLES_PER_CATEGORY = 30
MIN_WORDS = 3000
YEAR, NEXT_YEAR = 2026, 2027
BASE_DATE = datetime(2026, 10, 6, 8, 0, tzinfo=timezone(timedelta(hours=7)))
ADS_CLIENT = "ca-pub-9308517202792186"
ADS_SLOT = "8374036730"
GA_ID = "G-GN5PGKKM3T"
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober",
         "November", "Desember"]

GROUP_IMAGES = {g: f"/img/blog/{g}.jpg" for g in GROUPS}
FALLBACK_IMAGES = ["/img/bahasa-jawa.jpeg", "/img/ai.jpeg", "/img/3d.jpeg", "/img/macapat.jpeg",
                   "/img/maps.jpeg", "/img/calendar.jpeg"]

SITE_URL = ""
USE_CDN = False

esc = html.escape


# --------------------------------------------------------------------------- helpers
def seeded(*parts):
    return random.Random(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest())


def abs_url(path):
    return SITE_URL + path


def img_src(path, w):
    if USE_CDN:
        return f"/.netlify/images?url={quote(path)}&w={w}&fm=webp&q=75"
    return path


def fmt_date(d):
    return f"{d.day} {BULAN[d.month - 1]} {d.year}"


def word_count(text):
    return len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", text)))


# --------------------------------------------------------------------------- model data
class Category:
    def __init__(self, idx, slug, label, group, subs):
        self.idx, self.slug, self.label, self.group, self.subs = idx, slug, label, group, subs
        self.ctx = GROUPS[group]
        self.places = REGION_PLACES.get(slug, PLACES)
        self.url = f"/{slug}/index.html"
        self.articles = []

    @property
    def image(self):
        return GROUP_IMAGES[self.group]


class Article:
    def __init__(self, cat, n):
        self.cat, self.n = cat, n
        self.sub = cat.subs[(n - 1) % len(cat.subs)]
        self.title = TITLE_ANGLES[n - 1].format(sub=self.sub, cat=cat.label, year=YEAR, next=NEXT_YEAR)
        self.url = f"/{cat.slug}/artikel{n}.html"
        self.date = BASE_DATE - timedelta(days=(n - 1) * 3 + cat.idx % 3, hours=cat.idx % 9, minutes=(cat.idx * 7) % 60)
        rng = seeded("meta", cat.slug, n)
        self.author = AUTHORS[(cat.idx + n) % len(AUTHORS)]
        self.views = rng.randint(1200, 48000) + (ARTICLES_PER_CATEGORY - n) * 350
        self.read_min = 14
        self.image = cat.image if n % 3 != 0 or not os.path.exists(os.path.join(ROOT, cat.image.lstrip("/"))) \
            else FALLBACK_IMAGES[(cat.idx + n) % len(FALLBACK_IMAGES)]
        self.desc = (f"{self.sub}: ulasan lengkap rubrik {cat.label} PAWARTA tentang data, tantangan, peluang, "
                     f"dan strategi praktis {YEAR} berbalut kearifan budaya Jawa.")
        self.keywords = ", ".join([self.sub.lower(), cat.label.lower(), f"berita {cat.label.lower()}",
                                   f"{self.sub.lower()} {YEAR}", "pawarta", "warta jawa", "berita indonesia"])
        self.img_alt = f"Ilustrasi {self.sub} - rubrik {cat.label} PAWARTA"


def build_model():
    cats = [Category(i, *c) for i, c in enumerate(CATEGORIES)]
    for c in cats:
        c.articles = [Article(c, n) for n in range(1, ARTICLES_PER_CATEGORY + 1)]
    for c in cats:
        if not os.path.exists(os.path.join(ROOT, c.image.lstrip("/"))):
            fb = FALLBACK_IMAGES[c.idx % len(FALLBACK_IMAGES)]
            GROUP_IMAGES[c.group] = fb
            for a in c.articles:
                if a.image.startswith("/img/blog/"):
                    a.image = fb
    return cats


# --------------------------------------------------------------------------- text engine
class Writer:
    """Nggawe paragraf kanthi seed deterministik, ora mbaleni ukara ing artikel sing padha."""

    def __init__(self, art):
        self.art = art
        self.rng = seeded("body", art.cat.slug, art.n)
        self.pool = SENTENCES[:]
        self.rng.shuffle(self.pool)
        self.used = set()

    def fill(self, tpl):
        c = self.art.cat
        r = self.rng
        return tpl.format(sub=self.art.sub, cat=c.label, actor=r.choice(c.ctx["actors"]),
                          ind=r.choice(c.ctx["indicators"]), chal=r.choice(c.ctx["challenges"]),
                          opp=r.choice(c.ctx["opps"]), place=r.choice(c.places), pct=r.randint(8, 46),
                          year=YEAR, next=NEXT_YEAR)

    def combo(self):
        r = self.rng
        for _ in range(20):
            s = " ".join([r.choice(OPENERS), r.choice(self.art.cat.ctx["actors"]), r.choice(VERBS),
                          r.choice(OBJECTS), r.choice(MANNERS), r.choice(PURPOSES)])
            s = self.fill(s)
            if s not in self.used:
                break
        self.used.add(s)
        return s[0].upper() + s[1:]

    def sentence(self):
        if self.pool and self.rng.random() < 0.62:
            return self.fill(self.pool.pop())
        return self.combo()

    def para(self, n=5):
        return "<p>" + " ".join(self.sentence() for _ in range(n)) + "</p>"


# --------------------------------------------------------------------------- shared layout
def head(title, desc, keywords, canonical, og_image, og_type="website", jsonld=None):
    ld = ""
    if jsonld:
        ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n'
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>

<!-- Meta SEO & Verification -->
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(keywords)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="PAWARTA">
<meta name="google-site-verification" content="IAcn_DcNzAkFuMAjiMDNMoUEMZV5oKau1XrJ4aDJlRc">
<meta name="msvalidate.01" content="E9411F953448412F854C1FBA584B1383">
<script async custom-element="amp-ad" src="https://cdn.ampproject.org/v0/amp-ad-0.1.js"></script>

<!-- Open Graph / Social Media Meta -->
<meta property="og:site_name" content="PAWARTA">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{esc(og_image)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="id_ID">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(og_image)}">

<!-- Favicon & Icons -->
<link rel="icon" href="https://pawarta.github.io/pawarta.ico" type="image/x-icon">
<link rel="shortcut icon" href="https://pawarta.github.io/pawarta.ico" type="image/x-icon">
<link rel="icon" href="https://pawarta.github.io/pawarta.jpg" type="image/x-icon">
<link rel="shortcut icon" href="https://pawarta.github.io/pawarta.png" type="image/x-icon">

<!-- Canonical & Hreflang Links -->
<link rel="canonical" href="{esc(canonical)}">
<link rel="alternate" href="https://pawarta.github.io/en-us/" hreflang="en-us">
<link rel="alternate" href="https://pawarta.github.io/en/" hreflang="en">
<link rel="alternate" href="https://pawarta.github.io/es/" hreflang="es">
<link rel="alternate" href="https://pawarta.github.io/" hreflang="x-default">
<link rel="alternate" hreflang="fr" href="https://pawarta.github.io/fr/">
<link rel="alternate" hreflang="de" href="https://pawarta.github.io/de/">
<link rel="alternate" hreflang="th" href="https://pawarta.github.io/th/">
<link rel="alternate" hreflang="id" href="https://pawarta.github.io/id/">

<!-- Stylesheets (Bootstrap 5, Icons, Animate.css) -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
<link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
<link href="/assets/blog.css" rel="stylesheet">

<!-- AMP Auto Ads -->
<script async custom-element="amp-auto-ads" src="https://cdn.ampproject.org/v0/amp-auto-ads-0.1.js"></script>

<!-- Google AdSense -->
<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADS_CLIENT}"></script>

<!-- Google tag (gtag.js) - GA4 ID: {GA_ID} -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>
{ld}</head>
<body class="d-flex flex-column min-vh-100">
<amp-auto-ads type="adsense" data-ad-client="{ADS_CLIENT}"></amp-auto-ads>
"""


def cookie_banner():
    return """
<div id="cookieBanner" class="cookie-banner d-flex flex-column flex-md-row justify-content-between align-items-center gap-3">
  <div><p class="mb-0 small"><i class="fas fa-cookie-bite text-java-gold me-2"></i>Situs web menika nggunakaken cookies kanggé ningkataken pengalaman pangguna sarta analitik iklan (Google AdSense). Kanthi nglajengaken, panjenengan sarujuk dhateng kawicaksanan cookies.</p></div>
  <div class="d-flex gap-2">
    <button onclick="acceptCookies()" class="btn btn-sm btn-java-gold px-4">Sarujuk</button>
    <button onclick="rejectCookies()" class="btn btn-sm btn-outline-light px-3">Tolak</button>
  </div>
</div>
"""


def navbar(cats, active=None):
    by = {c.slug: c for c in cats}

    def items(slugs):
        return "".join(f'<li><a class="dropdown-item" href="{by[s].url}">{esc(by[s].label)}</a></li>' for s in slugs)

    mega = "".join(f'<a class="dropdown-item{" active" if c.slug == active else ""}" href="{c.url}">{esc(c.label)}</a>'
                   for c in cats)
    return f"""
<!-- Header & Navigation -->
<header class="sticky-top shadow-sm">
  <nav class="navbar navbar-expand-lg navbar-dark bg-java-maroon py-2">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center gap-2" href="/index.html">
        <img src="https://pawarta.github.io/pawarta.jpg" alt="Logo Pawarta" width="45" height="45">
        <div>
          <span class="rainbow-text fs-4 font-heading">PAWARTA</span>
          <div style="font-size: 10px; color: #d4af37;">ꦥꦮꦂꦠ - Javanese Portal</div>
        </div>
      </a>
      <button class="navbar-toggler border-0 text-white" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-label="Menu">
        <i class="fas fa-bars fs-2"></i>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-lg-center gap-lg-2">
          <li class="nav-item"><a class="nav-link" href="/index.html"><i class="fas fa-home me-1"></i> Utami</a></li>
          <li class="nav-item dropdown position-static">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Rubrik</a>
            <div class="dropdown-menu mega-menu p-3"><div class="mega-grid">{mega}</div>
              <div class="border-top border-warning mt-2 pt-2 text-center"><a class="text-java-gold small" href="/kategori.html">Deleng sedaya rubrik &raquo;</a></div></div>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Ekonomi</a>
            <ul class="dropdown-menu">{items(["market", "finance", "macro", "economy", "money", "perbankan", "sharia", "business", "smes", "property"])}</ul>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Warta</a>
            <ul class="dropdown-menu">{items(["news", "politics", "public-policy", "international", "commentary", "opinion", "interview", "whos-who"])}</ul>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Daerah</a>
            <ul class="dropdown-menu">{items(["dki", "diy", "jabar", "jateng", "jatim", "bali", "sumatra", "kalimantan", "sulawesi", "papua", "aceh"])}</ul>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Budaya &amp; Gaya</a>
            <ul class="dropdown-menu">{items(["culture", "sejarah", "arts", "lifestyle", "health", "sports", "football", "celebrities", "zodiak"])}</ul>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Tekno</a>
            <ul class="dropdown-menu">{items(["tech", "ai", "teknologi", "science", "astronomi", "automotive", "maps"])}</ul>
          </li>
          <li class="nav-item"><a class="nav-link" href="#kontak">Kontak</a></li>
          <li class="nav-item ms-lg-2">
            <button class="btn btn-java-gold btn-sm px-3 rounded-pill" data-bs-toggle="modal" data-bs-target="#searchModal">
              <i class="fas fa-search"></i> Golek
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</header>
"""


def slider(slides):
    ind, items = [], []
    for i, s in enumerate(slides):
        active = ' class="active" aria-current="true"' if i == 0 else ""
        ind.append(f'<button type="button" data-bs-target="#pawartaSlider" data-bs-slide-to="{i}"'
                   f'{active} aria-label="Slide {i + 1}"></button>')
        items.append(f"""
    <div class="carousel-item{' active' if i == 0 else ''}" style="background-image: url('{img_src(s['img'], 1600)}');" role="img" aria-label="{esc(s['alt'])}">
      <div class="carousel-overlay"></div>
      <div class="carousel-caption text-center animate__animated animate__fadeInDown">
        <h2 class="honocoroko-title">{s['aksara']}</h2>
        <p class="display-5 fw-bold text-white mb-3 font-heading">{s['title']}</p>
        <p class="lead text-light">{esc(s['text'])}</p>
        <a href="{s['href']}" class="btn btn-warning btn-lg fw-bold mt-2 shadow">{esc(s['cta'])}</a>
      </div>
    </div>""")
    return f"""
<!-- Responsive Slider Section -->
<div id="pawartaSlider" class="carousel slide carousel-fade shadow" data-bs-ride="carousel">
  <div class="carousel-indicators">{''.join(ind)}</div>
  <div class="carousel-inner">{''.join(items)}
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#pawartaSlider" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span><span class="visually-hidden">Sadurunge</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#pawartaSlider" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span><span class="visually-hidden">Sabanjure</span>
  </button>
</div>
"""


def ad_block(label="Ruang Iklan / Google AdSense"):
    return f"""
<div class="ad-slot my-4 text-center">
  <div class="small text-muted mb-1">--- {label} ---</div>
  <!-- Banners ads -->
  <ins class="adsbygoogle" style="display:block" data-ad-client="{ADS_CLIENT}" data-ad-slot="{ADS_SLOT}" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>
"""


def share_buttons(url, title):
    u, t = quote(url, safe=""), quote(title, safe="")
    links = [
        ("Facebook", "fab fa-facebook-f", "#1877f2", f"https://www.facebook.com/sharer/sharer.php?u={u}"),
        ("X / Twitter", "fab fa-x-twitter", "#000", f"https://twitter.com/intent/tweet?url={u}&text={t}"),
        ("WhatsApp", "fab fa-whatsapp", "#25d366", f"https://api.whatsapp.com/send?text={t}%20{u}"),
        ("Telegram", "fab fa-telegram", "#229ed9", f"https://t.me/share/url?url={u}&text={t}"),
        ("LinkedIn", "fab fa-linkedin-in", "#0a66c2", f"https://www.linkedin.com/sharing/share-offsite/?url={u}"),
        ("Pinterest", "fab fa-pinterest-p", "#e60023", f"https://pinterest.com/pin/create/button/?url={u}&description={t}"),
        ("Email", "fas fa-envelope", "#6c757d", f"mailto:?subject={t}&body={u}"),
    ]
    btns = "".join(f'<a class="share-btn" style="background:{c}" href="{h}" target="_blank" rel="noopener noreferrer" '
                   f'aria-label="Bagikan ke {n}" title="Bagikan ke {n}"><i class="{i}"></i></a>' for n, i, c, h in links)
    return f"""
<div class="share-box d-flex flex-wrap align-items-center gap-2 my-4">
  <span class="fw-bold small text-java-maroon me-1"><i class="fas fa-share-nodes"></i> Bagikan:</span>{btns}
  <button class="share-btn" style="background:#D4AF37" onclick="copyLink(this)" data-url="{esc(url)}" aria-label="Salin tautan" title="Salin tautan"><i class="fas fa-link"></i></button>
</div>
"""


def contact_form():
    return """
<div class="sidebar-widget" id="kontak">
  <h5 class="font-heading fw-bold text-java-maroon mb-3 border-bottom pb-2"><i class="fas fa-paper-plane text-success me-2"></i>Kirim Saran / Warta</h5>
  <form name="kontak-pawarta" method="POST" action="/terima-kasih.html" data-netlify="true" netlify-honeypot="bot-field" class="pawarta-contact">
    <input type="hidden" name="form-name" value="kontak-pawarta">
    <p class="d-none"><label>Aja diisi: <input name="bot-field"></label></p>
    <input type="hidden" name="halaman" value="">
    <div class="mb-3"><label class="form-label small fw-bold">Asma Panjenengan</label>
      <input type="text" name="nama" class="form-control form-control-sm" required placeholder="Sartono..."></div>
    <div class="mb-3"><label class="form-label small fw-bold">Serat Elektronik (Email)</label>
      <input type="email" name="email" class="form-control form-control-sm" required placeholder="sartono@mail.com"></div>
    <div class="mb-3"><label class="form-label small fw-bold">Pesen / Pawarta</label>
      <textarea name="pesan" class="form-control form-control-sm" rows="3" required placeholder="Tulis pesen panjenengan wonten mriki..."></textarea></div>
    <button type="submit" class="btn btn-java-gold btn-sm w-100 fw-bold">Kirim Pesen</button>
  </form>
</div>
"""


def mini_list(arts, icon, show_cat=True):
    rows = []
    for a in arts:
        meta = f'{esc(a.cat.label)} · {fmt_date(a.date)}' if show_cat else fmt_date(a.date)
        rows.append(f"""<li class="d-flex gap-2 py-2 border-bottom">
  <img src="{img_src(a.image, 120)}" alt="{esc(a.img_alt)}" width="64" height="48" loading="lazy" class="rounded object-fit-cover flex-shrink-0">
  <div><a href="{a.url}" class="text-decoration-none text-dark small fw-semibold d-block lh-sm">{esc(a.title)}</a>
  <span class="text-muted" style="font-size:11px"><i class="{icon} me-1"></i>{meta}</span></div></li>""")
    return '<ul class="list-unstyled mb-0">' + "".join(rows) + "</ul>"


def sidebar(cat, cats, all_articles, current=None):
    arts = [a for a in cat.articles if a is not current]
    popular = sorted(arts, key=lambda a: -a.views)[:5]
    latest = sorted(all_articles, key=lambda a: a.date, reverse=True)
    latest = [a for a in latest if a is not current][:5]
    oldest = sorted(arts, key=lambda a: a.date)[:5]
    labels = "".join(f'<a href="{c.url}" class="badge rounded-pill label-pill text-decoration-none">{esc(c.label)}</a>'
                     for c in cats)
    months = {}
    for a in all_articles:
        k = a.date.strftime("%Y-%m")
        months[k] = months.get(k, 0) + 1
    archive = "".join(
        f'<li class="py-2 border-bottom d-flex justify-content-between align-items-center"><a href="/arsip.html#arsip-{k}" '
        f'class="text-decoration-none text-dark">{BULAN[int(k[5:]) - 1]} {k[:4]}</a> <span class="badge bg-secondary">{v}</span></li>'
        for k, v in sorted(months.items(), reverse=True))
    return f"""
<aside class="col-lg-4">
  <div class="sidebar-widget text-center bg-light">{ad_block()}</div>
  <div class="sidebar-widget">
    <h5 class="font-heading fw-bold text-java-maroon mb-3 border-bottom pb-2"><i class="fas fa-fire text-danger me-2"></i>Artikel Populer</h5>
    {mini_list(popular, "fas fa-eye", show_cat=False)}
  </div>
  <div class="sidebar-widget">
    <h5 class="font-heading fw-bold text-java-maroon mb-3 border-bottom pb-2"><i class="fas fa-bolt text-warning me-2"></i>Artikel Terbaru</h5>
    {mini_list(latest, "far fa-clock")}
  </div>
  <div class="sidebar-widget">
    <h5 class="font-heading fw-bold text-java-maroon mb-3 border-bottom pb-2"><i class="fas fa-hourglass-start text-secondary me-2"></i>Artikel Terlama</h5>
    {mini_list(oldest, "far fa-calendar", show_cat=False)}
  </div>
  <div class="sidebar-widget">
    <h5 class="font-heading fw-bold text-java-maroon mb-3 border-bottom pb-2"><i class="fas fa-tags text-info me-2"></i>Label</h5>
    <div class="d-flex flex-wrap gap-1">{labels}</div>
  </div>
  <div class="sidebar-widget">
    <h5 class="font-heading fw-bold text-java-maroon mb-3 border-bottom pb-2"><i class="fas fa-archive text-warning me-2"></i>Arsip Warta</h5>
    <ul class="list-unstyled mb-0 small">{archive}</ul>
  </div>
  {contact_form()}
  <div class="card shadow-sm border-0 rounded-4 mb-4">
    <div class="card-header bg-dark text-white fw-bold"><i class="bi bi-link-45deg"></i> Pranala Penting</div>
    <div class="list-group list-group-flush rounded-bottom small">
      <a href="/index.html" class="list-group-item list-group-item-action">Portal Utama (Home)</a>
      <a href="/about.html" class="list-group-item list-group-item-action">Babagan Kami (About)</a>
      <a href="/contact.html" class="list-group-item list-group-item-action">Hubungi Kami (Contact)</a>
      <a href="/privacy.html" class="list-group-item list-group-item-action">Kebijakan Privasi (Privacy)</a>
      <a href="/terms.html" class="list-group-item list-group-item-action">Syarat &amp; Ketentuan (Terms)</a>
      <a href="/disclaimer.html" class="list-group-item list-group-item-action">Penyangkalan (Disclaimer)</a>
      <a href="/{cat.slug}/sitemap.html" class="list-group-item list-group-item-action">Sitemap Rubrik {esc(cat.label)}</a>
      <a href="/kategori.html" class="list-group-item list-group-item-action">Sedaya Rubrik</a>
    </div>
  </div>
  <div class="card shadow-sm border-0 rounded-4">
    <div class="card-header rainbow-badge text-white fw-bold"><i class="bi bi-tools"></i> Pilihan Tools &amp; Layanan</div>
    <div class="list-group list-group-flush rounded-bottom small">
      <a href="/tools/ai/index.html" class="list-group-item list-group-item-action">AI Assistant Tool</a>
      <a href="/tools/bahasa-jawa/index.html" class="list-group-item list-group-item-action">Penerjemah Bahasa Jawa</a>
      <a href="/tools/calendar/index.html" class="list-group-item list-group-item-action">Kalender Jawa / Weton</a>
      <a href="/tools/macapat/index.html" class="list-group-item list-group-item-action">Tembang Macapat</a>
      <a href="/tools/keyboard-jawa/index.html" class="list-group-item list-group-item-action">Keyboard Aksara Jawa</a>
      <a href="/tools/wayang/index.html" class="list-group-item list-group-item-action">Katalog Wayang Kulit</a>
      <a href="/tools/maps/index.html" class="list-group-item list-group-item-action">Peta Lokasi</a>
    </div>
  </div>
</aside>
"""


def footer(cats):
    by = {c.slug: c for c in cats}

    def li(slugs):
        return "".join(f'<li><a href="{by[s].url}" class="text-decoration-none text-white-50">{esc(by[s].label)}</a></li>' for s in slugs)

    return f"""
<!-- Footer -->
<footer class="bg-java-brown text-white pt-5 pb-3 mt-auto border-top border-warning">
  <div class="container">
    <div class="row g-4 mb-4">
      <div class="col-lg-4">
        <div class="d-flex align-items-center gap-2 mb-3">
          <img src="https://pawarta.github.io/pawarta.jpg" alt="Logo PAWARTA" width="40" height="40" class="rounded-circle">
          <span class="font-heading fs-3 rainbow-text">PAWARTA</span>
        </div>
        <p class="small text-white-50">Portal warta digital inovatif kang nyawijiake kabudayan Jawi, aksara Honocoroko, lan teknologi informasi modheren ing donya maya. Melayani informasi terpercaya dengan menjunjung tinggi etika jurnalistik dan nilai luhur nusantara.</p>
        <div class="fs-4 text-warning">ꦫꦲꦪꦸ ꦫꦲꦪꦸ ꦫꦲꦪꦸ</div>
        <div class="d-flex gap-3 mt-3">
          <a href="https://www.facebook.com/" target="_blank" rel="noopener noreferrer" class="text-java-gold fs-5" aria-label="Facebook"><i class="fab fa-facebook"></i></a>
          <a href="https://x.com/" target="_blank" rel="noopener noreferrer" class="text-java-gold fs-5" aria-label="X"><i class="fab fa-x-twitter"></i></a>
          <a href="https://www.youtube.com/" target="_blank" rel="noopener noreferrer" class="text-java-gold fs-5" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
          <a href="https://www.instagram.com/" target="_blank" rel="noopener noreferrer" class="text-java-gold fs-5" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
          <a href="https://github.com/pawarta/pawarta.github.io" target="_blank" rel="noopener noreferrer" class="text-java-gold fs-5" aria-label="GitHub"><i class="fab fa-github"></i></a>
        </div>
      </div>
      <div class="col-6 col-lg-2">
        <h6 class="text-java-gold font-heading fw-bold mb-3">Kategori Warta</h6>
        <ul class="list-unstyled small d-flex flex-column gap-2">{li(["news", "politics", "economy", "tech", "sports", "international"])}</ul>
      </div>
      <div class="col-6 col-lg-2">
        <h6 class="text-java-gold font-heading fw-bold mb-3">Budaya &amp; Sastra</h6>
        <ul class="list-unstyled small d-flex flex-column gap-2">{li(["culture", "sejarah", "arts", "kisah", "zodiak", "diy"])}</ul>
      </div>
      <div class="col-6 col-lg-2">
        <h6 class="text-java-gold font-heading fw-bold mb-3">Pranala Kaca</h6>
        <ul class="list-unstyled small d-flex flex-column gap-2">
          <li><a href="/index.html" class="text-decoration-none text-white-50">Beranda / Index</a></li>
          <li><a href="/about.html" class="text-decoration-none text-white-50">Tentang Kami</a></li>
          <li><a href="/contact.html" class="text-decoration-none text-white-50">Kontak</a></li>
          <li><a href="/privacy.html" class="text-decoration-none text-white-50">Kebijakan Privasi</a></li>
          <li><a href="/terms.html" class="text-decoration-none text-white-50">Syarat &amp; Ketentuan</a></li>
          <li><a href="/kategori.html" class="text-decoration-none text-white-50">Sedaya Rubrik</a></li>
          <li><a href="/arsip.html" class="text-decoration-none text-white-50">Arsip Warta</a></li>
        </ul>
      </div>
      <div class="col-6 col-lg-2">
        <h6 class="text-java-gold font-heading fw-bold mb-3">Warta Langganan</h6>
        <p class="small text-white-50">Kintunaken email panjenengan kanggé langganan warta pilihan saben minggu.</p>
        <div class="input-group input-group-sm mb-3">
          <input type="email" class="form-control" placeholder="Email..." aria-label="Email">
          <button class="btn btn-java-gold" type="button" onclick="subscribeNewsletter()">Langganan</button>
        </div>
      </div>
    </div>
    <div class="row small text-white-50 mb-3">
      <div class="col-md-12">
        <h6 class="text-white fw-bold mb-2">Informasi Aliran Data</h6>
        <span class="me-3">Nama Aliran: <strong>pawarta</strong></span>
        <span class="me-3">ID Pengukuran: <code class="text-warning">{GA_ID}</code></span>
        <span>URL: <a href="https://pawarta.github.io" target="_blank" rel="noopener noreferrer" class="text-java-gold">https://pawarta.github.io</a></span>
      </div>
    </div>
    <div class="border-top border-secondary pt-3 text-center small text-white-50">
      <p class="mb-0">&copy; 2026 PAWARTA (pawarta.github.io). Hak Cipta Dilindungi Undang-Undang. Kinarya kanti katresnan tumrap Budaya Jawi.</p>
    </div>
  </div>
</footer>

<!-- Search Modal -->
<div class="modal fade" id="searchModal" tabindex="-1" aria-label="Pados Warta">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content bg-java-maroon text-white border-warning">
      <div class="modal-header border-bottom border-secondary">
        <h5 class="modal-title font-heading text-java-gold">Pados Warta</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Tutup"></button>
      </div>
      <div class="modal-body">
        <input id="searchInput" type="search" class="form-control" placeholder="Tulis kata kunci warta utawi budaya..." autocomplete="off">
        <div id="searchResults" class="list-group mt-3 search-results"></div>
      </div>
    </div>
  </div>
</div>

<!-- Success Message Modal -->
<div class="modal fade" id="msgModal" tabindex="-1">
  <div class="modal-dialog modal-sm modal-dialog-centered">
    <div class="modal-content text-center p-4">
      <i class="fas fa-check-circle text-success fa-3x mb-3"></i>
      <h5 class="fw-bold font-heading mb-2">Matur Nuwun!</h5>
      <p class="small text-muted mb-3" id="modalMsgContent">Pesen panjenengan sampun katampi.</p>
      <button type="button" class="btn btn-sm btn-java-gold" data-bs-dismiss="modal">Tutup</button>
    </div>
  </div>
</div>

<!-- Bootstrap JS & AOS Animation Script -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
<script src="/assets/blog.js"></script>

<div class="container">
  <!-- Banners ads -->
  <ins class="adsbygoogle" style="display:block" data-ad-client="{ADS_CLIENT}" data-ad-slot="{ADS_SLOT}" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>

<amp-ad width="100vw" height="320" type="adsense" data-ad-client="{ADS_CLIENT}" data-ad-slot="{ADS_SLOT}" data-auto-format="rspv" data-full-width="">
  <div overflow=""></div>
</amp-ad>

</body>
</html>
"""


def breadcrumb_html(items):
    lis = []
    for i, (name, href) in enumerate(items):
        if href and i < len(items) - 1:
            lis.append(f'<li class="breadcrumb-item"><a href="{href}" class="text-decoration-none text-java-maroon">{esc(name)}</a></li>')
        else:
            lis.append(f'<li class="breadcrumb-item active" aria-current="page">{esc(name)}</li>')
    return f'<nav aria-label="breadcrumb" class="mb-3"><ol class="breadcrumb small text-muted mb-0">{"".join(lis)}</ol></nav>'


def breadcrumb_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, **({"item": abs_url(h)} if h else {})}
        for i, (n, h) in enumerate(items)]}


def article_card(a, big=False):
    w, h = (900, 506) if big else (480, 270)
    return f"""
<div class="{'col-12' if big else 'col-md-6'}" data-aos="fade-up">
  <article class="card h-100 border-0 shadow-sm rounded-4 overflow-hidden news-card">
    <a href="{a.url}"><img src="{img_src(a.image, w)}" alt="{esc(a.img_alt)}" width="{w}" height="{h}" loading="lazy" class="card-img-top object-fit-cover" style="aspect-ratio:16/9"></a>
    <div class="card-body">
      <span class="badge bg-java-maroon text-java-gold mb-2">{esc(a.cat.label)}</span>
      <{'h2' if big else 'h3'} class="{'h3' if big else 'h5'} font-heading"><a href="{a.url}" class="text-decoration-none text-java-brown">{esc(a.title)}</a></{'h2' if big else 'h3'}>
      <p class="small text-muted mb-2">{esc(a.desc)}</p>
      <div class="small text-muted"><i class="far fa-calendar-alt text-java-gold me-1"></i>{fmt_date(a.date)}
        <span class="ms-2"><i class="fas fa-user-edit text-java-gold me-1"></i>{esc(a.author[0])}</span>
        <span class="ms-2"><i class="fas fa-eye text-java-gold me-1"></i>{a.views:,}</span></div>
    </div>
  </article>
</div>"""


# --------------------------------------------------------------------------- article page
def render_article(a, cats, all_articles):
    cat = a.cat
    w = Writer(a)
    rng = seeded("struct", cat.slug, a.n)
    fill = w.fill
    place = rng.choice(cat.places)

    # Internal links: 4 rubrik padha + 3 rubrik liya
    same = [x for x in cat.articles if x is not a]
    rng.shuffle(same)
    same = same[:4]
    others_pool = [c for c in cats if c is not cat]
    related_cats = [c for c in others_pool if c.group == cat.group] or others_pool
    rng.shuffle(related_cats)
    while len(related_cats) < 3:
        related_cats.append(rng.choice(others_pool))
    cross = [rng.choice(c.articles) for c in related_cats[:3]]
    internal = same + cross

    refs = cat.ctx["refs"][:]
    rng.shuffle(refs)
    refs = refs[:7]

    body = []
    toc = []

    # Pambuka
    intro = [w.para(5), w.para(5), w.para(4)]
    intro[0] = intro[0].replace("<p>", f'<p class="lead-para"><strong>PAWARTA, {esc(place)}</strong> — ', 1)
    intro.append(f'<p>Artikel ini merupakan bagian dari rubrik <a href="{cat.url}">{esc(cat.label)}</a> di PAWARTA. '
                 f'Kami membahas {esc(a.sub)} secara menyeluruh: mulai dari latar belakang, data terbaru, tantangan, '
                 f'peluang, perspektif budaya Jawa, hingga strategi praktis dan proyeksi menuju {NEXT_YEAR}.</p>')
    body.extend(intro)
    body.append(ad_block("Iklan"))

    alt_imgs = [img for img in FALLBACK_IMAGES + list(GROUP_IMAGES.values())
                if img != a.image and os.path.exists(os.path.join(ROOT, img.lstrip("/")))]
    rng.shuffle(alt_imgs)

    for si, (h2t, h3s) in enumerate(SECTIONS):
        h2 = fill(h2t)
        sid = f"bagian-{si + 1}"
        toc.append((sid, h2, []))
        body.append(f'<h2 id="{sid}">{esc(h2)}</h2>')
        body.append(w.para(3))
        if si == 2:
            body.append(data_table(a, rng))
            r0 = refs[0]
            body.append(f'<p>Untuk data resmi yang lebih rinci, pembaca dapat merujuk ke <a href="{r0[1]}" target="_blank" '
                        f'rel="noopener noreferrer">{esc(r0[0])}</a> serta lembaga terkait lainnya yang kami cantumkan pada '
                        f'bagian referensi.</p>')
        for hi, h3t in enumerate(h3s):
            h3 = fill(h3t)
            hid = f"{sid}-{hi + 1}"
            toc[-1][2].append((hid, h3))
            body.append(f'<h3 id="{hid}">{esc(h3)}</h3>')
            body.append(w.para(5))
        if si == 1:
            body.append(read_also("Baca Juga di Rubrik " + cat.label, same))
        if si in (3, 7) and alt_imgs:
            im = alt_imgs.pop()
            cap = f"Ilustrasi pendukung: {a.sub} dan dinamika {cat.label} di Indonesia ({YEAR})."
            body.append(f'<figure class="figure w-100 my-4"><img src="{img_src(im, 900)}" alt="{esc(cap)}" width="900" height="506" '
                        f'loading="lazy" class="figure-img img-fluid rounded-4 w-100 object-fit-cover" style="aspect-ratio:16/9">'
                        f'<figcaption class="figure-caption text-center">{esc(cap)}</figcaption></figure>')
        if si == 5:
            body.append(ad_block("Iklan"))
            body.append(read_also("Rubrik Terkait", cross))
        if si == 9:
            tips = TIPS[:]
            rng.shuffle(tips)
            body.append('<ol class="tips-list">' + "".join(f"<li>{esc(fill(t))}</li>" for t in tips[:6]) + "</ol>")

    # Mesthekake minimal 3000 tembung
    while word_count("".join(body)) < MIN_WORDS - 350:
        body.append(w.para(5))

    # FAQ
    faq_items = []
    toc.append(("faq", "Pertanyaan yang Sering Diajukan (FAQ)", []))
    body.append('<h2 id="faq">Pertanyaan yang Sering Diajukan (FAQ)</h2>')
    acc = []
    for i, (q, ans) in enumerate(FAQS):
        q2, a2 = fill(q), fill(ans)
        faq_items.append((q2, a2))
        acc.append(f"""<div class="accordion-item"><h3 class="accordion-header" id="faq-h{i}">
<button class="accordion-button{' collapsed' if i else ''}" type="button" data-bs-toggle="collapse" data-bs-target="#faq-c{i}" aria-expanded="{'true' if i == 0 else 'false'}">{esc(q2)}</button></h3>
<div id="faq-c{i}" class="accordion-collapse collapse{' show' if i == 0 else ''}" data-bs-parent="#faqAcc"><div class="accordion-body">{esc(a2)}</div></div></div>""")
    body.append(f'<div class="accordion mb-4" id="faqAcc">{"".join(acc)}</div>')

    # Kesimpulan
    toc.append(("kesimpulan", "Kesimpulan", []))
    body.append('<h2 id="kesimpulan">Kesimpulan</h2>')
    body.append(w.para(5))
    body.append(w.para(4))
    body.append(f'<p>Pada akhirnya, {esc(a.sub)} bukan sekadar isu sesaat, melainkan bagian dari perjalanan panjang bangsa. '
                f'Seperti pesan leluhur Jawa, <em>"urip iku urup"</em> — hidup hendaknya memberi manfaat bagi sesama. '
                f'Ikuti terus perkembangan terbaru di rubrik <a href="{cat.url}">{esc(cat.label)}</a> dan '
                f'<a href="/kategori.html">rubrik lain PAWARTA</a>.</p>')

    # Referensi eksternal
    toc.append(("referensi", "Referensi dan Bacaan Lanjutan", []))
    body.append('<h2 id="referensi">Referensi dan Bacaan Lanjutan</h2><ul class="ref-list">' + "".join(
        f'<li><a href="{u}" target="_blank" rel="noopener noreferrer">{esc(n)}</a> <i class="fas fa-arrow-up-right-from-square small text-muted"></i></li>'
        for n, u in refs) + "</ul>")

    body_html = "\n".join(body)
    words = word_count(body_html)

    toc_html = "".join(
        f'<li><a href="#{i}">{esc(t)}</a>' + (
            '<ol>' + "".join(f'<li><a href="#{si}">{esc(st)}</a></li>' for si, st in subs) + '</ol>' if subs else "") + "</li>"
        for i, t, subs in toc)

    crumbs = [("Kaca Utama", "/index.html"), (cat.label, cat.url), (a.title, None)]
    canonical = abs_url(a.url)
    og_img = abs_url(a.image)
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "NewsArticle", "headline": a.title[:110], "description": a.desc, "image": [og_img],
         "datePublished": a.date.isoformat(), "dateModified": a.date.isoformat(), "wordCount": words,
         "articleSection": cat.label, "keywords": a.keywords, "inLanguage": "id-ID",
         "mainEntityOfPage": canonical,
         "author": {"@type": "Person", "name": a.author[0], "jobTitle": a.author[1]},
         "publisher": {"@type": "Organization", "name": "PAWARTA",
                       "logo": {"@type": "ImageObject", "url": "https://pawarta.github.io/pawarta.jpg"}}},
        breadcrumb_ld(crumbs),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in faq_items]},
    ]}

    idx = a.n - 1
    prev_a = cat.articles[idx - 1] if idx > 0 else None
    next_a = cat.articles[idx + 1] if idx + 1 < len(cat.articles) else None
    pager = '<div class="d-flex justify-content-between gap-3 my-4">'
    pager += (f'<a class="btn btn-outline-secondary btn-sm text-start" href="{prev_a.url}">&laquo; {esc(prev_a.title[:60])}</a>'
              if prev_a else "<span></span>")
    pager += (f'<a class="btn btn-outline-secondary btn-sm text-end" href="{next_a.url}">{esc(next_a.title[:60])} &raquo;</a>'
              if next_a else "<span></span>")
    pager += "</div>"

    page = head(f"{a.title} | {cat.label} - PAWARTA", a.desc, a.keywords, canonical, og_img, "article", jsonld)
    page += cookie_banner() + navbar(cats, cat.slug)
    page += f"""
<main id="artikels" class="container my-5 flex-grow-1">
  <div class="row g-4">
    <div class="col-lg-8" data-aos="fade-up">
      <article class="bg-white p-4 p-md-5 rounded-4 shadow-sm border article-content">
        {breadcrumb_html(crumbs)}
        <span class="badge bg-java-maroon text-java-gold mb-2">{esc(cat.label)} • {words:,} Kata Wawasan</span>
        <h1 class="display-6 fw-bold text-java-brown mb-3">{esc(a.title)}</h1>
        <div class="d-flex flex-wrap align-items-center gap-3 text-muted small pb-3 mb-3 border-bottom">
          <div><i class="fas fa-user-edit text-java-gold me-1"></i> <strong class="text-dark">{esc(a.author[0])}</strong> <span class="d-none d-md-inline">· {esc(a.author[1])}</span></div>
          <div><i class="far fa-calendar-alt text-java-gold me-1"></i> <time datetime="{a.date.isoformat()}">{fmt_date(a.date)}</time></div>
          <div><i class="far fa-clock text-java-gold me-1"></i> {max(a.read_min, words // 220)} menit maca</div>
          <div><i class="fas fa-eye text-java-gold me-1"></i> {a.views:,} kali diwaca</div>
        </div>
        <figure class="figure w-100 mb-3">
          <img src="{img_src(a.image, 1200)}" alt="{esc(a.img_alt)}" width="1200" height="675" fetchpriority="high" class="figure-img img-fluid rounded-4 w-100 object-fit-cover" style="aspect-ratio:16/9">
          <figcaption class="figure-caption">{esc(a.img_alt)}. Foto: Dokumentasi PAWARTA.</figcaption>
        </figure>
        {share_buttons(canonical, a.title)}
        <div class="toc-box mb-4">
          <button class="btn btn-sm btn-java-gold mb-2" type="button" data-bs-toggle="collapse" data-bs-target="#tocList" aria-expanded="true"><i class="fas fa-list-ol me-1"></i> Daftar Isi</button>
          <div class="collapse show" id="tocList"><ol class="toc small mb-0">{toc_html}</ol></div>
        </div>
        {body_html}
        <div class="mt-4 d-flex flex-wrap gap-1">
          <span class="small fw-bold me-1"><i class="fas fa-tag text-java-gold"></i> Label:</span>
          <a href="{cat.url}" class="badge rounded-pill label-pill text-decoration-none">{esc(cat.label)}</a>
          {"".join(f'<a href="{c.url}" class="badge rounded-pill label-pill text-decoration-none">{esc(c.label)}</a>' for c in related_cats[:3])}
        </div>
        {share_buttons(canonical, a.title)}
        <div class="author-box d-flex gap-3 align-items-center p-3 rounded-4 mb-3" id="author">
          <img src="https://pawarta.github.io/pawarta.jpg" alt="Penulis {esc(a.author[0])}" width="64" height="64" class="rounded-circle">
          <div><div class="fw-bold">{esc(a.author[0])}</div><div class="small text-muted">{esc(a.author[1])} di PAWARTA. Nulis babagan {esc(cat.label.lower())}, budaya, lan kabar aktual Nusantara.</div></div>
        </div>
        {pager}
      </article>
    </div>
    {sidebar(cat, cats, all_articles, a)}
  </div>
</main>
"""
    page += footer(cats)
    return page, words


def data_table(a, rng):
    rows = []
    for r in TABLE_ROWS:
        rows.append(f"<tr><th scope=\"row\">{r}</th><td>{rng.choice(TABLE_NOW)}</td><td>{rng.choice(TABLE_NEXT)}</td>"
                    f"<td>{rng.choice(TABLE_IMPACT)}</td></tr>")
    return f"""
<div class="table-responsive my-4">
  <table class="table table-bordered table-striped align-middle">
    <caption>Tabel ringkasan kondisi {esc(a.sub)} {YEAR} dan proyeksi {NEXT_YEAR} (olahan redaksi PAWARTA)</caption>
    <thead class="table-dark"><tr><th scope="col">Aspek</th><th scope="col">Kondisi {YEAR}</th><th scope="col">Proyeksi {NEXT_YEAR}</th><th scope="col">Dampak bagi Pembaca</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</div>"""


def read_also(title, arts):
    lis = "".join(f'<li><a href="{x.url}">{esc(x.title)}</a> <span class="text-muted small">({esc(x.cat.label)})</span></li>'
                  for x in arts)
    return f'<div class="read-also my-4"><div class="fw-bold mb-2 text-java-maroon"><i class="fas fa-book-open me-1"></i> {esc(title)}</div><ul class="mb-0">{lis}</ul></div>'


# --------------------------------------------------------------------------- category index
def render_category_index(cat, cats, all_articles):
    arts = cat.articles
    slides = [
        {"img": cat.image, "alt": f"Rubrik {cat.label} PAWARTA", "aksara": "ꦥꦮꦂꦠ",
         "title": f'Rubrik <span class="rainbow-text">{esc(cat.label)}</span>',
         "text": f"Warta pilihan {cat.label}: {', '.join(cat.subs[:3])}, lan liyane.", "href": "#warta-terkini", "cta": "Miwiti Warta"},
        {"img": arts[0].image, "alt": arts[0].img_alt, "aksara": "ꦮꦂꦠꦄꦚꦂ", "title": esc(arts[0].title),
         "text": "Warta paling anyar ing rubrik iki.", "href": arts[0].url, "cta": "Waca Selengkapnya"},
        {"img": "/img/bahasa-jawa.jpeg", "alt": "Kabudayan Jawi", "aksara": "ꦲꦏ꧀ꦱꦫꦗꦮ",
         "title": 'Sugeng Rawuh ing <span class="rainbow-text">PAWARTA</span>',
         "text": "Pusat warta digital modheren kanthi dhasar budaya lan kearifan lokal Jawi.", "href": "/index.html", "cta": "Kaca Utama"},
    ]
    crumbs = [("Kaca Utama", "/index.html"), (cat.label, None)]
    desc = (f"Rubrik {cat.label} PAWARTA: 30 artikel mendalam tentang {', '.join(cat.subs)}. "
            f"Warta terkini, populer, dan analisis berbalut budaya Jawa.")
    canonical = abs_url(cat.url)
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": f"Rubrik {cat.label} - PAWARTA", "url": canonical, "description": desc,
         "inLanguage": "id-ID"},
        breadcrumb_ld([("Kaca Utama", "/index.html"), (cat.label, cat.url)]),
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": abs_url(x.url), "name": x.title} for i, x in enumerate(arts)]},
    ]}
    ctx = cat.ctx
    intro = (f"<p>Sugeng rawuh ing rubrik <strong>{esc(cat.label)}</strong> PAWARTA. Rubrik ini menghadirkan liputan, "
             f"analisis, dan panduan seputar {esc(', '.join(cat.subs[:-1]))}, serta {esc(cat.subs[-1])}. Setiap artikel "
             f"disusun mendalam lengkap dengan data, tabel ringkasan, FAQ, dan referensi tepercaya.</p>"
             f"<p>Kami percaya warta yang baik berangkat dari nilai luhur: jujur, jernih, dan bermanfaat. Karena itu, setiap "
             f"pembahasan di rubrik {esc(cat.label)} juga menautkan isu terkini dengan kearifan budaya Jawa, mulai dari "
             f"<em>memayu hayuning bawana</em> hingga <em>eling lan waspada</em>. Isu yang kami pantau antara lain "
             f"{esc(ctx['challenges'][0])} serta peluang dari {esc(ctx['opps'][0])}.</p>")
    page = head(f"Rubrik {cat.label} - PAWARTA Portal Warta & Kabudayan Jawi", desc,
                f"pawarta, {cat.label.lower()}, berita {cat.label.lower()}, " + ", ".join(s.lower() for s in cat.subs),
                canonical, abs_url(cat.image), "website", jsonld)
    page += cookie_banner() + navbar(cats, cat.slug) + slider(slides)
    cards = "".join(article_card(x) for x in arts[1:])
    page += f"""
<main id="artikels" class="container my-5 flex-grow-1">
  <div class="row g-4">
    <div class="col-lg-8">
      <section class="bg-white p-4 p-md-5 rounded-4 shadow-sm border article-content mb-4" data-aos="fade-up">
        {breadcrumb_html(crumbs)}
        <h1 class="display-6 fw-bold text-java-brown">Rubrik {esc(cat.label)}: Warta, Analisis, lan Panduan {YEAR}</h1>
        {intro}
        <div class="d-flex flex-wrap gap-1">{"".join(f'<span class="badge rounded-pill label-pill">{esc(s)}</span>' for s in cat.subs)}</div>
        {share_buttons(canonical, f"Rubrik {cat.label} - PAWARTA")}
      </section>
      <h2 id="warta-terkini" class="h3 font-heading text-java-maroon mb-3"><i class="fas fa-newspaper me-2 text-java-gold"></i>Warta Terkini</h2>
      <div class="row g-4 mb-4">{article_card(arts[0], big=True)}</div>
      {ad_block()}
      <h2 class="h3 font-heading text-java-maroon mb-3"><i class="fas fa-layer-group me-2 text-java-gold"></i>Sedaya Artikel {esc(cat.label)}</h2>
      <div class="row g-4">{cards}</div>
      <div class="text-center my-4">
        <a href="/{cat.slug}/sitemap.html" class="btn btn-java-gold me-2"><i class="fas fa-sitemap me-1"></i> Sitemap Rubrik</a>
        <a href="/kategori.html" class="btn btn-outline-secondary">Sedaya Rubrik</a>
      </div>
    </div>
    {sidebar(cat, cats, all_articles)}
  </div>
</main>
"""
    page += footer(cats)
    return page


# --------------------------------------------------------------------------- sitemaps & global pages
def render_sitemaps(cat, cats, all_articles):
    urls = [cat.url] + [a.url for a in cat.articles] + [f"/{cat.slug}/sitemap.html"]
    lastmod = {cat.url: cat.articles[0].date}
    for a in cat.articles:
        lastmod[a.url] = a.date
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u in urls:
        d = lastmod.get(u, BASE_DATE)
        pr = "0.9" if u == cat.url else ("0.4" if u.endswith("sitemap.html") else "0.8")
        img = ""
        art = next((a for a in cat.articles if a.url == u), None)
        if art:
            img = f"<image:image><image:loc>{esc(abs_url(art.image))}</image:loc><image:title>{esc(art.img_alt)}</image:title></image:image>"
        xml.append(f"<url><loc>{esc(abs_url(u))}</loc><lastmod>{d.date().isoformat()}</lastmod>"
                   f"<changefreq>weekly</changefreq><priority>{pr}</priority>{img}</url>")
    xml.append("</urlset>")
    txt = "\n".join(abs_url(u) for u in urls) + "\n"

    crumbs = [("Kaca Utama", "/index.html"), (cat.label, cat.url), ("Sitemap", None)]
    rows = "".join(f'<li class="py-1"><a href="{a.url}">{esc(a.title)}</a> <span class="small text-muted">— {fmt_date(a.date)}</span></li>'
                   for a in cat.articles)
    page = head(f"Sitemap Rubrik {cat.label} - PAWARTA", f"Peta situs rubrik {cat.label} PAWARTA berisi 30 artikel.",
                f"sitemap {cat.label.lower()}, pawarta", abs_url(f"/{cat.slug}/sitemap.html"), abs_url(cat.image))
    page += cookie_banner() + navbar(cats, cat.slug)
    page += f"""
<main class="container my-5 flex-grow-1">
  <div class="row g-4">
    <div class="col-lg-8">
      <section class="bg-white p-4 p-md-5 rounded-4 shadow-sm border article-content">
        {breadcrumb_html(crumbs)}
        <h1 class="h2 fw-bold text-java-brown">Sitemap Rubrik {esc(cat.label)}</h1>
        <p>Daftar lengkap artikel rubrik <a href="{cat.url}">{esc(cat.label)}</a>. Format mesin: <a href="/{cat.slug}/sitemap.xml">sitemap.xml</a> · <a href="/{cat.slug}/sitemap.txt">sitemap.txt</a></p>
        <ol>{rows}</ol>
      </section>
    </div>
    {sidebar(cat, cats, all_articles)}
  </div>
</main>
"""
    page += footer(cats)
    return "\n".join(xml) + "\n", txt, page


def simple_page(cats, all_articles, title, desc, path, inner):
    page = head(f"{title} - PAWARTA", desc, "pawarta, " + title.lower(), abs_url(path), "https://pawarta.github.io/pawarta.jpg")
    page += cookie_banner() + navbar(cats)
    page += f"""
<main class="container my-5 flex-grow-1">
  <div class="row g-4">
    <div class="col-lg-8">
      <section class="bg-white p-4 p-md-5 rounded-4 shadow-sm border article-content">
        {breadcrumb_html([("Kaca Utama", "/index.html"), (title, None)])}
        {inner}
      </section>
    </div>
    {sidebar(cats[0], cats, all_articles)}
  </div>
</main>
"""
    return page + footer(cats)


def render_global(cats, all_articles, out):
    # kategori.html
    groups = {}
    for c in cats:
        groups.setdefault(c.ctx["label"], []).append(c)
    blocks = []
    for g, cs in groups.items():
        items = "".join(f"""<div class="col-sm-6 col-md-4"><a href="{c.url}" class="cat-tile d-block rounded-4 overflow-hidden text-decoration-none">
<img src="{img_src(c.image, 400)}" alt="Rubrik {esc(c.label)}" width="400" height="225" loading="lazy" class="w-100 object-fit-cover" style="aspect-ratio:16/9">
<div class="p-2"><div class="fw-bold text-java-brown">{esc(c.label)}</div><div class="small text-muted">{len(c.articles)} artikel · <a href="/{c.slug}/sitemap.html">sitemap</a></div></div></a></div>"""
                        for c in cs)
        blocks.append(f'<h2 class="h4 mt-4">{esc(g)}</h2><div class="row g-3">{items}</div>')
    write(out, "kategori.html", simple_page(
        cats, all_articles, "Sedaya Rubrik", f"Daftar {len(cats)} rubrik PAWARTA dengan {len(all_articles)} artikel.",
        "/kategori.html",
        f'<h1 class="h2 fw-bold text-java-brown">Sedaya Rubrik PAWARTA</h1><p>{len(cats)} rubrik, {len(all_articles):,} artikel mendalam.</p>' + "".join(blocks)))

    # arsip.html
    months = {}
    for a in sorted(all_articles, key=lambda x: x.date, reverse=True):
        months.setdefault(a.date.strftime("%Y-%m"), []).append(a)
    arch = []
    for k, arts in months.items():
        lis = "".join(f'<li><a href="{a.url}">{esc(a.title)}</a> <span class="small text-muted">— {esc(a.cat.label)}, {fmt_date(a.date)}</span></li>' for a in arts)
        arch.append(f'<h2 id="arsip-{k}" class="h4 mt-4">{BULAN[int(k[5:]) - 1]} {k[:4]} <span class="badge bg-secondary">{len(arts)}</span></h2>'
                    f'<details><summary class="small text-java-maroon">Tampilkan {len(arts)} artikel</summary><ul class="small">{lis}</ul></details>')
    write(out, "arsip.html", simple_page(cats, all_articles, "Arsip Warta", "Arsip seluruh artikel PAWARTA per bulan.",
                                         "/arsip.html", '<h1 class="h2 fw-bold text-java-brown">Arsip Warta</h1>' + "".join(arch)))

    # terima-kasih.html
    write(out, "terima-kasih.html", simple_page(
        cats, all_articles, "Matur Nuwun", "Pesan Anda telah kami terima.", "/terima-kasih.html",
        '<h1 class="h2 fw-bold text-java-brown">Matur Nuwun!</h1><p>Pesen panjenengan sampun katampi dening redaksi PAWARTA. '
        'Kami badhe mangsuli enggal.</p><a href="/index.html" class="btn btn-java-gold">Wangsul dhateng Kaca Utama</a>'))

    # search.json
    data = [{"t": a.title, "u": a.url, "c": a.cat.label} for a in all_articles]
    write(out, "search.json", json.dumps(data, ensure_ascii=False, separators=(",", ":")))

    # sitemap-index.xml
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
          f"<sitemap><loc>{abs_url('/sitemap.xml')}</loc></sitemap>",
          f"<sitemap><loc>{abs_url('/sitemap-pages.xml')}</loc></sitemap>"]
    sm += [f"<sitemap><loc>{abs_url(f'/{c.slug}/sitemap.xml')}</loc><lastmod>{c.articles[0].date.date().isoformat()}</lastmod></sitemap>" for c in cats]
    sm.append("</sitemapindex>")
    write(out, "sitemap-index.xml", "\n".join(sm) + "\n")
    pages = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    pages += [f"<url><loc>{abs_url(p)}</loc><changefreq>daily</changefreq></url>" for p in ("/kategori.html", "/arsip.html")]
    pages.append("</urlset>")
    write(out, "sitemap-pages.xml", "\n".join(pages) + "\n")

    # robots.txt: tambahake sitemap index
    robots_src = os.path.join(out, "robots.txt")
    robots = open(robots_src, encoding="utf-8").read() if os.path.exists(robots_src) else "User-agent: *\nAllow: /\n"
    robots = "\n".join(l for l in robots.splitlines() if not l.lower().startswith("sitemap:")).rstrip() + "\n\n"
    robots += f"Sitemap: {abs_url('/sitemap.xml')}\nSitemap: {abs_url('/sitemap-index.xml')}\n"
    write(out, "robots.txt", robots)

    write(out, "assets/blog.css", CSS)
    write(out, "assets/blog.js", JS)


def write(out, rel, content):
    path = os.path.join(out, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


CSS = """:root{--java-maroon:#581845;--java-gold:#D4AF37;--java-brown:#3E2723;--java-cream:#FDFBF7;--java-accent:#800020;--accent-gold:#D4AF37}
body{font-family:'Inter',sans-serif;background-color:var(--java-cream);color:#2c2c2c}
h1,h2,h3,h4,h5,h6,.font-heading{font-family:'Playfair Display',serif}
.navbar-brand img{width:45px;height:45px;border-radius:50%;border:2px solid var(--accent-gold);object-fit:cover}
.navbar-brand{font-weight:700;letter-spacing:1px;color:var(--java-gold)!important}
@keyframes rainbowGlow{0%{color:#ff0000}14%{color:#ff7f00}28%{color:#ffff00}42%{color:#00ff00}57%{color:#00bfff}71%{color:#9b59ff}85%{color:#ff00d4}100%{color:#ff0000}}
@keyframes rainbowBg{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.rainbow-text{animation:rainbowGlow 6s infinite linear;font-weight:bold}
.rainbow-badge{background:linear-gradient(270deg,#ff416c,#ff4b2b,#f12711,#f5af19,#00b09b,#96c93d);background-size:400% 400%;animation:rainbowBg 10s ease infinite;color:#fff}
.carousel-item{height:480px;background-size:cover;background-position:center;position:relative}
@media(max-width:768px){.carousel-item{height:400px}.carousel-caption .display-5{font-size:1.6rem}}
.carousel-overlay{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.55)}
.carousel-caption{bottom:18%}
.honocoroko-title{font-size:2.2rem;letter-spacing:2px;color:var(--accent-gold);text-shadow:2px 2px 4px rgba(0,0,0,.8)}
.bg-java-maroon{background-color:var(--java-maroon)!important}.bg-java-brown{background-color:var(--java-brown)!important}
.text-java-gold{color:var(--java-gold)!important}.text-java-maroon{color:var(--java-maroon)!important}.text-java-brown{color:var(--java-brown)!important}
.btn-java-gold{background-color:var(--java-gold);color:var(--java-brown);font-weight:600;border:none}
.btn-java-gold:hover{background-color:#c19b2e;color:#fff}
.nav-link{color:rgba(255,255,255,.85)!important;font-weight:500}
.nav-link:hover,.nav-link.active{color:var(--java-gold)!important}
.dropdown-menu{background-color:var(--java-maroon);border:1px solid var(--java-gold)}
.dropdown-item{color:#fff}.dropdown-item:hover,.dropdown-item.active{background-color:var(--java-brown);color:var(--java-gold)}
.mega-menu{width:min(960px,96vw);left:50%!important;transform:translateX(-50%);max-height:75vh;overflow:auto}
.mega-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:2px}
.mega-grid .dropdown-item{font-size:.85rem;border-radius:6px;padding:.3rem .6rem}
@media(max-width:991px){.mega-menu{transform:none;left:0!important;width:100%}}
.article-content p{line-height:1.85;font-size:1.06rem;margin-bottom:1.3rem}
.article-content h2{border-left:5px solid var(--java-gold);padding-left:15px;margin-top:2.5rem;margin-bottom:1rem;color:var(--java-maroon);scroll-margin-top:90px}
.article-content h3{margin-top:1.8rem;color:var(--java-brown);font-size:1.35rem;scroll-margin-top:90px}
.article-content a{color:var(--java-accent)}
.sidebar-widget{background:#fff;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,.05);padding:20px;margin-bottom:25px;border-top:4px solid var(--java-gold)}
.cookie-banner{position:fixed;bottom:0;left:0;right:0;background:var(--java-brown);color:#fff;z-index:9999;padding:15px 20px;box-shadow:0 -4px 20px rgba(0,0,0,.2)}
.toc-box{background:#fffaf0;border:1px dashed var(--java-gold);border-radius:12px;padding:1rem 1.25rem}
.toc a{color:var(--java-brown);text-decoration:none}.toc a:hover{color:var(--java-accent);text-decoration:underline}
.toc ol{margin-top:.2rem}
.read-also{background:#f8f3ea;border-left:4px solid var(--java-maroon);border-radius:8px;padding:1rem 1.25rem}
.read-also a{font-weight:600}
.share-btn{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;color:#fff!important;border:none;text-decoration:none;transition:transform .15s}
.share-btn:hover{transform:translateY(-2px)}
.label-pill{background:#f3e7c7;color:var(--java-brown)!important;font-weight:500}
.label-pill:hover{background:var(--java-gold)}
.author-box{background:#f8f3ea}
.news-card img{transition:transform .3s}.news-card:hover img{transform:scale(1.04)}
.cat-tile{background:#fff;box-shadow:0 4px 15px rgba(0,0,0,.06);transition:transform .2s}.cat-tile:hover{transform:translateY(-3px)}
.search-results{max-height:55vh;overflow:auto}
.search-results .list-group-item{background:transparent;color:#fff;border-color:rgba(212,175,55,.3)}
.search-results .list-group-item:hover{background:var(--java-brown);color:var(--java-gold)}
footer a:hover{color:var(--java-gold)!important}
.ad-slot{min-height:90px}
.tips-list li{margin-bottom:.5rem;line-height:1.7}
"""

JS = """AOS.init({duration:800,once:true});
function acceptCookies(){document.getElementById('cookieBanner').style.display='none';localStorage.setItem('pawarta_cookie','accepted');}
function rejectCookies(){document.getElementById('cookieBanner').style.display='none';localStorage.setItem('pawarta_cookie','rejected');}
if(localStorage.getItem('pawarta_cookie')){var cb=document.getElementById('cookieBanner');if(cb)cb.style.display='none';}
function showMsg(t){document.getElementById('modalMsgContent').innerText=t;new bootstrap.Modal(document.getElementById('msgModal')).show();}
function subscribeNewsletter(){showMsg('Matur nuwun sampun langganan warta PAWARTA!');}
function copyLink(btn){navigator.clipboard.writeText(btn.dataset.url).then(function(){showMsg('Tautan sampun kasalin.');});}
document.querySelectorAll('form.pawarta-contact').forEach(function(f){
  var h=f.querySelector('input[name=halaman]');if(h)h.value=location.pathname;
  f.addEventListener('submit',function(e){
    e.preventDefault();
    fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f)).toString()})
      .then(function(r){if(!r.ok)throw new Error(r.status);showMsg('Pesen lan saran panjenengan sampun kasil kasimpen. Matur nuwun!');f.reset();})
      .catch(function(){showMsg('Nyuwun pangapunten, pesen durung kakirim. Mangga dicoba malih.');});
  });
});
(function(){
  var idx=null,inp=document.getElementById('searchInput'),res=document.getElementById('searchResults');
  if(!inp)return;
  document.getElementById('searchModal').addEventListener('shown.bs.modal',function(){inp.focus();
    if(!idx)fetch('/search.json').then(function(r){return r.json();}).then(function(d){idx=d;run();});});
  function run(){
    var q=inp.value.trim().toLowerCase();res.innerHTML='';if(!idx||q.length<2)return;
    var words=q.split(/\\s+/),out=[];
    for(var i=0;i<idx.length&&out.length<15;i++){var s=(idx[i].t+' '+idx[i].c).toLowerCase();
      if(words.every(function(w){return s.indexOf(w)>-1;}))out.push(idx[i]);}
    if(!out.length){res.innerHTML='<div class="small text-white-50">Mboten wonten asil.</div>';return;}
    out.forEach(function(o){var a=document.createElement('a');a.className='list-group-item list-group-item-action';a.href=o.u;
      a.innerHTML='<div class="fw-semibold"></div><div class="small text-warning"></div>';
      a.children[0].textContent=o.t;a.children[1].textContent=o.c;res.appendChild(a);});
  }
  inp.addEventListener('input',run);
})();
"""

STATIC_EXCLUDE = {".git", ".netlify", "dist", "node_modules", "__pycache__", ".github", "netlify.toml",
                  "AGENTS.md", ".gitignore", ".netlify-cache"}


def copy_static(out):
    out_abs = os.path.abspath(out)
    for name in os.listdir(ROOT):
        if name in STATIC_EXCLUDE or name.endswith(".py"):
            continue
        src = os.path.join(ROOT, name)
        if os.path.abspath(src) == out_abs:
            continue
        dst = os.path.join(out, name)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)


def main():
    global SITE_URL, USE_CDN
    ap = argparse.ArgumentParser(description="Generator blog PAWARTA")
    ap.add_argument("--out", default=ROOT, help="direktori output (default: root repo)")
    ap.add_argument("--copy-static", action="store_true", help="salin file statis repo menyang output")
    ap.add_argument("--site-url", default=None)
    ap.add_argument("--cdn", action="store_true", help="gunakake Netlify Image CDN kanggo gambar")
    args = ap.parse_args()

    SITE_URL = (args.site_url or os.environ.get("SITE_URL") or os.environ.get("URL") or "https://pawarta.github.io").rstrip("/")
    USE_CDN = args.cdn or os.environ.get("NETLIFY") == "true"
    out = args.out
    os.makedirs(out, exist_ok=True)
    if args.copy_static:
        copy_static(out)

    cats = build_model()
    all_articles = [a for c in cats for a in c.articles]
    min_w, total = 10 ** 9, 0
    for c in cats:
        write(out, f"{c.slug}/index.html", render_category_index(c, cats, all_articles))
        for a in c.articles:
            page, words = render_article(a, cats, all_articles)
            min_w = min(min_w, words)
            total += 1
            write(out, f"{c.slug}/artikel{a.n}.html", page)
        xml, txt, html_page = render_sitemaps(c, cats, all_articles)
        write(out, f"{c.slug}/sitemap.xml", xml)
        write(out, f"{c.slug}/sitemap.txt", txt)
        write(out, f"{c.slug}/sitemap.html", html_page)
    render_global(cats, all_articles, out)
    print(f"PAWARTA: {len(cats)} rubrik, {total} artikel (minimal {min_w} tembung/artikel) -> {out} [{SITE_URL}]")


if __name__ == "__main__":
    main()
