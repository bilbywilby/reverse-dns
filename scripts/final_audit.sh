#!/bin/bash
# Carter's Final Audit Suite
set -e
echo "--- Repository Status ---"
git status --short
echo "--- Latest Commit on Remote ---"
git ls-remote --heads origin | head -n 1
echo "--- GitHub Actions Workflow Status ---"
gh run list --repo bilbywilby/reverse-dns --limit 5 || curl -s https://api.github.com/repos/bilbywilby/reverse-dns/actions/runs | grep -E '"status"|"conclusion"|"display_title"'
echo "--- Repository Visibility ---"
w3m -dump "https://github.com/bilbywilby/reverse-dns" | grep -E "Latest commit|branches|tags"
