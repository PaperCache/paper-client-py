from paper_client.policy import PaperPolicy

class PaperStats:
	def __init__(
		self,
		max_size: int,
		used_size: int,
		total_gets: int,
		total_sets: int,
		total_dels: int,
		miss_ratio: float,
		policy: PaperPolicy,
		uptime: int
	):
		self.max_size = max_size
		self.used_size = used_size

		self.total_gets = total_gets
		self.total_sets = total_sets
		self.total_dels = total_dels

		self.miss_ratio = miss_ratio

		self.policy = policy
		self.uptime = uptime
