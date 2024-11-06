from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from backend.db_connection import (
    fetch_users,
    fetch_tilat,
    fetch_varaukset,
    add_tila,
    add_varaaja,
    add_varaus,
    delete_tila,
    delete_varaaja,
    delete_varaus
)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("templates/index.html", "rb") as f:
                self.wfile.write(f.read())

        elif self.path == "/data":
            tilat = fetch_tilat()
            users = fetch_users()
            varaukset = fetch_varaukset()

            # Create a response JSON
            response = {"tilat": tilat, "varaajat": users, "varaukset": varaukset}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        elif self.path == "/tilat":
            tilat = fetch_tilat()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(tilat).encode())

        elif self.path == "/varaajat":
            users = fetch_users()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(users).encode())

        elif self.path == "/varaukset":
            varaukset = fetch_varaukset()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(varaukset).encode())

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 - Not Found")


    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/add_tila":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            add_tila(data["tilan_nimi"])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"message": "Tila added"}')

        elif parsed_path.path == "/add_varaaja":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            add_varaaja(data["nimi"])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"message": "Varaaja added"}')

        elif parsed_path.path == "/add_varaus":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            tila_id = data["tila_id"]
            varaaja_id = data["varaaja_id"]
            varauspaiva = data["varauspaiva"]
            add_varaus(tila_id, varaaja_id, varauspaiva)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"message": "Varaus added"}')

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith("/delete_tila/"):
            tila_id = parsed_path.path.split("/delete_tila/")[1]
            warning = delete_tila(int(tila_id))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"warning": warning}).encode())

        elif parsed_path.path.startswith("/delete_varaaja/"):
            varaaja_id = parsed_path.path.split("/delete_varaaja/")[1]
            warning = delete_varaaja(int(varaaja_id))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"warning": warning}).encode())

        elif parsed_path.path.startswith("/delete_varaus/"):
            varaus_id = parsed_path.path.split("/delete_varaus/")[1]
            deleted = delete_varaus(int(varaus_id))
            if deleted:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"message": "Varaus deleted"}')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"message": "No varaus found with that ID"}')

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 - Not Found')


server = HTTPServer(("localhost", 8000), MyHandler)
print("Server running on http://localhost:8000")
server.serve_forever()
