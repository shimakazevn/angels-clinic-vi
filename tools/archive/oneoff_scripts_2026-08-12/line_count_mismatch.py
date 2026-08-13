#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm tra chính xác: với những blocks đã match được trong CSV,
JP có bao nhiêu dòng vs VN có bao nhiêu dòng? Chênh lệch là gì?
"""
import os, sys, csv, json, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT   = r"e:\天使の早漏治療クリニック - RJ01644040"
CSV_FP = os.path.join(ROOT, "translation", "text_export.csv")
CE_JP  = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data", "CommonEvents.json")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

# Build CSV map: (ce_id, jp_merged) -> vn_lines count
csv_map = {}
with open(CSV_FP, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('file') != 'CommonEvents': continue
        eid = row.get('entry_id', '').strip()
        jp  = row.get('original_jp', '').strip()
        vn  = row.get('vietnamese', '').strip()
        if not jp or not vn: continue
        vn_lines = vn.split('\n')
        jp_lines = jp.split('\n')
        csv_map[(eid, jp)] = (jp_lines, vn_lines)

# Walk JP master blocks
jp_more_than_vn = 0   # blocks where JP has more lines than VN
equal_lines = 0       # blocks where JP == VN lines
vn_more_than_jp = 0   # blocks where VN has more lines than JP
total_jp_lines_matched = 0
total_vn_lines_matched = 0
sample_mismatch = []

with open(CE_JP, 'r', encoding='utf-8') as f:
    ce_jp = json.load(f)

for ev in ce_jp:
    if not ev or 'list' not in ev: continue
    ev_id_s = str(ev.get('id', ''))
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
                jp_merged = '\n'.join(parts)
                if (ev_id_s, jp_merged) in csv_map:
                    jp_ls, vn_ls = csv_map[(ev_id_s, jp_merged)]
                    n_jp = len(parts)
                    n_vn = len(vn_ls)
                    total_jp_lines_matched += n_jp
                    total_vn_lines_matched += n_vn
                    if n_jp > n_vn:
                        jp_more_than_vn += 1
                        if len(sample_mismatch) < 3:
                            sample_mismatch.append({
                                'ce': ev_id_s,
                                'jp_lines': parts,
                                'vn_lines': vn_ls,
                                'n_jp': n_jp,
                                'n_vn': n_vn
                            })
                    elif n_jp == n_vn:
                        equal_lines += 1
                    else:
                        vn_more_than_jp += 1
            i = j
        else:
            i += 1

print(f"=== Line count comparison for matched blocks ===")
print(f"JP lines total (in matched blocks): {total_jp_lines_matched}")
print(f"VN lines total (in matched blocks): {total_vn_lines_matched}")
print(f"Difference (uncoverable): {total_jp_lines_matched - total_vn_lines_matched}")
print()
print(f"Blocks where JP > VN lines: {jp_more_than_vn}")
print(f"Blocks where JP = VN lines: {equal_lines}")
print(f"Blocks where JP < VN lines: {vn_more_than_jp}")
print()
print("=== Sample blocks where JP has more lines than VN ===")
for s in sample_mismatch:
    print(f"CE {s['ce']}: JP={s['n_jp']} lines vs VN={s['n_vn']} lines")
    for l in s['jp_lines']:
        print(f"  JP: {repr(l)}")
    for l in s['vn_lines']:
        print(f"  VN: {repr(l)}")
    print()
