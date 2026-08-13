# BUILD GUIDE — Pipeline chuẩn tái tạo Patch (sau refactor 2026-08-12)

> Quy tắc VÀNG: **CSV = nguồn sự thật duy nhất.** Mọi sửa bản dịch chỉ sửa trong
> `translation/text_export.csv`, sau đó chạy lại pipeline từ đầu. KHÔNG sửa tay
> vào file JSON trong `translation/data_vn` / `patch-release/patch/data`.

## Kiến trúc

```
 game gốc JP (PRISTINE)   +   translation/text_export.csv (bản dịch chuẩn)
              │                           │
              └───────────► import_text.py ◄───────────┘
                              │
                              ▼
                    translation/data_vn   (TÁI SINH SẠCH, không sửa tay)
                              │
              ┌───────────────┴────────────────┐
              ▼                                 ▼
   sync_all_to_patch.py                 build_vietnamese_game.py
              ▼                                 ▼
   patch-release/patch/data      Tenshi_no_Hayarou_Clinic_VN/Game (game thử nghiệm)
```

## Các bước chuẩn (chạy từ thư mục gốc `E:\...RJ01644040`)

### 1. Kiểm tra game gốc còn PRISTINE
```bash
# Không được có file .bak trong game/data
Get-ChildItem "天使の早漏治療クリニック\Game\data" -Filter *.bak*
# gameTitle phải là 天使の早漏治療クリニック
python -c "import json;print(json.load(open(r'天使の早漏治療クリニック\Game\data\System.json',encoding='utf-8'))['gameTitle'])"
```

### 2. Sửa bản dịch (chỉ trong CSV)
- `translation/text_export.csv` — hội thoại & database.
- `translation/plugin_text.csv` — text plugin JS.
- Sau khi sửa CSV: chạy kiểm tra (0 dòng trống, 0 chữ Nhật trong cột `vietnamese`).

### 3. Tái sinh JSON từ đầu
```bash
# XÓA sạch data_vn cũ rồi import lại từ game gốc
Remove-Item translation\data_vn\*.json
python tools/import_text.py
```
> Script tự báo nếu có khối hội thoại gốc không khớp row CSV (fail-safe).

### 4. Đồng bộ vào patch + game thử
```bash
python tools/build_vietnamese_game.py    # tạo lại game thử nghiệm từ game gốc
python tools/sync_all_to_patch.py        # data_vn -> patch/data + game thử + AutoWordWrap.js
```

### 5. Kiểm soát chất lượng (bắt buộc)
```bash
python tools/full_translation_status.py          # kỳ vọng: 100% dịch, 0 trống, 0 Nhật
python tools/scan_all_game_data_for_japanese.py  # kỳ vọng: 0 file còn Nhật
python tools/verify_structure_vs_jp.py           # chênh cmd count là BÌNH THƯỜNG (do điều chỉnh số dòng 401)
```
> `verify_structure_vs_jp.py` báo "cmd count X vs Y" là hiển thị số dòng hội thoại
> 401 thay đổi để khớp độ dài bản dịch — **đúng bản chất, không phải lỗi cấu trúc**.
> Kiểm tra cấu trúc CHUẨN xác (gom 101+N×401 thành 1 khối) phải ra 0 lỗi.

### 6. Đóng gói phát hành
- Copy nguyên `patch-release/` → nén zip → giao cho người chơi.
- Android: `python patch-release/android/build_apk.py --game-dir "C:\path\to\game"`.

## Vòng đời sửa đổi an toàn
1. Sửa CSV → commit git (message rõ).
2. Rebuild (bước 3–4) → audit (bước 5) → commit kết quả.
3. Nếu sai: `git revert` hoặc sửa CSV rồi rebuild lại — không bao giờ sửa JSON tay.

## Cấm kỵ (nguyên nhân gây hỏng patch trước đây)
- ❌ Sửa trực tiếp JSON trong data_vn / patch/data / game thử.
- ❌ Đổ chuỗi rỗng `""` vào dòng 401 "thừa" (dùng import_text để xóa đúng cách).
- ❌ Chạy nhiều script translate chồng chéo lên cùng file.
- ❌ Mất backup → luôn commit git trước khi thay đổi lớn.
