import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import threading
import socket

class NetworkToolsSuite:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Network Tools Suite")
        self.create_widgets()

    def create_widgets(self):
        self.port_scan_frame = tk.LabelFrame(self.root, text="Port Scanning")
        self.port_scan_frame.pack(padx=10, pady=5, fill="both", expand=True)
        self.setup_port_scanning()

        self.brute_force_frame = tk.LabelFrame(self.root, text="Brute Force")
        self.brute_force_frame.pack(padx=10, pady=5, fill="both", expand=True)
        self.setup_brute_force()

    def setup_port_scanning(self):
        tk.Label(self.port_scan_frame, text="Target IP:").pack(side=tk.LEFT, padx=5, pady=5)
        self.target_ip_entry = tk.Entry(self.port_scan_frame)
        self.target_ip_entry.pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.port_scan_frame, text="Scan", command=self.start_port_scan).pack(side=tk.LEFT, padx=5, pady=5)
        self.port_scan_output = scrolledtext.ScrolledText(self.port_scan_frame, height=5, width=50)
        self.port_scan_output.pack(padx=10, pady=5)

    def start_port_scan(self):
        target_ip = self.target_ip_entry.get()
        self.port_scan_output.delete(1.0, tk.END)
        thread = threading.Thread(target=self.run_port_scan, args=(target_ip,))
        thread.start()

    def run_port_scan(self, target_ip):
        try:
            open_ports = self.scan_ports(target_ip)
            result_text = "Open Ports: " + ", ".join(map(str, open_ports))
            self.port_scan_output.insert(tk.END, result_text)
        except Exception as e:
            print(f"Error during port scanning: {e}")  # Add this line for debugging
            self.port_scan_output.insert(tk.END, f"Error during port scanning: {e}\n")

    def scan_ports(self, target_ip):
        open_ports = []
        for port in range(1, 1025):  # Scan common ports from 1 to 1024
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        return open_ports

    def setup_brute_force(self):
        tk.Label(self.brute_force_frame, text="Target URL:").pack(side=tk.LEFT, padx=5, pady=5)
        self.target_url_entry = tk.Entry(self.brute_force_frame)
        self.target_url_entry.pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.brute_force_frame, text="Start Brute Force", command=self.start_brute_force).pack(side=tk.LEFT, padx=5, pady=5)
        self.brute_force_output = scrolledtext.ScrolledText(self.brute_force_frame, height=5, width=50)
        self.brute_force_output.pack(padx=10, pady=5)

    def start_brute_force(self):
        target_url = self.target_url_entry.get()
        self.brute_force_output.delete(1.0, tk.END)
        thread = threading.Thread(target=self.run_brute_force, args=(target_url,))
        thread.start()

    def run_brute_force(self, target_url):
        try:
            # Implement your brute force logic here
            # Use requests, urllib, or any library of your choice for HTTP requests
            # Example: result = requests.get(target_url)
            result = "Brute force results go here"
            self.brute_force_output.insert(tk.END, result)
        except Exception as e:
            self.brute_force_output.insert(tk.END, f"Error during brute force: {e}\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = NetworkToolsSuite()
    app.run()
