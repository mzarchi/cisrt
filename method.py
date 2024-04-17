import time
import re

def showArp(shell, ip):
    shell.send(f"show arp {ip}\n")
    time.sleep(1)
    text = shell.recv(65535).decode("utf-8")
    mac_pattern = r'\s*([0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4})'
    return re.findall(mac_pattern, text)

def showMacAddressTable(shell, mac):
    result = {}
    shell.send(f"show mac address-table | include {mac}\n")
    time.sleep(1)
    text = shell.recv(65535).decode("utf-8")
    result['text'] = text
    result['port'] = re.findall(r'\w+\/(?:\w+\/)*\w+', text)
    return result
    
def showCdpNeighborsDetails(shell, port):
    result = {}
    shell.send(f"show cdp neighbors {port} detail\n")
    time.sleep(1)
    text = shell.recv(65535).decode("utf-8")
    result['ip'] = re.findall(r'\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', text)
    result['text'] = text
    return result