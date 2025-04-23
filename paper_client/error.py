from enum import Enum, auto

class PaperError(Enum):
	INTERNAL = auto(),

	MAX_CONNECTIONS_EXCEEDED = auto(),
	UNAUTHORIZED = auto(),

	KEY_NOT_FOUND = auto(),

	ZERO_VALUE_SIZE = auto(),
	EXCEEDING_VALUE_SIZE = auto(),

	ZERO_CACHE_SIZE = auto(),

	UNCONFIGURED_POLICY = auto(),
	INVALID_POLICY = auto(),
