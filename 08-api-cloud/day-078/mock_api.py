"""
mock_api.py - a tiny local REST API for practising HTTP without the internet.

It runs in a background thread on 127.0.0.1 using only the standard library.
Usage in your scripts:

    import mock_api
    BASE_URL = mock_api.start()        # e.g. "http://127.0.0.1:54321"

Endpoints
    GET    /health                      -> {"status": "ok", "version": "1.0.0"}
    GET    /api/servers[?env=prod&page=1&per_page=2]
    GET    /api/servers/<id>
    POST   /api/servers                 JSON body {"name": ..., "env": ...} -> 201
    PUT    /api/servers/<id>            JSON body (partial update)
    DELETE /api/servers/<id>            -> 204
    POST   /api/token                   JSON {"client_id": "demo-client", "client_secret": "demo-secret"}
    GET    /api/secure/metrics          header "Authorization: Bearer <token>"
    GET    /api/keyed/report            header "X-API-Key: demo-api-key"
    GET    /status/<code>               responds with that HTTP status
    GET    /flaky                       fails twice with 503, then succeeds (per process)
    GET    /slow?seconds=N              waits N seconds before answering
    POST   /echo                        returns the request headers and body it received
All credentials here are FAKE demo values for local practice only.
"""
import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

VALID_CLIENT = ("demo-client", "demo-secret")
VALID_API_KEY = "demo-api-key"
_TOKENS = {}
_STATE = {"flaky_calls": 0, "next_id": 4}
_SERVERS = {
    1: {"id": 1, "name": "web-01", "env": "prod", "cpu": 4, "status": "running"},
    2: {"id": 2, "name": "web-02", "env": "prod", "cpu": 4, "status": "running"},
    3: {"id": 3, "name": "batch-01", "env": "dev", "cpu": 8, "status": "stopped"},
}
_server = None
_lock = threading.Lock()


class _Handler(BaseHTTPRequestHandler):
    server_version = "MockAPI/1.0"

    def log_message(self, *args):          # keep the console quiet
        pass

    def _send(self, status, payload=None, headers=None):
        body = b"" if payload is None else json.dumps(payload).encode()
        self.send_response(status)
        if payload is not None:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def _json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""
        if not raw:
            return {}
        return json.loads(raw)

    def _route(self, method):
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        query = {k: v[0] for k, v in parse_qs(url.query).items()}
        try:
            return self._dispatch(method, parts, query)
        except json.JSONDecodeError:
            return self._send(400, {"error": "request body is not valid JSON"})

    def _dispatch(self, method, parts, query):
        if parts == ["health"] and method == "GET":
            return self._send(200, {"status": "ok", "version": "1.0.0"})
        if parts[:1] == ["status"] and len(parts) == 2:
            code = int(parts[1])
            return self._send(code, {"status_code": code} if code != 204 else None)
        if parts == ["flaky"]:
            with _lock:
                _STATE["flaky_calls"] += 1
                calls = _STATE["flaky_calls"]
            if calls % 3 != 0:
                return self._send(503, {"error": "temporarily unavailable", "attempt": calls},
                                  {"Retry-After": "1"})
            return self._send(200, {"status": "ok", "attempt": calls})
        if parts == ["slow"]:
            time.sleep(float(query.get("seconds", 2)))
            return self._send(200, {"status": "finally done"})
        if parts == ["echo"] and method == "POST":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode() if length else ""
            interesting = {k: v for k, v in self.headers.items()
                           if k.lower() in ("content-type", "user-agent", "authorization", "x-request-id")}
            return self._send(200, {"headers": interesting, "body": body})
        if parts == ["api", "token"] and method == "POST":
            data = self._json_body()
            if (data.get("client_id"), data.get("client_secret")) != VALID_CLIENT:
                return self._send(401, {"error": "invalid client credentials"})
            token = f"tok-{len(_TOKENS) + 1:04d}"
            _TOKENS[token] = time.time() + float(data.get("ttl", 60))
            return self._send(200, {"access_token": token, "token_type": "Bearer",
                                    "expires_in": int(float(data.get("ttl", 60)))})
        if parts == ["api", "secure", "metrics"]:
            auth = self.headers.get("Authorization", "")
            token = auth.removeprefix("Bearer ").strip()
            if not auth.startswith("Bearer ") or token not in _TOKENS:
                return self._send(401, {"error": "missing or invalid token"},
                                  {"WWW-Authenticate": "Bearer"})
            if _TOKENS[token] < time.time():
                return self._send(401, {"error": "token expired"}, {"WWW-Authenticate": "Bearer"})
            return self._send(200, {"cpu": 41.5, "memory": 63.2, "requests_per_minute": 1280})
        if parts == ["api", "keyed", "report"]:
            if self.headers.get("X-API-Key") != VALID_API_KEY:
                return self._send(403, {"error": "invalid API key"})
            return self._send(200, {"report": "daily-costs", "total_usd": 123.45})
        if parts[:2] == ["api", "servers"]:
            return self._servers(method, parts[2:], query)
        return self._send(404, {"error": f"no route for {method} /{'/'.join(parts)}"})

    def _servers(self, method, rest, query):
        with _lock:
            if not rest:
                if method == "GET":
                    items = [s for s in _SERVERS.values() if s["env"] == query.get("env", s["env"])]
                    page, per_page = int(query.get("page", 1)), int(query.get("per_page", 10))
                    start = (page - 1) * per_page
                    return self._send(200, {"items": items[start:start + per_page], "page": page,
                                            "per_page": per_page, "total": len(items)})
                if method == "POST":
                    data = self._json_body()
                    missing = [f for f in ("name", "env") if f not in data]
                    if missing:
                        return self._send(422, {"error": "missing fields", "fields": missing})
                    new_id = _STATE["next_id"]
                    _STATE["next_id"] += 1
                    item = {"id": new_id, "name": data["name"], "env": data["env"],
                            "cpu": int(data.get("cpu", 2)), "status": "provisioning"}
                    _SERVERS[new_id] = item
                    return self._send(201, item, {"Location": f"/api/servers/{new_id}"})
                return self._send(405, {"error": "method not allowed"})
            server_id = int(rest[0])
            if server_id not in _SERVERS:
                return self._send(404, {"error": f"server {server_id} not found"})
            if method == "GET":
                return self._send(200, _SERVERS[server_id])
            if method in ("PUT", "PATCH"):
                _SERVERS[server_id].update({k: v for k, v in self._json_body().items() if k != "id"})
                return self._send(200, _SERVERS[server_id])
            if method == "DELETE":
                del _SERVERS[server_id]
                return self._send(204)
            return self._send(405, {"error": "method not allowed"})

    def do_GET(self):
        self._route("GET")

    def do_POST(self):
        self._route("POST")

    def do_PUT(self):
        self._route("PUT")

    def do_PATCH(self):
        self._route("PATCH")

    def do_DELETE(self):
        self._route("DELETE")


def start(port=0):
    """Start the API once per process and return its base URL."""
    global _server
    # make sure HTTP clients talk to localhost directly, not through a corporate proxy
    for var in ("NO_PROXY", "no_proxy"):
        current = os.environ.get(var, "")
        if "127.0.0.1" not in current:
            os.environ[var] = ",".join(filter(None, [current, "127.0.0.1", "localhost"]))
    if _server is None:
        _server = ThreadingHTTPServer(("127.0.0.1", port), _Handler)
        threading.Thread(target=_server.serve_forever, daemon=True).start()
    host, real_port = _server.server_address
    return f"http://{host}:{real_port}"


if __name__ == "__main__":
    url = start(8000)
    print(f"Mock API running at {url} - press Ctrl+C to stop")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("bye")
