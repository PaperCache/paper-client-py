import socket
from struct import unpack

OK_VALUE = 33

class TcpClient:
	def __init__(self, host: str, port: int):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((host, port))

	def send(self, buf):
		self.client.sendall(buf.data)

	def read_bool(self):
		return self.read_u8() == OK_VALUE

	def read_u8(self):
		data = self.client.recv(1)
		return data[0]

	def read_u32(self):
		data = self.client.recv(4)
		return unpack("<I", data)[0]

	def read_u64(self):
		data = self.client.recv(8)
		return unpack("<Q", data)[0]

	def read_f64(self):
		data = self.client.recv(8)
		return unpack("<d", data)[0]

	def read_str(self):
		length = self.read_u32()
		data = self.client.recv(length)
		return data.decode("utf-8")
