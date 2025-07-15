import unittest
from paper_client import PaperStatus
from tests.tester import Tester

class TestResize(Tester):
	def test_resize(self):
		INITIAL_SIZE = 10 * 1024 ** 2;
		UPDATED_SIZE = 20 * 1024 ** 2;

		(initial_is_ok, _) = self.client.resize(INITIAL_SIZE)

		self.assertTrue(initial_is_ok)
		self.assertEqual(self.get_size(), INITIAL_SIZE)

		(updated_is_ok, _) = self.client.resize(UPDATED_SIZE)

		self.assertTrue(updated_is_ok)
		self.assertEqual(self.get_size(), UPDATED_SIZE)

	def get_size(self):
		(_, data) = self.client.status()

		if isinstance(data, PaperStatus):
			return data.max_size

		self.fail("Could not get size of cache")

if __name__ == "__main__":
	unittest.main()
