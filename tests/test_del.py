import unittest
from tests.tester import Tester
from paper_client import PaperError

class TestDel(Tester):
	def test_del_existent(self):
		self.client.set("key", "value")
		(is_ok, _) = self.client.delete("key")

		self.assertTrue(is_ok)

	def test_del_non_existent(self):
		(is_ok, error) = self.client.delete("key")

		self.assertFalse(is_ok)
		self.assertEqual(error, PaperError.KEY_NOT_FOUND)

if __name__ == "__main__":
	unittest.main()
