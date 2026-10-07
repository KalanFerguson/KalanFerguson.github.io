"""Stamp the shared head, header and footer onto every page.

Run from the repository root:  python _tools/chrome.py
Each page keeps its own content. The script only rewrites the regions between
<!-- chrome:head -->, <!-- chrome:header --> and <!-- chrome:footer --> markers, and
converts a page that has no markers yet. Folders starting with "_" are not published by
GitHub Pages, so this file never goes live.
"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://kalanferguson.com/"
EMAIL = "kalanferguson005@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/kalan-ferguson-288858326/"
# GoatCounter site code (the "xxx" in xxx.goatcounter.com). Empty means no analytics script is added.
# Cookie-free, so no consent banner. It skips file:// and localhost, so local previews are never counted.
GOATCOUNTER = "kalanferguson"

PAGES = {
    "index.html": dict(title="Kalan Ferguson, mechanical engineer", og="home", type="website", css=["home.css"], nav=None,
        desc="Kalan Ferguson, mechanical engineering student at QUT. Case studies in the thermal limits of AI hardware, structural fatigue and small-aircraft design."),
    "writing.html": dict(title="Writing / Kalan Ferguson", og="writing", type="website", css=["article-style.css"], nav="writing",
        desc="Essays on defence systems and energy infrastructure, written from an engineer's view of the physics underneath them."),
    "ghostbat.html": dict(title="MQ-28A Ghost Bat / Kalan Ferguson", og="ghostbat", type="article", css=["article-style.css"], nav="writing",
        desc="Why the MQ-28A Ghost Bat's modular nose matters: SWaP constraints, sovereign manufacturing and crewed-uncrewed teaming."),
    "resume.html": dict(title="Resume / Kalan Ferguson", og="resume", type="website", css=["resume.css"], nav="resume",
        desc="Resume of Kalan Ferguson, Mechanical Engineering (Honours) with an aerospace minor at QUT."),
    "_article-template.html": dict(title="ARTICLE TITLE / Kalan Ferguson", og="writing", type="article", css=["article-style.css"], nav="writing",
        desc="ONE-SENTENCE SUMMARY OF THE PIECE."),
    "projects/egh404-liquid-cooling.html": dict(title="Where single-phase cooling runs out / Kalan Ferguson", og="egh404", type="article", css=["project-style.css", "egh404.css"], nav="work",
        desc="Research proposal: a boundary-consistent comparison of single- and two-phase direct-to-chip liquid cooling for AI accelerator racks above 200 kW."),
    "projects/weld-fatigue.html": dict(title="Weld Fatigue Design Audit / Kalan Ferguson", og="weld-fatigue", type="article", css=["project-style.css"], nav="work",
        desc="Fatigue design audit of a trailer hanger weld: five load cases, Modified Goodman, an ANSYS mesh convergence study and a reconciliation of hand and FEA results."),
    "projects/uav-aerostructures.html": dict(title="Twin-Boom Autonomous UAV / Kalan Ferguson", og="uav-aerostructures", type="article", css=["project-style.css"], nav="work",
        desc="Aerostructural sizing of a hand-launched twin-boom UAV: a 650 mm wing derived from hand-launch speed, span and weight constraints."),
    "projects/planetary-gearbox.html": dict(title="Planetary Gearbox / Kalan Ferguson", og="planetary-gearbox", type="article", css=["project-style.css"], nav="work",
        desc="Design, analysis and test to failure of a 64:1 three-stage planetary gearbox delivering 20 Nm."),
    "projects/walking-robot.html": dict(title="Walking Robot / Kalan Ferguson", og="walking-robot", type="article", css=["project-style.css"], nav="work",
        desc="Coupled four-bar crank-rocker linkages with a 180-degree phase offset. The robot walked 2 m in 18 s."),
    "projects/diesel-engine.html": dict(title="Diesel Engine Analysis / Kalan Ferguson", og="diesel-engine", type="article", css=["project-style.css"], nav="work",
        desc="Thermodynamic analysis of a Perkins 404D-22 diesel engine across six operating points: performance, energy balance and PV cycle."),
    "projects/aerofoil-flow.html": dict(title="E387 Aerofoil Flow Control / Kalan Ferguson", og="aerofoil-flow", type="article", css=["project-style.css"], nav="work",
        desc="Low-Reynolds-number flow control for the Eppler 387 aerofoil: a shape factor framework with passive and active control."),
    "projects/f35b-swivel.html": dict(title="F-35B Swivel Duct / Kalan Ferguson", og="f35b-swivel", type="article", css=["project-style.css"], nav="work",
        desc="Independent parametric SolidWorks rebuild of the F-35B three-bearing swivel duct and its rotational synchronisation."),
}

def analytics():
    if not GOATCOUNTER:
        return ""
    return f'\n<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'

def head(path, cfg):
    pre = "../" * path.count("/")
    url = SITE + ("" if path == "index.html" else path)
    e = lambda s: html.escape(s, quote=True)
    css = "\n".join(f'<link rel="stylesheet" href="{c}">' for c in cfg["css"])
    return f"""<!-- chrome:head -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(cfg['title'])}</title>
<meta name="description" content="{e(cfg['desc'])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{cfg['type']}">
<meta property="og:site_name" content="Kalan Ferguson">
<meta property="og:title" content="{e(cfg['title'].split(' / ')[0])}">
<meta property="og:description" content="{e(cfg['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}img/og/{cfg['og']}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="{pre}img/favicon-32.png">
<link rel="apple-touch-icon" href="{pre}img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gelasio:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<link rel="stylesheet" href="{pre}site.css">
{css}
<script>document.documentElement.classList.add('js')</script>
<script src="{pre}site.js" defer></script>{analytics()}
<!-- /chrome:head -->"""

def header(path, cfg):
    pre = "../" * path.count("/")
    cur = cfg["nav"]
    def item(key, href, label):
        aria = ' aria-current="page"' if key == cur and key in ("writing", "resume") else ""
        return f'<li><a href="{href}"{aria}>{label}</a></li>'
    return f"""<!-- chrome:header -->
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{pre}index.html"><img src="{pre}img/kf-logo-96.png" alt="" width="28" height="28">Kalan Ferguson</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav id="site-nav" aria-label="Main">
      <ul class="nav-list">
        {item('work', pre + 'index.html#work', 'Work')}
        {item('writing', pre + 'writing.html', 'Writing')}
        {item('about', pre + 'index.html#about', 'About')}
        {item('resume', pre + 'resume.html', 'Resume')}
        {item('contact', '#contact', 'Contact')}
      </ul>
    </nav>
  </div>
</header>
<!-- /chrome:header -->"""

def footer(path, cfg):
    pre = "../" * path.count("/")
    return f"""<!-- chrome:footer -->
<footer class="site-foot" id="contact">
  <div class="wrap">
    <div class="cols">
      <div>
        <p style="margin:0 0 .4rem;font-size:1.15rem;color:var(--ink)">Kalan Ferguson</p>
        <p class="muted" style="margin:0;max-width:34ch">Mechanical Engineering (Honours), aerospace minor, QUT. Seeking 2026/27 summer internships in aerospace, defence, energy and advanced manufacturing.</p>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a class="addr" href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{LINKEDIN}" rel="noopener">LinkedIn</a></li>
          <li><a href="{pre}resume.html">Resume</a></li>
        </ul>
      </div>
      <div>
        <h2>Selected work</h2>
        <ul>
          <li><a href="{pre}projects/egh404-liquid-cooling.html">Liquid cooling for AI racks</a></li>
          <li><a href="{pre}projects/weld-fatigue.html">Weld fatigue audit</a></li>
          <li><a href="{pre}projects/uav-aerostructures.html">Twin-boom UAV</a></li>
          <li><a href="{pre}index.html#more">All projects</a></li>
        </ul>
      </div>
      <div>
        <h2>Writing</h2>
        <ul>
          <li><a href="{pre}ghostbat.html">MQ-28A Ghost Bat</a></li>
          <li><a href="{pre}writing.html">All writing</a></li>
        </ul>
      </div>
    </div>
    <div class="fine">
      <span>Academic figures reflect QUT records as of Semester 1, 2026. Writing is personal and does not represent QUT, the QUT Aerospace Society or any company.</span>
      <span>&copy; 2026 Kalan Ferguson</span>
    </div>
  </div>
</footer>
<!-- /chrome:footer -->"""

def replace_region(text, name, block):
    pat = re.compile(rf"<!-- chrome:{name} -->.*?<!-- /chrome:{name} -->", re.S)
    if pat.search(text):
        return pat.sub(lambda m: block, text, count=1), True
    return text, False

def convert(text, path, cfg):
    # head: keep the page's own inline <style> blocks, rebuild everything else
    m = re.search(r"<head>(.*?)</head>", text, re.S)
    styles = "\n".join(re.findall(r"<style>.*?</style>", m.group(1), re.S)) if m else ""
    text = text[:m.start(1)] + "\n" + head(path, cfg) + ("\n" + styles if styles else "") + "\n" + text[m.end(1):]
    # header
    old = re.search(r'<header class="site-header">.*?</header>', text, re.S)
    hdr = header(path, cfg) + "\n<main id=\"main\">"
    text = text[:old.start()] + hdr + text[old.end():] if old else text.replace("<body>", "<body>\n" + hdr, 1)
    # footer
    text = text.replace("</body>", "</main>\n" + footer(path, cfg) + "\n</body>", 1)
    return text

def main():
    for path, cfg in PAGES.items():
        p = os.path.join(ROOT, path)
        if not os.path.exists(p):
            print("missing", path); continue
        text = open(p, encoding="utf-8").read()
        new, a = replace_region(text, "head", head(path, cfg))
        new, b = replace_region(new, "header", header(path, cfg))
        new, c = replace_region(new, "footer", footer(path, cfg))
        if not (a and b and c):
            new = convert(text, path, cfg)
        if new != text:
            open(p, "w", encoding="utf-8").write(new)
            print("updated", path)
        else:
            print("unchanged", path)

if __name__ == "__main__":
    main()
