#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
fp = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data", "CommonEvents.json")

with open(fp, 'r', encoding='utf-8') as f:
    ce = json.load(f)

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

jp_count = 0
for ev in ce:
    if ev and isinstance(ev, dict) and 'list' in ev:
        for idx, cmd in enumerate(ev['list']):
            if cmd.get('code') == 401 and cmd.get('parameters'):
                txt = cmd['parameters'][0]
                if isinstance(txt, str) and jp_regex.search(txt):
                    if not txt.strip().startswith('.'):
                        jp_count += 1
                        if jp_count <= 10:
                            print(f"CE {ev.get('id')} [{idx}]: {repr(txt)}")

print(f"Total remaining Japanese dialogue lines in test game CommonEvents.json: {jp_count}")
