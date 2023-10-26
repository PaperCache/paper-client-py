import unittest
from paper_client.client import PaperClient

class Tester(unittest.TestCase):
	client = PaperClient()

	def setUp(self):
		self.client.wipe()
