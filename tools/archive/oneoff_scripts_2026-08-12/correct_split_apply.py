#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECT approach:
- Dùng JP Master làm nguồn block → lấy vị trí từng cmd 401
- Tra CSV (jp_merged -> vn_lines) từ JP Master text
- Điền vào VN CommonEvents.json theo đúng vị trí (ce_id, cmd_idx)
"""
import os, sys, csv, json, re, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT       = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN    = os.path.join(ROOT, "translation", "data_vn")
CE_JP_FP   = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data", "CommonEvents.json")
CE_VN_FP   = os.path.join(DATA_VN, "CommonEvents.json")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_DATA  = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")
CSV_FP     = os.path.join(ROOT, "translation", "text_export.csv")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

# ── 1. Build CSV translation map: jp_merged -> vn_lines[]
#       keyed by entry_id for disambiguation
csv_map = {}   # (ce_id, jp_merged) -> [vn_line1, vn_line2, ...]
csv_global = {}  # jp_merged -> [vn_lines] (fallback, last wins)

with open(CSV_FP, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('file') != 'CommonEvents': continue
        eid = row.get('entry_id', '').strip()
        jp  = row.get('original_jp', '').strip()
        vn  = row.get('vietnamese', '').strip()
        if not jp or not vn: continue
        vn_lines = vn.split('\n')
        csv_map[(eid, jp)] = vn_lines
        csv_global[jp] = vn_lines

print(f"Loaded {len(csv_map)} entries from CSV (by CE id)")
print(f"Loaded {len(csv_global)} entries from CSV (global)")

# ── 2. Load JP Master and VN
with open(CE_JP_FP, 'r', encoding='utf-8') as f:
    ce_jp = json.load(f)
with open(CE_VN_FP, 'r', encoding='utf-8') as f:
    ce_vn = json.load(f)

# Build VN lookup by id
vn_by_id = {}
for ev in ce_vn:
    if ev: vn_by_id[ev.get('id')] = ev

# ── 3. Walk JP master block by block, find VN translation, apply to VN CE
applied_blocks = 0
applied_lines  = 0
no_match       = 0

for ev_jp in ce_jp:
    if not ev_jp or 'list' not in ev_jp: continue
    ev_id   = ev_jp.get('id')
    ev_id_s = str(ev_id)
    cmd_list_jp = ev_jp['list']

    ev_vn = vn_by_id.get(ev_id)
    if not ev_vn or 'list' not in ev_vn: continue
    cmd_list_vn = ev_vn['list']

    i = 0
    while i < len(cmd_list_jp):
        cmd_jp = cmd_list_jp[i]
        if cmd_jp.get('code') == 101:
            # Collect 401 indices and texts from JP
            j = i + 1
            block_idxs = []
            jp_parts = []
            while j < len(cmd_list_jp) and cmd_list_jp[j].get('code') == 401:
                p = cmd_list_jp[j].get('parameters', [])
                jp_parts.append(p[0] if p else '')
                block_idxs.append(j)
                j += 1

            if jp_parts:
                jp_merged = '\n'.join(jp_parts)

                # Check if VN already has translation for this block
                vn_parts_current = []
                if block_idxs and block_idxs[-1] < len(cmd_list_vn):
                    for idx in block_idxs:
                        if idx < len(cmd_list_vn):
                            p = cmd_list_vn[idx].get('parameters', [])
                            vn_parts_current.append(p[0] if p else '')

                still_jp = any(jp_regex.search(p) for p in vn_parts_current)

                if still_jp:
                    # Look up translation
                    vn_lines = csv_map.get((ev_id_s, jp_merged)) or csv_global.get(jp_merged)

                    if vn_lines:
                        for k, idx in enumerate(block_idxs):
                            if idx < len(cmd_list_vn) and k < len(vn_lines):
                                cmd_list_vn[idx]['parameters'][0] = vn_lines[k]
                                applied_lines += 1
                        applied_blocks += 1
                    else:
                        no_match += 1

            i = j
        else:
            i += 1

print(f"\nApplied: {applied_blocks} blocks, {applied_lines} lines")
print(f"No match in CSV: {no_match} blocks")

# ── 4. Final count
remaining = 0
for ev in ce_vn:
    if ev and 'list' in ev:
        for cmd in ev['list']:
            if cmd.get('code') == 401 and cmd.get('parameters'):
                txt = cmd['parameters'][0]
                if isinstance(txt, str) and jp_regex.search(txt):
                    if not txt.strip().startswith('.'):
                        remaining += 1

print(f"Remaining Japanese lines: {remaining}")

# ── 5. Save and sync
with open(CE_VN_FP, 'w', encoding='utf-8') as f:
    json.dump(ce_vn, f, ensure_ascii=False, indent=4)
shutil.copy2(CE_VN_FP, os.path.join(PATCH_DATA, "CommonEvents.json"))
shutil.copy2(CE_VN_FP, os.path.join(TEST_DATA, "CommonEvents.json"))
print("Synced!")
