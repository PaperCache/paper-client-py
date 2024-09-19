import unittest
from tests.tester import Tester
from paper_client import PaperError

class TestTtl(Tester):
	def test_ttl_existent(self):
		self.client.set("key", "value")
		(is_ok, _) = self.client.ttl("key", 5)

		self.assertTrue(is_ok)

	def test_ttl_non_existent(self):
		(is_ok, error) = self.client.ttl("key", 5)

		self.assertFalse(is_ok)
		self.assertEqual(error, PaperError.KEY_NOT_FOUND)

if __name__ == "__main__":
	unittest.main()
