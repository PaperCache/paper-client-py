import unittest
from tests.tester import Tester

class TestSize(Tester):
	def test_size_existent(self):
		self.client.set("key", "value")
		(is_ok, data) = self.client.size("key")

		self.assertTrue(is_ok)
		self.assertEqual(data, 5)

	def test_size_non_existent(self):
		(is_ok, data) = self.client.size("key")

		self.assertFalse(is_ok)
		self.assertNotEqual(data, 5)

if __name__ == "__main__":
	unittest.main()
