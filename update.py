import os, json, datetime, pathlib

folder = "writeups"
if not os.path.exists(folder):
    os.makedirs(folder)

files = [f for f in os.listdir(folder) if f.endswith(".md")]

# Load old data to preserve EVERYTHING
old_data = {}
if os.path.exists("writeups.json"):
    try:
        with open("writeups.json", "r", encoding="utf-8") as jf:
            for item in json.load(jf):
                old_data[item["file"]] = item
                old_data[item["file"].split("/")[-1]] = item
                old_data[f"writeups/{item['file'].split('/')[-1]}"] = item
    except Exception as e:
        print(f"Warning: could not load old writeups.json: {e}")

data = []

# OG PAGE TEMPLATE - This is what WhatsApp sees
OG_TEMPLATE = """<!doctype html>
<html><head>
<meta charset="utf-8">
<title>{title} | 0xSoloh</title>
<meta property="og:title" content="{title} | 0xSoloh" />
<meta property="og:description" content="{desc}" />
<meta property="og:image" content="https://kimsec.netlify.app/{image}" />
<meta property="og:url" content="https://kimsec.netlify.app/w/{slug}/" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />
<meta http-equiv="refresh" content="0; url=/{redirect_target}" />
<style>body{{background:#080808;color:#0f0;font-family:monospace;display:grid;place-items:center;height:100vh}}a{{color:#00FF41}}</style>
</head>
<body>Loading {title}... <a href="/{redirect_target}">Click here if not redirected</a></body></html>
"""

for f in files:
    full_path = f"writeups/{f}"
    slug = f.replace(".md","") # pickle-rick
    title_raw = f.replace(".md","").replace("-"," ").replace("_"," ").title()
    
    old = old_data.get(f) or old_data.get(full_path) or {}
    
    img = old.get("image", "")
    possible = f"writeups/images/{f.replace('.md','.png')}"
    possible2 = f"writeups/images/{f.replace('.md','.jpg')}"
    if not img and os.path.exists(possible):
        img = possible
    if not img and os.path.exists(possible2):
        img = possible2
    # fallback logo if no cover
    if not img:
        img = "logo.jpeg"

    entry = {
        "file": full_path,
        "title": old.get("title", title_raw),
        "platform": old.get("platform", "TryHackMe" if "thm" in f.lower() else "HackTheBox"),
        "level": old.get("level", "Medium"),
        "date": old.get("date", datetime.date.today().isoformat()),
        "tags": old.get("tags", [f.split("-")[0].lower()]),
        "image": img,
        "slug": slug # new field for share link
    }
    
    for key in ["premium", "price", "active", "restricted", "unlockKey", "season", "desc", "platform", "level"]:
        if key in old:
            entry[key] = old[key]
    
    if "premium" in f.lower() and "premium" not in old:
        entry["premium"] = True
        entry["price"] = 50

    data.append(entry)

    # --- BUILD SHARE PAGE FOR THIS WRITEUP ---
    desc = old.get("desc", f"{entry['title']} - {entry['platform']} {entry['level']} writeup by 0xSoloh")
    # Your main site likely opens writeup via index.html# or viewer - redirect there
    # If you use viewer.html for md->pdf, change to f"viewer.html?file={full_path}"
    redirect_target = f"index.html#writeup-{slug}" 

    out_dir = pathlib.Path(f"w/{slug}")
    out_dir.mkdir(parents=True, exist_ok=True)
    html = OG_TEMPLATE.format(
        title=entry['title'],
        desc=desc,
        image=img,
        slug=slug,
        redirect_target=redirect_target
    )
    (out_dir/"index.html").write_text(html, encoding='utf-8')

# Sort and save
data.sort(key=lambda x: x.get("date",""), reverse=True)
with open("writeups.json","w", encoding="utf-8") as out:
    json.dump(data, out, indent=2)

print(f"✅ Done! {len(files)} writeups + {len(files)} OG share pages built")
print("Example share link: https://kimsec.netlify.app/w/pickle-rick/")