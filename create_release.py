#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_release.py — Đóng gói release đa nền tảng (PC ZIP / Android APK / iOS IPA).

Quy trình:
  1. Lấy Git commit SHA hiện tại
  2. Cập nhật Game Title trong System.json + package.json
  3. Sync data/*.json → patch/, Android assets
  4. Đóng gói Full Game PC → release_dist/ThienSuClinic-PC-<version>.zip
  5. Biên dịch Android APK  → release_dist/ThienSuClinic-Android-<version>.apk
  6. Biên dịch iOS IPA       → release_dist/ThienSuClinic-iOS-<version>.ipa

Để upload lên GitHub, dùng: python upload_github_release.py --version <version>

Cách dùng:
    python create_release.py --version v1.2.0
    python create_release.py --version v1.2.0 --skip-android --skip-ios
    python create_release.py --version v1.2.0 --dry-run
"""

import os
import re
import sys
import io
import json
import shutil
import zipfile
import subprocess
import argparse
import time
import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).resolve().parent
REPO_ROOT     = BASE_DIR                                          # patch-release is the git repo
GAME_TEST_DIR = BASE_DIR.parent / "天使の早漏治療クリニック - TEST" / "Game"
PATCH_DIR     = BASE_DIR / "patch"
ANDROID_DIR   = BASE_DIR / "android"
IOS_DIR       = BASE_DIR / "ios"
RELEASE_OUT   = BASE_DIR / "release_dist"
F_DRIVE       = Path("F:\\")                                     # Local quick-copy drive

# ─── Logger ──────────────────────────────────────────────────────────────────
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


class Logger:
    """
    Structured logger: in ra console (màu ANSI) VÀ ghi song song vào file log.
    File log tự động tạo tại: release_dist/logs/release_<timestamp>.log
    """

    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    CYAN   = "\033[96m"
    GREY   = "\033[90m"

    def __init__(self, dry_run: bool = False, log_dir: Path | None = None):
        self.dry_run  = dry_run
        self.warnings = 0
        self.errors   = 0
        self._t_start = time.time()

        # ── File log setup ──────────────────────────────────────────
        ts_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = log_dir or (RELEASE_OUT / "logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = log_dir / f"release_{ts_file}.log"
        self._log_fh  = open(self.log_path, "w", encoding="utf-8", errors="replace")
        self._log_fh.write(
            f"=== create_release.py log — {datetime.datetime.now().isoformat()} ===\n"
            f"dry_run={dry_run}\n\n"
        )
        self._log_fh.flush()
        # Print log path to console so user knows where it is
        print(f"{self.GREY}📄 Log file: {self.log_path}{self.RESET}")

    # ── Internal write ────────────────────────────────────────────────
    # Map unicode symbols → ASCII for log file readability
    _SYMBOL_MAP = str.maketrans({
        "✓": "[OK]",  "✗": "[ERR]", "⚠": "[WARN]",
        "▶": "[>]",   "·": "[-]",    "—": "--",
        "→": "->",    "═": "=",     "║": "|",
        "╔": "+",     "╗": "+",     "╚": "+",
        "╝": "+",     "─": "-",     "–": "-",
        "📄": "",     "🌸": "",
    })

    def _write(self, line: str):
        """Write ASCII-safe plain text line to log file."""
        plain = _strip_ansi(line).translate(self._SYMBOL_MAP)
        self._log_fh.write(plain + "\n")
        self._log_fh.flush()

    def _emit(self, line: str, *, err: bool = False):
        """Print to console and mirror to log file."""
        if err:
            print(line, file=sys.stderr)
        else:
            print(line)
        self._write(line)

    # ── Helpers ───────────────────────────────────────────────────────
    def _ts(self) -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")

    def _elapsed(self) -> str:
        s = int(time.time() - self._t_start)
        return f"{s // 60:02d}m{s % 60:02d}s"

    # ── Public API ────────────────────────────────────────────────────
    def header(self, title: str):
        bar = "═" * 58
        self._emit(f"")
        self._emit(f"{self.BOLD}{self.CYAN}╔{bar}╗")
        self._emit(f"║  {title:<56}║")
        self._emit(f"╚{bar}╝{self.RESET}")

    def step(self, msg: str):
        prefix = "[DRY-RUN] " if self.dry_run else ""
        self._emit(f"{self.BOLD}{self.CYAN}[{self._ts()}]{self.RESET} {self.BOLD}▶{self.RESET} {prefix}{msg}")

    def ok(self, msg: str):
        self._emit(f"{self.BOLD}{self.GREEN}[{self._ts()}]  ✓{self.RESET}  {msg}")

    def info(self, msg: str):
        self._emit(f"{self.GREY}[{self._ts()}]  ·  {msg}{self.RESET}")

    def warn(self, msg: str):
        self.warnings += 1
        self._emit(f"{self.YELLOW}[{self._ts()}]  ⚠  WARN: {msg}{self.RESET}", err=True)

    def error(self, msg: str):
        self.errors += 1
        self._emit(f"{self.RED}{self.BOLD}[{self._ts()}]  ✗  ERROR: {msg}{self.RESET}", err=True)

    def cmd(self, parts):
        display = " ".join(parts) if isinstance(parts, list) else parts
        self._emit(f"{self.GREY}[{self._ts()}]     $ {display}{self.RESET}")

    def summary(self, version: str, assets: list):
        elapsed = self._elapsed()
        bar = "─" * 58
        self._emit(f"")
        self._emit(f"{self.BOLD}{self.CYAN}{bar}{self.RESET}")
        self._emit(f"{self.BOLD}  BUILD SUMMARY  —  {version}  —  {elapsed}{self.RESET}")
        self._emit(f"{self.CYAN}{bar}{self.RESET}")
        for label, path in assets:
            if path and Path(path).exists():
                size_mb = Path(path).stat().st_size / (1024 * 1024)
                self._emit(f"  {self.GREEN}✓{self.RESET}  {label:<20} {Path(path).name}  ({size_mb:.1f} MB)")
            else:
                self._emit(f"  {self.YELLOW}–{self.RESET}  {label:<20} (skipped / not built)")
        self._emit(f"{self.CYAN}{bar}{self.RESET}")
        status_label = "OK" if self.errors == 0 else "FAILED"
        status_color = self.GREEN if self.errors == 0 else self.RED
        self._emit(
            f"  Warnings: {self.warnings}  |  Errors: {self.errors}  "
            f"|  Status: {status_color}{self.BOLD}{status_label}{self.RESET}"
        )
        self._emit(f"{self.CYAN}{bar}{self.RESET}")
        self._emit(f"")

    def close(self):
        """Flush và đóng file log. Gọi sau khi tất cả output đã xong."""
        if not self._log_fh.closed:
            elapsed = self._elapsed()
            self._log_fh.write(f"\n=== END — elapsed {elapsed} ===\n")
            self._log_fh.close()
            print(f"{self.GREY}📄 Full log saved: {self.log_path}{self.RESET}")


log: "Logger | None" = None  # initialized in main()


# ─── Helpers ─────────────────────────────────────────────────────────────────
def run(cmd: list, *, cwd=None, capture=True, timeout=300) -> tuple[bool, str, str]:
    """Run a subprocess command, return (success, stdout, stderr).
    timeout: giây tối đa chờ lệnh hoàn thành (mặc định 5 phút).
    """
    log.cmd(cmd)
    if log.dry_run:
        return True, "(dry-run)", ""
    try:
        res = subprocess.run(
            cmd, cwd=cwd,
            capture_output=capture,
            text=True, encoding="utf-8", errors="replace",
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        log.error(f"Command timed out after {timeout}s: {' '.join(cmd[:4])}")
        return False, "", "TimeoutExpired"
    if res.returncode != 0:
        log.error(f"Command exited {res.returncode}: {' '.join(cmd[:3])}…")
        if res.stderr.strip():
            for line in res.stderr.strip().splitlines()[-10:]:
                print(f"         {line}", file=sys.stderr)
        return False, res.stdout or "", res.stderr or ""
    if res.stdout.strip():
        for line in res.stdout.strip().splitlines()[-5:]:
            log.info(line)
    return True, res.stdout or "", res.stderr or ""


def git_commit_sha() -> str:
    ok, out, _ = run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT)
    return out.strip() if ok and out.strip() else "dev"


def git_current_branch() -> str:
    ok, out, _ = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO_ROOT)
    return out.strip() if ok and out.strip() else "main"


def file_size_mb(path: Path) -> str:
    if path and path.exists():
        return f"{path.stat().st_size / (1024 * 1024):.2f} MB"
    return "N/A"


# ─── Step 1: Update Game Title ───────────────────────────────────────────────
def update_game_title(version: str, commit_sha: str) -> str:
    log.header("STEP 1 — UPDATE GAME TITLE & SYNC DATA")

    base_title  = "Phòng Khám Thiên Sứ: Chuyên Trị Xuất Tinh Sớm"
    full_title  = f"{base_title} [{version}-{commit_sha}]"
    log.step(f"Game Title → '{full_title}'")

    # System.json (TEST game)
    sys_file = GAME_TEST_DIR / "data" / "System.json"
    if sys_file.exists():
        if not log.dry_run:
            data = json.loads(sys_file.read_text(encoding="utf-8"))
            data["gameTitle"] = full_title
            sys_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        log.ok(f"System.json updated: {sys_file}")
    else:
        log.warn(f"System.json not found: {sys_file}")

    # package.json (TEST game)
    pkg_file = GAME_TEST_DIR / "package.json"
    if pkg_file.exists():
        if not log.dry_run:
            pkg = json.loads(pkg_file.read_text(encoding="utf-8"))
            pkg.setdefault("window", {})["title"] = full_title
            pkg["version"] = version.lstrip("v")
            pkg_file.write_text(json.dumps(pkg, ensure_ascii=False, indent=2), encoding="utf-8")
        log.ok(f"package.json updated: {pkg_file}")
    else:
        log.warn(f"package.json not found: {pkg_file}")

    # Sync → patch/data/
    patch_data = PATCH_DIR / "data"
    patch_data.mkdir(parents=True, exist_ok=True)
    test_data  = GAME_TEST_DIR / "data"
    json_files = sorted(test_data.glob("*.json"))
    log.step(f"Sync {len(json_files)} JSON files → patch/data/")
    if not log.dry_run:
        for jf in json_files:
            shutil.copy2(jf, patch_data / jf.name)
    log.ok(f"Synced {len(json_files)} files → {patch_data}")

    # Sync → patch/package.json
    if pkg_file.exists():
        if not log.dry_run:
            shutil.copy2(pkg_file, PATCH_DIR / "package.json")
        log.ok(f"Synced package.json → {PATCH_DIR / 'package.json'}")

    # Sync → Android assets (only files that already exist there)
    android_assets = ANDROID_DIR / "template" / "app" / "src" / "main" / "assets" / "data"
    if android_assets.exists():
        synced = 0
        if not log.dry_run:
            for jf in json_files:
                dst = android_assets / jf.name
                if dst.exists():
                    shutil.copy2(jf, dst)
                    synced += 1
        log.ok(f"Synced {synced} files → Android assets ({android_assets})")
    else:
        log.info(f"Android assets dir not found, skipping: {android_assets}")

    return full_title


# ─── Step 2: Git commit ───────────────────────────────────────────────────────
def git_commit_version(version: str, commit_sha: str):
    log.header("STEP 2 — GIT COMMIT VERSION BUMP")
    branch = git_current_branch()
    log.step(f"Committing version bump on branch '{branch}'")
    run(["git", "add", "."], cwd=REPO_ROOT)
    run(["git", "commit", "--allow-empty", "-m",
         f"chore(release): bump version to {version} [{commit_sha}]"], cwd=REPO_ROOT)
    new_sha = git_commit_sha()
    log.ok(f"Committed. New SHA: {new_sha}")
    return new_sha


# ─── Step 3: PC ZIP ──────────────────────────────────────────────────────────
def build_pc_zip(version: str) -> Path | None:
    log.header("STEP 3 — PACKAGE PC FULL GAME ZIP")

    zip_name = f"ThienSuClinic-PC-{version}.zip"
    zip_path = RELEASE_OUT / zip_name
    RELEASE_OUT.mkdir(parents=True, exist_ok=True)

    if zip_path.exists():
        log.info(f"Removing existing ZIP: {zip_path.name}")
        if not log.dry_run:
            zip_path.unlink()

    root_folder = f"ThienSuClinic-PC-{version}"
    EXCLUDE_DIRS  = {"save"}
    EXCLUDE_EXTS  = {".tmp", ".bak", ".rmmzsave"}
    EXCLUDE_FILES = {"thumbs.db", ".ds_store"}

    log.step(f"Scanning game dir: {GAME_TEST_DIR}")
    all_files = []
    for root, dirs, files in os.walk(GAME_TEST_DIR):
        root_path = Path(root)
        rel_root  = root_path.relative_to(GAME_TEST_DIR)

        # Prune excluded dirs in-place
        dirs[:] = [d for d in dirs if d.lower() not in EXCLUDE_DIRS]

        for fname in files:
            # Skip unwanted files
            if fname.lower() in EXCLUDE_FILES:
                continue
            if Path(fname).suffix.lower() in EXCLUDE_EXTS:
                continue
            # Skip developer save states only inside save/
            if rel_root.parts and rel_root.parts[0] == "save" and fname.startswith("file"):
                continue
            full_p = root_path / fname
            rel_p  = full_p.relative_to(GAME_TEST_DIR)
            all_files.append((full_p, Path(root_folder) / rel_p))

    log.info(f"Total files to pack: {len(all_files)}")

    if not log.dry_run:
        t0 = time.time()
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
            for idx, (full_p, arc_p) in enumerate(all_files, 1):
                zf.write(full_p, arc_p)
                if idx % 500 == 0 or idx == len(all_files):
                    pct = idx * 100 // len(all_files)
                    log.info(f"  Packing… {idx}/{len(all_files)} ({pct}%)")
        elapsed = time.time() - t0
        log.ok(f"ZIP created: {zip_path}  [{file_size_mb(zip_path)}]  ({elapsed:.1f}s)")
    else:
        log.ok(f"[DRY-RUN] Would create: {zip_path}")

    # Quick-copy to F: drive if available
    f_dst = F_DRIVE / "ThienSuClinic-PC.zip"
    if F_DRIVE.exists() and not log.dry_run:
        shutil.copy2(zip_path, f_dst)
        log.ok(f"Copied to F: drive → {f_dst}")

    return zip_path


# ─── Step 4: Android APK ─────────────────────────────────────────────────────
def build_android_apk(version: str) -> Path | None:
    log.header("STEP 4 — BUILD ANDROID APK")

    build_script = ANDROID_DIR / "build_apk.py"
    if not build_script.exists():
        log.warn(f"build_apk.py not found: {build_script}  — skipping Android build")
        return None

    log.step(f"Running: {build_script.name}")
    ok, out, err = run(
        [sys.executable, str(build_script), "--game-dir", str(GAME_TEST_DIR)],
        cwd=ANDROID_DIR
    )
    if not ok:
        log.error("Android APK build failed.")
        return None

    src_apk = ANDROID_DIR / "output" / "viet-hoa-thiensu.apk"
    if not src_apk.exists() and not log.dry_run:
        log.error(f"APK not found after build: {src_apk}")
        return None

    dst_apk = RELEASE_OUT / f"ThienSuClinic-Android-{version}.apk"
    if not log.dry_run:
        shutil.copy2(src_apk, dst_apk)
    log.ok(f"APK ready: {dst_apk}  [{file_size_mb(dst_apk)}]")

    f_dst = F_DRIVE / "ThienSuClinic-Android.apk"
    if F_DRIVE.exists() and not log.dry_run:
        shutil.copy2(dst_apk, f_dst)
        log.ok(f"Copied to F: drive → {f_dst}")

    return dst_apk


# ─── Step 5: iOS IPA ─────────────────────────────────────────────────────────
def build_ios_ipa(version: str) -> Path | None:
    log.header("STEP 5 — BUILD iOS IPA")

    build_script = IOS_DIR / "inject_game_ios.py"
    if not build_script.exists():
        log.warn(f"inject_game_ios.py not found: {build_script}  — skipping iOS build")
        return None

    log.step(f"Running: {build_script.name}")
    ok, out, err = run(
        [sys.executable, str(build_script)],
        cwd=IOS_DIR
    )
    if not ok:
        log.error("iOS IPA build failed.")
        return None

    src_ipa = IOS_DIR / "output" / "ThienSuClinic-VietHoa.ipa"
    if not src_ipa.exists() and not log.dry_run:
        log.error(f"IPA not found after build: {src_ipa}")
        return None

    dst_ipa = RELEASE_OUT / f"ThienSuClinic-iOS-{version}.ipa"
    if not log.dry_run:
        shutil.copy2(src_ipa, dst_ipa)
    log.ok(f"IPA ready: {dst_ipa}  [{file_size_mb(dst_ipa)}]")

    f_dst = F_DRIVE / "ThienSuClinic-VietHoa.ipa"
    if F_DRIVE.exists() and not log.dry_run:
        shutil.copy2(src_ipa, f_dst)
        log.ok(f"Copied to F: drive → {f_dst}")

    return dst_ipa


# ─── Git push ────────────────────────────────────────────────────────────────
def git_push():
    log.header("STEP 6 — GIT PUSH")
    branch = git_current_branch()
    log.step(f"Pushing branch '{branch}' and tags to origin")
    run(["git", "push", "origin", branch], cwd=REPO_ROOT)
    run(["git", "push", "--tags", "origin"], cwd=REPO_ROOT)
    log.ok("Push complete.")


# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Dong goi release da nen tang (PC / Android / iOS). "
                    "Upload len GitHub: dung upload_github_release.py"
    )
    parser.add_argument("--version",       default="",    help="Phien ban release, vd: v1.2.0 (bat buoc)")
    parser.add_argument("--skip-android",  action="store_true", help="Bo qua build Android APK")
    parser.add_argument("--skip-ios",      action="store_true", help="Bo qua build iOS IPA")
    parser.add_argument("--skip-git",      action="store_true", help="Bo qua git commit va push")
    parser.add_argument("--dry-run",       action="store_true", help="Chay thu, khong thuc su ghi file")
    args = parser.parse_args()

    # ── Version: hỏi nếu không truyền ──
    version = args.version.strip()
    if not version:
        try:
            version = input("Nhap phien ban release (vi du: v1.2.0): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHuy.")
            sys.exit(0)
    if not version:
        print("[ERR] Phai nhap phien ban! Vi du: python create_release.py --version v1.2.0")
        sys.exit(1)
    if not version.startswith("v"):
        version = "v" + version

    global log
    RELEASE_OUT.mkdir(parents=True, exist_ok=True)
    log = Logger(dry_run=args.dry_run, log_dir=RELEASE_OUT / "logs")

    log.header(f"CREATE RELEASE — {version}")
    if args.dry_run:
        log.warn("DRY-RUN mode: không có file nào được ghi/thay đổi")

    commit_sha = git_commit_sha()
    log.info(f"Version    : {version}")
    log.info(f"Commit SHA : {commit_sha}")
    log.info(f"Branch     : {git_current_branch()}")
    log.info(f"Game dir   : {GAME_TEST_DIR}")
    log.info(f"Output dir : {RELEASE_OUT}")

    # ── Steps ────────────────────────────────────────────────────────────────
    update_game_title(version, commit_sha)

    if not args.skip_git:
        commit_sha = git_commit_version(version, commit_sha)

    pc_zip  = build_pc_zip(version)
    apk     = None if args.skip_android else build_android_apk(version)
    ipa     = None if args.skip_ios     else build_ios_ipa(version)

    if not args.skip_git:
        git_push()

    # ── Summary ──────────────────────────────────────────────────────────────
    log.summary(version, [
        ("PC Full Game ZIP", pc_zip),
        ("Android APK",      apk),
        ("iOS IPA",          ipa),
    ])

    if log.errors > 0:
        log.error(f"Build hoàn thành với {log.errors} lỗi. Kiểm tra output ở trên.")
        log.close()
        sys.exit(1)
    else:
        log.ok("Build thành công! Để upload lên GitHub, chạy:")
        log.info(f"    python upload_github_release.py --version {version}")
        log.close()


if __name__ == "__main__":
    main()
