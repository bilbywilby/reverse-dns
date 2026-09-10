#!/usr/bin/env python3
import os
import sys
import socket
import concurrent.futures
from collections import defaultdict
import dpkt

if len(sys.argv) > 1:
    PCAP_PATH = os.path.expanduser(sys.argv[1])
else:
    PCAP_PATH = os.path.expanduser("~/shared/gms_root_capture.pcap")

DNS_CACHE = {}
IPV6_EXT_HEADERS = {0, 43, 44, 50, 51, 60, 135}

def _single_ptr_lookup(ip_str: str, timeout: float = 1.5) -> str:
    if ip_str in DNS_CACHE:
        return DNS_CACHE[ip_str]
    try:
        import dns.resolver
        import dns.reversename
        rev_name = dns.reversename.from_address(ip_str)
        resolver = dns.resolver.Resolver()
        resolver.lifetime = timeout
        resolver.timeout = timeout
        answers = resolver.resolve(rev_name, "PTR")
        if answers:
            res = str(answers[0]).rstrip(".")
            DNS_CACHE[ip_str] = res
            return res
    except Exception:
        pass
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_str)
        DNS_CACHE[ip_str] = hostname
        return hostname
    except (socket.herror, socket.gaierror, socket.timeout, OverflowError, OSError):
        DNS_CACHE[ip_str] = "[Unresolved]"
        return "[Unresolved]"

def bulk_resolve_hostnames(ip_list: list, max_workers: int = 20) -> dict:
    results = {}
    to_resolve = list(set(ip_list))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {executor.submit(_single_ptr_lookup, ip): ip for ip in to_resolve}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                results[ip] = future.result()
            except Exception:
                results[ip] = "[Error]"
    return results

def parse_pcap():
    if not os.path.isfile(PCAP_PATH):
        print(f"[!] File not found: {PCAP_PATH}")
        sys.exit(1)

    stats = defaultdict(lambda: {"tcp": 0, "udp": 0, "total": 0})
    ips_found = set()

    with open(PCAP_PATH, "rb") as f:
        try:
            pcap = dpkt.pcap.Reader(f)
            dl = pcap.datalink()
        except Exception as e:
            print(f"[!] PCAP Header Error: {e}")
            sys.exit(1)

        count = 0
        for ts, buf in pcap:
            count += 1
            try:
                # Handle DLT_USBPCAP (228) or Raw IP buffers
                if dl == 228 or (len(buf) > 0 and buf[0] in (0x45, 0x60)):
                    ip = dpkt.ip.IP(buf)
                elif dl == 1: # Ethernet
                    eth = dpkt.ethernet.Ethernet(buf)
                    if not isinstance(eth.data, dpkt.ip.IP):
                        continue
                    ip = eth.data
                else:
                    continue

                dst_ip = socket.inet_ntop(socket.AF_INET if ip.v == 4 else socket.AF_INET6, ip.dst)
                ips_found.add(dst_ip)
                stats[dst_ip]["total"] += 1

                if isinstance(ip.data, dpkt.tcp.TCP):
                    stats[dst_ip]["tcp"] += 1
                elif isinstance(ip.data, dpkt.udp.UDP):
                    stats[dst_ip]["udp"] += 1

            except Exception:
                continue

    print(f"[*] Parsed {count} packets from {PCAP_PATH}")
    
    resolutions = bulk_resolve_hostnames(list(ips_found))
    
    print(f"{'Destination IP':<20} {'Resolved Hostname':<30} {'Total':<8} {'TCP':<8} {'UDP':<8}")
    print("-" * 74)
    
    for ip in sorted(stats.keys()):
        s = stats[ip]
        host = resolutions.get(ip, "[Unresolved]")
        print(f"{ip:<20} {host:<30} {s['total']:<8} {s['tcp']:<8} {s['udp']:<8}")

if __name__ == "__main__":
    parse_pcap()
