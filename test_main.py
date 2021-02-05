from main import app
import unittest
import requests


class Json_testcase(unittest.TestCase):
    def test_get_method(self):
        url = 'http://127.0.0.1:8000/'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
