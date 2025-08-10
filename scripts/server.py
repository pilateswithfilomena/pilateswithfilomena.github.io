#!/usr/bin/env python3

import http.server
import socketserver
import os
import urllib.parse

PORT = 3000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # parse URL to remove params
        parsed_url = urllib.parse.urlparse(self.path)
        path_without_params = parsed_url.path

        original_path = path_without_params
        html_path = f"{original_path}.html"
        file_path = self.translate_path(original_path)
        html_file_path = self.translate_path(html_path)

        # if request file does not exist but version with .html does, use that
        if not os.path.exists(file_path) and os.path.exists(html_file_path):
          self.path = html_path

        super().do_GET()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at: http://localhost:{PORT}")
    httpd.serve_forever()
