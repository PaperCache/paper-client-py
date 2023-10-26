import unittest
from tests.tester import Tester

class TestStats(Tester):
	def test_stats(self):
		(is_ok, _) = self.client.stats()

		self.assertTrue(is_ok)

if __name__ == "__main__":
	unittest.main()
