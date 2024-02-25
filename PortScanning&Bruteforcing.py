import socket
import threading
import unittest
import requests

class PortScanner:
    def __init__(self, target_ip, ports, timeout=1):
        self.target_ip = target_ip
        self.ports = ports
        self.timeout = timeout
        self.results = []

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target_ip, port))
            if result == 0:
                self.results.append(port)
            sock.close()
        except Exception as e:
            print(f"Error scanning port {port}: {e}")

    def scan(self):
        threads = []
        for port in self.ports:
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        return self.results

class TestPortScanner(unittest.TestCase):
    def test_scan(self):
        target_ip = input("Enter the target IP address: ")
        webpage = f"http://{target_ip}/"
        scanner = PortScanner(target_ip, [20, 21, 22, 23, 80, 443, 8080])
        open_ports = scanner.scan()
        print("Open Ports:", open_ports)
        response = requests.get(webpage)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
