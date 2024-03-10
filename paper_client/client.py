from enum import Enum
from typing import Union, Tuple, Literal
from paper_client.tcp_client import TcpClient
from paper_client.buffer import Buffer
from paper_client.policy import PaperPolicy
from paper_client.stats import PaperStats

class PaperClient:
	def __init__(self, host: str = "127.0.0.1", port: int = 3145):
		self.client = TcpClient(host, port)
		(ping_ok, _) = self.ping()

		if not ping_ok:
			raise Exception("Connection refused")

	def ping(self) -> Tuple[bool, str]:
		buf = Buffer()
		buf.write_u8(CommandByte.PING.value)

		return self.__process_str(buf)

	def version(self) -> Tuple[bool, str]:
		buf = Buffer()
		buf.write_u8(CommandByte.VERSION.value)

		return self.__process_str(buf)

	def get(self, key: str) -> Tuple[bool, str]:
		buf = Buffer()
		buf.write_u8(CommandByte.GET.value)
		buf.write_str(key)

		return self.__process_str(buf)

	def set(self, key: str, value: str, ttl: int = 0) -> Tuple[bool, str]:
		buf = Buffer()
		buf.write_u8(CommandByte.SET.value)
		buf.write_str(key)
		buf.write_str(value)
		buf.write_u32(ttl)

		return self.__process_str(buf)

	def delete(self, key: str) -> Tuple[bool, str]:
		buf = Buffer()
		buf.write_u8(CommandByte.DEL.value)
		buf.write_str(key)

		return self.__process_str(buf)

	def has(self, key: str) -> Union[Tuple[Literal[True], bool], Tuple[Literal[False], str]]:
		buf = Buffer()
		buf.write_u8(CommandByte.HAS.value)
		buf.write_str(key)

		self.client.send(buf)

		is_ok = self.client.read_bool()

		if not is_ok:
			data = self.client.read_str()
			return (is_ok, data)

		has = self.client.read_bool()

		return (is_ok, has)

	def peek(self, key: str) -> Tuple[bool, str]:
		buf = Buffer()
		buf.write_u8(CommandByte.PEEK.value)
		buf.write_str(key)

		return self.__process_str(buf)

	def ttl(self, key: str, ttl: int = 0) -> Tuple[bool, str]:
		buf = Buffer()
		buf.write_u8(CommandByte.TTL.value)
		buf.write_str(key)
		buf.write_u32(ttl)

		return self.__process_str(buf)

	def wipe(self) -> Tuple[bool, str]:
		buf = Buffer()
		buf.write_u8(CommandByte.WIPE.value)

		return self.__process_str(buf)

	def resize(self, size: int) -> Tuple[bool, str]:
		buf = Buffer()
		buf.write_u8(CommandByte.RESIZE.value)
		buf.write_u64(size)

		return self.__process_str(buf)

	def policy(self, paper_policy: PaperPolicy) -> Tuple[bool, str]:
		buf = Buffer()
		buf.write_u8(CommandByte.POLICY.value)
		buf.write_u8(paper_policy.value)

		return self.__process_str(buf)

	def stats(self) -> Union[Tuple[Literal[True], PaperStats], Tuple[Literal[False], str]]:
		buf = Buffer()
		buf.write_u8(CommandByte.STATS.value)

		self.client.send(buf)

		is_ok = self.client.read_bool()

		if not is_ok:
			data = self.client.read_str()
			return (is_ok, data)

		max_size = self.client.read_u64()
		used_size = self.client.read_u64()
		total_gets = self.client.read_u64()
		total_sets = self.client.read_u64()
		total_dels = self.client.read_u64()
		miss_ratio = self.client.read_f64()
		policy_index = self.client.read_u8()
		uptime = self.client.read_u64()

		stats = PaperStats(
			max_size,
			used_size,
			total_gets,
			total_sets,
			total_dels,
			miss_ratio,
			get_policy_from_index(policy_index),
			uptime
		)

		return (is_ok, stats)

	def __process_str(self, buf):
		self.client.send(buf)

		is_ok = self.client.read_bool()
		data = self.client.read_str()

		return (is_ok, data)

def get_policy_from_index(policy_index: int) -> PaperPolicy:
	if policy_index == 0:
		return PaperPolicy.LFU

	if policy_index == 1:
		return PaperPolicy.FIFO

	if policy_index == 2:
		return PaperPolicy.LRU

	if policy_index == 3:
		return PaperPolicy.MRU

	raise ValueError("Invalid policy index")

class CommandByte(Enum):
	PING = 0
	VERSION = 1

	GET = 2
	SET = 3
	DEL = 4

	HAS = 5
	PEEK = 6
	TTL = 7

	WIPE = 8

	RESIZE = 9
	POLICY = 10

	STATS = 11
