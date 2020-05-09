class Item:
	def __init__(self):
		self.name = ""
		self.description = ""


class RealityGun(Item):
	def __init__(self):
		self.name = "Reality Gun"
		self.description = "Briefly alters the beliefs of an autonomous agent. Requires careful aim."
		self.stats = {"charge": 100}

