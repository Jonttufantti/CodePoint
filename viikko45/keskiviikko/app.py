from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from random import randint
from backend.db_connection import (
    fetch_users,
    fetch_tilat,
    fetch_varaukset,
    add_tila,
    add_varaaja,
    add_varaus,
    delete_tila,
    delete_varaaja,
    delete_varaus,
    verify_user
)

sessions = {}

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/login": self.login_page,
            "/logout": self.logout,
            "/": self.home,
            "/tilat": self.fetch_tilat,
            "/varaajat": self.fetch_varaajat,
            "/varaukset": self.fetch_varaukset
        }

        self.cookie = None

        try:
            response = 200
            cookies = self.parse_cookies(self.headers["Cookie"])
            if "sid" in cookies:
                self.user = cookies["sid"] if (cookies["sid"] in sessions) else False
            else:
                self.user = False

            if not self.user and self.path not in routes:
                response = 403
                content = "Access Denied"
            else:
                content = routes.get(self.path, self.not_found)()

        except Exception:
            response = 404
            content = "Not Found"
   
        self.send_response(response)
        self.send_header('Content-type','text/html')

        if self.cookie:
            self.send_header('Set-Cookie', self.cookie)
        
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

        # Handle the root path to serve index.html
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("templates/index.html", "rb") as f:
                self.wfile.write(f.read())

        # General case for handling .html pages
        elif self.path.endswith(".html"):
            page = self.path[1:]  # Remove the leading slash
            try:
                with open(f"templates/{page}", "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_response(404)
                self.send_header("Content-Type", "text/html")
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
            self.wfile.write(b"404 - Not Found")

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        force = 'force' in query_params and query_params['force'][0].lower() == 'true'

        if parsed_path.path.startswith("/delete_tila/"):
            tila_id = parsed_path.path.split("/delete_tila/")[1]
            warning = delete_tila(int(tila_id), force)
            if warning:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"warning": warning}).encode())
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"message": "Tila deleted"}')

        elif parsed_path.path.startswith("/delete_varaaja/"):
            varaaja_id = parsed_path.path.split("/delete_varaaja/")[1]
            warning = delete_varaaja(int(varaaja_id), force)
            if warning:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"warning": warning}).encode())
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"message": "Varaaja deleted"}')

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

    
    def home(self):
        return "Welcome User!" if self.user else "Welcome Stranger!"
    
    def login_page(self):
        with open("templates/login.html", "rb") as f:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(f.read())

    def login(self):
        # Handle login logic
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        data = parse_qs(body.decode("utf-8"))

        username = data.get("username", [None])[0]
        password = data.get("password", [None])[0]

        if username and password:
            user = verify_user(username, password)
            if user:
                sid = self.generate_sid()
                self.cookie = f"sid={sid}"
                sessions[sid] = {"username": username}
                return f"Logged in as {username}"
            else:
                return "Invalid credentials"
        return "Missing username or password"
 
    def logout(self):
        if not self.user:
            return "No user is logged in"
        
        self.cookie = "sid="
        del sessions[self.user]
        return "Logged out"
    
    def fetch_tilat(self):
        tilat = fetch_tilat()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(tilat).encode())

    def fetch_varaajat(self):
        users = fetch_users()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(users).encode())

    def fetch_varaukset(self):
        varaukset = fetch_varaukset()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(varaukset).encode())
    
    def not_found(self):
        return "404 Not Found"

    def generate_sid(self):
        return "".join(str(randint(1,9)) for _ in range(100))
    
    def parse_cookies(self, cookie_list):
        return dict(((c.split("=")) for c in cookie_list.split(";"))) if cookie_list else {}



server = HTTPServer(("localhost", 8000), MyHandler)
print("Server running on http://localhost:8000")
server.serve_forever()
