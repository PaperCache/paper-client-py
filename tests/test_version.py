import unittest
from tests.tester import Tester
from paper_client import PaperError

class TestVersion(Tester):
	def test_version(self):
		(is_ok, data) = self.client.version()

		self.assertTrue(is_ok)
		self.assertNotIsInstance(data, PaperError)

if __name__ == "__main__":
	unittest.main()
