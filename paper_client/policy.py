from enum import Enum

class PaperPolicy(Enum):
	LFU = 0
	FIFO = 1
	LRU = 2
	MRU = 3
