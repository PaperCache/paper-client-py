from struct import *

class Buffer:
	def __init__(self):
		self.data = bytes()

	def write_u8(self, value):
		self.data += pack('<B', value)

	def write_u32(self, value):
		self.data += pack('<I', value)

	def write_u64(self, value):
		self.data += pack('<Q', value)

	def write_str(self, value):
		self.write_u32(len(value))
		self.data += bytes(value, 'utf-8')
