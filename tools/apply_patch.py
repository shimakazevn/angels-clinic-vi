#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
apply_patch.py -- Áp patch Việt hóa vào game RPG Maker MZ
Game: 天使の早漏治療クリニック (RJ01644040)

Cách dùng:
    Windows : double-click apply_patch.bat  (hoặc: python tools/apply_patch.py)
    Mac/Linux: bash tools/apply_patch.sh    (hoặc: python3 tools/apply_patch.py)
"""

import os
import shutil
import json
import platform
from pathlib import Path

# Màu sắc console
if platform.system() == "Windows":
    import ctypes
    ctypes.windll.kernel32.SetConsoleMode(
        ctypes.windll.kernel32.GetStdHandle(-11), 7
    )

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

BANNER = f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════╗
║       PATCH VIỆT HÓA - Thiên Sứ Clinic               ║
╚══════════════════════════════════════════════════════╝{RESET}
"""

# ---- Cấu hình đường dẫn ----
SCRIPT_DIR  = Path(__file__).resolve().parent
ROOT_DIR    = SCRIPT_DIR.parent
PATCH_DIR   = ROOT_DIR / "patch"
PATCH_DATA  = PATCH_DIR / "data"
PATCH_IMG   = PATCH_DIR / "img"
PATCH_JS    = PATCH_DIR / "js"

# ========== Helpers ==========

def ok(msg):    print(f"  {GREEN}[OK]{RESET} {msg}")
def warn(msg):  print(f"  {YELLOW}[!!]{RESET} {msg}")
def err(msg):   print(f"  {RED}[XX]{RESET} {msg}")
def info(msg):  print(f"  {CYAN}[..]{RESET} {msg}")
def header(msg): print(f"\n{BOLD}{msg}{RESET}")

def is_rmmz_game(folder: Path) -> bool:
    """Kiểm tra đây có phải game RPG Maker MZ không."""
    checks = [
        folder / "data" / "System.json",
        folder / "js" / "rmmz_core.js",
        folder / "index.html",
    ]
    return all(c.exists() for c in checks)

def validate_game_title(folder: Path, expected_id="80563259") -> bool:
    """Kiểm tra đúng game (qua gameId trong System.json)."""
    system_json = folder / "data" / "System.json"
    try:
        with open(system_json, encoding="utf-8") as f:
            data = json.load(f)
        game_id = str(data.get("advanced", {}).get("gameId", ""))
        return game_id == expected_id
    except Exception:
        return False

def backup_file(src: Path) -> Path:
    """Tạo file backup .bak nếu chưa có."""
    backup = src.with_suffix(".bak" + src.suffix)
    if not backup.exists():
        shutil.copy2(src, backup)
    return backup

def copy_patch_tree(src_dir: Path, dst_dir: Path) -> tuple[int, int]:
    """Copy toàn bộ cây thư mục patch -> game. Trả về (số file copy, số file lỗi)."""
    copied = 0
    errors = 0
    for src_file in src_dir.rglob("*"):
        if not src_file.is_file():
            continue
        rel = src_file.relative_to(src_dir)
        dst_file = dst_dir / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            if dst_file.exists():
                backup_file(dst_file)
            shutil.copy2(src_file, dst_file)
            copied += 1
        except Exception as e:
            err(f"Lỗi copy {rel}: {e}")
            errors += 1
    return copied, errors

def ask_game_folder() -> Path:
    """Hỏi đường dẫn thư mục game từ user."""
    header("BƯỚC 1: Chọn thư mục game")
    print(f"  Nhập đường dẫn đến thư mục game (nơi có file Game.exe).")
    print(f"  Ví dụ: C:\\Games\\TienSuClinic")
    print()

    while True:
        try:
            raw = input(f"  {BOLD}Đường dẫn:{RESET} ").strip().strip('"').strip("'")
        except (EOFError, KeyboardInterrupt):
            print()
            err("Đã hủy.")
            sys.exit(0)

        if not raw:
            warn("Vui lòng nhập đường dẫn.")
            continue

        folder = Path(raw)
        if not folder.exists():
            err(f"Không tìm thấy thư mục: {folder}")
            continue
        if not folder.is_dir():
            err("Đây không phải thư mục.")
            continue
        if not is_rmmz_game(folder):
            err("Không phát hiện game RPG Maker MZ trong thư mục này.")
            warn("Hãy chọn thư mục chứa file Game.exe, index.html và thư mục data/.")
            continue

        return folder

# ========== Main ==========

def main():
    print(BANNER)

    # -- Kiểm tra patch tồn tại --
    if not PATCH_DATA.exists() and not PATCH_IMG.exists() and not PATCH_JS.exists():
        err("Không tìm thấy thư mục patch/")
        err(f"Hãy đảm bảo patch/ nằm cùng cấp với script này: {ROOT_DIR}")
        sys.exit(1)

    # -- Chọn thư mục game --
    if len(sys.argv) > 1:
        game_dir = Path(sys.argv[1])
        if not is_rmmz_game(game_dir):
            err(f"Thư mục không hợp lệ: {game_dir}")
            sys.exit(1)
        info(f"Sử dụng thư mục game từ tham số: {game_dir}")
    else:
        game_dir = ask_game_folder()

    header("BƯỚC 2: Kiểm tra game")

    if validate_game_title(game_dir):
        ok("Xác nhận đúng game: Thiên Sứ no Hayarou Clinic (RJ01644040)")
    else:
        warn("Không xác nhận được game ID (có thể là phiên bản khác hoặc game đã bị chỉnh sửa)")
        warn("Patch vẫn sẽ được áp dụng, nhưng có thể có lỗi.")

    already_patched = (game_dir / "data" / "System.bak.json").exists()
    if already_patched:
        warn("Phát hiện bản patch cũ! File backup đã tồn tại.")
        warn("Patch này sẽ GHI ĐÈ lên bản dịch cũ.")
        try:
            confirm = input("  Tiếp tục? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        if confirm != "y":
            info("Đã hủy.")
            sys.exit(0)

    header("BƯỚC 3: Áp dụng patch")

    total_copied = 0
    total_errors = 0

    # -- Patch data/ (JSON) --
    if PATCH_DATA.exists():
        info(f"Đang patch {len(list(PATCH_DATA.rglob('*.json')))} file JSON...")
        n, e = copy_patch_tree(PATCH_DATA, game_dir / "data")
        ok(f"Đã patch {n} file JSON")
        total_copied += n
        total_errors += e
    else:
        warn("Không tìm thấy patch/data/ -- bỏ qua patch text")

    # -- Patch img/ (ảnh UI) --
    if PATCH_IMG.exists():
        img_count = len(list(PATCH_IMG.rglob("*.png")))
        info(f"Đang patch {img_count} ảnh UI...")
        n, e = copy_patch_tree(PATCH_IMG, game_dir / "img")
        ok(f"Đã patch {n} ảnh UI")
        total_copied += n
        total_errors += e
    else:
        warn("Không tìm thấy patch/img/ -- bỏ qua patch ảnh")

    # -- Patch js/ (plugin text / plugins.js) --
    if PATCH_JS.exists():
        js_count = len(list(PATCH_JS.rglob("*.js")))
        info(f"Đang patch {js_count} file plugin JS...")
        n, e = copy_patch_tree(PATCH_JS, game_dir / "js")
        ok(f"Đã patch {n} file plugin JS")
        total_copied += n
        total_errors += e

    # -- Patch index.html & package.json --
    patch_index = PATCH_DIR / "index.html"
    if patch_index.exists():
        backup_file(game_dir / "index.html")
        shutil.copy2(patch_index, game_dir / "index.html")
        ok("Đã patch index.html")
        total_copied += 1

    patch_pkg = PATCH_DIR / "package.json"
    if patch_pkg.exists():
        backup_file(game_dir / "package.json")
        shutil.copy2(patch_pkg, game_dir / "package.json")
        ok("Đã patch package.json")
        total_copied += 1

    # -- Kết quả --
    header("BƯỚC 4: Kết quả")
    print()
    print(f"  {GREEN}{BOLD}PATCH THÀNH CÔNG!{RESET}")
    print(f"  Tổng file đã patch: {total_copied}")
    if total_errors:
        warn(f"  Có {total_errors} lỗi (xem phía trên để biết chi tiết)")
    print()
    print(f"  {BOLD}Để chơi:{RESET} Mở thư mục game và chạy Game.exe")
    print(f"  {BOLD}Để hoàn tác:{RESET} Đổi tên các file .bak trong game/ về tên cũ")
    print()

    if platform.system() == "Windows":
        input("  Nhấn Enter để thoát...")

if __name__ == "__main__":
    main()
