class Edge:
	"""" Stores cost from a particular node to another as an edge """
	
	def __init__(self, state_a, state_b, cost):
		""" Constructor """
		self.state_a = state_a
		self.state_b = state_b
		self.cost = cost