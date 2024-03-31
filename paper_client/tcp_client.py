import socket
from struct import unpack

OK_VALUE = 33

class TcpClient:
	def __init__(self, host: str, port: int):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((host, port))

	def disconnect(self):
		self.client.close()

	def send(self, buf):
		self.client.sendall(buf.data)

	def read_bool(self):
		return self.read_u8() == OK_VALUE

	def read_u8(self):
		data = self.client.recv(1)

		if len(data) != 1:
			raise Exception("Could not receive data from PaperServer.")

		return data[0]

	def read_u32(self):
		data = self.client.recv(4)

		if len(data) != 4:
			raise Exception("Could not receive data from PaperServer.")

		return unpack("<I", data)[0]

	def read_u64(self):
		data = self.client.recv(8)

		if len(data) != 8:
			raise Exception("Could not receive data from PaperServer.")

		return unpack("<Q", data)[0]

	def read_f64(self):
		data = self.client.recv(8)

		if len(data) != 8:
			raise Exception("Could not receive data from PaperServer.")

		return unpack("<d", data)[0]

	def read_str(self):
		length = self.read_u32()
		data = self.client.recv(length)

		if len(data) != length:
			raise Exception("Could not receive data from PaperServer.")

		return data.decode("utf-8")
