# reverse-dns

A high-performance CLI utility for analyzing PCAP/PCAPNG captures. It extracts destination IP addresses and performs concurrent reverse DNS lookups to map network traffic to hostnames.

## Technical Specifications
- **Parser Engine**: `dpkt` with Raw-IP fallback for DLT_USBPCAP (Type 228).
- **Resolution Logic**: Concurrent `dnspython` resolver with `socket.gethostbyaddr` fallback.
- **Complexity**: Time $O(N)$ for packet traversal; Space $O(U)$ for unique IP caching.

## Installation
```bash
pip install -r requirements.txt

bash


python3 reverse\_dns.py [path/to/capture.pcap]
