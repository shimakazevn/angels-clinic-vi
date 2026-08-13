#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
fp = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data", "CommonEvents.json")

with open(fp, 'r', encoding='utf-8') as f:
    ce = json.load(f)

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

for ce_id in [402, 403]:
    ev = next((e for e in ce if e and e.get('id') == ce_id), None)
    if not ev: continue
    print(f"\n=================== CE {ce_id} ({ev.get('name')}) ===================")
    jp_in_ev = 0
    bad_excl = 0
    for idx, cmd in enumerate(ev.get('list', [])):
        code = cmd.get('code')
        if code == 101:
            p = cmd.get('parameters', [])
            spk = p[4] if len(p) >= 5 else ''
            print(f"\n[{idx}] SPEAKER: {repr(spk)}")
        elif code == 401:
            txt = cmd['parameters'][0] if cmd.get('parameters') else ''
            if jp_regex.search(txt):
                jp_in_ev += 1
                print(f"  [JP {idx}]: {repr(txt)}")
            elif '!' in txt and any(c in txt for c in ['す!ごく', 'だ!たら', 'しま!た']):
                bad_excl += 1
                print(f"  [BAD ! {idx}]: {repr(txt)}")
            else:
                print(f"  [{idx}]: {txt}")
    print(f"CE {ce_id} Total Japanese lines: {jp_in_ev}, Bad '!' count: {bad_excl}")
