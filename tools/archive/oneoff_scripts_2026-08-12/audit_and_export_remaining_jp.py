#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re, csv

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

# Count in all 3 sources
sources = {
    "JP Master": os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data", "CommonEvents.json"),
    "EN Version": os.path.join(ROOT, "The_Angelic_PE_Treatment_Clinic_v3_EN", "data", "CommonEvents.json"),
    "VN Current": os.path.join(ROOT, "translation", "data_vn", "CommonEvents.json"),
}

for name, fp in sources.items():
    if not os.path.exists(fp):
        print(f"{name}: FILE NOT FOUND")
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        ce = json.load(f)
    
    total_401 = 0
    jp_401 = 0
    vn_401 = 0
    en_401 = 0
    empty_401 = 0

    for ev in ce:
        if ev and 'list' in ev:
            for cmd in ev['list']:
                if cmd.get('code') == 401 and cmd.get('parameters'):
                    txt = cmd['parameters'][0]
                    if isinstance(txt, str):
                        total_401 += 1
                        if not txt.strip():
                            empty_401 += 1
                        elif jp_regex.search(txt):
                            jp_401 += 1
                        else:
                            # Non-JP, non-empty
                            vn_401 += 1
    
    print(f"\n=== {name} ===")
    print(f"  Total code 401 lines: {total_401}")
    print(f"  Japanese text lines:  {jp_401}")
    print(f"  Non-JP text lines:    {vn_401}")
    print(f"  Empty lines:          {empty_401}")

# Also export remaining JP lines in VN to CSV for manual translation
print("\n\nExporting remaining Japanese lines to CSV for manual translation...")
fp_vn = sources["VN Current"]
with open(fp_vn, 'r', encoding='utf-8') as f:
    ce_vn = json.load(f)

fp_jp = sources["JP Master"]
with open(fp_jp, 'r', encoding='utf-8') as f:
    ce_jp = json.load(f)

csv_fp = os.path.join(ROOT, "tools", "remaining_jp_lines.csv")
rows = []

for ev_vn in ce_vn:
    if not ev_vn or 'list' not in ev_vn: continue
    ev_id = ev_vn.get('id', 0)
    ev_name = ev_vn.get('name', '')
    for cmd_idx, cmd in enumerate(ev_vn['list']):
        if cmd.get('code') == 401 and cmd.get('parameters'):
            txt = cmd['parameters'][0]
            if isinstance(txt, str) and jp_regex.search(txt):
                rows.append({
                    'ce_id': ev_id,
                    'ce_name': ev_name,
                    'cmd_idx': cmd_idx,
                    'japanese_text': txt,
                    'vietnamese_translation': ''
                })

with open(csv_fp, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['ce_id', 'ce_name', 'cmd_idx', 'japanese_text', 'vietnamese_translation'])
    writer.writeheader()
    writer.writerows(rows)

print(f"Exported {len(rows)} remaining Japanese lines to: tools/remaining_jp_lines.csv")
