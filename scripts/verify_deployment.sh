#!/bin/bash
# Carter's Deployment Verification Suite
set -e
echo "--- Remote Repository Status ---"
git remote -v
echo "--- Latest Commit on Remote ---"
git ls-remote --heads origin | head -n 1
echo "--- GitHub Actions Workflow Status ---"
w3m -dump "https://github.com/bilbywilby/reverse-dns.git/actions" | grep -A 3 "Latest workflow run"
