#!/bin/bash
# Smoke test for reverse-dns analyzer
mkdir -p tests/fixtures
echo "--- Running Smoke Test ---"
python3 tests/gen_fixture.py

# Run analyzer against fixture
OUTPUT=$(python3 reverse_dns.py tests/fixtures/smoke_test.pcap)

# Validation 1: Destination IPs
if echo "$OUTPUT" | grep -q "8.8.8.8" && echo "$OUTPUT" | grep -q "1.1.1.1"; then
    echo "✅ PASS: Destination IPs identified."
else
    echo "❌ FAIL: IPs not found in output."
    exit 1
fi

# Validation 2: Aggregation (Check for 8.8.8.8: Total=2, TCP=0, UDP=2)
# We look for the IP and the specific count sequence in the same line
if echo "$OUTPUT" | grep "8.8.8.8" | grep -q "2.*0.*2"; then
    echo "✅ PASS: Protocol aggregation accurate for 8.8.8.8."
else
    echo "❌ FAIL: Aggregation error for 8.8.8.8."
    echo "DEBUG OUTPUT: $OUTPUT"
    exit 1
fi

echo "--- Smoke Test Complete ---"
