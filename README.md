<a id="top"></a>

#

<h1 align="center">
Proxy Grabber
</h1>

<p align="center"> 
  <kbd>
<img src="https://raw.githubusercontent.com/r0xd4n3t/proxy-grab/main/img/proxy.png"></img>
  </kbd>
</p>

<p align="center">
<img src="https://img.shields.io/github/last-commit/r0xd4n3t/proxy-grab?style=flat">
<img src="https://img.shields.io/github/stars/r0xd4n3t/proxy-grab?color=brightgreen">
<img src="https://img.shields.io/github/forks/r0xd4n3t/proxy-grab?color=brightgreen">
</p>

# 📜 Proxy Grabber
This is a Python script that tests the validity of different types of proxies (HTTP, HTTPS, SOCKS4, and SOCKS5) using concurrent execution to speed up the process. The script reads a list of proxy URLs from different sources and saves the working proxies to a file.

## 🕹️ Usage
The script uses the argparse library to parse command-line arguments.

The available options are:
-    -s4 or --socks4: test SOCKS4 proxies
-    -s5 or --socks5: test SOCKS5 proxies
-    -http or --http: test HTTP proxies
-    -https or --https: test HTTPS proxies
-    -v or --verbose: verbose mode

The main function is divided into several sub-functions:
-    write_to_file(data: List[str], filename: str) -> None: writes a list of strings to a file
-    test_proxy(proxy: str, url: str, proxies: dict) -> bool: tests the validity of a single proxy by sending a request to a given URL
-    test_http_proxies(proxies: List[str], verbose: bool) -> List[str]: tests a list of HTTP proxies
-    test_https_proxies(proxies: List[str], verbose: bool) -> List[str]: tests a list of HTTPS proxies
-    test_socks_proxies(proxies: List[str], http_url: str, https_url: str, socks4: bool, socks5: bool, verbose: bool) -> List[str]: tests a list of SOCKS4 or SOCKS5 proxies

The script first fetches proxy URLs from various sources and saves them to a file named "proxy.txt". It then reads the list of proxies from the file, removes duplicates, and tests the validity of the proxies based on the command-line arguments provided.

The script uses the concurrent.futures module to speed up the testing process. The maximum number of threads used is set to 20, and the proxies are split into chunks of equal size for parallel execution.

Finally, the script saves the working proxies to a file named "working_proxies.txt". The number of working proxies and the execution time are printed to the console.

> Socks4

![](https://raw.githubusercontent.com/r0xd4n3t/proxy-grab/main/img/s4.png)

> Socks5

![](https://raw.githubusercontent.com/r0xd4n3t/proxy-grab/main/img/s5.png)

> https

![](https://raw.githubusercontent.com/r0xd4n3t/proxy-grab/main/img/https.png)

## 📝 Prerequisites
To run this script, you will need to have Python 3.x installed on your computer, as well as the following Python packages:

-    argparse
-    concurrent.futures
-    requests
-    beautifulsoup4

You can install these packages using pip, the package installer for Python. To install the packages, open a command prompt or terminal and type the following commands:

```
pip install argparse
pip install futures
pip install requests
pip install beautifulsoup4
```

Once you have installed the required packages, you can run the script from the command line by navigating to the directory where the script is saved and typing:

```
python proxy_grabber.py
```

Make sure you have a stable internet connection before running the script, as it will need to fetch data from various proxy sources.


<p align="center"><a href=#top>Back to Top</a></p>
