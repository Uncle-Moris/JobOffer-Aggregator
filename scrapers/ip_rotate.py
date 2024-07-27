import requests
from bs4 import BeautifulSoup
import threading
import queue


def get_ips():
    """Fetches avaliable proxy IPs from free0proxy-list.net"""
    response = requests.get('https://free-proxy-list.net/')
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'lxml')
    element = soup.select_one('textarea.form-control')
    value = element.text.strip() if element else None
    ips = value.split('\n')[3:]
    return ips


def check_proxy(proxy, valid_ip):
    try:
        res = requests.get('https://justjoin.it/', proxies={"https": proxy}, timeout=5)
        if res.status_code == 200:
            valid_ip.append(proxy)
    except requests.exceptions.RequestException:
        pass


def valid_proxies_ips(ips=get_ips()):
    valid_ip = []
    q = queue.Queue()
    
    for proxy in ips:
        q.put(proxy)
    
    threads = []
    
    def worker():
        while not q.empty():
            proxy = q.get()
            check_proxy(proxy, valid_ip)
            q.task_done()
    
    for _ in range(10):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    
    q.join()
    
    for t in threads:
        t.join()
    
    return valid_ip

