import socket
import threading
import unittest
import requests
import subprocess

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
        except ConnectionRefusedError:
            print(f"Connection to port {port} was refused.")
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

    def run_gobuster(self, target_url):
        results = []
        wordlist = "/usr/share/wordlists/dirb/common.txt"  # Default wordlist path
        results.append(f"Running Gobuster on {target_url}...")
        try:
            result = subprocess.run(["gobuster", "dir", "-u", target_url, "-w", wordlist], capture_output=True, text=True)
            if result.returncode == 0:
                results.extend(result.stdout.splitlines())
            else:
                results.append(result.stderr)
        except FileNotFoundError:
            results.append("Gobuster not found. Please make sure it's installed.")
        except Exception as e:
            results.append(f"Error running Gobuster: {e}")

        return results

class TestPortScanner(unittest.TestCase):
    def test_scan(self):
        target_ip = input("Enter the target IP address: ")
        brute_force_option = input("Do you want to perform brute force? (yes/no): ").lower()
        scanner = PortScanner(target_ip, [20, 21, 22, 23, 80, 443, 8080])
        open_ports = scanner.scan()
        print("Open Ports:", open_ports)

        try:
            response = requests.get(f"http://{target_ip}/")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error making HTTP request: {e}")
        else:
            self.assertEqual(response.status_code, 200)

        if brute_force_option == "yes":
            target_url = f"http://{target_ip}/"
            brute_forcer = PortScanner(target_ip, [80])  # Assuming only HTTP port for directory brute forcing
            brute_force_results = brute_forcer.run_gobuster(target_url)
            print("\nBrute Force Results:")
            for result in brute_force_results:
                print(result)

if __name__ == "__main__":
    unittest.main()
