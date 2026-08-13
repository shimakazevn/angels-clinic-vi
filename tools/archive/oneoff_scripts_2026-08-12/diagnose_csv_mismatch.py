#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnose why block matching fails: compare JP text from CSV vs. JP text from VN CommonEvents.json
"""
import os, sys, csv, json, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT    = r"e:\天使の早漏治療クリニック - RJ01644040"
CSV_FP  = os.path.join(ROOT, "translation", "text_export.csv")
CE_JP   = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data", "CommonEvents.json")
CE_VN   = os.path.join(ROOT, "translation", "data_vn", "CommonEvents.json")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

# Load a sample of CSV JP texts
csv_samples = []
with open(CSV_FP, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('file') == 'CommonEvents':
            jp = row.get('original_jp', '').strip()
            vn = row.get('vietnamese', '').strip()
            if jp and jp_regex.search(jp):
                csv_samples.append({'jp': jp, 'vn': vn})
            if len(csv_samples) >= 5:
                break

print("=== CSV sample JP texts (first 5 with Japanese) ===")
for s in csv_samples:
    print(f"JP: {repr(s['jp'])}")
    print(f"VN: {repr(s['vn'])}")
    print()

# Load CommonEvents.json (JP master) and extract first 5 dialogue blocks
with open(CE_JP, 'r', encoding='utf-8') as f:
    ce_jp = json.load(f)

print("=== JP Master first 5 dialogue blocks (CE 125) ===")
ev125 = next((e for e in ce_jp if e and e.get('id') == 125), None)
if ev125:
    cnt = 0
    i = 0
    cmd_list = ev125['list']
    while i < len(cmd_list) and cnt < 5:
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
                print(f"Block at cmd {i}: {repr(merged)}")
                cnt += 1
            i = j
        else:
            i += 1

# Compare: does the CSV JP text match the JP master text?
print("\n=== Checking if CSV JP matches JP Master block text ===")
csv_jp_set = set()
with open(CSV_FP, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('file') == 'CommonEvents':
            jp = row.get('original_jp', '').strip()
            if jp:
                csv_jp_set.add(jp)

matched = 0
unmatched = 0
for ev in ce_jp:
    if not ev or 'list' not in ev: continue
    cmd_list = ev['list']
    i = 0
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
                if merged.strip() in csv_jp_set:
                    matched += 1
                else:
                    unmatched += 1
            i = j
        else:
            i += 1

print(f"Blocks matched in CSV: {matched}")
print(f"Blocks NOT matched:    {unmatched}")
