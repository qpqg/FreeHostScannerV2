#-*-coding:utf8;-*-
#qpy:2
#qpy:console

import requests
from threading import Thread

from os import system, popen
import socket
 
site_path = "/storage/sdcard1/QZ/Subdomain/Axis,telkomsel,dll/viu.txt"

proxy_path = "/storage/emulated/0/pp4.txt"

#Log_save
log_status = "/storage/emulated/0/FreeHostScan/log_status.txt"

#Method
methods_list = ["GET","POST","HEAD","TRACE","MOVE","PATCH"]

#search_status_code
status_codes = [200, 302, 400]

#Putuskan_paksa_pada
timeouts = 3
#Get Host name Time Out
set_hostname_TM = 2

garis = "="*25
def baleho():
    print garis
    print green("Simple Free Host Scanner").replace("\n","")
    print "Author: ", bad("Qiuby Zhukhi").replace("\n","")
    print garis
    
def user_details():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()
        print green("IP Local ISP: " + ip[0]).split("\n")[0]
        print green("Your Host Name: " + requests.request("GET", "http://api.webprovider.cz/ip.php", timeout=set_hostname_TM).json()["ip"])
    
    except socket.error as e:
        print eror(e)
    except requests.exceptions.Timeout:
        print eror("Your Host Name: " + "CAN'T DETECTED")
    print "Network type: " + open_info('gsm.network.type')
    print "[DNS INFO]"
    print " - NetDns: ", open_info("net.dns1")
    print " - DNS 1: ", open_info("net.ppp0.dns1")
    print " - DNS 2: ", open_info("net.ppp0.dns2")
    print "[WLAN0 INFO]"
    print " - Gateway: " + open_info("dhcp.wlan0.gateway")
    print " - SubnetMask: " + open_info("dhcp.wlan0.mask")
    print " - wlan0 DNS 1: " + open_info("dhcp.wlan0.dns1")
    print " - wlan0 DNS 2: " + open_info("dhcp.wlan0.dns2")
    print " - wlan0 Ip Address: " + open_info("dhcp.wlan0.ipaddress")
    print garis

def open_info(s):
    return popen("getprop "+s).read().split("\n")[0]
def green(s):
    return "\033[1;32;40m{}\033[00m \n".format(s)
def eror(s):
    return "\033[1;31;40m{}\033[00m \n".format(s)
def bad(s):
    return "\033[93m{}\033[00m \n".format(s)
def headers_color(v, k):
    return "\033[1;36;40m-{}\033[00m : \033[1;37;40m{}\033[00m".format(k,v)

def save_files(f, isi):
    print "Saved to: " + green(f)
    print "Format\r\n" + green(isi)
    with open(f, "a+") as salin:
        	salin.writelines(isi)
        	salin.close()
        
#OpenProxy
def open_files(file):
    ok_proxy = []
    list_proxy = open(file).readlines()
    for proxy in list_proxy:
        proxy = proxy.replace("\n","")
        proxy, port = proxy.split(":")
        ok_proxy.append([proxy,port])
    return ok_proxy

#Open Site list
def list_sites(f):
    ok_site = []
    sites = open(f).readlines()
    for site in sites:
        site = site.replace("\n","")
        if site.startswith("http://") or site.startswith("https://"):
            ok_site.append(site)
        else:
            site = "http://"+site
            ok_site.append(site)
    return ok_site

#Configuration for web responses
def webdriver(site,methods=None, prox=None):
    global proxy
    print "Scan [%s] [%s]" % (methods, site)
    if prox != None:
        proxy = prox["http"].replace("http://","")
        print "Proxy: [%s] " % (proxy)
    else:
        proxy = "Direct Proxy"
        print "Proxy Mode: " + proxy
    try:
        qiubyz = requests.request(method=methods, url=site, proxies=prox, timeout=timeouts)
        if qiubyz.status_code in status_codes:
            print "[SERVER RESPONSE]\n- Status Code: %s" % (green(qiubyz.status_code))
        else:
            print "[SERVER RESPONSE]\n- Status Code: %s" % (bad(qiubyz.status_code))
        print "\n".join([headers_color(v, k) for k, v in qiubyz.headers.items()])
           
        format_isi = "Method: [{}]\nHost: [{}]\nProxy Mode: [{}]\nStatus: [{}]\r\n\r\n".format(methods,site, proxy, qiubyz.status_code)
        save_files(log_status, format_isi)
    except Exception as e:
        print eror(str(e))
    print garis + "\r\n"

def startget():
    for site in open_sites:
        singT(m=webdriver, argumen=(site, "GET", None))

def start_random_method():
    for sit in open_sites:
        for method in methods_list:
           singT(m=webdriver, argumen=(sit, method, None))

def start_random_method_proxy():
    for proxy in open_proxy:
        proxy, port = proxy[0], proxy[1]
        format = { 'http': 'http://{}:{}'.format(proxy,port)}
        for site in open_sites:
            for method in methods_list:
                singT(m=webdriver, argumen=(site, method, format))
                
def proxy_get():
    for proxy in open_proxy:
        proxy, port = proxy[0], proxy[1]
        format = { 'http': 'http://{}:{}'.format(proxy,port)}
        for site in open_sites:
            singT(m=webdriver, argumen=(site, 'GET', format))

def proxy_testing():
    for proxy in open_proxy:
        proxy, port = proxy[0], proxy[1]
        format = { 'http': 'http://{}:{}'.format(proxy,port)}
        singT(webdriver, (format["http"], 'CONNECT', format))

#Youcan mod this thread
def singT(m=None, argumen=None):
    t = Thread(target=m, args=argumen)
    t.daemon = True
    t.start()
    t.join()
    
def Options():
    global open_sites
    global open_proxy
    dic = {
    	1:"1. Method \'GET\' SCANNER HostList", 
    	2:"2. HostList + MethodList",
    	3:"3. ProxyList + MethodList + HostList scanner",
    	4:"4. ProxyList + HostList + Method \'GET\' ",
    	5:"5. ProxyList Testing"
    	}
    while 1:
        baleho()
        user_details()
        print "====== [ M E N U ] ======"
        print "\n".join([ m for _, m in dic.items()])
        try:
            ops = int(raw_input("Input nomor: "))
            print garis
            print dic[ops]
            print garis+"\r\n"
        except KeyError as e:
            print eror("\n[Pilihan Salah: {} ]".fromat(str(e)))
            continue
        except ValueError as e:
            print eror("\n[{}]".format(str(e)))
            continue
        except Exception as e:
            print eror("\n[{}]".format(str(e)))
            
        try:
            site_path = raw_input("Insert your pathsite: ")
            open_sites = list_sites(site_path)
        except Exception as e:
            print eror("\n[{}]".format(str(e)))
            continue
        print garis
        if ops == 1: startget()
        elif ops == 2: start_random_method()
        elif ops == 3:
            try:
                proxy_path = raw_input("Insert your Path proxy: ")
                open_proxy = open_files(proxy_path)
                start_random_method_proxy()
            except Exception as e:
                print "Directory: " , eror(str(e))
                continue
        elif ops == 4:
            proxy_path = raw_input("Insert your Path proxy: ")
            open_proxy = open_files(proxy_path)
            proxy_get()
        elif ops == 5:
            proxy_path = raw_input("Insert your Path proxy: ")
            open_proxy = open_files(proxy_path)
            proxy_testing()
        else: print "Silahkan untuk menambahkan opsinya sendiri"
        break
    system("clear")
if __name__ == "__main__":
    Options()
