import subprocess
import time
import requests
import unittest
import os
import signal
import socket
from pathlib import Path

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

class TestUvicornIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = get_free_port()
        backend_dir = Path(__file__).resolve().parent.parent.parent  # points to .../backend
        env = os.environ.copy()
        env["PYTHONPATH"] = str(backend_dir)
        cls.server = subprocess.Popen(
            ["uvicorn", "app.main:app", "--port", str(cls.port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid,
            cwd=str(backend_dir),
            env=env
        )

        # Wait for server to start
        for _ in range(40):  # try for 20 seconds
            try:
                response = requests.get(f"http://127.0.0.1:{cls.port}")
                if response.status_code == 200:
                    break
            except requests.ConnectionError:
                time.sleep(0.5)
        else:
            # Print server logs for debugging
            if cls.server:
                try:
                    out, err = cls.server.communicate(timeout=2)
                    print("==== Uvicorn stdout ====")
                    print(out.decode())
                    print("==== Uvicorn stderr ====")
                    print(err.decode())
                except Exception as e:
                    print(f"Error reading server logs: {e}")
            cls.tearDownClass()
            raise RuntimeError(f"Server did not start in time on port {cls.port}.")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'server') and cls.server:
            try:
                if cls.server.poll() is None:
                    os.killpg(os.getpgid(cls.server.pid), signal.SIGTERM)
                    cls.server.wait()
            except ProcessLookupError:
                pass
            except Exception as e:
                print(f"Error during server teardown: {e}")
            finally:
                cls.server = None

    def test_server_root_endpoint(self):
        response = requests.get(f"http://127.0.0.1:{self.port}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome", response.text)
