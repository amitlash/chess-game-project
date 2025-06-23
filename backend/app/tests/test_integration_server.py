import subprocess
import time
import requests
import unittest
import os
import signal

class TestUvicornIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the FastAPI server using uvicorn
        cls.server = subprocess.Popen(
            ["uvicorn", "app.main:app", "--port", "8001"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # allows clean termination later
        )

        # Wait for server to start
        for _ in range(20):  # try for 10 seconds
            try:
                response = requests.get("http://127.0.0.1:8001")
                if response.status_code == 200:
                    break
            except requests.ConnectionError:
                time.sleep(0.5)
        else:
            cls.tearDownClass()
            raise RuntimeError("Server did not start in time.")

    @classmethod
    def tearDownClass(cls):
        if cls.server:
            os.killpg(os.getpgid(cls.server.pid), signal.SIGTERM)
            cls.server.wait()

    def test_server_root_endpoint(self):
        response = requests.get("http://127.0.0.1:8001")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome", response.text)
