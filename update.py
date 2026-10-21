import os, json, datetime

folder = "writeups"
files = [f for f in os.listdir(folder) if f.endswith(".md")]

data = []
for f in files:
    title = f.replace(".md","").replace("-"," ").title()
    data.append({
        "file": f,
        "title": title,
        "platform": "TryHackMe" if "thm" in f else "HackTheBox",
        "level": "Medium",
        "date": datetime.date.today().isoformat(),
        "tags": [f.split("-")[0]]
    })

with open("writeups.json","w") as out:
    json.dump(data, out, indent=2)

print(f"Done! {len(files)} writeups added to writeups.json")