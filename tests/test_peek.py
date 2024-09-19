import unittest
from tests.tester import Tester
from paper_client import PaperError

class TestPeek(Tester):
	def test_peek_existent(self):
		self.client.set("key", "value")
		(is_ok, data) = self.client.peek("key")

		self.assertTrue(is_ok)
		self.assertEqual(data, "value")

	def test_peek_non_existent(self):
		(is_ok, error) = self.client.peek("key")

		self.assertFalse(is_ok)
		self.assertEqual(error, PaperError.KEY_NOT_FOUND)

if __name__ == "__main__":
	unittest.main()
