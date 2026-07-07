"""Alnedd control plane as a local HTTP service.

- ``GET /api/dashboard`` — module registry health (READY/DEGRADED).
- ``POST /api/order`` — turn a message into a routed work order
  (``{"kind", "owner", "title", "status"}``).

Registry path: ``ALNEDD_REGISTRY`` (default ``<project>/config/modules.json``).
"""

from __future__ import annotations

import os
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT
from .core import dashboard, work_order
from .http_base import BaseServiceHandler, build_server


def registry_path() -> Path:
    raw = os.environ.get("ALNEDD_REGISTRY", "").strip()
    return Path(raw) if raw else PROJECT_ROOT / "config" / "modules.json"


def _order_route(data: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    message = str(data.get("message") or "").strip()
    if not message:
        return 400, {"ok": False, "error": "missing 'message'"}
    return 200, {"ok": True, **work_order(message)}


def _dashboard_route() -> tuple[int, dict[str, Any]]:
    return 200, {"ok": True, **dashboard(registry_path())}


class Handler(BaseServiceHandler):
    post_routes = {"/api/order": staticmethod(_order_route)}
    get_routes = {"/api/dashboard": staticmethod(_dashboard_route)}


def create_server(host: str | None = None, port: int | None = None) -> ThreadingHTTPServer:
    return build_server(Handler, host=host, port=port)


def run_server(host: str | None = None, port: int | None = None) -> None:
    from .version import __version__

    server = create_server(host=host, port=port)
    print(f"alnedd service v{__version__}: http://{server.server_address[0]}:{server.server_address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
