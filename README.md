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
This is a Python script that can be used to test the availability of proxy servers. The script can fetch proxy lists from various sources, test them for availability, and save the working proxies to separate files based on their protocol. The supported proxy protocols are HTTP, HTTPS, SOCKS4, and SOCKS5.

Keep in mind that the speed of the testing process will also depend on the number of proxies you are testing, the quality of the proxies, and the speed of your internet connection.

## 🕹️ Usage
To run the script, open a terminal in the directory containing the script and run the following command:

```
python proxy_tester.py [options]
```

The available options are:
-    -s4     Test SOCKS4 proxies only
-    -s5     Test SOCKS5 proxies only
-    -http   Test HTTP proxies only
-    -https  Test HTTPS proxies only

> HELP

![](https://raw.githubusercontent.com/r0xd4n3t/proxy-grab/main/img/help.png)

If no options are specified, the script will show help message and exit. The script will fetch proxy lists from various sources, test them for availability, and save the working proxies to separate files based on their protocol.

> Socks4

![](https://raw.githubusercontent.com/r0xd4n3t/proxy-grab/main/img/s4.png)

> Socks5

![](https://raw.githubusercontent.com/r0xd4n3t/proxy-grab/main/img/s5.png)

> https

![](https://raw.githubusercontent.com/r0xd4n3t/proxy-grab/main/img/https.png)

> http

![](https://raw.githubusercontent.com/r0xd4n3t/proxy-grab/main/img/http.png)

## 📝 Prerequisites
To run this script, you will need to have Python 3.x installed on your computer, as well as the following Python packages:

-    requests
-    beautifulsoup4
-    PySocks

You can install these packages using pip, the package installer for Python. To install the packages, open a command prompt or terminal and type the following commands:

```
pip3 install requests beautifulsoup4 PySocks
```
or
```
pip3 install -r requirements.txt
```

<p align="center"><a href=#top>Back to Top</a></p>
