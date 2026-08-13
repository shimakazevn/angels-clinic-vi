#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full audit: so sánh JP Master (7798 dòng) vs CSV (5181 dòng khi split)
Tìm những CE nào, block nào hoàn toàn bị bỏ sót trong CSV.
"""
import os, sys, csv, json, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT   = r"e:\天使の早漏治療クリニック - RJ01644040"
CSV_FP = os.path.join(ROOT, "translation", "text_export.csv")
CE_JP  = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data", "CommonEvents.json")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

# 1. Build CSV lookup: jp_merged -> vn_merged  (per CE entry_id)
csv_by_id = {}  # {ce_id: [(jp_merged, vn_merged), ...]}
with open(CSV_FP, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('file') != 'CommonEvents': continue
        eid = row.get('entry_id', '')
        jp  = row.get('original_jp', '').strip()
        vn  = row.get('vietnamese', '').strip()
        if not jp: continue
        if eid not in csv_by_id:
            csv_by_id[eid] = []
        csv_by_id[eid].append((jp, vn))

# Also flat set of all JP texts in CSV
csv_jp_flat = set()
for rows in csv_by_id.values():
    for jp, vn in rows:
        csv_jp_flat.add(jp)

# 2. Walk JP Master and count blocks per CE
with open(CE_JP, 'r', encoding='utf-8') as f:
    ce_jp = json.load(f)

total_blocks_jp   = 0
total_lines_jp    = 0
covered_blocks    = 0
covered_lines     = 0
missed_blocks     = 0
missed_lines      = 0

missed_ces = {}  # {ce_id: {name, missed_blocks, missed_lines}}

for ev in ce_jp:
    if not ev or 'list' not in ev: continue
    ev_id   = str(ev.get('id', ''))
    ev_name = ev.get('name', '')
    cmd_list = ev['list']

    i = 0
    ev_missed_blocks = 0
    ev_missed_lines  = 0
    while i < len(cmd_list):
        cmd = cmd_list[i]
        if cmd.get('code') == 101:
            j = i + 1
            parts = []
            while j < len(cmd_list) and cmd_list[j].get('code') == 401:
                p = cmd_list[j].get('parameters', [])
                parts.append(p[0] if p else '')
                j += 1
            if parts:
                merged = '\n'.join(parts)
                n_lines = len(parts)
                total_blocks_jp += 1
                total_lines_jp  += n_lines

                if merged.strip() in csv_jp_flat:
                    covered_blocks += 1
                    covered_lines  += n_lines
                else:
                    missed_blocks += 1
                    missed_lines  += n_lines
                    ev_missed_blocks += 1
                    ev_missed_lines  += n_lines
            i = j
        else:
            i += 1

    if ev_missed_blocks > 0:
        missed_ces[ev_id] = {
            'name': ev_name,
            'missed_blocks': ev_missed_blocks,
            'missed_lines': ev_missed_lines
        }

print(f"=== JP Master Dialogue Block Audit ===")
print(f"Total blocks (101+401):  {total_blocks_jp}")
print(f"Total lines (401):       {total_lines_jp}")
print(f"Covered in CSV:          {covered_blocks} blocks / {covered_lines} lines")
print(f"MISSED (not in CSV):     {missed_blocks} blocks / {missed_lines} lines")
print(f"\nCEs with missed blocks:  {len(missed_ces)}")
print(f"\n=== Top 20 CEs with most missed lines ===")
top = sorted(missed_ces.items(), key=lambda x: x[1]['missed_lines'], reverse=True)[:20]
for ce_id, info in top:
    print(f"  CE {ce_id:>4} ({info['name'][:30]:<30}): {info['missed_blocks']} blocks, {info['missed_lines']} lines missed")
