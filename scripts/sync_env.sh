#!/bin/bash
# Carter's Env Sync - Omnipotent Default
set -e
cd ~/reverse-dns-repo

echo "[+] Updating requirements.txt to compatible version..."
cat << 'INNER' > requirements.txt
dpkt==1.9.8
dnspython==2.6.1
INNER

echo "[+] Re-provisioning virtual environment..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[+] Verifying module imports..."
python3 -c "import dpkt; import dns.resolver; print('✅ Dependencies verified for Python 3.13')"

echo "[+] Testing script execution (Smoke Test)..."
./tests/smoke_test.sh
