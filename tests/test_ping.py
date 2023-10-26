import unittest
from tests.tester import Tester

class TestPing(Tester):
	def test_ping(self):
		(is_ok, data) = self.client.ping()

		self.assertTrue(is_ok)
		self.assertEqual(data, "pong")

if __name__ == "__main__":
	unittest.main()
