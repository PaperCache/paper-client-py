import unittest
from tests.tester import PoolTester

class TestPool(PoolTester):
	def test_pool(self):
		client = self.pool.lock_client()
		(is_ok, data) = client.ping()
		self.pool.unlock_client(client)

		self.assertTrue(is_ok)
		self.assertEqual(data, "pong")

	def test_pool_auth_invalid(self):
		client = self.pool.lock_client()
		(is_ok, _) = client.has("key")
		self.pool.unlock_client(client)

		self.assertFalse(is_ok)

	def test_pool_auth_valid(self):
		self.pool.auth("auth_token")

		client = self.pool.lock_client()
		(is_ok, _) = client.has("key")
		self.pool.unlock_client(client)

		self.assertTrue(is_ok)

if __name__ == "__main__":
	unittest.main()
