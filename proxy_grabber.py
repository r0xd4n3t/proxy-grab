import argparse
import requests
import re
import socks
import sys
import socket
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

# Define the URLs to use for grabbing proxy lists
PROXY_LIST_URLS = [
    'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http',
    'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https',
    'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4',
    'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5',
    'https://free-proxy-list.net/',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt',
    'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
    'https://www.proxy-list.download/api/v1/get?type=https'
]

# Define the filename to save the proxy list to
PROXY_LIST_FILE = 'proxy_list.txt'

# Define a function to extract the IP address from a proxy address
def extract_ip(proxy):
    match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', proxy)
    return match.group(1) if match else None

def grab_proxy_list(url, proxy_types, counter, total):
    print(f"[*] Fetching data from the server {counter}/{total} ...please wait")
    proxies = []
    try:
        response = requests.get(url, timeout=7)
        if response.status_code == 200:
            if url == "https://free-proxy-list.net/":
                soup = BeautifulSoup(response.content, "html.parser")
                table = soup.find("table")
                rows = table.find_all("tr")
                proxies += [f"{row.contents[0].text.strip()}:{row.contents[1].text.strip()}" for row in rows[1:]]
            else:
                proxies += response.text.splitlines()

            # Check each proxy to see if it's valid and add it to the list if it is
            for proxy in proxies:
                parts = proxy.split(':')
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    if '-http' in proxy_types and url.endswith('http.txt'):
                        with open('http.txt', 'a') as f:
                            f.write(f'{proxy}\n')
                    elif '-https' in proxy_types and url.endswith('https.txt'):
                        with open('https.txt', 'a') as f:
                            f.write(f'{proxy}\n')
                    elif '-s4' in proxy_types and url.endswith('socks4.txt'):
                        with open('socks4.txt', 'a') as f:
                            f.write(f'{proxy}\n')
                    elif '-s5' in proxy_types and url.endswith('socks5.txt'):
                        with open('socks5.txt', 'a') as f:
                            f.write(f'{proxy}\n')
                    elif not proxy_types:
                        # If no proxy types are specified, add all proxies to the list
                        with open(PROXY_LIST_FILE, 'a') as f:
                            f.write(f'{proxy}\n')
    except:
        pass
    return proxies

# Parse command-line arguments for the proxy types to test
parser = argparse.ArgumentParser(description='Test proxy servers for availability')
parser.add_argument('-s4', action='store_true', help='test SOCKS4 proxies only')
parser.add_argument('-s5', action='store_true', help='test SOCKS5 proxies only')
parser.add_argument('-http', action='store_true', help='test HTTP proxies only')
parser.add_argument('-https', action='store_true', help='test HTTPS proxies only')
args = parser.parse_args()

# Show help if no arguments are given
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# Grab the proxy lists from each URL and add them to a set
proxy_types = []
if args.s4:
    proxy_types.append('-s4')
if args.s5:
    proxy_types.append('-s5')
if args.http:
    proxy_types.append('-http')
if args.https:
    proxy_types.append('-https')

proxies = []
num_urls = len(PROXY_LIST_URLS)
with ThreadPoolExecutor(max_workers=11) as executor:
    results = executor.map(lambda i, url: grab_proxy_list(url, proxy_types, i+1, num_urls), range(num_urls), PROXY_LIST_URLS)
    for result in results:
        proxies.extend(result)

# Remove duplicates from the proxy list
num_proxies_before = len(proxies)
proxies = set([proxy for proxy in proxies if proxy.strip()])

# Save the list of unique proxies to a file
if not proxy_types:
    with open(PROXY_LIST_FILE, 'w') as f:
        f.writelines([f'{proxy}\n' for proxy in proxies])

num_proxies_after = len(proxies)

if not proxy_types:
    print(f"[+] Fetched and saved {num_proxies_before} proxies to {PROXY_LIST_FILE}")
    print(f"[-] Removed {num_proxies_before - num_proxies_after} duplicates, {num_proxies_after} unique proxies remaining\n")
else:
    print(f"[+] Fetched proxies. Writing output to files based on the parameter...\n")

# Define the URLs to use for testing proxies
TEST_HTTP_URL = 'http://httpbin.org/ip'
TEST_HTTPS_URL = 'https://httpbin.org/ip'
TEST_SOCKS4_URL = 'http://httpbin.org/ip'
TEST_SOCKS5_URL = 'https://httpbin.org/ip'

# Define dictionaries to store the working proxies for each protocol
working_http_proxies = {}
working_https_proxies = {}
working_socks4_proxies = {}
working_socks5_proxies = {}

# Define a function to test the availability of a proxy for a given protocol
def test_proxy(proxy, protocol, proxy_types):
    proxies = {protocol: proxy}
    try:
        if protocol.startswith('http') or protocol.startswith('https') or protocol.startswith('socks4') or protocol.startswith('socks5'):
            if protocol.startswith('http') or protocol.startswith('https'):
                url = TEST_HTTPS_URL if protocol.startswith('https') else TEST_HTTP_URL
                response = requests.get(url, proxies=proxies, timeout=7)
            elif protocol.startswith('socks4'):
                socks.set_default_proxy(socks.SOCKS4, proxy.split(':')[0], int(proxy.split(':')[1]))
                socket.socket = socks.socksocket
                response = requests.get(TEST_SOCKS4_URL, timeout=7)
            elif protocol.startswith('socks5'):
                socks.set_default_proxy(socks.SOCKS5, proxy.split(':')[0], int(proxy.split(':')[1]))
                socket.socket = socks.socksocket
                response = requests.get(TEST_SOCKS5_URL, timeout=7)
            
            ip_address = extract_ip(response.content.decode())
            if ip_address is not None and ip_address != '':
                if ip_address == proxy.split(':')[0]:
                    if '-http' in proxy_types and protocol == 'http':
                        working_http_proxies[proxy] = ip_address
                        print(f'[+] Found HTTP Proxy: {proxy}')
                    elif '-https' in proxy_types and protocol == 'https':
                        working_https_proxies[proxy] = ip_address
                        print(f'[+] Found HTTPS Proxy: {proxy}')
                    elif '-s4' in proxy_types and protocol == 'socks4':
                        working_socks4_proxies[proxy] = ip_address
                        print(f'[+] Found SOCKS4 Proxy: {proxy}')
                    elif '-s5' in proxy_types and protocol == 'socks5':
                        working_socks5_proxies[proxy] = ip_address
                        print(f'[+] Found SOCKS5 Proxy: {proxy}')
                    elif not proxy_types:
                        # If no proxy types are specified, add all proxies to the list
                        if protocol == 'http':
                            working_http_proxies[proxy] = ip_address
                            print(f'[+] Found HTTP Proxy: {proxy}')
                        elif protocol == 'https':
                            working_https_proxies[proxy] = ip_address
                            print(f'[+] Found HTTPS Proxy: {proxy}')
                        elif protocol == 'socks4':
                            working_socks4_proxies[proxy] = ip_address
                            print(f'[+] Found SOCKS4 Proxy: {proxy}')
                        elif protocol == 'socks5':
                            working_socks5_proxies[proxy] = ip_address
                            print(f'[+] Found SOCKS5 Proxy: {proxy}')
                    return True
            return False
    except:
        return False

# Loop through the list of proxies and test their availability for the selected protocol
with ThreadPoolExecutor(max_workers=1000) as executor:
    for proxy in proxies:
        if args.s4:
            protocol = 'socks4'
        elif args.s5:
            protocol = 'socks5'
        elif args.https:
            protocol = 'https'
        elif args.http:
            protocol = 'http'
        else:
            # Test all protocols if no specific protocol is selected
            for protocol in ['socks4', 'socks5', 'https', 'http']:
                executor.submit(test_proxy, proxy, protocol, proxy_types)
            break  # exit the loop after submitting all jobs

        executor.submit(test_proxy, proxy, protocol, proxy_types)

# Save the working proxies to separate files based on their protocol
if '-http' in proxy_types:
    with open('http.txt', 'w') as f:
        f.writelines([f'{proxy}\n' for proxy in working_http_proxies.keys()])
if '-https' in proxy_types:
    with open('https.txt', 'w') as f:
        f.writelines([f'{proxy}\n' for proxy in working_https_proxies.keys()])
if '-s4' in proxy_types:
    with open('socks4.txt', 'w') as f:
        f.writelines([f'{proxy}\n' for proxy in working_socks4_proxies.keys()])
if '-s5' in proxy_types:
    with open('socks5.txt', 'w') as f:
        f.writelines([f'{proxy}\n' for proxy in working_socks5_proxies.keys()])

# Print the message indicating the types and number of proxies found
num_http_proxies = len(working_http_proxies)
num_https_proxies = len(working_https_proxies)
num_socks4_proxies = len(working_socks4_proxies)
num_socks5_proxies = len(working_socks5_proxies)

if num_http_proxies > 0 and num_https_proxies == 0 and num_socks4_proxies == 0 and num_socks5_proxies == 0:
    message = f"\n[*] Testing complete. {num_http_proxies} HTTP proxies found! Results saved to http.txt"
elif num_https_proxies > 0 and num_http_proxies == 0 and num_socks4_proxies == 0 and num_socks5_proxies == 0:
    message = f"\n[*] Testing complete. {num_https_proxies} HTTPS proxies found! Results saved to https.txt"
elif num_socks4_proxies > 0 and num_socks5_proxies == 0 and num_http_proxies == 0 and num_https_proxies == 0:
    message = f"\n[*] Testing complete. {num_socks4_proxies} SOCKS4 proxies found! Results saved to socks4.txt"
elif num_socks5_proxies > 0 and num_socks4_proxies == 0 and num_http_proxies == 0 and num_https_proxies == 0:
    message = f"\n[*] Testing complete. {num_socks5_proxies} SOCKS5 proxies found! Results saved to socks5.txt"
elif num_http_proxies == 0 and num_https_proxies == 0 and num_socks4_proxies == 0 and num_socks5_proxies == 0:
    message = "\n[*] Testing complete. No proxies found."
else:
    message = ""

print(message)
