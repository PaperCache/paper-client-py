from struct import *
from enum import Enum
from paper_client.tcp_client import TcpClient;
from paper_client.buffer import Buffer;

OK_VALUE = 33

class PaperPolicy(Enum):
	LRU = 0
	MRU = 1

class PaperClient:
	def __init__(self, host, port):
		self.client = TcpClient(host, port)

	def ping(self):
		buf = Buffer()
		buf.write_u8(0)

		return self.__process_str(buf)

	def version(self):
		buf = Buffer()
		buf.write_u8(1)

		return self.__process_str(buf)

	def get(self, key):
		buf = Buffer()
		buf.write_u8(2)
		buf.write_str(key)

		return self.__process_str(buf)

	def set(self, key, value, ttl = 0):
		buf = Buffer()
		buf.write_u8(3)
		buf.write_str(key)
		buf.write_str(value)
		buf.write_u32(ttl)

		return self.__process_str(buf)

	def delete(self, key):
		buf = Buffer()
		buf.write_u8(4)
		buf.write_str(key)

		return self.__process_str(buf)

	def clear(self):
		buf = Buffer()
		buf.write_u8(5)

		return self.__process_str(buf)

	def resize(self, size):
		buf = Buffer()
		buf.write_u8(6)
		buf.write_u64(size)

		return self.__process_str(buf)

	def policy(self, paper_policy):
		buf = Buffer()
		buf.write_u8(7)
		buf.write_u8(paper_policy.value)

		return self.__process_str(buf)

	def stats(self):
		buf = Buffer()
		buf.write_u8(8)

		self.client.send(buf)

		ok = self.client.read_u8() == OK_VALUE

		if not ok:
			data = self.client.read_str()
			return (ok, data)

		max_size = self.client.read_u64()
		used_size = self.client.read_u64()
		total_gets = self.client.read_u64()
		miss_ratio = self.client.read_f64()

		return (
			ok,
			max_size,
			used_size,
			total_gets,
			miss_ratio
		)

	def __process_str(self, buf):
		self.client.send(buf)

		ok = self.client.read_u8() == OK_VALUE
		data = self.client.read_str()

		return (ok, data)
