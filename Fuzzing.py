import socket
import subprocess
import threading
import tkinter as tk
from tkinter import ttk

class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner with Gobuster")
        
        # Create style
        self.style = ttk.Style()
        self.style.configure("Bold.TLabel", font=('Helvetica', 14, 'bold'))
        self.style.configure("Red.TLabel", foreground="red")
        self.style.configure("Green.TLabel", foreground="green")
        self.style.configure("Blue.TLabel", foreground="blue")
        
        # Port Scanning Section
        self.create_port_scanning_section()
        
        # Gobuster Section
        self.create_gobuster_section()

        # Text Area for displaying output
        self.text_area = tk.Text(root, height=15, width=50)
        self.text_area.pack(pady=10)

        # Configure text tags for color coding
        self.text_area.tag_configure("green", foreground="green")
        self.text_area.tag_configure("red", foreground="red")
        self.text_area.tag_configure("blue", foreground="blue")
        self.text_area.tag_configure("bold", font=('Helvetica', 14, 'bold'))
        
        # Thread variable to keep track of the scanning thread
        self.scanning_thread = None
        # Flag to indicate if scanning should be stopped
        self.stop_scan_flag = False

    def create_port_scanning_section(self):
        port_scan_frame = ttk.Frame(self.root, relief=tk.GROOVE, padding=(10, 10, 10, 0))
        port_scan_frame.pack(pady=10, padx=10)
        
        port_scan_header = ttk.Label(port_scan_frame, text="Port Scanning", style="Bold.TLabel")
        port_scan_header.grid(row=0, column=0, sticky="w")
        
        port_scan_subframe = ttk.Frame(port_scan_frame)
        port_scan_subframe.grid(row=1, column=0, sticky="ew")
        port_scan_subframe.columnconfigure(1, weight=1)
        
        ttk.Label(port_scan_subframe, text="Target Host:", anchor="e").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.target_host_entry = ttk.Entry(port_scan_subframe, width=30, font=('Helvetica', 12))
        self.target_host_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        self.target_host_entry.insert(tk.END, "127.0.0.1")  # Default value
        
        ttk.Label(port_scan_subframe, text="Start Port:", anchor="e").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.start_port_entry = ttk.Entry(port_scan_subframe, width=10, font=('Helvetica', 12))
        self.start_port_entry.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.start_port_entry.insert(tk.END, "1")  # Default value
        
        ttk.Label(port_scan_subframe, text="End Port:", anchor="e").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.end_port_entry = ttk.Entry(port_scan_subframe, width=10, font=('Helvetica', 12))
        self.end_port_entry.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        self.end_port_entry.insert(tk.END, "1024")  # Default value
        
        self.scan_ports_button = ttk.Button(port_scan_subframe, text="Scan Ports", command=self.start_scan_ports, style="Bold.TButton")
        self.scan_ports_button.grid(row=3, column=0, columnspan=2, pady=(5,0))
        
        self.clear_button = ttk.Button(port_scan_subframe, text="Clear", command=self.clear_text_area, style="Bold.TButton")
        self.clear_button.grid(row=4, column=0, columnspan=2, pady=(5,0))
        
        self.stop_scan_button = ttk.Button(port_scan_subframe, text="Stop", command=self.stop_scan_ports, style="Bold.TButton")
        self.stop_scan_button.grid(row=5, column=0, columnspan=2, pady=(5,0))
        self.stop_scan_button.configure(state=tk.DISABLED)  # Disable initially

        # Output section for Port Scan
        self.port_scan_output_frame = ttk.Frame(port_scan_frame, relief=tk.GROOVE, padding=(10, 0, 10, 10))
        self.port_scan_output_frame.grid(row=2, column=0, sticky="nsew")

        ttk.Label(self.port_scan_output_frame, text="Port Scan Output", style="Bold.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.port_scan_output_text = tk.Text(self.port_scan_output_frame, height=5, width=50, font=('Helvetica', 10))
        self.port_scan_output_text.grid(row=1, column=0, pady=5)
        self.port_scan_output_text.tag_configure("green", foreground="green")
        self.port_scan_output_text.tag_configure("red", foreground="red")
        self.port_scan_output_text.tag_configure("bold", font=('Helvetica', 10, 'bold'))

    def create_gobuster_section(self):
        gobuster_frame = ttk.Frame(self.root, relief=tk.GROOVE, padding=(10, 10, 10, 0))
        gobuster_frame.pack(pady=10, padx=10)
        
        gobuster_header = ttk.Label(gobuster_frame, text="Gobuster", style="Bold.TLabel")
        gobuster_header.grid(row=0, column=0, sticky="w", pady=5)
        
        gobuster_subframe = ttk.Frame(gobuster_frame)
        gobuster_subframe.grid(row=1, column=0, sticky="ew")
        gobuster_subframe.columnconfigure(1, weight=1)
        
        ttk.Label(gobuster_subframe, text="Target URL:", anchor="e").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.target_url_entry = ttk.Entry(gobuster_subframe, width=30, font=('Helvetica', 12))
        self.target_url_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        
        self.gobuster_scan_button = ttk.Button(gobuster_subframe, text="Run Gobuster", command=self.run_gobuster, style="Bold.TButton")
        self.gobuster_scan_button.grid(row=1, column=0, columnspan=2, pady=(5,0))
        
        # Output section for Gobuster
        self.gobuster_output_frame = ttk.Frame(gobuster_frame, relief=tk.GROOVE, padding=(10, 0, 10, 10))
        self.gobuster_output_frame.grid(row=2, column=0, sticky="nsew")

        ttk.Label(self.gobuster_output_frame, text="Gobuster Output", style="Bold.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.gobuster_output_text = tk.Text(self.gobuster_output_frame, height=5, width=50, font=('Helvetica', 10))
        self.gobuster_output_text.grid(row=1, column=0, pady=5)
        self.gobuster_output_text.tag_configure("blue", foreground="blue")
        self.gobuster_output_text.tag_configure("red", foreground="red")
        self.gobuster_output_text.tag_configure("bold", font=('Helvetica', 10, 'bold'))

        # Hide the Gobuster section initially
        gobuster_frame.configure(height=0)
        self.gobuster_frame = gobuster_frame
        
    def start_scan_ports(self):
        self.stop_scan_flag = False
        self.port_scan_output_text.delete(1.0, tk.END)
        self.stop_scan_button.configure(state=tk.NORMAL)  # Enable stop button
        self.scan_ports_button.configure(state=tk.DISABLED)  # Disable scan button
        self.scanning_thread = threading.Thread(target=self.scan_ports)
        self.scanning_thread.start()
        
    def stop_scan_ports(self):
        if self.scanning_thread and self.scanning_thread.is_alive():
            self.stop_scan_flag = True
            self.stop_scan_button.configure(state=tk.DISABLED)  # Disable stop button

    def scan_ports(self):
        target_host = self.target_host_entry.get()
        start_port = int(self.start_port_entry.get())
        end_port = int(self.end_port_entry.get())
        self.port_scan_output_text.insert(tk.END, f"Scanning ports for {target_host}...\n", "bold")
        for port in range(start_port, end_port + 1):
            # Check if the stop flag is set
            if self.stop_scan_flag:
                self.port_scan_output_text.insert(tk.END, "Port scan stopped.\n", "bold")
                self.scan_ports_button.configure(state=tk.NORMAL)  # Enable scan button
                return

            self.port_scan_output_text.insert(tk.END, f"Scanning port {port}...\n")
            try:
                # Create a socket object
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Set a timeout for the connection attempt
                sock.settimeout(1)
                # Attempt to connect to the target host and port
                result = sock.connect_ex((target_host, port))
                if result == 0:
                    self.port_scan_output_text.insert(tk.END, f"Port {port}/TCP is open\n", "green")
                else:
                    self.port_scan_output_text.insert(tk.END, f"Port {port}/TCP is closed\n", "red")
                # Close the socket
                sock.close()
            except socket.error:
                self.port_scan_output_text.insert(tk.END, f"Could not connect to {target_host}:{port}\n", "red")

            # Check if the stop flag is set after each port
            if self.stop_scan_flag:
                self.port_scan_output_text.insert(tk.END, "Port scan stopped.\n", "bold")
                self.scan_ports_button.configure(state=tk.NORMAL)  # Enable scan button
                return

    def run_gobuster(self):
        self.gobuster_output_text.delete(1.0, tk.END)
        target_url = self.target_url_entry.get()
        wordlist = "/usr/share/wordlists/dirb/common.txt"  # Default wordlist path
        self.gobuster_output_text.insert(tk.END, f"Running Gobuster on {target_url}...\n", "bold")
        try:
            result = subprocess.run(["gobuster", "dir", "-u", target_url, "-w", wordlist], capture_output=True, text=True)
            if result.returncode == 0:
                self.gobuster_output_text.insert(tk.END, result.stdout, "blue")
            else:
                self.gobuster_output_text.insert(tk.END, result.stderr, "red")
        except FileNotFoundError:
            self.gobuster_output_text.insert(tk.END, "Gobuster not found. Please make sure it's installed and added to your PATH.\n", "red")
                
    def clear_text_area(self):
        self.text_area.delete(1.0, tk.END)
        self.port_scan_output_text.delete(1.0, tk.END)
        self.gobuster_output_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()
