# Hướng dẫn Build APK Android

> Hướng dẫn này dành cho người muốn chơi game trên điện thoại Android.
> Bạn cần thực hiện các bước này trên máy tính Windows/Mac/Linux trước.

---

## Tổng quan

```
PC của bạn:
  Game gốc (mua từ DLsite)
      ↓  apply_patch.bat
  Game đã Việt hóa
      ↓  build_apk.py
  viet-hoa-thiensu.apk (~800MB)
      ↓  copy sang điện thoại
  Cài đặt trên Android ✅
```

---

## Bước 1: Chuẩn bị trên PC

### 1a. Patch game tiếng Việt trước

Chạy `apply_patch.bat` và nhập đường dẫn game. Xem README.md để biết chi tiết.

### 1b. Cài Java JDK 17

1. Vào https://adoptium.net/
2. Tải **Temurin 17** (LTS) cho hệ điều hành của bạn
3. Cài đặt, **bật "Add to PATH"** khi được hỏi
4. Kiểm tra: mở CMD → gõ `java -version` → phải hiện phiên bản

### 1c. Cài Android SDK Command-line Tools

1. Vào https://developer.android.com/studio#command-tools
2. Cuộn xuống phần **"Command line tools only"**
3. Tải file ZIP cho Windows/Mac/Linux
4. Giải nén vào: `C:\Android\Sdk\cmdline-tools\latest\` (Windows)
   - Mac/Linux: `~/Android/Sdk/cmdline-tools/latest/`
5. Mở CMD/Terminal, chạy:

```bash
# Windows
C:\Android\Sdk\cmdline-tools\latest\bin\sdkmanager "platforms;android-34" "build-tools;34.0.0"

# Mac/Linux
~/Android/Sdk/cmdline-tools/latest/bin/sdkmanager "platforms;android-34" "build-tools;34.0.0"
```

6. Gõ `y` khi được hỏi chấp nhận license

---

## Bước 2: Build APK

Mở CMD/Terminal trong thư mục patch, chạy:

```bash
# Windows
python android\build_apk.py --game-dir "C:\Games\TienSuClinic"

# Mac/Linux
python3 android/build_apk.py --game-dir "/home/user/Games/TienSuClinic"
```

Nếu không biết đường dẫn, chạy không có tham số và script sẽ hỏi:

```bash
python android\build_apk.py
```

**Lần đầu build có thể mất 5-15 phút** do tải Gradle và compile.

---

## Bước 3: Cài APK lên Android

Sau khi build xong, file APK ở: `android/output/viet-hoa-thiensu.apk`

### Cách 1: USB (nhanh nhất)

1. Kết nối điện thoại với máy tính qua USB
2. Copy file APK vào điện thoại (thư mục Download)
3. Mở File Manager trên điện thoại → Tìm file APK → Nhấn để cài

### Cách 2: Gửi qua Telegram/Discord

1. Gửi file APK cho chính mình qua Telegram (Saved Messages)
2. Mở Telegram trên điện thoại → Tải file APK
3. Nhấn file APK để cài

### Bật "Cài từ nguồn lạ" (bắt buộc)

Khi Android hỏi, chọn **"Settings"** → Bật **"Install unknown apps"** cho ứng dụng đang dùng để mở APK.

---

## Lỗi thường gặp

### "Java not found"
→ Cài JDK 17 và đảm bảo bật "Add to PATH"
→ Đóng CMD và mở lại sau khi cài

### "Android SDK not found"
→ Thêm biến môi trường:
```
ANDROID_HOME = C:\Android\Sdk
```
Windows: Tìm kiếm "Environment Variables" → System Variables → New

### Build bị lỗi "SDK Platform not found"
→ Chạy lại lệnh sdkmanager ở Bước 1c

### APK cài được nhưng game crash ngay khi mở
→ Điện thoại thiếu RAM (cần ít nhất 3GB RAM)
→ Android quá cũ (cần Android 8.0+)
→ Thử tắt bớt app nền trước khi mở game

### Game chạy nhưng không có âm thanh
→ Bình thường với một số máy lần đầu mở
→ Thoát hẳn app và mở lại
→ Nếu vẫn không có, nhấn màn hình 1 lần trước khi game load xong

---

## Lưu ý quan trọng

> ⚠️ **Save game lưu trong app!**
> Nếu bạn gỡ cài đặt APK → **MẤT SAVE VĨNH VIỄN**
> Hãy dùng tính năng Export Save (nếu game hỗ trợ) trước khi gỡ.

> ⚠️ **Không lên Play Store**
> APK này là debug-signed, chỉ dùng cá nhân, không thể upload Play Store.

---

*Cần hỗ trợ thêm? Liên hệ [link nhóm/discord của bạn]*
