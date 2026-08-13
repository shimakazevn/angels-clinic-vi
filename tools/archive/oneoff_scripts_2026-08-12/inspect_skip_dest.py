#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

ROOT    = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_JP = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data")
DATA_VN = os.path.join(ROOT, "translation", "data_vn")

# Map 36 - destination when "skip all" is chosen
for map_id in [36, 3]:
    fname = f"Map{map_id:03d}.json"
    fp = os.path.join(DATA_JP, fname)
    if not os.path.exists(fp):
        print(f"{fname}: NOT FOUND")
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"\n=== {fname} ===")
    for ev in data.get('events', []):
        if not ev: continue
        for pi, page in enumerate(ev.get('pages', [])):
            for i, cmd in enumerate(page.get('list', [])):
                code = cmd.get('code')
                # Look for spine calls and autorun events
                if code in [355, 655]:
                    params = cmd.get('parameters', [])
                    txt = params[0] if params else ''
                    if 'spine' in str(txt).lower() or 'setAnim' in str(txt):
                        print(f"  Ev {ev['id']} ({ev['name']}) page {pi} [{i}]: code={code} {repr(txt)}")
                if code == 117:  # call CE
                    params = cmd.get('parameters', [])
                    print(f"  Ev {ev['id']} ({ev['name']}) page {pi} [{i}]: Call CE {params}")
    # Check if it's autorun
    for ev in data.get('events', []):
        if not ev: continue
        for pi, page in enumerate(ev.get('pages', [])):
            trigger = page.get('trigger', -1)
            if trigger == 3:  # Autorun
                print(f"  AUTORUN: Ev {ev['id']} ({ev['name']}) page {pi}")

# Also check what CE 610 does (referenced from Map008 line [24])
with open(os.path.join(DATA_VN, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    ce = json.load(f)

ce610 = next((e for e in ce if e and e.get('id') == 610), None)
if ce610:
    print(f"\n=== CE 610 ({ce610.get('name')}) ===")
    for i, cmd in enumerate(ce610.get('list', [])[:30]):
        code = cmd.get('code')
        if code != 0:
            params = cmd.get('parameters', [])
            print(f"  [{i}] code={code} params={params}")
