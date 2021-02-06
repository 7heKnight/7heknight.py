from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import re

DRIVER = r'driver_location'
URL = r'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1'
compileIP = re.compile(r'''	<td>(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})</td>
    <td>(\w{1,})</td>''')
compileHREF = re.compile(r'<td align="left"><a>More Free Proxies</a>(.*)</td>')

def getHTML():
    # browser = webdriver.Chrome(executable_path=DRIVER)
    # browser.get(URL)
    # html = browser.page_source
    html = requests.get(URL).text
    # print(html)
    # time.sleep(10)
    return html

def parseHTML(html):
    ipAddress = re.findall(compileIP, html)
    pages = re.findall(compileHREF, html)
    href = re.findall(r"<a href=\\'(Fresh-HTTP-Proxy-List-\d{1,})\\'>", str(pages))
    for i in range(len(href)):
        href[i] = r'https://list.proxylistplus.com/' + href[i]
    for i in range(len(ipAddress)):
        ipAddress[i] = ipAddress[i][0]+ ':' + ipAddress[i][1]
    print(href)
    print(ipAddress)

if __name__ == '__main__':
    html = getHTML()
    parseHTML(html)

