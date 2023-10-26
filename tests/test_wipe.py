import unittest
from tests.tester import Tester

class TestWipe(Tester):
	def test_wipe(self):
		(is_ok, data) = self.client.wipe()

		self.assertTrue(is_ok)
		self.assertEqual(data, "done")

if __name__ == "__main__":
	unittest.main()
