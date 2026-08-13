#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
import_logtext.py -- Import battle log (LogMessage, code 357) + choice prompts
(LL_GalgeChoiceWindow showChoice, code 357) từ CSV vào data_vn.

Nguồn CSV:
  - translation/logtext.csv      (battle log, 2 cột: original_jp, vietnamese)
  - translation/galge_choice.csv (choice prompts, 2 cột: original_jp, vietnamese)

Cách dùng:
    python tools/import_logtext.py
"""
import json
import csv
import os
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent
TRANS_DIR  = ROOT_DIR / "translation"
DATA_VN    = TRANS_DIR / "data_vn"
LOGTEXT_CSV  = TRANS_DIR / "logtext_new.csv" if (TRANS_DIR / "logtext_new.csv").exists() else TRANS_DIR / "logtext.csv"
GALGE_CSV    = TRANS_DIR / "galge_choice.csv"


def load_lut(csv_path):
    """{original_jp: vietnamese}. Key được strip để khớp lookup; value giữ nguyên
    whitespace (vd trailing \\n của messageText GalgeChoice)."""
    lut = {}
    if not csv_path.exists():
        return lut
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= 2 and row[1].strip():
                lut[row[0].strip()] = row[1]
    return lut


def walk_cmd_lists(data):
    """Trả về generator các (cmd_list, cmd) cho code 357."""
    containers = data.get("events") if isinstance(data, dict) else data
    if containers is None:
        return
    for ev in containers:
        if ev is None:
            continue
        if isinstance(ev, dict):
            pages = ev.get("pages")
            if pages:
                for page in pages:
                    if page:
                        cmd_list = page.get("list", [])
                        for cmd in cmd_list:
                            yield cmd_list, cmd
            elif isinstance(ev.get("list"), list):
                cmd_list = ev["list"]
                for cmd in cmd_list:
                    yield cmd_list, cmd
        elif isinstance(ev, list):
            for cmd in ev:
                yield ev, cmd


def patch_logmessage(data, lut):
    count = 0
    for cmd_list, cmd in walk_cmd_lists(data):
        if cmd.get("code") != 357:
            continue
        p = cmd.get("parameters", [])
        if not p or p[0] != "LogMessage" or len(p) <= 3 or not isinstance(p[3], dict):
            continue
        raw = str(p[3].get("text", ""))
        lead = raw[: len(raw) - len(raw.lstrip())]
        t = raw.strip()
        if t and t in lut:
            p[3]["text"] = lead + lut[t]
            count += 1
    return count


def rebuild_choices(choices_raw, lut):
    """Dịch nhãn choice bên trong JSON string của LL_GalgeChoiceWindow."""
    try:
        choices = json.loads(choices_raw or "[]")
    except Exception:
        return choices_raw
    if not isinstance(choices, list):
        return choices_raw
    changed = False
    rebuilt = []
    for elm in choices:
        try:
            d = json.loads(elm)
        except Exception:
            rebuilt.append(elm)
            continue
        if isinstance(d, dict) and str(d.get("label", "")).strip() in lut:
            d["label"] = lut[str(d["label"]).strip()]
            changed = True
            elm = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
        rebuilt.append(elm)
    if not changed:
        return choices_raw
    return json.dumps(rebuilt, ensure_ascii=False, separators=(",", ":"))


def patch_galge(data, lut):
    count = 0
    for cmd_list, cmd in walk_cmd_lists(data):
        if cmd.get("code") != 357:
            continue
        p = cmd.get("parameters", [])
        if not p or p[0] != "LL_GalgeChoiceWindow" or len(p) <= 3 or not isinstance(p[3], dict):
            continue
        mt = str(p[3].get("messageText", "")).strip()
        if mt and mt in lut:
            p[3]["messageText"] = lut[mt]
            count += 1
        cr = p[3].get("choices", "")
        if cr:
            rebuilt = rebuild_choices(cr, lut)
            if rebuilt != cr:
                p[3]["choices"] = rebuilt
                count += 1
    return count


def patch_657(data, lut):
    """Dịch các command code-657 (bản mirror editor: テキスト = <text>, 質問メッセージ/選択肢リスト)."""
    count = 0
    for cmd_list, cmd in walk_cmd_lists(data):
        if cmd.get("code") != 657:
            continue
        p = cmd.get("parameters", [])
        if not p or not isinstance(p[0], str):
            continue
        s = p[0].strip()
        if s in lut:
            p[0] = lut[s]
            count += 1
        elif " = " in s:
            key, val = s.split(" = ", 1)
            lead = val[: len(val) - len(val.lstrip())]
            if val.strip() in lut:
                p[0] = key + " = " + lead + lut[val.strip()]
                count += 1
    return count


def save_json(data, filename):
    out_path = DATA_VN / filename
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    print("=" * 60)
    print("Import battle log (LogMessage) + Choice prompts (GalgeChoice)")
    print("=" * 60)

    log_lut = load_lut(LOGTEXT_CSV)
    galge_lut = load_lut(GALGE_CSV)
    print(f"  logtext LUT: {len(log_lut)} entries ({LOGTEXT_CSV.name})")
    print(f"  galge LUT:   {len(galge_lut)} entries")

    total_log = 0
    total_galge = 0
    total_657 = 0

    # CommonEvents
    ce_fp = DATA_VN / "CommonEvents.json"
    if ce_fp.exists():
        with open(ce_fp, encoding="utf-8") as f:
            data = json.load(f)
        n = patch_logmessage(data, log_lut)
        m = patch_galge(data, galge_lut)
        k = patch_657(data, galge_lut) + patch_657(data, log_lut)
        save_json(data, "CommonEvents.json")
        total_log += n
        total_galge += m
        total_657 += k
        print(f"  CommonEvents.json: LogMessage {n}, GalgeChoice {m}, code-657 {k}")

    # Maps
    for mf in sorted(DATA_VN.glob("Map[0-9]*.json")):
        if mf.name == "MapInfos.json":
            continue
        with open(mf, encoding="utf-8") as f:
            data = json.load(f)
        n = patch_logmessage(data, log_lut)
        m = patch_galge(data, galge_lut)
        k = patch_657(data, galge_lut) + patch_657(data, log_lut)
        if n or m or k:
            save_json(data, mf.name)
            print(f"  {mf.name}: LogMessage {n}, GalgeChoice {m}, code-657 {k}")
        total_log += n
        total_galge += m
        total_657 += k

    print(f"\nXong! LogMessage patched: {total_log}, GalgeChoice patched: {total_galge}, code-657 patched: {total_657}")


if __name__ == "__main__":
    main()
