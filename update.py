import os, json, datetime

folder = "writeups"
if not os.path.exists(folder):
    os.makedirs(folder)

files = [f for f in os.listdir(folder) if f.endswith(".md")]

# Load old images to preserve
old_data = {}
if os.path.exists("writeups.json"):
    try:
        with open("writeups.json", "r", encoding="utf-8") as jf:
            for item in json.load(jf):
                old_data[item["file"]] = item
                # also allow lookup by just filename
                old_data[item["file"].split("/")[-1]] = item
    except:
        pass

data = []
for f in files:
    title = f.replace(".md","").replace("-"," ").replace("_"," ").title()
    
    old = old_data.get(f, {}) or old_data.get(f"writeups/{f}", {})
    img = old.get("image", "") if isinstance(old, dict) else ""
    
    possible = f"writeups/images/{f.replace('.md','.png')}"
    possible2 = f"writeups/images/{f.replace('.md','.jpg')}"
    if not img and os.path.exists(possible):
        img = possible
    if not img and os.path.exists(possible2):
        img = possible2

    data.append({
        "file": f"writeups/{f}",
        "title": old.get("title", title) if isinstance(old, dict) else title,
        "platform": old.get("platform", "TryHackMe" if "thm" in f.lower() else "HackTheBox") if isinstance(old, dict) else ("TryHackMe" if "thm" in f.lower() else "HackTheBox"),
        "level": old.get("level", "Medium") if isinstance(old, dict) else "Medium",
        "date": old.get("date", datetime.date.today().isoformat()) if isinstance(old, dict) else datetime.date.today().isoformat(),
        "tags": old.get("tags", [f.split("-")[0].lower()]) if isinstance(old, dict) else [f.split("-")[0].lower()],
        "image": img
    })

with open("writeups.json","w", encoding="utf-8") as out:
    json.dump(data, out, indent=2)

print(f"Done! {len(files)} writeups - preserved {len(old_data)}")