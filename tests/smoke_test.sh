#!/bin/bash
# Smoke test for reverse-dns analyzer
echo "--- Running Smoke Test ---"
python3 tests/gen_fixture.py

# Run analyzer against fixture
OUTPUT=$(python3 reverse_dns.py tests/fixtures/smoke_test.pcap)

# Validation Logic
if echo "$OUTPUT" | grep -q "8.8.8.8" && echo "$OUTPUT" | grep -q "1.1.1.1"; then
    echo "✅ PASS: Destination IPs identified."
else
    echo "❌ FAIL: IPs not found in output."
    exit 1
fi

if echo "$OUTPUT" | grep -q "Total.*2" && echo "$OUTPUT" | grep -q "UDP.*2"; then
    echo "✅ PASS: Protocol aggregation accurate."
else
    echo "❌ FAIL: Aggregation error."
    exit 1
fi

echo "--- Smoke Test Complete ---"
