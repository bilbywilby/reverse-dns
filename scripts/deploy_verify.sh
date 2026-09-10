#!/bin/bash
echo "--- Repository Integrity Check ---"
ls -R ~/reverse-dns-repo
echo "--- Dependency Verification ---"
python3 -c "import dpkt; import dns.resolver; print('✅ Dependencies satisfied')" || echo "❌ Missing dependencies"
