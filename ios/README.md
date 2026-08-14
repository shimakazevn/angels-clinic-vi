# Hướng Dẫn Build & Đóng Gói Game Cho iOS (.IPA)

Quy trình tạo file `.ipa` hoàn chỉnh cho iPhone / iPad áp dụng kiến trúc **Vỏ App (Shell) + Tiêm Dữ Liệu (Injection)**.

---

## 1. Tải Vỏ Ứng Dụng (Shell IPA) Từ GitHub Actions
1. Vào repository trên GitHub: `https://github.com/shimakazevn/angels-clinic-vi`
2. Chuyển sang tab **Actions** ➔ Chọn workflow **Build iOS Shell (.IPA)**.
3. Chọn bản chạy mới nhất (hoặc bấm nút **Run workflow** trên nhánh `ios-build`).
4. Trong mục **Artifacts** ở dưới cùng trang kết quả build, tải file **`ThienSuClinic-shell-ipa.zip`** về.
5. Giải nén được file `ThienSuClinic-shell.ipa` (~3 MB).

---

## 2. Tiêm Dữ Liệu Game Cục Bộ (Tạo File IPA Hoàn Chỉnh)
1. Copy file `ThienSuClinic-shell.ipa` vào thư mục `ios/` này.
2. Chạy file **`TIEM_GAME_IOS.bat`** (trên Windows) hoặc gõ lệnh:
   ```bash
   python inject_game_ios.py
   ```
3. Script sẽ tự động:
   - Đọc dữ liệu game Việt hóa từ thư mục `Game/` (~700 MB).
   - Tối ưu hóa file mã nguồn cho iOS WebKit (WebGL, Fullscreen viewport-fit=cover, WebAudio unlock).
   - Bơm toàn bộ dữ liệu vào `Payload/ThienSuClinic.app/www/`.
   - Xuất file IPA hoàn chỉnh tại: **`ios/output/ThienSuClinic-VietHoa.ipa`**.

---

## 3. Cài Đặt Lên iPhone / iPad
Sử dụng một trong các công cụ sideload phổ biến sau:
- **Sideloadly** (Windows / macOS - Miễn phí): Cắm cáp USB, kéo thả file `ThienSuClinic-VietHoa.ipa` vào, nhập Apple ID và bấm **Start**.
- **AltStore / Scarlet / TrollStore / LiveContainer / ESign**: Cài đặt trực tiếp file `.ipa` vào máy không cần máy tính (nếu máy hỗ trợ TrollStore / LiveContainer).
