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

# OG PAGE TEMPLATE - This is what WhatsApp sees - NOW AUTO DETECTS LAB NAME
OG_TEMPLATE = """<!doctype html>
<html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | 0xSoloh</title>
<meta property="og:title" content="{title} | 0xSoloh" />
<meta property="og:description" content="{desc}" />
<meta property="og:image" content="https://kimsec.netlify.app/{image}" />
<meta property="og:url" content="https://kimsec.netlify.app/labs/{slug}/" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
body{{background:#080808;color:#ddd;font-family:monospace;margin:0}}
.bar{{background:#111;border-bottom:1px solid #222;padding:10px 15px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10}}
#content{{max-width:900px;margin:20px auto;padding:20px;line-height:1.7;color:#ccc}}
#content h1,#content h2{{color:#00FF41}}
button#shareBtn{{background:#00FF41;color:#000;border:0;padding:7px 14px;border-radius:8px;font-weight:bold;cursor:pointer}}
a{{color:#00FF41}}
</style>
</head>
<body>
<div class="bar">
  <a href="/" style="color:#00FF41;text-decoration:none">← 0xSoloh</a>
  <button id="shareBtn">🔗 Share {title}</button>
</div>
<div id="content">Loading {title}...</div>
<script>
const slug = "{slug}";
const shareUrl = "https://kimsec.netlify.app/labs/"+slug+"/";
document.getElementById('shareBtn').onclick = async () => {{
  if(navigator.share){{ await navigator.share({{title: "{title} | 0xSoloh", url: shareUrl}}); }}
  else {{ await navigator.clipboard.writeText(shareUrl); 
    const b=document.getElementById('shareBtn'); b.textContent="✅ Copied!"; setTimeout(()=>b.textContent="🔗 Share",2000);
  }}
}};
fetch("/{file}").then(r=>r.text()).then(t=>{{
  document.getElementById('content').innerHTML = marked.parse(t);
}}).catch(()=>{{ document.getElementById('content').innerHTML="Failed to load."; }});
</script>
</body></html>
"""

for f in files:
    full_path = f"writeups/{f}"
    slug = f.replace(".md","") # layover - AUTO DETECTED
    title_raw = f.replace(".md","").replace("-"," ").replace("_"," ").title()
    
    old = old_data.get(f) or old_data.get(full_path) or {}
    
    img = old.get("image", "")
    possible = f"writeups/images/{f.replace('.md','.png')}"
    possible2 = f"writeups/images/{f.replace('.md','.jpg')}"
    if not img and os.path.exists(possible):
        img = possible
    if not img and os.path.exists(possible2):
        img = possible2
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
        "slug": slug
    }
    
    for key in ["premium", "price", "active", "restricted", "unlockKey", "season", "desc", "platform", "level"]:
        if key in old:
            entry[key] = old[key]
    
    if "premium" in f.lower() and "premium" not in old:
        entry["premium"] = True
        entry["price"] = 50

    data.append(entry)

    # --- BUILD SHARE PAGE FOR THIS WRITEUP - AUTO NAME ---
    desc = old.get("desc", f"{entry['title']} - {entry['platform']} {entry['level']} writeup by 0xSoloh")

    out_dir = pathlib.Path(f"labs/{slug}") # CHANGED: w/ -> labs/
    out_dir.mkdir(parents=True, exist_ok=True)
    html = OG_TEMPLATE.format(
        title=entry['title'],
        desc=desc,
        image=img,
        slug=slug,
        file=full_path
    )
    (out_dir/"index.html").write_text(html, encoding='utf-8')

# Sort and save
data.sort(key=lambda x: x.get("date",""), reverse=True)
with open("writeups.json","w", encoding="utf-8") as out:
    json.dump(data, out, indent=2)

print(f"✅ Done! {len(files)} labs built in /labs/")
print(f"Example: https://kimsec.netlify.app/labs/layover/")