#!/usr/bin/env python3
"""
NETRAVEN ONE — Yajath.R Edition
Single-file cybersecurity learning toolkit.

SAFE TRAINING DESIGN:
- Port scanning is intended only for systems you own or have permission to test.
- Web tools use ordinary HTTP requests and same-domain crawling.
- Wi-Fi tools are awareness/checklist tools; no cracking or packet injection.
- The phishing lab is a local awareness simulation. It never reads, stores,
  logs, or transmits the submitted password.
- Use only on systems and websites you are authorized to assess.
"""

import os
import sys
import re
import json
import time
import socket
import hashlib
import secrets
import base64
import platform
import subprocess
import threading
import webbrowser
import datetime
import ipaddress
import urllib.parse
import urllib.request
import urllib.error
import http.server
from html.parser import HTMLParser

# -------------------- THEME --------------------

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
PURPLE = "\033[35m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"

CREATOR = "Yajath.R"
TOOL_NAME = "NETRAVEN ONE"
VERSION = "2.0"

REPORTS = []
PHISH_EVENTS = []
XP = 0
LEVEL = 1

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
}

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]

def enable_ansi():
    if os.name == "nt":
        try:
            os.system("")
        except Exception:
            pass

enable_ansi()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(f"\n{DIM}Press ENTER to continue...{RESET}")

def neon(text, color=CYAN):
    print(color + text + RESET)

def typeprint(text, delay=0.008):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def banner():
    clear()
    neon(r"""
███╗   ██╗███████╗████████╗██████╗  █████╗ ██╗   ██╗███████╗███╗   ██╗
████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║
██╔██╗ ██║█████╗     ██║   ██████╔╝███████║██║   ██║█████╗  ██╔██╗ ██║
██║╚██╗██║██╔══╝     ██║   ██╔══██╗██╔══██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║
██║ ╚████║███████╗   ██║   ██║  ██║██║  ██║ ╚████╔╝ ███████╗██║ ╚████║
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝
""", MAGENTA)
    neon(f"              [ {TOOL_NAME} v{VERSION} ]", CYAN)
    neon(f"                 CREATED BY {CREATOR}", PURPLE)
    neon("          CYBERSECURITY LEARNING CONSOLE", BLUE)
    print()

def add_xp(amount):
    global XP, LEVEL
    XP += amount
    new_level = XP // 100 + 1
    if new_level > LEVEL:
        LEVEL = new_level
        neon(f"\n★ LEVEL UP! You are now Level {LEVEL}! ★", YELLOW)

def section(title):
    print("\n" + MAGENTA + "╔" + "═" * 64 + "╗" + RESET)
    print(MAGENTA + "║ " + CYAN + f"{title:<62}" + MAGENTA + "║" + RESET)
    print(MAGENTA + "╚" + "═" * 64 + "╝" + RESET)

def record(title, data):
    REPORTS.append({
        "tool": title,
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "creator": CREATOR,
        "data": data
    })

# -------------------- NETWORK --------------------

def network_information():
    section("NETWORK + SYSTEM INFORMATION")
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "Unavailable"

    info = {
        "hostname": hostname,
        "local_ip": local_ip,
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version()
    }

    for k, v in info.items():
        print(f"{CYAN}{k:<12}{RESET}: {v}")

    record("Network Information", info)
    add_xp(5)
    pause()

def ping_host():
    section("PING / LATENCY CHECK")
    host = input("Host/IP: ").strip()
    if not host:
        return
    count = "4"
    command = ["ping", "-n", count, host] if os.name == "nt" else ["ping", "-c", count, host]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        print(result.stdout[-5000:] if result.stdout else result.stderr)
        record("Ping", {"host": host, "return_code": result.returncode})
        add_xp(5)
    except Exception as e:
        neon(f"Ping error: {e}", RED)
    pause()

def dns_lookup():
    section("DNS LOOKUP")
    host = input("Domain/hostname: ").strip()
    if not host:
        return
    try:
        results = socket.getaddrinfo(host, None)
        addresses = sorted(set(r[4][0] for r in results))
        for addr in addresses:
            print(f"{GREEN}→ {addr}{RESET}")
        record("DNS Lookup", {"host": host, "addresses": addresses})
        add_xp(5)
    except Exception as e:
        neon(f"DNS error: {e}", RED)
    pause()

def reverse_dns():
    section("REVERSE DNS")
    ip = input("IP address: ").strip()
    try:
        name = socket.gethostbyaddr(ip)[0]
        print(f"{GREEN}Hostname: {name}{RESET}")
        record("Reverse DNS", {"ip": ip, "hostname": name})
        add_xp(5)
    except Exception as e:
        neon(f"No reverse DNS result: {e}", YELLOW)
    pause()

def subnet_calculator():
    section("CIDR / SUBNET CALCULATOR")
    value = input("Network (example 192.168.1.0/24): ").strip()
    try:
        net = ipaddress.ip_network(value, strict=False)
        print(f"Network:       {net.network_address}")
        print(f"Broadcast:     {net.broadcast_address}")
        print(f"Prefix:        /{net.prefixlen}")
        print(f"Netmask:       {net.netmask}")
        print(f"Total addresses: {net.num_addresses}")
        if net.num_addresses > 2:
            print(f"First usable:  {next(net.hosts())}")
            hosts = list(net.hosts()) if net.num_addresses <= 100000 else None
            if hosts:
                print(f"Last usable:   {hosts[-1]}")
        record("Subnet Calculator", {
            "input": value, "network": str(net.network_address),
            "broadcast": str(net.broadcast_address),
            "prefix": net.prefixlen, "netmask": str(net.netmask)
        })
        add_xp(10)
    except Exception as e:
        neon(f"Invalid network: {e}", RED)
    pause()

def port_scanner():
    section("AUTHORIZED TCP PORT SCANNER")
    target = input("Target you own / have permission to test: ").strip()
    if not target:
        return

    mode = input("Use common ports or custom range? [C/r]: ").strip().lower()
    if mode == "r":
        try:
            start = int(input("Start port: "))
            end = int(input("End port: "))
            if start < 1 or end > 65535 or end < start or end - start > 1000:
                raise ValueError("Range must be valid and at most 1000 ports.")
            ports = range(start, end + 1)
        except Exception as e:
            neon(str(e), RED)
            pause()
            return
    else:
        ports = COMMON_PORTS.keys()

    open_ports = []
    print(f"\n{YELLOW}Scanning {target}... only scan systems you are authorized to test.{RESET}\n")

    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.25)
                if s.connect_ex((target, port)) == 0:
                    service = COMMON_PORTS.get(port, "Unknown")
                    open_ports.append({"port": port, "service": service})
                    print(f"{GREEN}[OPEN] {port:<5} {service}{RESET}")
        except socket.gaierror:
            neon("Could not resolve target.", RED)
            break
        except Exception:
            pass

    if not open_ports:
        neon("No open ports found in the selected range.", YELLOW)

    record("Authorized Port Scanner", {"target": target, "open_ports": open_ports})
    add_xp(15)
    pause()

# -------------------- WEB TOOLS --------------------

def normalize_url(url):
    url = url.strip()
    if not re.match(r"^https?://", url, re.I):
        url = "https://" + url
    return url

def fetch_url(url, timeout=8, max_bytes=500000, method="GET"):
    url = normalize_url(url)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "NETRAVEN-ONE-YajathR-Learning/2.0"},
        method=method
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = response.read(max_bytes)
        return response, data

def security_headers():
    section("HTTP SECURITY HEADER AUDITOR")
    url = input("URL: ").strip()
    try:
        response, _ = fetch_url(url)
        headers = {k.lower(): v for k, v in response.headers.items()}
        score = 0

        print(f"\nStatus: {response.status}\n")
        results = {}
        for wanted in SECURITY_HEADERS:
            present = wanted.lower() in headers
            results[wanted] = present
            if present:
                score += 1
                neon(f"[+] {wanted}", GREEN)
            else:
                neon(f"[-] {wanted}", RED)

        print(f"\nSecurity-header score: {score}/{len(SECURITY_HEADERS)}")
        record("HTTP Security Headers", {"url": url, "score": score, "headers": results})
        add_xp(15)
    except Exception as e:
        neon(f"Request failed: {e}", RED)
    pause()

def cookie_checker():
    section("COOKIE SECURITY CHECKER")
    url = input("URL: ").strip()
    try:
        response, _ = fetch_url(url)
        cookies = response.headers.get_all("Set-Cookie") or []
        if not cookies:
            neon("No Set-Cookie header found.", YELLOW)
        else:
            for c in cookies:
                low = c.lower()
                secure = "secure" in low
                httponly = "httponly" in low
                samesite = "samesite=" in low
                print("\nCookie:", c.split(";", 1)[0])
                print("  Secure   :", "YES" if secure else "NO")
                print("  HttpOnly :", "YES" if httponly else "NO")
                print("  SameSite :", "YES" if samesite else "NO")
        record("Cookie Checker", {"url": url, "cookie_count": len(cookies)})
        add_xp(10)
    except Exception as e:
        neon(f"Request failed: {e}", RED)
    pause()

def redirect_analyzer():
    section("REDIRECT CHAIN ANALYZER")
    url = input("URL: ").strip()
    try:
        response, _ = fetch_url(url)
        print(f"Final URL: {response.geturl()}")
        print(f"Status:    {response.status}")
        record("Redirect Analyzer", {
            "input_url": normalize_url(url),
            "final_url": response.geturl(),
            "status": response.status
        })
        add_xp(10)
    except Exception as e:
        neon(f"Request failed: {e}", RED)
    pause()

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.scripts = []
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag.lower() == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data

def webpage_scraper():
    section("PUBLIC WEBPAGE SCRAPER")
    url = input("Public URL: ").strip()
    try:
        response, data = fetch_url(url)
        text = data.decode("utf-8", errors="ignore")
        parser = LinkParser()
        parser.feed(text)

        print(f"Status: {response.status}")
        print(f"Title:  {parser.title.strip() or '(none)'}")
        print("\nText preview:")
        clean = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.S | re.I)
        clean = re.sub(r"<[^>]+>", " ", clean)
        clean = re.sub(r"\s+", " ", clean).strip()
        print(clean[:2500])

        print("\nLinks:")
        for link in parser.links[:30]:
            print(" •", urllib.parse.urljoin(response.geturl(), link))

        print("\nJavaScript files:")
        for src in parser.scripts[:30]:
            print(" •", urllib.parse.urljoin(response.geturl(), src))

        record("Webpage Scraper", {
            "url": url, "status": response.status,
            "title": parser.title.strip(),
            "links_found": len(parser.links),
            "scripts_found": len(parser.scripts)
        })
        add_xp(15)
    except Exception as e:
        neon(f"Scrape failed: {e}", RED)
    pause()

def same_domain_crawler():
    section("SAME-DOMAIN CRAWLER")
    start_url = normalize_url(input("Starting URL: ").strip())
    try:
        base = urllib.parse.urlparse(start_url)
        domain = base.netloc
    except Exception:
        neon("Invalid URL.", RED)
        pause()
        return

    queue = [start_url]
    seen = set()
    found = []

    while queue and len(seen) < 20:
        current = queue.pop(0)
        if current in seen:
            continue
        try:
            parsed = urllib.parse.urlparse(current)
            if parsed.netloc != domain:
                continue
            response, data = fetch_url(current)
            seen.add(current)
            found.append(current)
            print(f"{GREEN}[{len(found):02}] {current}{RESET}")

            parser = LinkParser()
            parser.feed(data.decode("utf-8", errors="ignore"))
            for href in parser.links:
                nxt = urllib.parse.urljoin(current, href)
                p = urllib.parse.urlparse(nxt)
                clean = urllib.parse.urlunparse((p.scheme, p.netloc, p.path, "", p.query, ""))
                if p.netloc == domain and clean not in seen and clean not in queue:
                    queue.append(clean)
            time.sleep(0.15)
        except Exception:
            seen.add(current)

    print(f"\nDiscovered {len(found)} same-domain pages.")
    record("Same-Domain Crawler", {"start": start_url, "pages": found})
    add_xp(20)
    pause()

def robots_sitemap():
    section("ROBOTS.TXT + SITEMAP CHECKER")
    url = normalize_url(input("Base URL: ").strip()).rstrip("/")
    results = {}
    for path in ("/robots.txt", "/sitemap.xml"):
        try:
            response, data = fetch_url(url + path)
            print(f"{GREEN}{path}: HTTP {response.status}{RESET}")
            preview = data.decode("utf-8", errors="ignore")[:1500]
            print(preview)
            results[path] = {"status": response.status}
        except Exception as e:
            print(f"{YELLOW}{path}: unavailable ({e}){RESET}")
            results[path] = {"error": str(e)}
    record("Robots Sitemap", {"base": url, "results": results})
    add_xp(10)
    pause()

def url_risk_analyzer():
    section("SUSPICIOUS-URL EDUCATION ANALYZER")
    raw = input("URL to analyze: ").strip()
    try:
        p = urllib.parse.urlparse(normalize_url(raw))
        flags = []

        if p.scheme != "https":
            flags.append("Not using HTTPS")
        if "@" in p.netloc:
            flags.append("Contains @ in authority section")
        if len(p.netloc) > 60:
            flags.append("Unusually long hostname")
        if p.netloc.count(".") >= 4:
            flags.append("Many hostname components")
        if any(x in p.netloc.lower() for x in ["xn--"]):
            flags.append("Punycode hostname")
        if re.search(r"\d+\.\d+\.\d+\.\d+", p.netloc):
            flags.append("Uses a numeric IP address")
        if any(word in p.path.lower() for word in ["login", "verify", "signin", "password"]):
            flags.append("Contains authentication-related path wording")

        print("\nEducational indicators:")
        if flags:
            for f in flags:
                neon("⚠ " + f, YELLOW)
        else:
            neon("No obvious indicators from this simple heuristic.", GREEN)
        print("\nThis is NOT a verdict. A URL can be dangerous even without these flags.")

        record("URL Risk Analyzer", {"url": raw, "flags": flags})
        add_xp(10)
    except Exception as e:
        neon(f"Could not analyze URL: {e}", RED)
    pause()

# -------------------- CRYPTO / ENCODING --------------------

def hash_tool():
    section("HASH LAB")
    text = input("Text to hash: ").encode()
    print("MD5:    ", hashlib.md5(text).hexdigest())
    print("SHA1:   ", hashlib.sha1(text).hexdigest())
    print("SHA256: ", hashlib.sha256(text).hexdigest())
    print("\nNote: MD5/SHA-1 are included for learning and legacy identification,")
    print("not for securely storing passwords.")
    record("Hash Lab", {"sha256": hashlib.sha256(text).hexdigest()})
    add_xp(10)
    pause()

def encoding_lab():
    section("ENCODING / DECODING LAB")
    value = input("Text: ")
    print("\nBase64:", base64.b64encode(value.encode()).decode())
    print("Hex:   ", value.encode().hex())
    print("URL:   ", urllib.parse.quote(value))
    record("Encoding Lab", {"base64": base64.b64encode(value.encode()).decode()})
    add_xp(5)
    pause()

def random_password():
    section("RANDOM PASSWORD GENERATOR")
    try:
        length = int(input("Length (8-64): "))
        length = max(8, min(length, 64))
    except Exception:
        length = 16
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
    value = "".join(secrets.choice(alphabet) for _ in range(length))
    print(f"\nGenerated password:\n{GREEN}{value}{RESET}")
    print(f"{DIM}For learning only; don't paste sensitive passwords into chat or public sites.{RESET}")
    add_xp(5)
    pause()

def password_strength():
    section("PASSWORD STRENGTH METER")
    value = input("Enter a TEST password (never a real password): ")
    score = 0
    checks = [
        (len(value) >= 12, "12+ characters"),
        (bool(re.search(r"[a-z]", value)), "lowercase"),
        (bool(re.search(r"[A-Z]", value)), "uppercase"),
        (bool(re.search(r"\d", value)), "number"),
        (bool(re.search(r"[^A-Za-z0-9]", value)), "symbol"),
    ]
    for ok, label in checks:
        print(f"{GREEN if ok else RED}[{'✓' if ok else '✗'}] {label}{RESET}")
        score += int(ok)
    rating = ["Very weak", "Weak", "Fair", "Good", "Strong", "Very strong"][score]
    print(f"\nRating: {rating}")
    record("Password Strength", {"score": score, "rating": rating})
    add_xp(10)
    pause()

def file_integrity():
    section("FILE SHA-256 INTEGRITY CHECKER")
    path = input("File path: ").strip()
    if not os.path.isfile(path):
        neon("File not found.", RED)
        pause()
        return
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        digest = h.hexdigest()
        print(f"\nSHA-256: {GREEN}{digest}{RESET}")
        expected = input("Expected SHA-256 (optional): ").strip().lower()
        if expected:
            print("MATCH" if secrets.compare_digest(digest, expected) else "MISMATCH")
        record("File Integrity", {"file": os.path.basename(path), "sha256": digest})
        add_xp(10)
    except Exception as e:
        neon(f"Error: {e}", RED)
    pause()

# -------------------- LOCAL DEVICE TOOLS --------------------

def system_info():
    section("SYSTEM INFORMATION")
    items = {
        "OS": platform.system(),
        "OS release": platform.release(),
        "Version": platform.version(),
        "Architecture": platform.machine(),
        "Processor": platform.processor() or "Unavailable",
        "Python": platform.python_version(),
        "Hostname": socket.gethostname(),
    }
    for k, v in items.items():
        print(f"{CYAN}{k:<16}{RESET}: {v}")
    record("System Information", items)
    add_xp(5)
    pause()

def running_processes():
    section("RUNNING PROCESS VIEWER — READ ONLY")
    try:
        command = ["tasklist"] if os.name == "nt" else ["ps", "-e", "-o", "pid,comm"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        print(result.stdout[:10000])
        record("Process Viewer", {"platform": platform.system(), "return_code": result.returncode})
        add_xp(10)
    except Exception as e:
        neon(f"Could not list processes: {e}", RED)
    pause()

def disk_space():
    section("DISK SPACE")
    try:
        path = os.path.abspath(os.sep)
        usage = __import__("shutil").disk_usage(path)
        gb = 1024 ** 3
        print(f"Total: {usage.total / gb:.2f} GB")
        print(f"Used : {usage.used / gb:.2f} GB")
        print(f"Free : {usage.free / gb:.2f} GB")
        record("Disk Space", {"total": usage.total, "used": usage.used, "free": usage.free})
        add_xp(5)
    except Exception as e:
        neon(str(e), RED)
    pause()

def local_arp_table():
    section("LOCAL ARP / NEIGHBOR TABLE — READ ONLY")
    commands = [["arp", "-a"]] if os.name == "nt" else [["ip", "neigh"], ["arp", "-a"]]
    for command in commands:
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=8)
            if result.stdout:
                print(result.stdout[:8000])
                break
        except Exception:
            continue
    else:
        neon("ARP/neighbor command unavailable on this system.", YELLOW)
    add_xp(5)
    pause()

def firewall_status():
    section("FIREWALL STATUS — READ ONLY")
    commands = []
    if os.name == "nt":
        commands.append(["netsh", "advfirewall", "show", "allprofiles"])
    else:
        commands.extend([["ufw", "status"], ["iptables", "-L"]])

    shown = False
    for command in commands:
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            if result.stdout:
                print(result.stdout[:10000])
                shown = True
                break
        except Exception:
            pass
    if not shown:
        neon("No supported firewall-status command was available.", YELLOW)
    add_xp(10)
    pause()

# -------------------- WI-FI / DEFENSIVE --------------------

def wifi_awareness():
    section("WI-FI SECURITY AWARENESS")
    checks = [
        "Use WPA2-AES or WPA3 rather than legacy security.",
        "Use a long unique Wi-Fi passphrase.",
        "Disable WPS if you don't need it.",
        "Change the router's default administrator password.",
        "Keep router firmware updated.",
        "Use a guest network for untrusted devices.",
        "Review connected devices regularly.",
    ]
    for item in checks:
        print(f"{GREEN}✓{RESET} {item}")
    print("\nThis module intentionally does NOT crack Wi-Fi passwords or inject packets.")
    record("Wi-Fi Awareness", {"checks": checks})
    add_xp(10)
    pause()

def deauth_awareness():
    section("DEAUTHENTICATION AWARENESS LAB")
    print("802.11 deauthentication frames can disconnect clients from an access point.")
    print("A real attack would transmit crafted management frames.")
    print("\nNETRAVEN does not transmit deauthentication packets.")
    print("\nDefensive signs:")
    for item in [
        "Unexpected repeated Wi-Fi disconnects.",
        "Clients repeatedly reconnecting.",
        "A sudden pattern of management-frame activity in a controlled lab.",
        "Multiple devices losing connectivity at the same time."
    ]:
        print(f"{YELLOW}⚠{RESET} {item}")
    print("\nDefenses: WPA3 where supported, protected management frames (PMF/802.11w),")
    print("updated firmware, and monitoring in authorized environments.")
    add_xp(10)
    pause()

# -------------------- PHISHING AWARENESS LAB --------------------

PHISH_HTML = r"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PhotoShare — Awareness Lab</title>
<style>
body{margin:0;background:#070014;color:#eee;font-family:Arial,sans-serif}
.wrap{max-width:420px;margin:40px auto;padding:20px}
.card{background:#110022;border:1px solid #c000ff;border-radius:18px;padding:28px;box-shadow:0 0 35px #7000aa}
h1{color:#ff4dff;text-align:center}
.badge{text-align:center;background:#331100;color:#ffd36a;padding:10px;border-radius:8px;font-weight:bold}
input,button{box-sizing:border-box;width:100%;padding:13px;margin-top:12px;border-radius:8px;border:1px solid #8d00c7}
button{background:#a900ff;color:white;font-weight:bold;cursor:pointer}
.note{font-size:13px;color:#bbb;margin-top:15px}
#result{display:none;margin-top:18px;padding:15px;background:#172b18;border:1px solid #54ff75;border-radius:10px}
</style>
</head>
<body>
<div class="wrap">
<div class="card">
<div class="badge">SIMULATION — NOT INSTAGRAM</div>
<h1>PhotoShare</h1>
<p style="text-align:center">Yajath.R phishing-awareness lab</p>

<form id="training">
<input id="user" placeholder="Training username" autocomplete="off">
<input id="pass" type="password" placeholder="Dummy password — DO NOT USE A REAL ONE" autocomplete="off">
<button type="submit">Continue Training</button>
</form>

<div id="result">
<strong>🛡 Training result</strong>
<p>This was a phishing-awareness simulation.</p>
<p>Your password was <strong>NOT captured or sent anywhere.</strong></p>
<p>Look for warning signs such as unfamiliar domains, urgent requests, and unusual login pages.</p>
</div>

<p class="note">For education only. Never enter a real password into a security-training form.</p>
</div>
</div>
<script>
document.getElementById("training").addEventListener("submit", function(e){
    e.preventDefault();
    document.getElementById("result").style.display="block";
    document.getElementById("pass").value="";
});
</script>
</body>
</html>"""

class TrainingHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = PHISH_HTML.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        # Intentionally DO NOT read the request body.
        # This means form values are not captured or logged.
        PHISH_EVENTS.append({
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
            "demo_username": "training_user",
            "password_status": "NOT CAPTURED",
            "event": "training_form_submitted"
        })
        self.send_response(204)
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress request logging so credentials cannot appear in logs.
        return

def phishing_lab():
    section("LOCAL PHISHING-AWARENESS SIMULATOR")
    print("Starting safe local training page on 127.0.0.1:8080")
    print("No submitted password is read, stored, displayed, or transmitted.")
    print("\nDashboard demo event:")
    print(f"{MAGENTA}╔{'═'*54}╗")
    print(f"║ {CYAN}PHISHING AWARENESS EVENT{' '*29}║")
    print(f"╠{'═'*54}╣")
    print(f"║ Demo username : {GREEN}training_user{' '*28}║")
    print(f"║ Password      : {YELLOW}[NOT CAPTURED]{' '*31}║")
    print(f"║ Status        : {GREEN}SIMULATION DETECTED{' '*25}║")
    print(f"╚{'═'*54}╝{RESET}")

    try:
        server = http.server.HTTPServer(("127.0.0.1", 8080), TrainingHandler)
    except OSError as e:
        neon(f"Could not start server: {e}", RED)
        pause()
        return

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    url = "http://127.0.0.1:8080"
    neon(f"\nTraining page: {url}", GREEN)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    input(f"\n{CYAN}Press ENTER here when you are finished with the simulator...{RESET}")
    server.shutdown()
    server.server_close()

    if PHISH_EVENTS:
        event = PHISH_EVENTS[-1]
        print("\nLatest dashboard event:")
        print(f"Username: {event['demo_username']}")
        print(f"Password: {YELLOW}{event['password_status']}{RESET}")
        print("Result: phishing-awareness event recorded safely.")

    record("Phishing Awareness Simulator", {
        "local_only": True,
        "demo_username": "training_user",
        "password": "NOT CAPTURED",
        "events": len(PHISH_EVENTS)
    })
    add_xp(20)
    pause()

# -------------------- LEARNING / QUIZ --------------------

def quiz():
    section("CYBER XP QUIZ")
    questions = [
        ("Which protocol normally provides encrypted web traffic?", ["FTP", "HTTPS", "Telnet", "HTTP"], 1),
        ("Which port is commonly associated with HTTPS?", ["21", "22", "80", "443"], 3),
        ("What does SHA-256 produce?", ["A hash", "A subnet", "A port", "A DNS record"], 0),
        ("Which is safer for modern Wi-Fi?", ["WEP", "WPA3", "Open Wi-Fi", "Telnet"], 1),
        ("What should you do before scanning a server?", ["Get authorization", "Hide the scan", "Guess credentials", "Disable logging"], 0),
    ]
    score = 0
    for i, (q, options, answer) in enumerate(questions, 1):
        print(f"\n{CYAN}{i}. {q}{RESET}")
        for n, option in enumerate(options, 1):
            print(f"  {n}) {option}")
        try:
            choice = int(input("Answer: ")) - 1
            if choice == answer:
                neon("✓ Correct!", GREEN)
                score += 1
                add_xp(10)
            else:
                neon(f"✗ Correct answer: {options[answer]}", RED)
        except Exception:
            neon("Invalid answer.", YELLOW)

    print(f"\nScore: {score}/{len(questions)}")
    record("Cyber Quiz", {"score": score, "total": len(questions)})
    pause()

def daily_challenge():
    section("DAILY CYBER CHALLENGE")
    challenges = [
        "Explain why HTTPS is safer than HTTP.",
        "Calculate the usable host range for 192.168.10.0/28.",
        "Name three signs of a suspicious login page.",
        "Explain the difference between hashing and encryption.",
        "List three ways to harden a home router."
    ]
    index = datetime.date.today().toordinal() % len(challenges)
    print(f"{YELLOW}★ Today's challenge ★{RESET}\n")
    print(challenges[index])
    print("\nComplete it in your notebook or lab and award yourself +25 XP.")
    pause()

# -------------------- REPORTING --------------------

def generate_report():
    section("JSON SECURITY-LEARNING REPORT")
    filename = f"netraven_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    report = {
        "tool": TOOL_NAME,
        "version": VERSION,
        "creator": CREATOR,
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "xp": XP,
        "level": LEVEL,
        "events": REPORTS,
        "phishing_awareness": PHISH_EVENTS
    }

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        neon(f"Report saved: {filename}", GREEN)
    except Exception as e:
        neon(f"Could not save report: {e}", RED)
    pause()

def dashboard():
    section("YAJATH.R COMMAND DASHBOARD")
    print(f"{CYAN}Creator:{RESET} {CREATOR}")
    print(f"{CYAN}Level  :{RESET} {LEVEL}")
    print(f"{CYAN}XP     :{RESET} {XP}/100 to next level")
    print(f"{CYAN}Reports:{RESET} {len(REPORTS)}")
    print(f"{CYAN}Phish training events:{RESET} {len(PHISH_EVENTS)}")

    if PHISH_EVENTS:
        event = PHISH_EVENTS[-1]
        print(f"\n{MAGENTA}╔{'═'*54}╗")
        print(f"║ {CYAN}LATEST PHISHING-AWARENESS EVENT{' '*22}║")
        print(f"╠{'═'*54}╣")
        print(f"║ Demo username : {GREEN}{event['demo_username']:<38}{MAGENTA}║")
        print(f"║ Password      : {YELLOW}{event['password_status']:<38}{MAGENTA}║")
        print(f"║ Event         : {event['event']:<38}║")
        print(f"╚{'═'*54}╝{RESET}")
    else:
        print(f"\n{DIM}No phishing-awareness event has been recorded yet.{RESET}")

    pause()

def about():
    section("ABOUT NETRAVEN ONE")
    print(f"{TOOL_NAME} v{VERSION}")
    print(f"Creator: {CREATOR}")
    print("A student-friendly cybersecurity learning and defensive lab.")
    print("\nDesign principles:")
    print(" • Learn networking and web security.")
    print(" • Practice only on systems you own or are authorized to test.")
    print(" • Keep phishing exercises local and non-credential-capturing.")
    print(" • Use defensive analysis rather than offensive abuse.")
    print("\nNo Wi-Fi cracking, deauthentication transmission, credential theft,")
    print("malware, persistence, stealth, or evasion features are included.")
    pause()

# -------------------- MENU --------------------

TOOLS = [
    ("Network information", network_information),
    ("Authorized TCP port scanner", port_scanner),
    ("HTTP security-header auditor", security_headers),
    ("Cookie security checker", cookie_checker),
    ("Redirect analyzer", redirect_analyzer),
    ("Public webpage scraper", webpage_scraper),
    ("Same-domain crawler", same_domain_crawler),
    ("robots.txt / sitemap checker", robots_sitemap),
    ("Suspicious-URL education analyzer", url_risk_analyzer),
    ("DNS lookup", dns_lookup),
    ("Reverse DNS", reverse_dns),
    ("CIDR subnet calculator", subnet_calculator),
    ("Ping / latency check", ping_host),
    ("Hash lab", hash_tool),
    ("Base64 / Hex / URL encoding lab", encoding_lab),
    ("Random password generator", random_password),
    ("Password strength meter", password_strength),
    ("File SHA-256 integrity checker", file_integrity),
    ("System information", system_info),
    ("Running-process viewer", running_processes),
    ("Disk-space viewer", disk_space),
    ("Local ARP/neighbor table", local_arp_table),
    ("Firewall status viewer", firewall_status),
    ("Wi-Fi security awareness", wifi_awareness),
    ("Deauthentication awareness lab", deauth_awareness),
    ("Local phishing-awareness simulator", phishing_lab),
    ("Cyber XP quiz", quiz),
    ("Daily cyber challenge", daily_challenge),
    ("JSON report generator", generate_report),
    ("Yajath.R dashboard", dashboard),
    ("About NETRAVEN", about),
]

def menu():
    while True:
        banner()
        print(f"{GREEN}LEVEL {LEVEL}{RESET}  |  XP {XP}  |  {CREATOR}\n")
        for i, (name, _) in enumerate(TOOLS, 1):
            color = CYAN if i % 2 else MAGENTA
            print(f"{color}[{i:02}] {name}{RESET}")
        print(f"{RED}[00] Exit{RESET}")

        choice = input(f"\n{YELLOW}NETRAVEN@YAJATH.R > {RESET}").strip()

        if choice == "0" or choice.lower() in ("q", "quit", "exit"):
            clear()
            neon("╔══════════════════════════════════════════════════════╗", MAGENTA)
            neon("║       NETRAVEN ONE — SESSION COMPLETE               ║", CYAN)
            neon(f"║       Yajath.R | XP: {XP} | Level: {LEVEL:<3}              ║", PURPLE)
            neon("╚══════════════════════════════════════════════════════╝", MAGENTA)
            break

        try:
            index = int(choice) - 1
            if 0 <= index < len(TOOLS):
                TOOLS[index][1]()
            else:
                neon("Invalid menu choice.", RED)
                time.sleep(0.8)
        except ValueError:
            neon("Enter a menu number.", RED)
            time.sleep(0.8)
        except KeyboardInterrupt:
            print()
            break
        except Exception as e:
            neon(f"Tool error: {e}", RED)
            pause()

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(f"\n{CYAN}NETRAVEN closed. Stay ethical, {CREATOR}!{RESET}")
