from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from backend.db_connection import (    fetch_users,
    fetch_tilat,
    fetch_varaukset,
    add_tila,
    add_varaaja,
    delete_tila,
    delete_varaaja)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('templates/index.html', 'rb') as f:
                self.wfile.write(f.read())
        
        elif self.path == '/data':
            users = fetch_users()
            tilat = fetch_tilat()
            varaukset = fetch_varaukset()

            # Create a response JSON
            response = {
                "tilat": tilat,
                "varaajat": users,
                "varaukset": varaukset
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

    def do_POST(self):
        if self.path == '/add_tila':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            add_tila(data['tilan_nimi'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"message": "Tila added"}')

        elif self.path == '/add_varaaja':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            add_varaaja(data['nimi'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"message": "Varaaja added"}')

        elif self.path == '/delete_tila':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            warning = delete_tila(data['id'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"warning": warning}).encode())

        elif self.path == '/delete_varaaja':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            warning = delete_varaaja(data['id'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"warning": warning}).encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

server = HTTPServer(('localhost', 8000), MyHandler)
print("Server running on http://localhost:8000")
server.serve_forever()
