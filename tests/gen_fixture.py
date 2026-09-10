#!/usr/bin/env python3
from scapy.all import wrpcap, Ether, IP, UDP, TCP

def generate():
    # Packet 1: Standard Ethernet -> IPv4 -> UDP (8.8.8.8)
    p1 = Ether()/IP(dst="8.8.8.8")/UDP(dport=53)
    # Packet 2: Standard Ethernet -> IPv4 -> TCP (1.1.1.1)
    p2 = Ether()/IP(dst="1.1.1.1")/TCP(dport=443)
    # Packet 3: Standard Ethernet -> IPv4 -> UDP (8.8.8.8)
    p3 = Ether()/IP(dst="8.8.8.8")/UDP(dport=53)
    
    wrpcap("tests/fixtures/smoke_test.pcap", [p1, p2, p3])
    print("[+] Fixture tests/fixtures/smoke_test.pcap generated.")

if __name__ == "__main__":
    generate()
