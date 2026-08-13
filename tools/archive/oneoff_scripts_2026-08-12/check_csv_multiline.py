#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, csv, json, re, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
csv_fp = os.path.join(ROOT, "translation", "text_export.csv")

# Check: how many VN translations have \n (multi-line merged)?
total_ce = 0
multiline = 0
singleline = 0
total_vn_lines = 0
sample_multi = []

with open(csv_fp, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('file') != 'CommonEvents':
            continue
        total_ce += 1
        vn = row.get('vietnamese', '')
        jp = row.get('original_jp', '')
        jp_line_count = jp.count('\n') + 1
        vn_line_count = vn.count('\n') + 1
        total_vn_lines += vn_line_count
        if jp_line_count > 1:
            multiline += 1
            if len(sample_multi) < 3:
                sample_multi.append({
                    'jp': jp,
                    'vn': vn,
                    'jp_lines': jp_line_count,
                    'vn_lines': vn_line_count
                })
        else:
            singleline += 1

print(f"Total CE rows in CSV: {total_ce}")
print(f"  Single-line (1 x code 401): {singleline}")
print(f"  Multi-line (merged 401s):   {multiline}")
print(f"  Total VN lines if split:    {total_vn_lines}")
print()
print("=== Sample multi-line rows ===")
for s in sample_multi:
    print(f"JP ({s['jp_lines']} lines): {repr(s['jp'])}")
    print(f"VN ({s['vn_lines']} lines): {repr(s['vn'])}")
    print()
