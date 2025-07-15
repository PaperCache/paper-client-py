import unittest
from tests.tester import Tester

class TestStatus(Tester):
	def test_status(self):
		(is_ok, _) = self.client.status()

		self.assertTrue(is_ok)

if __name__ == "__main__":
	unittest.main()
