from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from backend.db_connection import fetch_users, fetch_tilat, fetch_varaukset

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

            print("Fetched Users:", users)
            print("Fetched Rooms:", tilat)
            print("Fetched Reservations:", varaukset)

            # Create a response JSON
            response = {
                "tilat": tilat,
                "varaajat": users,
                "varaukset": varaukset
            }

            print("Response Data:", response)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

server = HTTPServer(('localhost', 8000), MyHandler)
print("Server running on http://localhost:8000")
server.serve_forever()
