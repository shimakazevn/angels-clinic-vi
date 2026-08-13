#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"e:\天使の早漏治療クリニック - RJ01644040"
ORIG_DATA = os.path.join(ROOT, "天使の早漏治療クリニック", "Game", "data")
EN_DATA = os.path.join(ROOT, "The_Angelic_PE_Treatment_Clinic_v3_EN", "data")
DATA_VN = os.path.join(ROOT, "translation", "data_vn")
PATCH_DATA = os.path.join(ROOT, "patch-release", "patch", "data")
TEST_GAME_DATA = os.path.join(ROOT, "Phòng_Khám_Trị_Liệu_Xuất_Tinh_Sớm_Của_Thiên_Sứ_VN", "Game", "data")

SPEAKER_MAP = {
    '\\N[1]': '\\N[1]',
    '\\C[4]セラ': '\\C[4]Sera',
    '\\C[4]セラL': '\\C[4]Sera L',
    '\\C[4]セラR': '\\C[4]Sera R',
    '\\C[5]サキュバス': '\\C[5]Succubus',
    '受付嬢': 'Lễ Tân Công Hội',
    'ギルドの受付嬢': 'Lễ Tân Công Hội',
    '\\C[5]？？？': '\\C[5]？？？',
    '魔物': 'Quái vật',
    '\\C[4]？？？': '\\C[4]？？？'
}

def translate_speaker(jp_speaker):
    if not jp_speaker: return ''
    if jp_speaker in SPEAKER_MAP: return SPEAKER_MAP[jp_speaker]
    if 'セラL' in jp_speaker: return '\\C[4]Sera L'
    if 'セラR' in jp_speaker: return '\\C[4]Sera R'
    if 'セラ' in jp_speaker: return '\\C[4]Sera'
    if 'サキュバス' in jp_speaker: return '\\C[5]Succubus'
    if '受付嬢' in jp_speaker: return 'Lễ Tân Công Hội'
    if '魔物' in jp_speaker: return 'Quái vật'
    return jp_speaker

with open(os.path.join(ORIG_DATA, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    orig_ce = json.load(f)

with open(os.path.join(EN_DATA, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    en_ce = json.load(f)

# Build a comprehensive translation dictionary from English CommonEvents.json + previous VN CommonEvents.json
jp_regex = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]')

master = json.loads(json.dumps(orig_ce))

translated_count = 0

for i in range(min(len(orig_ce), len(en_ce))):
    ev_o = orig_ce[i]
    ev_m = master[i]
    ev_e = en_ce[i]

    if not (ev_o and ev_m and ev_e and 'list' in ev_o and 'list' in ev_m and 'list' in ev_e):
        continue

    list_o = ev_o['list']
    list_m = ev_m['list']
    list_e = ev_e['list']

    for j in range(min(len(list_o), len(list_e))):
        cmd_o = list_o[j]
        cmd_m = list_m[j]
        cmd_e = list_e[j]

        code = cmd_o.get('code')
        if code == 101:
            p = cmd_m.get('parameters', [])
            if len(p) >= 5 and p[4]:
                p[4] = translate_speaker(p[4])
        elif code == 401:
            p_o = cmd_o.get('parameters', [])
            p_e = cmd_e.get('parameters', [])
            if p_o and p_e and len(p_o) > 0 and len(p_e) > 0:
                txt_o = p_o[0]
                txt_e = p_e[0]
                if isinstance(txt_o, str) and isinstance(txt_e, str):
                    if jp_regex.search(txt_o) and txt_e:
                        cmd_m['parameters'][0] = txt_e
                        translated_count += 1

print(f"Mapped {translated_count} dialogue commands to English/VN text in CommonEvents.json!")

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'w', encoding='utf-8') as f:
    json.dump(master, f, ensure_ascii=False, indent=4)

shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(PATCH_DATA, "CommonEvents.json"))
shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(TEST_GAME_DATA, "CommonEvents.json"))

print("Synced master CommonEvents.json to patch-release and test game!")
