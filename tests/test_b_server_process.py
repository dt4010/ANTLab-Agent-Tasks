import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


root = Path(__file__).resolve().parents[1]
cwd = root / "进阶" / "challenge_b"
server = subprocess.Popen(
    [sys.executable, "server.py", "--engine", "fixed_engine:Engine", "--port", "8768"],
    cwd=cwd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
try:
    time.sleep(0.5)
    req = urllib.request.Request(
        "http://127.0.0.1:8768/api/run",
        data=json.dumps({"case_id": "R02", "reset": True}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    value = json.load(urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req))
    assert [item["id"] for item in value["evidence"]] == ["b02"]
    assert value["actual_scope"]["snapshot"] == "v2"
    print("server process check passed")
finally:
    server.terminate()
    stdout, stderr = server.communicate(timeout=5)
