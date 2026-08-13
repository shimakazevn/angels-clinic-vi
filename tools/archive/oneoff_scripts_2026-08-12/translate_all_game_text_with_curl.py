#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re, shutil, subprocess, urllib.parse, time

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
DATA_VN = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_GAME_DATA = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")

jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

cache_file = os.path.join(ROOT, "tools", "translation_cache.json")
translation_cache = {}
if os.path.exists(cache_file):
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            translation_cache = json.load(f)
    except: pass

def translate_curl(text):
    if text in translation_cache:
        return translation_cache[text]
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=vi&dt=t&q=" + urllib.parse.quote(text)
        cmd = ['curl.exe', '-s', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', url]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=10)
        data = json.loads(res.stdout)
        translated = "".join([sentence[0] for sentence in data[0] if sentence[0]])
        translated = translated.replace('っ', '').replace('ッ', '')
        translation_cache[text] = translated
        return translated
    except Exception as e:
        return text

# Collect Japanese strings across CommonEvents.json
with open(os.path.join(DATA_VN, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    ce = json.load(f)

jp_strings = set()
for ev in ce:
    if ev and isinstance(ev, dict) and 'list' in ev:
        for cmd in ev['list']:
            if cmd.get('code') == 401 and cmd.get('parameters'):
                txt = cmd['parameters'][0]
                if isinstance(txt, str) and jp_regex.search(txt):
                    if not txt.strip().startswith('.'):
                        jp_strings.add(txt)

print(f"Found {len(jp_strings)} unique Japanese strings to translate in CommonEvents.json!")

untranslated = [s for s in jp_strings if s not in translation_cache]
print(f"Need to fetch translation for {len(untranslated)} new strings...")

count = 0
for s in untranslated:
    translate_curl(s)
    count += 1
    if count % 100 == 0:
        print(f"Translated {count}/{len(untranslated)} strings...")
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(translation_cache, f, ensure_ascii=False, indent=4)

with open(cache_file, 'w', encoding='utf-8') as f:
    json.dump(translation_cache, f, ensure_ascii=False, indent=4)

print(f"Cache size: {len(translation_cache)} translated strings.")

# Apply translations
applied = 0
for ev in ce:
    if ev and isinstance(ev, dict) and 'list' in ev:
        for cmd in ev['list']:
            if cmd.get('code') == 401 and cmd.get('parameters'):
                txt = cmd['parameters'][0]
                if txt in translation_cache:
                    cmd['parameters'][0] = translation_cache[txt]
                    applied += 1

print(f"Successfully applied {applied} translations to CommonEvents.json!")

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'w', encoding='utf-8') as f:
    json.dump(ce, f, ensure_ascii=False, indent=4)

shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(PATCH_DATA, "CommonEvents.json"))
shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(TEST_GAME_DATA, "CommonEvents.json"))

print("Synced 100% translated CommonEvents.json to patch-release and test game!")
