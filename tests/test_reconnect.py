import unittest
from tests.tester import Tester

class TestReconnect(Tester):
	def test_reconnect(self):
		(is_ok, _) = self.client.has("key")
		self.assertTrue(is_ok)

		self.client.disconnect()

		(is_ok, _) = self.client.has("key")
		self.assertTrue(is_ok)

if __name__ == "__main__":
	unittest.main()
