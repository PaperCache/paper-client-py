from typing import List
from threading import Lock
from paper_client.client import PaperClient

class PaperPool:
	def __init__(self, host: str = "127.0.0.1", port: int = 3145, size: int = 2):
		self.clients: List[PaperClient] = []
		self.client_locks: List[Lock] = []

		self.index = 0
		self.index_lock = Lock()

		for _ in range(size):
			self.clients.append(PaperClient(host, port))
			self.client_locks.append(Lock())

	def auth(self, token: str):
		for i in range(len(self.clients)):
			self.client_locks[i].acquire()
			self.clients[i].auth(token)
			self.client_locks[i].release()

	def lock_client(self) -> PaperClient:
		with self.index_lock:
			index = self.index
			self.index = (self.index + 1) % len(self.clients)

		self.client_locks[index].acquire()
		return self.clients[index]

	def unlock_client(self, client: PaperClient):
		index = -1

		for i in range(len(self.clients)):
			if client == self.clients[i]:
				index = i
				break

		if index != -1:
			self.client_locks[index].release()
