from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from evaluator import evaluate

class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/submit":

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            master = "The government has announced new policies for development"

            result = evaluate(master, data["user"])

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            self.wfile.write(json.dumps(result).encode())

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("Server running on port 8000...")
server.serve_forever()
