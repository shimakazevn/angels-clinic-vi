#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

ROOT    = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN = os.path.join(ROOT, "translation", "data_vn")

with open(os.path.join(DATA_VN, "Map008.json"), 'r', encoding='utf-8') as f:
    map8 = json.load(f)

for ev in map8.get('events', []):
    if not ev: continue
    for pi, page in enumerate(ev.get('pages', [])):
        cmds = page.get('list', [])
        has_choice = any(c.get('code') == 102 for c in cmds)
        has_transfer = any(c.get('code') == 201 for c in cmds)
        if has_choice or has_transfer:
            ev_id = ev['id']
            ev_name = ev['name']
            print(f"Ev {ev_id} ({ev_name}) page {pi}:")
            for i, cmd in enumerate(cmds):
                code = cmd.get('code')
                if code != 0:
                    print(f"  [{i}] code={code} params={cmd.get('parameters', [])}")
