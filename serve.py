#!/usr/bin/env python3
"""AI-Class static file server — fixed port 4200."""

import http.server
import os
import sys

PORT = 4200
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

os.chdir(DIRECTORY)

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

with http.server.HTTPServer(("0.0.0.0", PORT), NoCacheHandler) as httpd:
    print(f"AI-Class server running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
