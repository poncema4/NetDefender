#!/usr/bin/env bash
set -euo pipefail

# NetDefender local setup for Linux/macOS-like shells.
# Core development does not require VMware, Kali, Metasploitable, or tshark.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

printf '\n== NetDefender setup ==\n'
printf 'Repository: %s\n\n' "$ROOT_DIR"

find_python() {
    local candidate
    for candidate in python3 python; do
        if command -v "$candidate" >/dev/null 2>&1; then
            if "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1; then
                printf '%s' "$candidate"
                return 0
            fi
        fi
    done
    return 1
}

if ! PYTHON_BIN="$(find_python)"; then
    echo "ERROR: Python 3.11+ is required but was not found." >&2
    exit 1
fi

"$PYTHON_BIN" --version

if [[ ! -d .venv ]]; then
    echo "Creating .venv..."
    "$PYTHON_BIN" -m venv .venv
fi

VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
if [[ ! -x "$VENV_PYTHON" ]]; then
    echo "ERROR: expected virtual-environment Python at $VENV_PYTHON" >&2
    exit 1
fi

echo "Upgrading pip..."
"$VENV_PYTHON" -m pip install --upgrade pip

echo "Installing NetDefender and test dependencies..."
"$VENV_PYTHON" -m pip install -e '.[test]'

echo "Running complete automated test suite..."
"$VENV_PYTHON" -m pytest

echo "Running deterministic CLI smoke test..."
"$VENV_PYTHON" -m netdefender.cli data/samples/syn-scan.json --html local-report.html

if [[ ! -s local-report.html ]]; then
    echo "ERROR: CLI completed but local-report.html was not created or is empty." >&2
    exit 1
fi

echo "Checking optional tshark availability..."
if command -v tshark >/dev/null 2>&1; then
    tshark --version | head -n 1
    echo "tshark: available"
else
    echo "tshark: not installed (optional until real PCAP analysis)"
fi

echo
cat <<'EOF'
Setup complete.

Activate the environment with:
  source .venv/bin/activate

Run tests with:
  python -m pytest

Run the sample with:
  python -m netdefender.cli data/samples/syn-scan.json --html local-report.html
EOF
