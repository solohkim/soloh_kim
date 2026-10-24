import os, json, datetime, shutil, re

folder = "writeups"
LABS_DIR = "labs"
if not os.path.exists(folder):
    os.makedirs(folder)

files = [f for f in os.listdir(folder) if f.endswith(".md")]

# Load old data to preserve EVERYTHING (premium, active, etc)
old_data = {}
if os.path.exists("writeups.json"):
    try:
        with open("writeups.json", "r", encoding="utf-8") as jf:
            for item in json.load(jf):
                # lookup by both full path and filename
                old_data[item["file"]] = item
                old_data[item["file"].split("/")[-1]] = item
                old_data[f"writeups/{item['file'].split('/')[-1]}"] = item
                if item.get("slug"):
                    old_data[item["slug"]] = item
    except Exception as e:
        print(f"Warning: could not load old writeups.json: {e}")

def get_slug(filename):
    return os.path.splitext(filename)[0].lower().replace(' ','-').replace('_','-')

def make_lab_page(p):
    slug = p.get('slug')
    title = p.get('title', slug)
    # Use desc for og:description
    raw_desc = p.get('desc','') or ''
    desc = raw_desc[:160].replace('"','').replace('\n',' ') or f"{title} - 0xSoloh writeup"
    image = p.get('image','')
    if image and not image.startswith('http'):
        image_url = f"https://kimsec.netlify.app/{image.lstrip('/')}"
    else:
        image_url = image or "https://kimsec.netlify.app/writeups/images/logo.png"
    url = f"https://kimsec.netlify.app/labs/{slug}/"
    html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title} | 0xSoloh">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} | 0xSoloh">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{image_url}">
<title>{title} | 0xSoloh</title>
<meta http-equiv="refresh" content="4; url=https://kimsec.netlify.app/?lab={slug}">
<style>
body{{margin:0;background:#000;color:#00FF41;font-family:'JetBrains Mono',monospace;overflow:hidden}}
#matrix{{position:fixed;inset:0;opacity:.12}}
.terminal{{position:relative;z-index:2;max-width:620px;margin:12vh auto;padding:22px;background:rgba(10,10,10,.92);border:1px solid #00FF41;border-radius:14px;box-shadow:0 0 50px rgba(0,255,65,.25);transition:transform .1s}}
.bar{{height:9px;background:#111;border:1px solid #222;border-radius:20px;overflow:hidden;margin:16px 0}}
.fill{{height:100%;width:0%;background:linear-gradient(90deg,#00FF41,#FFD54F);animation:load 2.4s forwards}}
@keyframes load{{0%{{width:0%}} 30%{{width:45%}} 70%{{width:86%}} 100%{{width:100%}}}}
a{{color:#FFD54F;text-decoration:none}}a:hover{{text-decoration:underline}}
#granted{{position:fixed;inset:0;z-index:10;display:none;place-items:center;background:rgba(0,0,0,.88);}}
#granted h1{{font-size:54px;color:#00FF41;text-shadow:0 0 20px #00FF41,0 0 60px #00FF41;letter-spacing:6px;animation:glitch .15s infinite}}
@keyframes glitch{{0%{{transform:translate(0)}} 20%{{transform:translate(-3px,2px);text-shadow:3px 0 #ff00ff, -3px 0 #00ffff}} 40%{{transform:translate(3px,-2px)}} 60%{{transform:translate(-1px,1px)}} 100%{{transform:translate(0)}}}}
</style>
</head><body>
<canvas id="matrix"></canvas>
<div id="granted"><h1>ACCESS GRANTED</h1></div>
<div class="terminal">
<div style="display:flex;gap:6px;margin-bottom:14px"><span style="width:11px;height:11px;background:#ff5f56;border-radius:50%"></span><span style="width:11px;height:11px;background:#ffbd2e;border-radius:50%"></span><span style="width:11px;height:11px;background:#27c93f;border-radius:50%"></span><small style="color:#555;margin-left:8px">0xSoloh@vault:~ — decrypting</small></div>
<div id="type" style="min-height:110px;line-height:1.6"></div>
<div class="bar"><div class="fill"></div></div>
<small id="status" style="color:#888">> decrypting writeup... [HTB:// ACTIVE]</small>
<br><br>
<a href="https://kimsec.netlify.app/?lab={slug}">Click here if not redirected — BACK goes to kimsec.netlify.app</a>
</div>
<script>
const c=document.getElementById('matrix'),x=c.getContext('2d');
function r(){{c.width=innerWidth;c.height=innerHeight}}r();addEventListener('resize',r);
let d=Array(Math.floor(c.width/14)).fill(0);
setInterval(()=>{{x.fillStyle='rgba(0,0,0,.08)';x.fillRect(0,0,c.width,c.height);x.fillStyle='#00FF41';x.font='14px monospace';d.forEach((v,i)=>{{x.fillText(String.fromCharCode(33+Math.random()*90),i*14,v*14);if(v*14>c.height&&Math.random()>.975)d[i]=0;d[i]++}})}},50);
const lines=[`$ ./vault --open {slug}`,`> locating {slug}.md in ~/vault... FOUND`,`> bypassing paywall... OK`,`> injecting writeup...`];
let li=0,ci=0;const el=document.getElementById('type');
function type(){{if(li>=lines.length){{showGranted();return}}const cur=lines[li];if(ci==0){{el.innerHTML+= (li>0?'<br>':'') }}if(ci<cur.length){{el.innerHTML+=cur[ci];ci++;setTimeout(type,28)}}else{{el.innerHTML+='<br>';li++;ci=0;setTimeout(type,280)}}}}type();
function showGranted(){{
document.getElementById('status').innerHTML='> <b style="color:#00FF41">ACCESS GRANTED</b> - Redirecting to {title}...';
document.getElementById('granted').style.display='grid';
setTimeout(()=>{{window.location.replace("https://kimsec.netlify.app/?lab={slug}");}},1100);
}}
</script>
</body></html>'''
    folder_path = os.path.join(LABS_DIR, slug)
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

data = []
for f in files:
    full_path = f"writeups/{f}"
    title = f.replace(".md","").replace("-"," ").replace("_"," ").title()
    
    old = old_data.get(f) or old_data.get(full_path) or {}
    
    # Preserve image logic
    img = old.get("image", "")
    possible = f"writeups/images/{f.replace('.md','.png')}"
    possible2 = f"writeups/images/{f.replace('.md','.jpg')}"
    if not img and os.path.exists(possible):
        img = possible
    if not img and os.path.exists(possible2):
        img = possible2

    # Build entry - KEEP ALL OLD FIELDS
    entry = {
        "file": full_path,
        "title": old.get("title", title),
        "platform": old.get("platform", "TryHackMe" if "thm" in f.lower() else "HackTheBox"),
        "level": old.get("level", "Medium"),
        "date": old.get("date", datetime.date.today().isoformat()),
        "tags": old.get("tags", [f.split("-")[0].lower()]),
        "image": img,
        "slug": old.get("slug", get_slug(f))  # ADDED: keep slug
    }
    
    # === CRITICAL FIX: Preserve premium & restricted fields ===
    for key in ["premium", "price", "active", "restricted", "unlockKey", "season", "desc", "platform", "level", "slug"]:
        if key in old:
            entry[key] = old[key]

    # Auto-detect: if filename contains 'premium' mark it premium
    if "premium" in f.lower() and "premium" not in old:
        entry["premium"] = True
        entry["price"] = 50

    # If no desc, try read first 200 chars from md
    if not entry.get("desc"):
        try:
            with open(full_path, encoding="utf-8", errors="ignore") as mf:
                entry["desc"] = mf.read()[:200].replace("\n"," ")
        except:
            pass

    data.append(entry)

# Sort by date desc
data.sort(key=lambda x: x.get("date",""), reverse=True)

with open("writeups.json","w", encoding="utf-8") as out:
    json.dump(data, out, indent=2)

# === ADDED: Create labs/{slug}/index.html with own cover ===
if os.path.exists(LABS_DIR):
    shutil.rmtree(LABS_DIR)
os.makedirs(LABS_DIR, exist_ok=True)
for p in data:
    make_lab_page(p)

print(f"✅ Done! {len(files)} writeups - preserved {len(old_data)//3} old entries with premium/active flags")
print("Premium writeups:", [d["file"] for d in data if d.get("premium")])
print(f"✅ Created {len(data)} lab share pages in /{LABS_DIR}/ with own og:image + hacker loader + ACCESS GRANTED")