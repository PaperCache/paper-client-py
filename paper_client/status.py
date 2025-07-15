class PaperStatus:
	def __init__(
		self,
		pid: int,

		max_size: int,
		used_size: int,
		num_objects: int,

		rss: int,
		hwm: int,

		total_gets: int,
		total_sets: int,
		total_dels: int,

		miss_ratio: float,

		policies: list[str],
		policy: str,
		is_auto_policy: bool,

		uptime: int
	):
		self.pid = pid

		self.max_size = max_size
		self.used_size = used_size
		self.num_objects = num_objects

		self.rss = rss
		self.hwm = hwm

		self.total_gets = total_gets
		self.total_sets = total_sets
		self.total_dels = total_dels

		self.miss_ratio = miss_ratio

		self.policies = policies
		self.policy = policy
		self.is_auto_policy = is_auto_policy

		self.uptime = uptime
