import unittest
from time import sleep
from tests.tester import Tester
from paper_client import PaperError

class TestSet(Tester):
	def test_set_no_ttl(self):
		(is_ok, _) = self.client.set("key", "value")

		self.assertTrue(is_ok)

	def test_set_ttl(self):
		(is_ok, _) = self.client.set("key", "value", 1)

		self.assertTrue(is_ok)

	def test_ttl_expiry(self):
		(set_is_ok, _) = self.client.set("key", "value", 1)

		self.assertTrue(set_is_ok)

		(got_is_ok, got_data) = self.client.get("key")

		self.assertTrue(got_is_ok)
		self.assertEqual(got_data, "value")

		sleep(2)

		(expired_is_ok, expired_error) = self.client.get("key")

		self.assertFalse(expired_is_ok)
		self.assertEqual(expired_error, PaperError.KEY_NOT_FOUND)

if __name__ == "__main__":
	unittest.main()
