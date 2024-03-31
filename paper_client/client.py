from enum import Enum
from typing import Union, Tuple, Literal
from paper_client.tcp_client import TcpClient
from paper_client.buffer import Buffer
from paper_client.policy import PaperPolicy
from paper_client.stats import PaperStats

MAX_RECONNECT_ATTEMPTS = 3

class PaperClient:
	__host: str
	__port: int

	__auth_token: str
	__reconnect_attempts: int

	def __init__(self, host: str = "127.0.0.1", port: int = 3145):
		self.__host = host
		self.__port = port

		self.__auth_token = ""
		self.__reconnect_attempts = 0

		self.__client = TcpClient(host, port)
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

	def auth(self, token: str) -> Tuple[bool, str]:
		buf = Buffer()
		buf.write_u8(CommandByte.AUTH.value)
		buf.write_str(token)

		self.__auth_token = token

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

		return self.__process_has(buf)

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

	def size(self, key: str) -> Union[Tuple[Literal[True], int], Tuple[Literal[False], str]]:
		buf = Buffer()
		buf.write_u8(CommandByte.SIZE.value)
		buf.write_str(key)

		return self.__process_size(buf)

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

		return self.__process_stats(buf)

	def disconnect(self):
		self.__client.disconnect()

	def __reconnect(self) -> int:
		self.__reconnect_attempts += 1

		if self.__reconnect_attempts > MAX_RECONNECT_ATTEMPTS:
			return -1

		self.__client = TcpClient(self.__host, self.__port)

		if len(self.__auth_token) > 0:
			self.auth(self.__auth_token)

		return 0

	def __process_str(self, buf) -> Tuple[bool, str]:
		try:
			self.__client.send(buf)

			is_ok = self.__client.read_bool()
			data = self.__client.read_str()

			self.__reconnect_attempts = 0
			return (is_ok, data)
		except:
			if self.__reconnect() != 0:
				raise Exception("Could not reconnect to PaperServer")

			return self.__process_str(buf)

	def __process_has(self, buf) -> Union[Tuple[Literal[True], bool], Tuple[Literal[False], str]]:
		try:
			self.__client.send(buf)

			is_ok = self.__client.read_bool()

			if not is_ok:
				data = self.__client.read_str()
				return (is_ok, data)

			has = self.__client.read_bool()

			self.__reconnect_attempts = 0
			return (is_ok, has)
		except:
			if self.__reconnect() != 0:
				raise Exception("Could not reconnect to PaperServer")

			return self.__process_has(buf)

	def __process_size(self, buf) -> Union[Tuple[Literal[True], int], Tuple[Literal[False], str]]:
		try:
			self.__client.send(buf)

			is_ok = self.__client.read_bool()

			if not is_ok:
				data = self.__client.read_str()
				return (is_ok, data)

			size = self.__client.read_u64()

			self.__reconnect_attempts = 0
			return (is_ok, size)
		except:
			if self.__reconnect() != 0:
				raise Exception("Could not reconnect to PaperServer")

			return self.__process_size(buf)

	def __process_stats(self, buf) -> Union[Tuple[Literal[True], PaperStats], Tuple[Literal[False], str]]:
		try:
			self.__client.send(buf)

			is_ok = self.__client.read_bool()

			if not is_ok:
				data = self.__client.read_str()
				return (is_ok, data)

			max_size = self.__client.read_u64()
			used_size = self.__client.read_u64()
			total_gets = self.__client.read_u64()
			total_sets = self.__client.read_u64()
			total_dels = self.__client.read_u64()
			miss_ratio = self.__client.read_f64()
			policy_index = self.__client.read_u8()
			uptime = self.__client.read_u64()

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

			self.__reconnect_attempts = 0
			return (is_ok, stats)
		except:
			if self.__reconnect() != 0:
				raise Exception("Could not reconnect to PaperServer")

			return self.__process_stats(buf)

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

	AUTH = 2

	GET = 3
	SET = 4
	DEL = 5

	HAS = 6
	PEEK = 7
	TTL = 8
	SIZE = 9

	WIPE = 10

	RESIZE = 11
	POLICY = 12

	STATS = 13
