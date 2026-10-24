import os, json, datetime

folder = "writeups"
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
    except Exception as e:
        print(f"Warning: could not load old writeups.json: {e}")

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
        "image": img
    }
    
    # === CRITICAL FIX: Preserve premium & restricted fields ===
    for key in ["premium", "price", "active", "restricted", "unlockKey", "season", "desc", "platform", "level"]:
        if key in old:
            entry[key] = old[key]

    # Auto-detect: if filename contains 'premium' mark it premium
    if "premium" in f.lower() and "premium" not in old:
        entry["premium"] = True
        entry["price"] = 50

    data.append(entry)

# Sort by date desc
data.sort(key=lambda x: x.get("date",""), reverse=True)

with open("writeups.json","w", encoding="utf-8") as out:
    json.dump(data, out, indent=2)

print(f"✅ Done! {len(files)} writeups - preserved {len(old_data)//3} old entries with premium/active flags")
print("Premium writeups:", [d["file"] for d in data if d.get("premium")])