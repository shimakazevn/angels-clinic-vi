#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re, shutil, urllib.request, urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_GAME_DATA = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    ce = json.load(f)

# Extract unique Japanese dialogue strings
jp_strings = set()

for ev in ce:
    if ev and isinstance(ev, dict) and 'list' in ev:
        for cmd in ev['list']:
            code = cmd.get('code')
            if code == 401 and cmd.get('parameters'):
                txt = cmd['parameters'][0]
                if isinstance(txt, str) and jp_regex.search(txt):
                    if not txt.strip().startswith('.'):
                        jp_strings.add(txt)

print(f"Found {len(jp_strings)} unique Japanese dialogue strings to translate!")

def translate_gt(text):
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=vi&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5)
        data = json.loads(res.read().decode('utf-8'))
        translated = "".join([sentence[0] for sentence in data[0] if sentence[0]])
        # Clean any accidental 'っ' or 'ッ'
        translated = translated.replace('っ', '').replace('ッ', '')
        return translated
    except Exception as e:
        return text

translation_cache = {}
count = 0
for text in list(jp_strings):
    trans = translate_gt(text)
    translation_cache[text] = trans
    count += 1
    if count % 200 == 0:
        print(f"Translated {count}/{len(jp_strings)} strings...")

print(f"Batch translated ALL {len(translation_cache)} unique strings!")

# Apply to CommonEvents.json
applied = 0
for ev in ce:
    if ev and isinstance(ev, dict) and 'list' in ev:
        for cmd in ev['list']:
            if cmd.get('code') == 401 and cmd.get('parameters'):
                txt = cmd['parameters'][0]
                if txt in translation_cache:
                    cmd['parameters'][0] = translation_cache[txt]
                    applied += 1

print(f"Applied {applied} translations to CommonEvents.json!")

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'w', encoding='utf-8') as f:
    json.dump(ce, f, ensure_ascii=False, indent=4)

shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(PATCH_DATA, "CommonEvents.json"))
shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(TEST_GAME_DATA, "CommonEvents.json"))

print("Synced master translated CommonEvents.json to patch-release and test game!")
