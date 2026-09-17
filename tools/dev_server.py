# -*- coding: utf-8 -*-
"""
tools/dev_server.py
Local Development Server for Manu Jungle Forever.
Serves static files from www.manujungleforever.com and automatically proxies
any /media/* or /api/* request to the live Cloudflare production endpoints.
"""

import sys
import os
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8089
WWW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'www.manujungleforever.com'))
REMOTE_BASE = "https://www.manujungleforever.com"

class LocalProxyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WWW_DIR, **kwargs)

    def do_GET(self):
        # If requested path is in /media/ and does not exist locally, proxy from R2 production
        if self.path.startswith('/media/'):
            local_path = os.path.join(WWW_DIR, self.path.lstrip('/').split('?')[0])
            if not os.path.exists(local_path):
                remote_url = f"{REMOTE_BASE}{self.path}"
                try:
                    req = urllib.request.Request(
                        remote_url,
                        headers={'User-Agent': 'Mozilla/5.0 LocalDevServer'}
                    )
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        self.send_response(resp.status)
                        for header, value in resp.getheaders():
                            if header.lower() not in ('server', 'date', 'transfer-encoding'):
                                self.send_header(header, value)
                        self.end_headers()
                        self.wfile.write(resp.read())
                    return
                except urllib.error.HTTPError as e:
                    self.send_response(e.code)
                    self.end_headers()
                    self.wfile.write(f"Media proxy error: {e}".encode())
                    return
                except Exception as e:
                    self.send_response(502)
                    self.end_headers()
                    self.wfile.write(f"Proxy connection failed: {e}".encode())
                    return

        # Normal static file serving
        return super().do_GET()

def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, LocalProxyHandler)
    print(f"Local dev server running on http://localhost:{PORT}")
    print(f"Serving files from: {WWW_DIR}")
    print(f"Proxying missing /media/* to: {REMOTE_BASE}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()

if __name__ == '__main__':
    run()
