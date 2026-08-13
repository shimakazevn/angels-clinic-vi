#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
import_text.py -- Đọc CSV đã dịch (9 cột) và patch ngược vào JSON của RPG Maker MZ
Game: 天使の早漏治療クリニック (RJ01644040) — Bản tiếng Nhật

Đã tích hợp:
  - Tự động dịch tên nhân vật trong Namebox (parameters[4] của code 101)
  - Tự động điều chỉnh số dòng 401 (chèn/xóa dòng khi bản dịch dài hơn/ngắn hơn)
  - Tương thích 100% với CSV 9 cột gọn nhẹ cho Google Sheets / Gemini Workspace.

Cách dùng:
    python tools/import_text.py
"""

import json
import csv
import os
import re
import shutil
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent
GAME_DIR   = ROOT_DIR / "天使の早漏治療クリニック" / "Game"
DATA_DIR   = GAME_DIR / "data"
TRANS_DIR  = ROOT_DIR / "translation"
INPUT_CSV  = TRANS_DIR / "text_export.csv"
OUTPUT_DATA_DIR = TRANS_DIR / "data_vn"

OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Bảng dịch tự động tên nhân vật ở Namebox (Code 101 params[4])
SPEAKER_NAME_MAP = {
    r"\C[4]セラ": r"\C[4]Sera",
    r"\C[5]サキュバス": r"\C[5]Succubus",
    r"\C[4]セラ（左）": r"\C[4]Sera (Trái)",
    r"\C[4]セラ（右）": r"\C[4]Sera (Phải)",
    r"\C[4]セラ（右&左）": r"\C[4]Sera (Cả hai)",
    r"\C[4]セラR&L": r"\C[4]Sera (Cả hai)",
    r"\C[4]セラ×2": r"\C[4]Sera (Cả hai)",
    r"\C[4]セラR": r"\C[4]Sera R",
    r"\C[4]セラL": r"\C[4]Sera L",
    r"\C[4]セラの声": r"\C[4]Giọng Sera",
    r"\N[5]サキュバス": r"\N[5]Succubus",
    r"\C[4]セラ\C[0]&\C[5]サキュバス": r"\C[4]Sera\C[0]&\C[5]Succubus",
    "ギルドの受付嬢": "Lễ Tân Công Hội",
    "受付嬢": "Lễ Tân Công Hội",
    "天使？": "Thiên Sứ?",
    "魔物": "Ma Vật",
    "市民A": "Dân Thường A",
    "市民B": "Dân Thường B",
    "女性の声A": "Giọng Nữ A",
    "女性の声B": "Giọng Nữ B",
    "女性の声": "Giọng Nữ",
    "通行人A": "Người Qua Đường A",
    "通行人B": "Người Qua Đường B",
    "やせ細った男": "Gã Gầy Còm",
    "ガリガリの男": "Gã Gầy Còm",
    "店員": "Nhân Viên Cửa Hàng",
    r"\c[18]※注意※": r"\c[18]※Lưu Ý※",
    r"\C[4]？？？": r"\C[4]???",
    r"\C[5]？？？": r"\C[5]???",
    "？？？": "???",
}

def translate_speaker_name(raw_speaker: str) -> str:
    if not raw_speaker:
        return raw_speaker
    if raw_speaker in SPEAKER_NAME_MAP:
        return SPEAKER_NAME_MAP[raw_speaker]
    # Thử thay thế từng thành phần nếu là chuỗi kết hợp
    s = raw_speaker
    for jp, vn in SPEAKER_NAME_MAP.items():
        if jp in s:
            s = s.replace(jp, vn)
    return s

# Các khối hội thoại gốc KHÔNG khớp được với bất kỳ row nào trong CSV
# (fail-safe: báo rõ thay vì âm thầm bỏ qua để tránh sót tiếng Nhật)
UNMATCHED_BLOCKS = []

def _record_unmatched(block_text: str, limit: int = 20):
    if len(UNMATCHED_BLOCKS) < limit:
        UNMATCHED_BLOCKS.append(block_text[:120])

# ========== Load CSV ==========

def load_translations():
    if not INPUT_CSV.exists():
        print(f"❌ Không tìm thấy: {INPUT_CSV}")
        print("   Hãy chạy export_text.py trước!")
        sys.exit(1)

    trans = defaultdict(list)
    skipped = 0
    total = 0

    with open(INPUT_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            vn = row.get("vietnamese", "").strip()
            if not vn:
                skipped += 1
                continue
            trans[row["file"]].append(row)

    translated = total - skipped
    print(f"  CSV loaded: {total} rows, {translated} đã dịch, {skipped} chưa dịch (trống)")
    return trans

# ========== Helpers ==========

def load_json(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(data, filename):
    out_path = OUTPUT_DATA_DIR / filename
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ========== Patch Simple DB ==========

def patch_simple_db(file_key, trans_rows, fields):
    filename = f"{file_key}.json"
    data = load_json(filename)
    if data is None:
        return 0

    lookup = defaultdict(dict)
    for row in trans_rows:
        lookup[str(row["entry_id"])][row["event_name"]] = row["vietnamese"]

    count = 0
    for entry in data:
        if entry is None:
            continue
        eid = str(entry.get("id", "?"))
        if eid not in lookup:
            continue
        for field in fields:
            if field in lookup[eid]:
                entry[field] = lookup[eid][field]
                count += 1

    save_json(data, filename)
    print(f"  {filename}: {count} fields patched")
    return count

# ========== Patch System ==========

def patch_system(trans_rows):
    data = load_json("System.json")
    if data is None:
        return 0

    count = 0
    for row in trans_rows:
        field = row["event_name"]
        vn = row["vietnamese"]

        if field == "gameTitle":
            data["gameTitle"] = vn
            count += 1
        elif field.startswith("terms.basic["):
            idx = int(re.search(r'\[(\d+)\]', field).group(1))
            if 0 <= idx < len(data.get("terms", {}).get("basic", [])):
                data["terms"]["basic"][idx] = vn
                count += 1
        elif field.startswith("terms.commands["):
            idx = int(re.search(r'\[(\d+)\]', field).group(1))
            if 0 <= idx < len(data.get("terms", {}).get("commands", [])):
                data["terms"]["commands"][idx] = vn
                count += 1
        elif field.startswith("terms.params["):
            idx = int(re.search(r'\[(\d+)\]', field).group(1))
            if 0 <= idx < len(data.get("terms", {}).get("params", [])):
                data["terms"]["params"][idx] = vn
                count += 1
        elif field.startswith("terms.messages."):
            key = field.split("terms.messages.")[1]
            if "messages" in data.get("terms", {}):
                data["terms"]["messages"][key] = vn
                count += 1
        elif re.match(r'armorTypes\[(\d+)\]', field):
            idx = int(re.search(r'\[(\d+)\]', field).group(1))
            if 0 <= idx < len(data.get("armorTypes", [])):
                data["armorTypes"][idx] = vn
                count += 1
        elif re.match(r'weaponTypes\[(\d+)\]', field):
            idx = int(re.search(r'\[(\d+)\]', field).group(1))
            if 0 <= idx < len(data.get("weaponTypes", [])):
                data["weaponTypes"][idx] = vn
                count += 1
        elif re.match(r'skillTypes\[(\d+)\]', field):
            idx = int(re.search(r'\[(\d+)\]', field).group(1))
            if 0 <= idx < len(data.get("skillTypes", [])):
                data["skillTypes"][idx] = vn
                count += 1
        elif re.match(r'equipTypes\[(\d+)\]', field):
            idx = int(re.search(r'\[(\d+)\]', field).group(1))
            if 0 <= idx < len(data.get("equipTypes", [])):
                data["equipTypes"][idx] = vn
                count += 1
        elif re.match(r'elements\[(\d+)\]', field):
            idx = int(re.search(r'\[(\d+)\]', field).group(1))
            if 0 <= idx < len(data.get("elements", [])):
                data["elements"][idx] = vn
                count += 1

    save_json(data, "System.json")
    print(f"  System.json: {count} fields patched")
    return count

def patch_map_infos(trans_rows):
    data = load_json("MapInfos.json")
    if data is None:
        return 0
    lookup = {str(row["entry_id"]): row["vietnamese"] for row in trans_rows if row["event_name"] == "name"}
    count = 0
    for entry in data:
        if entry is None:
            continue
        eid = str(entry.get("id", "?"))
        if eid in lookup:
            entry["name"] = lookup[eid]
            count += 1
    save_json(data, "MapInfos.json")
    print(f"  MapInfos.json: {count} fields patched")
    return count

# ========== Event Dialogue Blocks Parser ==========

def get_speaker(cmd: dict) -> str:
    params = cmd.get("parameters", [])
    if len(params) > 4 and params[4]:
        return str(params[4])
    return ""

def extract_dialogue_blocks(cmd_list: list) -> list:
    blocks = []
    i = 0
    while i < len(cmd_list):
        cmd = cmd_list[i]
        code = cmd.get("code", 0)
        params = cmd.get("parameters", [])

        if code == 101:  # Show Text header
            speaker = get_speaker(cmd)
            lines = []
            j = i + 1
            while j < len(cmd_list) and cmd_list[j].get("code") == 401:
                p = cmd_list[j].get("parameters", [])
                if p: lines.append(str(p[0]))
                j += 1
            full_text = "\n".join(lines)
            if full_text.strip():
                blocks.append({
                    "type": "dialogue",
                    "index": i,
                    "end_401_index": j,
                    "speaker_raw": speaker,
                    "text": full_text.strip(),
                    "indent": cmd.get("indent", 0)
                })
            i = j
            continue

        elif code == 102:  # Show Choices
            choices = params[0] if params else []
            if isinstance(choices, list):
                for ci, choice in enumerate(choices):
                    if choice and str(choice).strip():
                        blocks.append({
                            "type": "choice",
                            "index": i,
                            "speaker_raw": "[Choice]",
                            "text": str(choice).strip(),
                            "choice_idx": ci,
                            "indent": cmd.get("indent", 0)
                        })
        i += 1
    return blocks

def patch_event_cmd_list(cmd_list: list, rows_for_page: list) -> int:
    blocks = extract_dialogue_blocks(cmd_list)
    if not blocks:
        return 0

    # Auto-patch tất cả tên nhân vật ở Namebox (Code 101 parameters[4])
    for cmd in cmd_list:
        if cmd.get("code") == 101:
            params = cmd.get("parameters", [])
            if len(params) > 4 and params[4]:
                orig_sp = str(params[4])
                trans_sp = translate_speaker_name(orig_sp)
                if trans_sp != orig_sp:
                    params[4] = trans_sp

    if not rows_for_page:
        return 0

    row_idx = 0
    count = 0
    cmd_offset = 0

    for block in blocks:
        if row_idx >= len(rows_for_page):
            _record_unmatched(block["text"])
            break

        row = rows_for_page[row_idx]
        row_jp = row["original_jp"].strip()
        vn_text = row["vietnamese"].strip()

        if block["text"] != row_jp:
            matched_idx = -1
            for search_i in range(row_idx, min(row_idx + 5, len(rows_for_page))):
                if rows_for_page[search_i]["original_jp"].strip() == block["text"]:
                    matched_idx = search_i
                    break
            if matched_idx != -1:
                row_idx = matched_idx
                row = rows_for_page[row_idx]
                vn_text = row["vietnamese"].strip()
            else:
                _record_unmatched(block["text"])
                continue

        row_idx += 1

        if not vn_text:
            continue

        cmd_idx = block["index"] + cmd_offset

        if block["type"] == "dialogue":
            vn_lines = vn_text.split("\n")

            j = cmd_idx + 1
            old_401_indices = []
            while j < len(cmd_list) and cmd_list[j].get("code") == 401:
                old_401_indices.append(j)
                j += 1

            old_count = len(old_401_indices)
            new_count = len(vn_lines)
            indent = block.get("indent", 0)

            min_len = min(old_count, new_count)
            for k in range(min_len):
                idx = old_401_indices[k]
                cmd_list[idx]["parameters"] = [vn_lines[k]]

            if new_count > old_count:
                insert_pos = old_401_indices[-1] + 1 if old_401_indices else cmd_idx + 1
                new_cmds = []
                for k in range(old_count, new_count):
                    new_cmds.append({"code": 401, "indent": indent, "parameters": [vn_lines[k]]})
                cmd_list[insert_pos:insert_pos] = new_cmds
                cmd_offset += (new_count - old_count)

            elif old_count > new_count:
                remove_start = old_401_indices[new_count]
                remove_end = old_401_indices[-1] + 1
                del cmd_list[remove_start:remove_end]
                cmd_offset -= (old_count - new_count)

            count += 1

        elif block["type"] == "choice":
            ci = block["choice_idx"]
            cmd = cmd_list[cmd_idx]
            if cmd.get("code") == 102 and cmd.get("parameters"):
                choices_list = cmd["parameters"][0]
                if isinstance(choices_list, list) and ci < len(choices_list):
                    choices_list[ci] = vn_text
                    count += 1

    return count

# ========== Patch Events ==========

def parse_page_idx(event_name: str) -> int:
    m = re.search(r'\[p(\d+)\]$', event_name)
    return int(m.group(1)) if m else 0

def patch_common_events(trans_rows):
    filename = "CommonEvents.json"
    data = load_json(filename)
    if data is None:
        return 0

    by_entry = defaultdict(list)
    for row in trans_rows:
        by_entry[str(row["entry_id"])].append(row)

    total = 0
    for entry in data:
        if entry is None:
            continue
        eid = str(entry.get("id", "?"))
        cmd_list = entry.get("list", [])
        entry_rows = by_entry.get(eid, [])
        n = patch_event_cmd_list(cmd_list, entry_rows)
        total += n

    save_json(data, filename)
    print(f"  {filename}: {total} dialogues/choices patched (Nameboxes auto-translated)")
    return total

def patch_map(file_key, trans_rows):
    filename = f"{file_key}.json"
    data = load_json(filename)
    if data is None:
        return 0

    by_entry = defaultdict(list)
    for row in trans_rows:
        by_entry[str(row["entry_id"])].append(row)

    total = 0
    events = data.get("events", [])
    for event in events:
        if event is None:
            continue
        eid = str(event.get("id", "?"))
        pages = event.get("pages", [])
        entry_rows = by_entry.get(eid, [])

        by_page = defaultdict(list)
        for r in entry_rows:
            p_idx = parse_page_idx(r["event_name"])
            by_page[p_idx].append(r)

        for page_idx, page in enumerate(pages):
            if not page:
                continue
            cmd_list = page.get("list", [])
            n = patch_event_cmd_list(cmd_list, by_page[page_idx])
            total += n

    save_json(data, filename)
    return total

# ========== Main ==========

def main():
    print("=" * 60)
    print("RPG Maker MZ — Import Translations from CSV (9 columns)")
    print(f"Input CSV: {INPUT_CSV}")
    print(f"Output:    {OUTPUT_DATA_DIR}")
    print("=" * 60)

    trans = load_translations()

    print(f"\n[1] Patch database files...")
    patch_simple_db("Actors", trans.get("Actors", []), ["name", "nickname", "profile"])
    patch_simple_db("Items", trans.get("Items", []), ["name", "description"])
    patch_simple_db("Weapons", trans.get("Weapons", []), ["name", "description"])
    patch_simple_db("Armors", trans.get("Armors", []), ["name", "description"])
    patch_simple_db("Enemies", trans.get("Enemies", []), ["name"])
    patch_simple_db("Classes", trans.get("Classes", []), ["name"])
    patch_simple_db("Skills", trans.get("Skills", []), ["name", "description", "message1", "message2"])
    patch_simple_db("States", trans.get("States", []), ["name", "message1", "message2", "message3", "message4"])
    patch_system(trans.get("System", []))
    patch_map_infos(trans.get("MapInfos", []))

    print(f"\n[2] Patch CommonEvents...")
    patch_common_events(trans.get("CommonEvents", []))

    print(f"\n[3] Patch Map files...")
    map_total = 0
    map_files = sorted(DATA_DIR.glob("Map[0-9]*.json"))
    for mf in map_files:
        if mf.name == "MapInfos.json":
            continue
        file_key = mf.name.replace(".json", "")
        rows = trans.get(file_key, [])
        n = patch_map(file_key, rows)
        if n > 0:
            print(f"  {mf.name}: {n} dialogues/choices patched")
        map_total += n
    print(f"  Maps total: {map_total} dialogues/choices patched")

    print(f"\n✅ Xong! Kết quả tại: {OUTPUT_DATA_DIR}")

    if UNMATCHED_BLOCKS:
        print(f"\n⚠️  Có {len(UNMATCHED_BLOCKS)}+ khối hội thoại gốc KHÔNG khớp row CSV (sẽ còn tiếng Nhật):")
        for b in UNMATCHED_BLOCKS:
            print(f"  - {b!r}")
    else:
        print("\n✅ Toàn bộ khối hội thoại gốc đều khớp row CSV (không bỏ sót tiếng Nhật).")

if __name__ == "__main__":
    main()
