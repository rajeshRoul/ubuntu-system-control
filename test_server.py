import unittest
from unittest.mock import patch, MagicMock
import server
import json

class TestSystemControlServer(unittest.TestCase):
    def setUp(self):
        self.app = server.app.test_client()
        self.app.testing = True

    @patch('subprocess.run')
    def test_sleep(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=0)
        response = self.app.post('/sleep')
        self.assertEqual(response.status_code, 200)
        mock_subprocess.assert_called_with(['systemctl', 'suspend'], check=True)

    @patch('subprocess.run')
    def test_screenoff(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=0)
        response = self.app.post('/screenoff')
        self.assertEqual(response.status_code, 200)
        mock_subprocess.assert_called_with(['xset', 'dpms', 'force', 'off'], check=False)

    @patch('subprocess.run')
    def test_exec(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=0, stdout="test output", stderr="")
        
        # Test valid script
        payload = {"script": "echo hello"}
        response = self.app.post('/exec', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        mock_subprocess.assert_called_with("echo hello", shell=True, capture_output=True, text=True)
        
        # Test missing script
        response = self.app.post('/exec', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
