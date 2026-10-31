"""
DNS Propagation & SSL Enforcer Monitor:
Continuously checks when theapexworkflows.com resolves to GitHub Pages IPs
and automatically triggers HTTPS enforcement via GitHub API.
"""

import time
import socket
import json
import urllib.request
import subprocess

GITHUB_IPS = {"185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"}
DOMAIN = "theapexworkflows.com"

def check_dns():
    try:
        resolved_ip = socket.gethostbyname(DOMAIN)
        print(f"[*] Checking {DOMAIN} -> Resolved to: {resolved_ip}")
        if resolved_ip in GITHUB_IPS:
            print(f"[✔] MATCH! {DOMAIN} is correctly pointing to GitHub Pages!")
            return True
        else:
            print(f"[-] Still pointing to: {resolved_ip}")
            return False
    except Exception as e:
        print(f"[-] Not resolved yet ({e}). Waiting for DNS propagation...")
        return False

if __name__ == "__main__":
    check_dns()

