import unittest
from paper_client.client import PaperClient

class TestPing(unittest.TestCase):
	def test_auth_incorrect(self):
		client = PaperClient()
		(is_ok, _) = client.auth("incorrect_auth_token")
		self.assertFalse(is_ok)
		client.disconnect()

	def test_auth_correct(self):
		client = PaperClient()
		(is_ok, _) = client.auth("auth_token")
		self.assertTrue(is_ok)
		client.disconnect()

if __name__ == "__main__":
	unittest.main()
