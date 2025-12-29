#!/usr/bin/env python3

import http.server
import socketserver
import os
import urllib.parse
import sys
import time

PORT = 3000

# Add the current script's directory to sys.path to allow importing generate.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import generate

class TemplateWatcher:
    @staticmethod
    def run_if_needed():
        template_dir = 'templates'
        if not os.path.isdir(template_dir):
            return

        # Get the latest modification time of any file in the templates directory
        latest_template_time = 0
        for root, _, files in os.walk(template_dir):
            for file in files:
                file_path = os.path.join(root, file)
                latest_template_time = max(latest_template_time, os.path.getmtime(file_path))

        # Get the latest modification time of any generated .html file in the root
        latest_output_time = 0
        for file in os.listdir('.'):
            if file.endswith('.html'):
                latest_output_time = max(latest_output_time, os.path.getmtime(file))
                
        if latest_template_time > latest_output_time:
            print("Changes detected in templates directory, regenerating...")
            try:
                generate.main()
            except Exception as e:
                print(f"Error during regeneration: {e}")

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        TemplateWatcher.run_if_needed()
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

# Allow the server to restart immediately by reusing the port
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at: http://localhost:{PORT}")
    httpd.serve_forever()
