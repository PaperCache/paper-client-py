import unittest
from paper_client import PaperStats
from tests.tester import Tester

class TestResize(Tester):
	def test_resize(self):
		INITIAL_SIZE = 10 * 1024 ** 2;
		UPDATED_SIZE = 20 * 1024 ** 2;

		(initial_is_ok, initial_data) = self.client.resize(INITIAL_SIZE)

		self.assertTrue(initial_is_ok)
		self.assertEqual(initial_data, "done")
		self.assertEqual(self.get_size(), INITIAL_SIZE)

		(updated_is_ok, updated_data) = self.client.resize(UPDATED_SIZE)

		self.assertTrue(updated_is_ok)
		self.assertEqual(updated_data, "done")
		self.assertEqual(self.get_size(), UPDATED_SIZE)

	def get_size(self):
		(_, data) = self.client.stats()

		if isinstance(data, PaperStats):
			return data.max_size

		self.fail("Could not get size of cache")

if __name__ == "__main__":
	unittest.main()
