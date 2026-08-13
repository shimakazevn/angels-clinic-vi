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

# Load EN CommonEvents.json (or backup VN)
with open(os.path.join(EN_DATA, "CommonEvents.json"), 'r', encoding='utf-8') as f:
    en_ce = json.load(f)

master = json.loads(json.dumps(orig_ce))

def extract_message_blocks(cmd_list):
    blocks = []
    curr = None
    for cmd in cmd_list:
        code = cmd.get('code')
        if code == 101:
            p = cmd.get('parameters', [])
            spk = p[4] if len(p) >= 5 else ''
            curr = {'cmd_101': cmd, 'speaker': spk, 'cmds_401': []}
            blocks.append(curr)
        elif code == 401 and curr is not None:
            curr['cmds_401'].append(cmd)
        elif code in [117, 355]:
            curr = None
    return blocks

total_blocks = 0
translated_401 = 0

for i in range(min(len(orig_ce), len(en_ce))):
    ev_o = orig_ce[i]
    ev_m = master[i]
    ev_e = en_ce[i]

    if not (ev_o and ev_m and ev_e and 'list' in ev_o and 'list' in ev_m and 'list' in ev_e):
        continue

    blocks_m = extract_message_blocks(ev_m['list'])
    blocks_e = extract_message_blocks(ev_e['list'])

    total_blocks += len(blocks_m)

    for b_idx in range(min(len(blocks_m), len(blocks_e))):
        bm = blocks_m[b_idx]
        be = blocks_e[b_idx]

        # Translate speaker tag
        p101 = bm['cmd_101'].get('parameters', [])
        if len(p101) >= 5 and p101[4]:
            p101[4] = translate_speaker(p101[4])

        # Map dialogue lines in block
        for l_idx in range(min(len(bm['cmds_401']), len(be['cmds_401']))):
            cmd_m = bm['cmds_401'][l_idx]
            cmd_e = be['cmds_401'][l_idx]

            p_e = cmd_e.get('parameters', [])
            if p_e and isinstance(p_e[0], str):
                cmd_m['parameters'][0] = p_e[0]
                translated_401 += 1

print(f"Aligned {total_blocks} dialogue blocks and mapped {translated_401} 401 commands!")

with open(os.path.join(DATA_VN, "CommonEvents.json"), 'w', encoding='utf-8') as f:
    json.dump(master, f, ensure_ascii=False, indent=4)

shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(PATCH_DATA, "CommonEvents.json"))
shutil.copy2(os.path.join(DATA_VN, "CommonEvents.json"), os.path.join(TEST_GAME_DATA, "CommonEvents.json"))

print("Synced master CommonEvents.json to patch-release and test game!")
