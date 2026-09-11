# CI Fix: missing tests/fixtures directory (v0.2.1)

## Symptom
CI Smoke Test failed in ~15s on push: FileNotFoundError at
scapy PcapWriter -> 'tests/fixtures/smoke_test.pcap'.

## Root cause
Git does not track empty directories, and *.pcap is gitignored, so
fresh clones (including CI runners) lacked tests/fixtures/.

## Fix (commit 6e2ea8d)
- tests/gen_fixture.py: os.makedirs("tests/fixtures", exist_ok=True)
- tests/smoke_test.sh: mkdir -p tests/fixtures

## Lesson
After heredoc pastes, always `cat` the file before committing —
half-written files were committed twice during this session.
