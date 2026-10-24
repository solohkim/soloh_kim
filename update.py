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
    html = f'''<!doctype html><html><head><meta charset="utf-8">
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
<meta http-equiv="refresh" content="0; url=/?lab={slug}">
</head><body style="background:#080808;color:#00FF41;font-family:monospace;padding:40px;text-align:center">
<p>Redirecting to {title}...</p>
<p><a href="https://kimsec.netlify.app/?lab={slug}" style="color:#00FF41">Click here if not redirected — BACK goes to kimsec.netlify.app</a></p>
<script>window.location.replace("https://kimsec.netlify.app/?lab={slug}");</script>
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
print(f"✅ Created {len(data)} lab share pages in /{LABS_DIR}/ with own og:image")