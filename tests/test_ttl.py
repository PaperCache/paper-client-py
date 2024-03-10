import unittest
from tests.tester import Tester

class TestTtl(Tester):
	def test_ttl_existent(self):
		self.client.set("key", "value")
		(is_ok, data) = self.client.ttl("key", 5)

		self.assertTrue(is_ok)
		self.assertEqual(data, "done")

	def test_ttl_non_existent(self):
		(is_ok, data) = self.client.ttl("key", 5)

		self.assertFalse(is_ok)
		self.assertNotEqual(len(data), 0)

if __name__ == "__main__":
	unittest.main()
