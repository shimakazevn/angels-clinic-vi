import os
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r"e:\天使の早漏治療クリニック - RJ01644040")
JP_GAME = ROOT / "天使の早漏治療クリニック"
VN_GAME = ROOT / "Tenshi_no_Hayarou_Clinic_VN"
PATCH_DIR = ROOT / "patch-release" / "patch"
DELETE_GAME = ROOT / "DELETE" / "Game"

print("=================================================================")
print("TẠO THƯ MỤC GAME TIẾNG VIỆT RIÊNG (GIỮ NGUYÊN GAME GỐC 100%)")
print("=================================================================")

# Ensure JP_GAME is pristine
if not (JP_GAME / "Game" / "Game.exe").exists() and not (JP_GAME / "Game.exe").exists():
    print("🚀 Restoring pristine Japanese game from DELETE/Game...")
    shutil.copytree(DELETE_GAME, JP_GAME, dirs_exist_ok=True)

# Copy JP_GAME to VN_GAME
print("🚀 Đang sao chép toàn bộ game gốc sang Tenshi_no_Hayarou_Clinic_VN...")
shutil.copytree(JP_GAME, VN_GAME, dirs_exist_ok=True)
print("✅ Đã sao chép game gốc thành công!")

game_sub = VN_GAME / "Game" if (VN_GAME / "Game").exists() else VN_GAME

# Apply ONLY from patch-release/patch/
print("📦 Đang áp dụng Master Patch từ patch-release/patch/...")

if (PATCH_DIR / "data").exists():
    shutil.copytree(PATCH_DIR / "data", game_sub / "data", dirs_exist_ok=True)
    print("   + [Patch Data] Applied 58 JSON dialog & database files")

if (PATCH_DIR / "js").exists():
    shutil.copytree(PATCH_DIR / "js", game_sub / "js", dirs_exist_ok=True)
    print("   + [Patch JS] Applied plugins.js & custom plugins")

if (PATCH_DIR / "img").exists():
    shutil.copytree(PATCH_DIR / "img", game_sub / "img", dirs_exist_ok=True)
    print("   + [Patch Image] Applied UI images")

print("=================================================================")
print("🎉 HOÀN THÀNH PATCH GAME TIẾNG VIỆT RIÊNG!")
print(f"📍 Game Việt Hóa: {VN_GAME}")
print(f"🛡️ Thư mục game gốc ({JP_GAME.name}) giữ nguyên 100% thuần Nhật!")
print("=================================================================")
