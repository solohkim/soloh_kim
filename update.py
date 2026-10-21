import os, json, datetime

folder = "writeups"
files = [f for f in os.listdir(folder) if f.endswith(".md")]

# Load old images so we don't lose them
old_images = {}
if os.path.exists("writeups.json"):
    try:
        for item in json.load(open("writeups.json", encoding="utf-8")):
            if item.get("image"):
                old_images[item["file"]] = item["image"]
    except: pass

data = []
for f in files:
    title = f.replace(".md","").replace("-"," ").replace("_"," ").title()
    
    # Keep old image if exists, else auto-find
    img = old_images.get(f, "")
    possible = f"writeups/images/{f.replace('.md','.png')}"
    possible2 = f"writeups/images/{f.split('-')[0]}.png"
    if not img and os.path.exists(possible):
        img = possible
    elif not img and os.path.exists(possible2):
        img = possible2
    
    data.append({
        "file": f,
        "title": title,
        "platform": "TryHackMe" if "thm" in f else "HackTheBox",
        "level": "Medium",
        "date": datetime.date.today().isoformat(),
        "tags": [f.split("-")[0]],
        "image": img
    })

with open("writeups.json","w", encoding="utf-8") as out:
    json.dump(data, out, indent=2)

print(f"Done! {len(files)} writeups added - {len(old_images)} images preserved")