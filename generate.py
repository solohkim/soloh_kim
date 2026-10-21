import os, json, glob

old = {}
if os.path.exists("writeups.json"):
    try:
        for item in json.load(open("writeups.json")):
            old[item["file"]] = item.get("image","")
    except: pass

writeups = []
for f in glob.glob("*.md"):
    if f.lower() in ["readme.md","contributing.md"]: continue
    name = f.replace(".md","").replace("-"," ").replace("_"," ")
    title = " ".join([w.capitalize() for w in name.split()])
    writeups.append({
        "file": f,
        "title": title,
        "platform": "HackTheBox",
        "level": "Medium",
        "date": "2026-10-21",
        "tags": [f.split("-")[0].lower()],
        "image": old.get(f, "")  # keeps old image
    })

json.dump(writeups, open("writeups.json","w"), indent=2)
print(f"Generated {len(writeups)} with images preserved")