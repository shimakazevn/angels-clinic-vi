#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

ROOT    = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN = os.path.join(ROOT, "translation", "data_vn")

# Check Map008.json - the New Game start menu with skip option
with open(os.path.join(DATA_VN, "Map008.json"), 'r', encoding='utf-8') as f:
    map8 = json.load(f)

print("=== Map008 events with choices (Skip option) ===")
for ev in map8.get('events', []):
    if not ev: continue
    for page in ev.get('pages', []):
        for i, cmd in enumerate(page.get('list', [])):
            if cmd.get('code') == 402:  # When [Branch] choice handler
                params = cmd.get('parameters', [])
                print(f"  Ev {ev.get('id')} [{ev.get('name')}] Choice branch [{params}]:")
                # Show next few commands in this branch
                for j in range(i+1, min(i+20, len(page['list']))):
                    c = page['list'][j]
                    code = c.get('code')
                    if code in [402, 404]: break  # next branch
                    print(f"    [{j}] code={code} params={c.get('parameters', [])}")

# Check CommonEvent 104
with open(os.path.join(DATA_VN, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    ce = json.load(f)

ce104 = next((e for e in ce if e and e.get('id') == 104), None)
if ce104:
    print(f"\n=== CE 104 ({ce104.get('name')}) ===")
    for i, cmd in enumerate(ce104.get('list', [])[:40]):
        code = cmd.get('code')
        params = cmd.get('parameters', [])
        if code not in [0]:
            print(f"  [{i}] code={code} params={params}")
