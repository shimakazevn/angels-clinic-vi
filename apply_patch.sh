#!/usr/bin/env bash
# apply_patch.sh -- Ap patch Viet hoa cho Mac/Linux
# Chay: bash apply_patch.sh [duong-dan-game]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║       PATCH VIET HOA - Thien Su no Hayarou Clinic    ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Kiem tra Python
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "[LOI] Khong tim thay Python 3!"
    echo ""
    echo "Cai dat Python:"
    echo "  Mac:   brew install python3"
    echo "  Linux: sudo apt install python3  (hoac dnf/pacman tuong duong)"
    echo ""
    exit 1
fi

echo "[..] Su dung: $($PYTHON --version)"
echo ""

# Chay patcher
$PYTHON "$SCRIPT_DIR/tools/apply_patch.py" "$@"
