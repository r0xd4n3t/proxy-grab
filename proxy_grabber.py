import argparse
import concurrent.futures
import requests
import random
from bs4 import BeautifulSoup
from typing import List

def write_to_file(data: List[str], filename: str) -> None:
    with open(filename, "w") as f:
        f.write("\n".join(data))

def test_proxy(proxy: str, http_url: str, https_url: str) -> bool:
    try:
        http_proxy = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
        http_response = requests.get(http_url, proxies=http_proxy, timeout=5)
        http_response.raise_for_status()
        print(f'[+] HTTP proxy {proxy} is working')
        return True
    except requests.exceptions.RequestException:
        pass

    try:
        https_proxy = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
        https_response = requests.get(https_url, proxies=https_proxy, timeout=5)
        https_response.raise_for_status()
        print(f'[+] HTTPS proxy {proxy} is working')
        return True
    except requests.exceptions.RequestException:
        pass

    return False

def test_proxies(proxies: List[str], http_url: str, https_url: str) -> List[str]:
    working_proxies = []
    for proxy in proxies:
        if test_proxy(proxy, http_url, https_url):
            working_proxies.append(proxy)
    return working_proxies

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true", help="Test the proxies")
    args = parser.parse_args()

    url = "https://free-proxy-list.net/"

    print("[*] Fetching data from the server...please wait")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        exit(1)

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")
    proxies = [f"{row.contents[0].text.strip()}:{row.contents[1].text.strip()}" for row in rows[1:]]
    write_to_file(proxies, "proxy.txt")
    print(f"[+] Saved {len(proxies)} unique proxies to proxy.txt")

    with open("proxy.txt", "r") as f:
        proxies = [proxy.strip() for proxy in f]
        print("[*] Removing duplicates...please wait")
        proxies = list(set(proxies))
        write_to_file(proxies, "proxy.txt")
        print(f"[+] Removed duplicates, {len(proxies)} unique proxies remaining")

    if args.test:
            http_url = "http://checkip.dyndns.org/"
            https_url = "https://checkip.dyndns.org/"
            num_threads = 20
            chunk_size = len(proxies) // num_threads
            print(f"[*] Testing {len(proxies)} proxies using {num_threads} threads...please wait")
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for i in range(num_threads):
                    chunk = proxies[i * chunk_size : (i + 1) * chunk_size]
                    futures.append(executor.submit(test_proxies, chunk, http_url, https_url))
                working_proxies = []
                for future in concurrent.futures.as_completed(futures):
                    working_proxies.extend(future.result())
            write_to_file(working_proxies, "working_proxies.txt")
            print(f"[+] Saved {len(working_proxies)} working proxies to working_proxies.txt")

    # Print 5 random proxies from working_proxies.txt
    try:
        with open("working_proxies.txt", "r") as f:
            proxies = f.read().splitlines()
    except FileNotFoundError:
        print("Error: working_proxies.txt not found")
        exit(1)
    random.shuffle(proxies)
    print("[*] Random working proxies:")
    for proxy in proxies[:5]:
        print(proxy)
