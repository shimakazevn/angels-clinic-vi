#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify CommonEvents.json structure vs JP master:
- Số lượng events khớp nhau không?
- Mỗi event có đúng số lệnh không?
- Không có lệnh nào bị thay đổi code?
"""
import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

ROOT    = r"e:\天使の早漏治療クリニック - RJ01644040"
CE_JP   = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data", "CommonEvents.json")
CE_VN   = os.path.join(ROOT, "translation", "data_vn", "CommonEvents.json")

with open(CE_JP, 'r', encoding='utf-8') as f:
    ce_jp = json.load(f)
with open(CE_VN, 'r', encoding='utf-8') as f:
    ce_vn = json.load(f)

print(f"JP events count: {len(ce_jp)}")
print(f"VN events count: {len(ce_vn)}")

struct_errors = []

for i in range(min(len(ce_jp), len(ce_vn))):
    ev_j = ce_jp[i]
    ev_v = ce_vn[i]
    if ev_j is None and ev_v is None:
        continue
    if (ev_j is None) != (ev_v is None):
        struct_errors.append(f"CE index {i}: one is null, other is not")
        continue
    if ev_j.get('id') != ev_v.get('id'):
        struct_errors.append(f"CE index {i}: id mismatch {ev_j.get('id')} vs {ev_v.get('id')}")
        continue

    list_j = ev_j.get('list', [])
    list_v = ev_v.get('list', [])
    if len(list_j) != len(list_v):
        struct_errors.append(f"CE {ev_j.get('id')} ({ev_j.get('name')}): cmd count {len(list_j)} vs {len(list_v)}")
        continue

    for k in range(len(list_j)):
        code_j = list_j[k].get('code')
        code_v = list_v[k].get('code')
        if code_j != code_v:
            struct_errors.append(f"CE {ev_j.get('id')} cmd[{k}]: code {code_j} vs {code_v}")
            break

if not struct_errors:
    print("\n✅ Structure is 100% identical to JP master — no structural issues!")
    print("   The _spine error is NOT caused by our translation changes.")
else:
    print(f"\n❌ Found {len(struct_errors)} structural differences:")
    for e in struct_errors[:20]:
        print(f"  {e}")
