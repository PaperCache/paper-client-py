import unittest
from tests.tester import Tester

class TestHas(Tester):
	def test_has_existent(self):
		self.client.set("key", "value")
		(is_ok, data) = self.client.has("key")

		self.assertTrue(is_ok)
		self.assertTrue(data)

	def test_has_non_existent(self):
		(is_ok, data) = self.client.has("key")

		self.assertTrue(is_ok)
		self.assertFalse(data)

if __name__ == "__main__":
	unittest.main()
