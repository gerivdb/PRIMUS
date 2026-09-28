#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.logic.benchmark.benchmark_latency import benchmark_latency, BenchmarkResult


def test_benchmark_returns_result():
    result = benchmark_latency("http://localhost:9999", runs=1)
    assert isinstance(result, BenchmarkResult)
    assert result.error is not None


def test_benchmark_success():
    import http.server
    import threading

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"{}")

        def log_message(self, *args, **kwargs):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        result = benchmark_latency(f"http://127.0.0.1:{port}", runs=3)
        assert isinstance(result, BenchmarkResult)
        assert result.error is None
        assert result.avg_ms >= 0
    finally:
        server.shutdown()


if __name__ == "__main__":
    test_benchmark_returns_result()
    test_benchmark_success()
    print("OK: All benchmark_latency tests passed")
