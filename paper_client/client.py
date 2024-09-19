from enum import Enum
from typing import TypeAlias, Union, Tuple, Literal
from paper_client.tcp_client import TcpClient
from paper_client.buffer import Buffer
from paper_client.error import PaperError
from paper_client.policy import PaperPolicy
from paper_client.stats import PaperStats

MAX_RECONNECT_ATTEMPTS = 3

ResponseResult: TypeAlias = Union[Tuple[Literal[True], None], Tuple[Literal[False], PaperError]]
DataResponseResult: TypeAlias = Union[Tuple[Literal[True], str], Tuple[Literal[False], PaperError]]
HasResponseResult: TypeAlias = Union[Tuple[Literal[True], bool], Tuple[Literal[False], PaperError]]
SizeResponseResult: TypeAlias = Union[Tuple[Literal[True], int], Tuple[Literal[False], PaperError]]
StatsResponseResult: TypeAlias = Union[Tuple[Literal[True], PaperStats], Tuple[Literal[False], PaperError]]

class PaperClient:
	__host: str
	__port: int

	__auth_token: str
	__reconnect_attempts: int

	def __init__(self, paper_addr: str = "paper://127.0.0.1:3145"):
		if not paper_addr.startswith("paper://"):
			raise Exception("Invalid Paper address")

		parsed = paper_addr.removeprefix("paper://").split(':')

		self.__host = parsed[0]
		self.__port = int(parsed[1])

		self.__auth_token = ""
		self.__reconnect_attempts = 0

		self.__client = TcpClient(self.__host, self.__port)

		if not handshake(self.__client)[0]:
			raise Exception("Connection refused")

	def ping(self) -> DataResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.PING.value)

		return self.__process_str(buf)

	def version(self) -> DataResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.VERSION.value)

		return self.__process_str(buf)

	def auth(self, token: str) -> ResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.AUTH.value)
		buf.write_str(token)

		self.__auth_token = token

		return self.__process(buf)

	def get(self, key: str) -> DataResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.GET.value)
		buf.write_str(key)

		return self.__process_str(buf)

	def set(self, key: str, value: str, ttl: int = 0) -> ResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.SET.value)
		buf.write_str(key)
		buf.write_str(value)
		buf.write_u32(ttl)

		return self.__process(buf)

	def delete(self, key: str) -> ResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.DEL.value)
		buf.write_str(key)

		return self.__process(buf)

	def has(self, key: str) -> HasResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.HAS.value)
		buf.write_str(key)

		return self.__process_has(buf)

	def peek(self, key: str) -> DataResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.PEEK.value)
		buf.write_str(key)

		return self.__process_str(buf)

	def ttl(self, key: str, ttl: int = 0) -> ResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.TTL.value)
		buf.write_str(key)
		buf.write_u32(ttl)

		return self.__process(buf)

	def size(self, key: str) -> SizeResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.SIZE.value)
		buf.write_str(key)

		return self.__process_size(buf)

	def wipe(self) -> ResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.WIPE.value)

		return self.__process(buf)

	def resize(self, size: int) -> ResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.RESIZE.value)
		buf.write_u64(size)

		return self.__process(buf)

	def policy(self, paper_policy: PaperPolicy) -> ResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.POLICY.value)
		buf.write_u8(paper_policy.value)

		return self.__process(buf)

	def stats(self) -> StatsResponseResult:
		buf = Buffer()
		buf.write_u8(CommandByte.STATS.value)

		return self.__process_stats(buf)

	def disconnect(self):
		self.__client.disconnect()

	def __reconnect(self) -> bool:
		self.__reconnect_attempts += 1

		if self.__reconnect_attempts > MAX_RECONNECT_ATTEMPTS:
			return False

		self.__client = TcpClient(self.__host, self.__port)

		if not handshake(self.__client)[0]:
			return False

		if len(self.__auth_token) > 0:
			self.auth(self.__auth_token)

		return True

	def __process(self, buf) -> ResponseResult:
		try:
			self.__client.send(buf)

			is_ok = self.__client.read_bool()

			if not is_ok:
				error = get_error_from_client(self.__client)
				return (is_ok, error)

			self.__reconnect_attempts = 0
			return (is_ok, None)
		except:
			if self.__reconnect() != 0:
				raise Exception("Could not reconnect to PaperServer")

			return self.__process(buf)

	def __process_str(self, buf) -> DataResponseResult:
		try:
			self.__client.send(buf)

			is_ok = self.__client.read_bool()

			if not is_ok:
				error = get_error_from_client(self.__client)
				return (is_ok, error)

			data = self.__client.read_str()

			self.__reconnect_attempts = 0
			return (is_ok, data)
		except:
			if not self.__reconnect():
				raise Exception("Could not reconnect to PaperServer")

			return self.__process_str(buf)

	def __process_has(self, buf) -> HasResponseResult:
		try:
			self.__client.send(buf)

			is_ok = self.__client.read_bool()

			if not is_ok:
				error = get_error_from_client(self.__client)
				return (is_ok, error)

			has = self.__client.read_bool()

			self.__reconnect_attempts = 0
			return (is_ok, has)
		except:
			if not self.__reconnect():
				raise Exception("Could not reconnect to PaperServer")

			return self.__process_has(buf)

	def __process_size(self, buf) -> SizeResponseResult:
		try:
			self.__client.send(buf)

			is_ok = self.__client.read_bool()

			if not is_ok:
				error = get_error_from_client(self.__client)
				return (is_ok, error)

			size = self.__client.read_u64()

			self.__reconnect_attempts = 0
			return (is_ok, size)
		except:
			if not self.__reconnect():
				raise Exception("Could not reconnect to PaperServer")

			return self.__process_size(buf)

	def __process_stats(self, buf) -> StatsResponseResult:
		try:
			self.__client.send(buf)

			is_ok = self.__client.read_bool()

			if not is_ok:
				error = get_error_from_client(self.__client)
				return (is_ok, error)

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
			if not self.__reconnect():
				raise Exception("Could not reconnect to PaperServer")

			return self.__process_stats(buf)

def handshake(client: TcpClient) -> Union[Tuple[Literal[True], None], Tuple[Literal[False], PaperError]]:
	is_ok = client.read_bool()

	if not is_ok:
		error = get_error_from_client(client)
		return (is_ok, error)

	return (is_ok, None)

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

def get_error_from_client(client: TcpClient) -> PaperError:
	code = client.read_u8()

	if code == 0:
		cache_code = client.read_u8()

		if cache_code == 1:
			return PaperError.KEY_NOT_FOUND
		elif cache_code == 2:
			return PaperError.ZERO_VALUE_SIZE
		elif cache_code == 3:
			return PaperError.EXCEEDING_VALUE_SIZE
		elif cache_code == 4:
			return PaperError.ZERO_CACHE_SIZE
		else:
			return PaperError.INTERNAL

	if code == 2:
		return PaperError.MAX_CONNECTIONS_EXCEEDED
	elif code == 3:
		return PaperError.UNAUTHORIZED
	else:
		return PaperError.INTERNAL

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
