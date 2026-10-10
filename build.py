#!/usr/bin/env python3
"""ErsenBox Apps: apps.json'dan ana sayfa ve her uygulama için landing page üretir.

Kullanım (proje kökünde):   python3 build.py
Girdi:   apps.json, assets/<slug>/ (görseller, isteğe bağlı)
Çıktı:   index.html, apps/<slug>/index.html
Sadece Python standart kütüphanesi kullanır.
"""
import html
import json
import os
import re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")

CSS = """
:root{--brand:#014720;--brand-dk:#012b14;--accent:#d9b662;--accent-2:#f0d491;--bg:#f7f5ee;--surface:#fff;--text:#0b1a10;--muted:#4a5b50;--line:#e6e2d4;--radius:16px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#07130c;--surface:#0e2117;--text:#e9f3ec;--muted:#a3bcab;--line:#1e3a29}}
:root[data-theme="dark"]{--bg:#07130c;--surface:#0e2117;--text:#e9f3ec;--muted:#a3bcab;--line:#1e3a29}
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
a{color:inherit}
img{display:block;max-width:100%;height:auto}
.wrap{width:min(1100px,calc(100% - 32px));margin:0 auto}
header{background:linear-gradient(180deg,var(--brand-dk),var(--brand));color:#fff;border-bottom:1px solid rgba(217,182,98,.35)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 0;flex-wrap:wrap}
.brand{color:var(--accent-2);font-weight:800;text-decoration:none;letter-spacing:.3px}
.back{color:#eaf6ee;text-decoration:none;font-size:.9rem}
.hero{color:#fff;padding:48px 0 40px;background:linear-gradient(160deg,var(--brand) 0%,var(--brand-dk) 100%)}
.hero-grid{display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:center}
h1{font-size:clamp(1.8rem,4.5vw,2.8rem);line-height:1.1;margin:0 0 10px;color:var(--accent-2)}
.lead{color:#e3f2e8;margin:0 0 22px;font-size:1.05rem}
.btns{display:flex;gap:10px;flex-wrap:wrap}
.btn{display:inline-block;background:linear-gradient(180deg,var(--accent-2),var(--accent));color:#241a04;font-weight:800;text-decoration:none;padding:12px 22px;border-radius:12px;box-shadow:0 10px 24px rgba(0,0,0,.25)}
.btn.ghost{background:rgba(255,255,255,.1);color:#fff;border:1px solid rgba(255,255,255,.6);box-shadow:none}
.btn.disabled{opacity:.5;pointer-events:none}
.cover{border-radius:14px;border:1px solid rgba(217,182,98,.5);box-shadow:0 16px 36px rgba(0,0,0,.4);width:100%;aspect-ratio:16/9;object-fit:cover}
.cover-ph{border-radius:14px;width:100%;aspect-ratio:16/9;display:grid;place-items:center;background:radial-gradient(circle at 30% 30%,rgba(240,212,145,.25),transparent 60%),rgba(255,255,255,.06);border:1px dashed rgba(217,182,98,.6);color:var(--accent-2);font-size:3rem}
section{padding:44px 0}
h2{font-size:1.5rem;color:var(--brand);margin:0 0 18px}
:root[data-theme="dark"] h2{color:#8fe0b0}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) h2{color:#8fe0b0}}
.feat{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;padding:0;margin:0;list-style:none}
.feat li{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px;border-left:3px solid var(--accent)}
.gal{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.gal img{border-radius:12px;border:1px solid var(--line);background:var(--surface)}
.steps{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;counter-reset:s;padding:0;margin:0;list-style:none}
.steps li{counter-increment:s;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px 14px 56px;position:relative}
.steps li::before{content:counter(s);position:absolute;left:14px;top:14px;width:30px;height:30px;border-radius:50%;background:var(--accent);color:#241a04;font-weight:900;display:grid;place-items:center}
.note{color:var(--muted);font-size:.9rem;margin-top:12px}
.search{width:100%;max-width:420px;padding:12px 14px;border-radius:12px;border:1px solid var(--line);background:var(--surface);color:var(--text);font-size:1rem;margin:0 0 22px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.card{background:var(--surface);border:1px solid var(--line);border-top:3px solid var(--accent);border-radius:var(--radius);padding:18px;display:flex;flex-direction:column;gap:10px}
.card img,.card .thumb{border-radius:10px;width:100%;aspect-ratio:16/9;object-fit:cover;background:var(--bg)}
.card .thumb{display:grid;place-items:center;color:var(--accent);font-size:2rem;border:1px dashed var(--line)}
.card h3{margin:0;font-size:1.05rem;color:var(--brand)}
:root[data-theme="dark"] .card h3{color:#8fe0b0}
.card p{margin:0;color:var(--muted);font-size:.93rem;flex:1}
.card .btns .btn{padding:9px 14px;font-size:.88rem;border-radius:10px}
.card .btn{background:var(--brand);color:#fff}
.card .btn.ghost{background:transparent;color:var(--brand);border:1px solid var(--brand);box-shadow:none}
:root[data-theme="dark"] .card .btn{background:var(--accent);color:#241a04}
footer{background:var(--brand-dk);color:#c9ddce;text-align:center;padding:28px 0;font-size:.9rem;margin-top:40px}
footer a{color:#7fe6d3}
.hidden{display:none!important}
.logo-sm{width:64px;height:64px;object-fit:contain;border-radius:14px;background:#fff;padding:6px;margin-bottom:12px;border:1px solid rgba(217,182,98,.5)}
.logo-big{width:62%;max-width:300px;aspect-ratio:1/1;object-fit:contain;margin:0 auto;display:block;filter:drop-shadow(0 12px 24px rgba(0,0,0,.35))}
.about p{color:var(--text);font-size:1rem;max-width:80ch;margin:0}
.card img.logo-card{aspect-ratio:1/1;object-fit:contain;padding:14px;background:#fff}
@media (max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}.hero-grid{grid-template-columns:1fr}}
@media (max-width:600px){.grid,.feat,.steps,.gal{grid-template-columns:1fr}.wrap{width:calc(100% - 32px)}.btn{width:100%;text-align:center}.btns{flex-direction:column}}
"""


def e(s):
    return html.escape(s or "", quote=True)


def images_for(slug):
    d = os.path.join(ROOT, "assets", slug)
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if f.lower().endswith(IMG_EXT) and not f.lower().startswith("logo"))


def logo_for(slug):
    p = os.path.join(ROOT, "assets", slug, "logo.png")
    return "logo.png" if os.path.isfile(p) else None


def footer(site):
    parts = ["© 2026 ErsenBox"]
    if site.get("contact_email"):
        parts.append(f'<a href="mailto:{e(site["contact_email"])}">{e(site["contact_email"])}</a>')
    if site.get("impressum_url"):
        parts.append(f'<a href="{e(site["impressum_url"])}">Impressum</a>')
    if site.get("privacy_url"):
        parts.append(f'<a href="{e(site["privacy_url"])}">Gizlilik Politikası</a>')
    return "<footer><div class='wrap'>" + " · ".join(parts) + "</div></footer>"


def page(title, desc, body, depth):
    rel = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="icon" href="data:,">
<style>{CSS}</style>
</head>
<body>
<header><div class="wrap bar"><a class="brand" href="{rel}index.html">ErsenBox Apps</a><a class="back" href="{rel}index.html">← Tüm uygulamalar</a></div></header>
{body}
</body>
</html>
"""


def app_page(app, site):
    slug = app["slug"]
    imgs = images_for(slug)
    cover = app.get("cover") or (imgs[0] if imgs else None)
    gallery = [f for f in imgs if f != cover]
    img_base = f"../../assets/{slug}/"

    logo = logo_for(slug)
    logo_html = f'<img class="logo-sm" src="{img_base}logo.png" alt="">' if logo else ""
    if cover:
        cover_html = f'<img class="cover" src="{img_base}{quote(cover)}" alt="{e(app["name"])}">'
    elif logo:
        cover_html = f'<img class="logo-big" src="{img_base}logo.png" alt="{e(app["name"])} logosu">'
    else:
        cover_html = '<div class="cover-ph" aria-hidden="true">☪</div>'

    apk = app.get("apk")
    web = app.get("web")
    btns = []
    if apk:
        btns.append(f'<a class="btn" href="{e(apk["url"])}" download>APK İndir</a>')
    if web:
        btns.append(f'<a class="btn {"ghost" if apk else ""}" href="{e(web)}" target="_blank" rel="noopener">Web\'de Aç</a>')
    if app.get("play"):
        btns.append(f'<a class="btn ghost" href="{e(app["play"])}" target="_blank" rel="noopener">Google Play</a>')

    feats = ""
    if app.get("features"):
        items = "".join(f"<li>{e(x)}</li>" for x in app["features"])
        feats = f'<section><div class="wrap"><h2>Özellikler</h2><ul class="feat">{items}</ul></div></section>'

    gal = ""
    if gallery:
        figs = "".join(f'<img loading="lazy" src="{img_base}{quote(g)}" alt="{e(app["name"])} ekran görüntüsü">' for g in gallery)
        gal = f'<section><div class="wrap"><h2>Ekran Görüntüleri</h2><div class="gal">{figs}</div></div></section>'

    install = ""
    if apk:
        install = """<section><div class="wrap"><h2>APK Kurulumu</h2><ol class="steps">
<li>“APK İndir” düğmesine dokunun ve dosyanın inmesini bekleyin.</li>
<li>İndirilen APK dosyasını açın.</li>
<li>Cihaz sorarsa tarayıcıya “bilinmeyen kaynaklardan uygulama yükleme” izni verin.</li>
<li>“Yükle” düğmesine dokunun.</li>
</ol></div></section>"""

    about = ""
    if app.get("description"):
        about = f'<section class="about"><div class="wrap"><h2>Hakkında</h2><p>{e(app["description"])}</p></div></section>'

    body = f"""<section class="hero"><div class="wrap hero-grid">
<div>{logo_html}<h1>{e(app["name"])}</h1><p class="lead">{e(app["tagline"])}</p>
<div class="btns">{''.join(btns)}</div></div>
<div>{cover_html}</div>
</div></section>
{about}{feats}{gal}{install}
{footer(site)}"""
    return page(f'{app["name"]} · ErsenBox', app["tagline"], body, 2), body


def index_page(apps, site):
    cards = []
    for a in apps:
        slug = a["slug"]
        imgs = images_for(slug)
        cover = a.get("cover") or (imgs[0] if imgs else None)
        if cover:
            thumb = f'<img loading="lazy" src="assets/{slug}/{quote(cover)}" alt="{e(a["name"])}">'
        elif logo_for(slug):
            thumb = f'<img class="logo-card" loading="lazy" src="assets/{slug}/logo.png" alt="{e(a["name"])} logosu">'
        else:
            thumb = '<div class="thumb" aria-hidden="true">☪</div>'
        btns = []
        if a.get("apk"):
            btns.append(f'<a class="btn" href="{e(a["apk"]["url"])}" download>APK</a>')
        if a.get("web"):
            btns.append(f'<a class="btn ghost" href="{e(a["web"])}" target="_blank" rel="noopener">Web</a>')
        cards.append(
            f'<article class="card" data-name="{e(a["name"].lower())}">{thumb}'
            f'<h3>{e(a["name"])}</h3><p>{e(a["tagline"])}</p>'
            f'<div class="btns">{"".join(btns)}</div>'
            f'<a class="note" href="apps/{slug}/">Detaylar →</a></article>'
        )
    body = f"""<section class="hero"><div class="wrap">
<h1>{e(site["name"])}</h1><p class="lead">{e(site["description"])}</p></div></section>
<section><div class="wrap">
<input class="search" id="q" type="search" placeholder="Uygulama ara…" aria-label="Uygulama ara">
<div class="grid" id="grid">{''.join(cards)}</div>
</div></section>
{footer(site)}
<script>
document.getElementById('q').addEventListener('input',function(){{
  var v=this.value.trim().toLowerCase();
  document.querySelectorAll('#grid .card').forEach(function(c){{
    c.classList.toggle('hidden', v!=='' && c.getAttribute('data-name').indexOf(v)===-1);
  }});
}});
</script>"""
    return page(site["title"], site["description"], body, 0)


def main():
    with open(os.path.join(ROOT, "apps.json"), encoding="utf-8") as f:
        data = json.load(f)
    site, apps = data["site"], data["apps"]

    slugs = [a["slug"] for a in apps]
    dup = {s for s in slugs if slugs.count(s) > 1}
    if dup:
        raise SystemExit(f"Aynı slug birden fazla: {dup}")

    warnings = []
    for a in apps:
        if not re.fullmatch(r"[a-z0-9-]+", a["slug"]):
            raise SystemExit(f"Geçersiz slug: {a['slug']}")
        if not (a.get("apk") or a.get("web")):
            warnings.append(f"{a['slug']}: APK ve web linki yok")
        if a.get("draft"):
            warnings.append(f"{a['slug']}: açıklama taslak (apps.json'da draft=true)")
        if not images_for(a["slug"]):
            warnings.append(f"{a['slug']}: görsel yok (assets/{a['slug']}/)")

    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_page(apps, site))
    for a in apps:
        out_dir = os.path.join(ROOT, "apps", a["slug"])
        os.makedirs(out_dir, exist_ok=True)
        full, _ = app_page(a, site)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(full)

    print(f"Üretildi: index.html + {len(apps)} uygulama sayfası")
    for w in warnings:
        print("UYARI:", w)


if __name__ == "__main__":
    main()
