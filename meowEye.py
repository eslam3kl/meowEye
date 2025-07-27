import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import argparse
import threading
import time

from selenium_driver import create_driver, request_in_scope
from payloads import get_payloads
from scan_utils import analyze_request
from config import LOGO, color_tag, OUTPUT_FILE

import tldextract

print(color_tag('[logo]'))

parser = argparse.ArgumentParser(description='MeowEye is a real-time scanner for identifying multiple web vulnerabilities in live applications.')
parser.add_argument('--mode', choices=['live', 'delay'], required=True, help='Scan mode: live or delay')
parser.add_argument('--attack', choices=['ref', 'lfiLinux', 'lfiWin', 'ssti'], required=True, help='Attack type')
parser.add_argument('--proxy', help='Proxy in format http://127.0.0.1:8080 (optional)', required=False)
parser.add_argument('--url', required=True, help='Target URL')
args = parser.parse_args()

scan_mode = args.mode
attack_choice = args.attack
user_url = args.url
proxy = args.proxy

proxies = {
    "http": proxy,
    "https": proxy
} if proxy else None

ext = tldextract.extract(user_url)
target_root_domain = f"{ext.domain}.{ext.suffix}"

payloads = get_payloads(attack_choice)
if not payloads:
    print(f"{color_tag('[ERROR]')} No payloads loaded, exiting.")
    exit(1)

output_file = open(OUTPUT_FILE, "a")

driver = create_driver(user_url, proxy)

def live_scan_loop():
    seen = set()
    while True:
        for request in driver.requests:
            if request.id in seen or not request.response:
                continue
            seen.add(request.id)
            if request.method in ['POST', 'GET'] and request_in_scope(request, target_root_domain):
                print(f"{color_tag('[info]')} Analyzing: {request.method} {request.url}")
                analyze_request(request, attack_choice, payloads, proxies, output_file)
        time.sleep(1)

def delayed_scan():
    print(f"{color_tag('[info]')} Delayed scan mode selected. Start browsing and then type 'yalla' in terminal to start scanning.")
    while True:
        trigger = input("Type 'yalla' to begin scanning: ")
        if trigger.lower() == 'yalla':
            break
    for request in driver.requests:
        if request.method in ['POST', 'GET'] and request.response and request_in_scope(request, target_root_domain):
            print(f"{color_tag('[info]')} Analyzing: {request.method} {request.url}")
            analyze_request(request, attack_choice, payloads, proxies, output_file)

def main():
    print(f"{color_tag('[info]')} Opening URL: {user_url}")
    driver.get(user_url)
    if scan_mode == 'live':
        threading.Thread(target=live_scan_loop, daemon=True).start()
    else:
        delayed_scan()

main()
input(f"{color_tag('[info]')} Press Enter to exit and close browser...\n\n")
driver.quit()
output_file.close()
