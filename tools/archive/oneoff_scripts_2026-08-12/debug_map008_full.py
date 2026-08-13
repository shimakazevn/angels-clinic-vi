#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
fp = os.path.join(ROOT, "translation", "data_vn", "Map008.json")

with open(fp, 'r', encoding='utf-8') as f:
    map8 = json.load(f)

print("=== Map008 Ev 1 page 0 full command list (all non-zero) ===")
for ev in map8.get('events', []):
    if not ev or ev.get('id') != 1: continue
    for pi, page in enumerate(ev.get('pages', [])):
        print(f"Page {pi}:")
        for i, cmd in enumerate(page.get('list', [])):
            code = cmd.get('code', 0)
            if code != 0:
                params = cmd.get('parameters', [])
                # Truncate long params
                p_str = str(params)
                if len(p_str) > 120:
                    p_str = p_str[:120] + '...'
                print(f"  [{i}] code={code} {p_str}")
