import unittest
from tests.tester import Tester

class TestGet(Tester):
	def test_size_existent(self):
		self.client.set("key", "value")
		(is_ok, size) = self.client.size("key")

		self.assertTrue(is_ok)
		self.assertEqual(size, 5)

	def test_size_non_existent(self):
		(is_ok, _) = self.client.size("key")

		self.assertFalse(is_ok)

if __name__ == "__main__":
	unittest.main()
