import unittest
from time import sleep
from tests.tester import Tester

class TestSet(Tester):
	def test_set_no_ttl(self):
		(is_ok, data) = self.client.set("key", "value")

		self.assertTrue(is_ok)
		self.assertEqual(data, "done")

	def test_set_ttl(self):
		(is_ok, data) = self.client.set("key", "value", 1)

		self.assertTrue(is_ok)
		self.assertEqual(data, "done")

	def test_ttl_expiry(self):
		(set_is_ok, set_data) = self.client.set("key", "value", 1)

		self.assertTrue(set_is_ok)
		self.assertEqual(set_data, "done")

		(got_is_ok, got_data) = self.client.get("key")

		self.assertTrue(got_is_ok)
		self.assertEqual(got_data, "value")

		sleep(2)

		(expired_is_ok, expired_data) = self.client.get("key")

		self.assertFalse(expired_is_ok)
		self.assertNotEqual(len(expired_data), 0)

if __name__ == "__main__":
	unittest.main()
