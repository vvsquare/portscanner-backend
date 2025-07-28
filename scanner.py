import socket
import threading
import csv
from datetime import datetime

open_ports = []
lock = threading.Lock()

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                with lock:
                    open_ports.append(port)
    except:
        pass

def run_scan(ip, ports):
    threads = []
    for port in ports:
        t = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return open_ports
