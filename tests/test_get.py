import unittest
from tests.tester import Tester

class TestGet(Tester):
	def test_get_existent(self):
		self.client.set("key", "value")
		(is_ok, data) = self.client.get("key")

		self.assertTrue(is_ok)
		self.assertEqual(data, "value")

	def test_get_non_existent(self):
		(is_ok, data) = self.client.get("key")

		self.assertFalse(is_ok)
		self.assertNotEqual(len(data), 0)

if __name__ == "__main__":
	unittest.main()
