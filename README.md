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
This is a Python script that fetches a list of free proxy servers from a website, removes duplicates, and tests each proxy server to see if it is working. It then saves the working proxies to a file called "working_proxies.txt" and prints five random working proxies to the console.

## 🕹️ Usage
To use the script, save it as a Python file (e.g., proxy_tester.py) and run it from the command line using Python. The script takes one optional argument, "-t" or "--test", which tells it to test the proxies.

To test the proxies, run the script with the argument: 

```python proxy_grabber.py -t```

Otherwise, simply run the script with 

```python proxy_grabber.py``` to grab proxy list

<img src="https://raw.githubusercontent.com/r0xd4n3t/proxy-grab/main/img/1.png"></img>

## 📝 Prerequisites
The script requires the installation of the following Python modules:

-   argparse
-   concurrent.futures
-   requests
-   beautifulsoup4

These modules can be installed using pip by running "pip install argparse concurrent.futures requests beautifulsoup4" in the terminal.

<p align="center"><a href=#top>Back to Top</a></p>
