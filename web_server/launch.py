from http.server import HTTPServer, CGIHTTPRequestHandler
from config import Config

server_address = ("", Config.webPort)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()
