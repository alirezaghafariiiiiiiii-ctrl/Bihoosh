from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
from urllib.parse import urlparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.brain import Brain

brain = Brain()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            directory=str(ROOT / "frontend"),
            **kwargs
        )

    def _json(self, code, obj):
        body = json.dumps(
            obj,
            ensure_ascii=False
        ).encode()

        self.send_response(code)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(body))
        )
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/health":
            return self._json(
                200,
                {
                    "ok": True,
                    "name": "بی‌هوش",
                    "provider": "local"
                }
            )

        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path

        if path != "/api/chat":
            return self._json(
                404,
                {"error": "not found"}
            )

        try:
            length = int(
                self.headers.get("Content-Length", "0")
            )

            raw = self.rfile.read(length) or b"{}"
            data = json.loads(raw)

            reply = brain.reply(
                data.get("message", ""),
                data.get("history", [])
            )

            return self._json(
                200,
                {
                    "reply": reply,
                    "provider": "local"
                }
            )

        except Exception as e:
            return self._json(
                400,
                {"error": str(e)}
            )


if __name__ == "__main__":
    server = ThreadingHTTPServer(
        ("127.0.0.1", 7860),
        Handler
    )

    print("BI-HOOSH running at:")
    print("http://127.0.0.1:7860")

    server.serve_forever()
