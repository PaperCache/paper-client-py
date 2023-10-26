import unittest
from paper_client import PaperPolicy, PaperStats
from tests.tester import Tester

class TestPolicy(Tester):
	def test_policy(self):
		INITIAL_POLICY = PaperPolicy.LFU
		UPDATED_POLICY = PaperPolicy.LRU

		(initial_is_ok, initial_data) = self.client.policy(INITIAL_POLICY)

		self.assertTrue(initial_is_ok)
		self.assertEqual(initial_data, "done")
		self.assertEqual(self.get_policy(), INITIAL_POLICY)

		(updated_is_ok, updated_data) = self.client.policy(UPDATED_POLICY)

		self.assertTrue(updated_is_ok)
		self.assertEqual(updated_data, "done")
		self.assertEqual(self.get_policy(), UPDATED_POLICY)

	def get_policy(self):
		(_, data) = self.client.stats()

		if isinstance(data, PaperStats):
			return data.policy

		self.fail("Could not get size of cache")

if __name__ == "__main__":
	unittest.main()
