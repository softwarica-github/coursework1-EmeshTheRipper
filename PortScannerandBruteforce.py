import tkinter as tk
import threading
import subprocess

class PortScannerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Port Scanner and Brute Force Tool")
        self.create_widgets()

    def create_widgets(self):
        # Port Scanning Section
        self.port_scan_frame = tk.LabelFrame(self.root, text="Port Scanning")
        self.port_scan_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.target_ip_label = tk.Label(self.port_scan_frame, text="Enter the target IP address:")
        self.target_ip_label.pack()
        self.target_ip_entry = tk.Entry(self.port_scan_frame)
        self.target_ip_entry.pack()

        self.scan_button = tk.Button(self.port_scan_frame, text="Scan Ports", command=self.start_port_scan)
        self.scan_button.pack()

        self.port_scan_output = tk.Text(self.port_scan_frame, height=10, width=50)
        self.port_scan_output.pack()

        # Brute Force Section
        self.brute_force_frame = tk.LabelFrame(self.root, text="Brute Force")
        self.brute_force_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.target_url_label = tk.Label(self.brute_force_frame, text="Enter the target URL:")
        self.target_url_label.pack()
        self.target_url_entry = tk.Entry(self.brute_force_frame)
        self.target_url_entry.pack()

        self.brute_force_button = tk.Button(self.brute_force_frame, text="Start Brute Force", command=self.start_brute_force)
        self.brute_force_button.pack()

        self.brute_force_output = tk.Text(self.brute_force_frame, height=10, width=50)
        self.brute_force_output.pack()

    def start_port_scan(self):
        target_ip = self.target_ip_entry.get()
        self.port_scan_output.delete(1.0, tk.END)  # Clear previous output
        self.port_scan_output.insert(tk.END, f"Scanning ports for {target_ip}...\n")

        t = threading.Thread(target=self.run_nmap_scan, args=(target_ip,))
        t.start()

    def run_nmap_scan(self, target_ip):
        try:
            result = subprocess.run(["nmap", "-A", target_ip], capture_output=True, text=True, timeout=300)
            self.port_scan_output.insert(tk.END, result.stdout)
        except subprocess.TimeoutExpired:
            self.port_scan_output.insert(tk.END, "Port scanning timed out.\n")
        except Exception as e:
            self.port_scan_output.insert(tk.END, f"Error during port scanning: {e}\n")

    def start_brute_force(self):
        target_url = self.target_url_entry.get()
        self.brute_force_output.delete(1.0, tk.END)  # Clear previous output
        self.brute_force_output.insert(tk.END, f"Brute forcing {target_url}...\n")

        t = threading.Thread(target=self.run_gobuster, args=(target_url,))
        t.start()

    def run_gobuster(self, target_url):
        try:
            result = subprocess.run(["gobuster", "dir", "-u", target_url, "-w", "/usr/share/wordlists/dirb/common.txt", "-t", "50", "-q"], capture_output=True, text=True, timeout=300)
            self.brute_force_output.insert(tk.END, result.stdout)
        except subprocess.TimeoutExpired:
            self.brute_force_output.insert(tk.END, "Brute forcing timed out.\n")
        except Exception as e:
            self.brute_force_output.insert(tk.END, f"Error during brute force: {e}\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PortScannerApp()
    app.run()
