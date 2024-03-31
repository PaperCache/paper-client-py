import unittest
from paper_client.client import PaperClient
from paper_client.pool import PaperPool

class Tester(unittest.TestCase):
	def setUp(self):
		self.client = PaperClient()
		self.client.auth("auth_token")
		self.client.wipe()

	def tearDown(self):
		self.client.disconnect()

class PoolTester(unittest.TestCase):
	pool = PaperPool()
