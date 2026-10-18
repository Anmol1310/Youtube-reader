"""HTTP API for YouTube Reader. Stdlib only (the transcript lib lives in .venv).

    .venv/bin/python server.py      # serves on http://localhost:8081

    POST /read   {"url": "https://www.youtube.com/watch?v=..."}  -> JSON
    GET  /health                                              -> {"ok": true}
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from yt import read_video


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"ok": True, "service": "youtube-reader", "v": 1})
        else:
            self._send(404, {"error": "use POST /read"})

    def do_POST(self):
        if self.path != "/read":
            self._send(404, {"error": "use POST /read"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            self._send(200, read_video(payload.get("url", "")))
        except ValueError:
            self._send(400, {"error": "send {\"url\": \"youtube link\"}"})
        except Exception:
            self._send(502, {"error": "read_failed"})

    def log_message(self, *args):
        pass  # quiet


if __name__ == "__main__":
    import os
    # Railway (and most hosts) give us a PORT env var and require 0.0.0.0.
    # Local runs still default to 127.0.0.1:8081.
    port = int(os.environ.get("PORT", "8081"))
    host = "0.0.0.0" if "PORT" in os.environ else "127.0.0.1"
    srv = HTTPServer((host, port), Handler)
    print("YouTube Reader API on http://%s:%d  (POST /read)" % (host, port))
    srv.serve_forever()
