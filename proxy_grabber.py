import argparse
import concurrent.futures
import requests
import random
from bs4 import BeautifulSoup
from typing import List

def write_to_file(data: List[str], filename: str) -> None:
    with open(filename, "w") as f:
        f.write("\n".join(data))

def test_proxy(proxy: str, url: str, proxies: dict) -> bool:
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        pass
    return False

def test_http_proxies(proxies: List[str], verbose: bool) -> List[str]:
    working_proxies = []
    url = "http://checkip.dyndns.org/"
    for i, proxy in enumerate(proxies):
        if test_proxy(proxy, url, None):
            working_proxies.append(proxy)
        if verbose:
            print(f"[*] Testing {i+1}/{len(proxies)} subset of the total HTTP proxies", end="\r")
    if verbose:
        print()
    return working_proxies

def test_https_proxies(proxies: List[str], verbose: bool) -> List[str]:
    working_proxies = []
    url = "https://checkip.dyndns.org/"
    count = 0
    for proxy in proxies:
        count += 1
        if test_proxy(proxy, url, None):
            working_proxies.append(proxy)
        if verbose:
            print(f"[*] Testing {count}/{len(proxies)} subset of the total HTTPS proxies", end="\r")
    return working_proxies

def test_socks_proxies(proxies: List[str], http_url: str, https_url: str, socks4: bool, socks5: bool, verbose: bool) -> List[str]:
    working_proxies = []
    count = 0
    for i in range(0, len(proxies), chunk_size):
        chunk = proxies[i:i + chunk_size]
        count += len(chunk)
        if socks4:
            proxy_type = "SOCKS4"
            proxy_dict = {"http": f"socks4://{random.choice(chunk)}", "https": f"socks4://{random.choice(chunk)}"}
        elif socks5:
            proxy_type = "SOCKS5"
            proxy_dict = {"http": f"socks5://{random.choice(chunk)}", "https": f"socks5://{random.choice(chunk)}"}
        else:
            proxy_type = "HTTP"
            proxy_dict = {"http": f"http://{random.choice(chunk)}", "https": f"https://{random.choice(chunk)}"}
        
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for proxy in chunk:
                futures.append(executor.submit(test_proxy, proxy, http_url, proxy_dict))
                futures.append(executor.submit(test_proxy, proxy, https_url, proxy_dict))

            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        for proxy, result in zip(chunk, results[::2]):
            if result and results[results.index(result) + 1]:
                working_proxies.append(proxy)

        if verbose:
            subset_size = min(len(proxies) - (count - 1), chunk_size)
            print(f"[*] Testing {count - len(chunk)}-{count - 1}/{len(proxies)} {proxy_type} proxies", end="\r")
    return working_proxies

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s4", "--socks4", action="store_true", help="Test SOCKS4 proxies")
    parser.add_argument("-s5", "--socks5", action="store_true", help="Test SOCKS5 proxies")
    parser.add_argument("-http", "--http", action="store_true", help="Test HTTP proxies")
    parser.add_argument("-https", "--https", action="store_true", help="Test HTTPS proxies")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()

    urls = [
        "https://free-proxy-list.net/",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=https",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5"
    ]

    proxies = []
    for url in urls:
        if args.verbose:
            print(f"[*] Fetching data from {url} ...please wait")
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")
            continue
        if url == "https://free-proxy-list.net/":
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table")
            rows = table.find_all("tr")
            proxies += [f"{row.contents[0].text.strip()}:{row.contents[1].text.strip()}" for row in rows[1:]]
        else:
            proxies += response.text.splitlines()

    write_to_file(proxies, "proxy.txt")
    print(f"[+] Saved {len(proxies)} proxies to proxy.txt")

    with open("proxy.txt", "r") as f:
        proxies = [proxy.strip() for proxy in f]
        if args.verbose:
            print("[*] Removing duplicates...please wait")
        proxies = list(set(proxies))
        write_to_file(proxies, "proxy.txt")
        print(f"[+] Removed duplicates, {len(proxies)} unique proxies remaining")
    if args.http:
        num_threads = 20
        chunk_size = len(proxies) // num_threads
        print(f"[*] Testing {len(proxies)} HTTP proxies using {num_threads} threads...please wait")
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for i in range(num_threads):
                chunk = proxies[i * chunk_size : (i + 1) * chunk_size]
                futures.append(executor.submit(test_http_proxies, chunk, args.verbose))
            working_proxies = []
            for future in concurrent.futures.as_completed(futures):
                working_proxies.extend(future.result())
        write_to_file(working_proxies, "working_proxies.txt")
        print(f"[+] Saved {len(working_proxies)} working HTTP proxies to working_proxies.txt")
    elif args.https:
        num_threads = 20
        chunk_size = len(proxies) // num_threads
        print(f"[*] Testing {len(proxies)} HTTPS proxies using {num_threads} threads...please wait")
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for i in range(num_threads):
                chunk = proxies[i * chunk_size : (i + 1) * chunk_size]
                futures.append(executor.submit(test_https_proxies, chunk, verbose=args.verbose)) # added verbose argument
            working_proxies = []
            for future in concurrent.futures.as_completed(futures):
                working_proxies.extend(future.result())
        write_to_file(working_proxies, "working_proxies.txt")
        print(f"[+] Saved {len(working_proxies)} working HTTPS proxies to working_proxies.txt")
    elif args.socks4:
        socks4 = True
        http_url = "http://checkip.dyndns.org/"
        https_url = "https://checkip.dyndns.org/"
        num_threads = 20
        chunk_size = len(proxies) // num_threads
        print(f"[*] Testing {len(proxies)} SOCKS4 proxies using {num_threads} threads...please wait")
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for i in range(num_threads):
                chunk = proxies[i * chunk_size : (i + 1) * chunk_size]
                futures.append(executor.submit(test_socks_proxies, chunk, http_url, https_url, socks4, False, verbose=args.verbose)) # added verbose argument
            working_proxies = []
            for future in concurrent.futures.as_completed(futures):
                working_proxies.extend(future.result())
        write_to_file(working_proxies, "working_proxies.txt")
        print(f"[+] Saved {len(working_proxies)} working SOCKS4 proxies to working_proxies.txt")
    elif args.socks5:
        socks5 = True
        http_url = "http://checkip.dyndns.org/"
        https_url = "https://checkip.dyndns.org/"
        num_threads = 20
        chunk_size = len(proxies) // num_threads
        print(f"[*] Testing {len(proxies)} SOCKS5 proxies using {num_threads} threads...please wait")
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for i in range(num_threads):
                chunk = proxies[i * chunk_size : (i + 1) * chunk_size]
                futures.append(executor.submit(test_socks_proxies, chunk, http_url, https_url, False, socks5, args.verbose))
            working_proxies = []
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                progress = f"[*] Testing {i+1}/{num_threads} SOCKS5"
                print(f"\r{progress}", end="")
                working_proxies.extend(future.result())
        write_to_file(working_proxies, "working_proxies.txt")
        print(f"\n[+] Saved {len(working_proxies)} working SOCKS5 proxies to working_proxies.txt")
