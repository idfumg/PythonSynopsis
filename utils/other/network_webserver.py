#!/usr/bin/env python

import http.server
import socketserver

ADDRESS = ("localhost", 80)
Handler = http.server.SimpleHTTPRequestHandler
httpd = http.server.HTTPServer(ADDRESS, Handler)
httpd.serve_forever()
