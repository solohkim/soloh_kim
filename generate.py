import os, json, re
from datetime import date

def scan(folder, json_file, kind):
    old = {}
    if os.path.exists(json_file):
        try:
            with open(json_file,'r') as f:
                for item in json.load(f):
                    old[item.get('file') or item.get('title')] = item
        except: pass
    if not os.path.exists(folder): os.makedirs(folder)
    files = [f for f in os.listdir(folder) if f.endswith('.md')]
    out = []
    for f in sorted(files, reverse=True):
        key = f
        if key in old: out.append(old[key])
        else:
            title = f.replace('.md','').replace('-',' ').title()
            if kind=='writeups': out.append({"file":f,"title":title,"platform":"Lab","level":"Medium","date":str(date.today()),"tags":["writeup"]})
            elif kind=='cheatsheets': out.append({"title":title,"icon":"📄","desc":"My notes on "+title,"file":f})
            else: out.append({"title":title,"desc":"Tool: "+title,"tags":["tool"],"link":"#","file":f})
    with open(json_file,'w') as jf: json.dump(out, jf, indent=2)
    print(f"✅ {kind}: {len(out)} items -> {json_file}")

scan("writeups","writeups.json","writeups")
scan("cheatsheets","cheatsheets.json","cheatsheets")
scan("tools","tools.json","tools")