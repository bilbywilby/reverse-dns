#!/bin/bash
# Carter's Live Repository Auditor
REPO_URL="https://github.com/bilbywilby/reverse-dns"
echo "[+] Auditing Remote State..."
w3m -dump "$REPO_URL" | grep -E "Latest commit|README.md|LICENSE"
echo "[+] Checking CI Workflow Trigger..."
w3m -dump "$REPO_URL/actions" | grep -E "CI Smoke Test|success|failure|in progress"
