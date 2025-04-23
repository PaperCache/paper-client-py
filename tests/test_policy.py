import unittest
from paper_client import PaperStats
from tests.tester import Tester

class TestPolicy(Tester):
	def test_policy(self):
		INITIAL_POLICY = "lfu"
		UPDATED_POLICY = "lru"

		(initial_is_ok, _) = self.client.policy(INITIAL_POLICY)

		self.assertTrue(initial_is_ok)
		self.assertEqual(self.get_policy(), INITIAL_POLICY)

		(updated_is_ok, _) = self.client.policy(UPDATED_POLICY)

		self.assertTrue(updated_is_ok)
		self.assertEqual(self.get_policy(), UPDATED_POLICY)

	def get_policy(self):
		(_, data) = self.client.stats()

		if isinstance(data, PaperStats):
			return data.policy

		self.fail("Could not get size of cache")

if __name__ == "__main__":
	unittest.main()
