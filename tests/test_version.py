import unittest
from tests.tester import Tester

class TestVersion(Tester):
	def test_version(self):
		(is_ok, data) = self.client.version()

		self.assertTrue(is_ok)
		self.assertNotEqual(len(data), 0)

if __name__ == "__main__":
	unittest.main()
