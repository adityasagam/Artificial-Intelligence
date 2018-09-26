class State:
	""" This class holds the data of a particular state (position) in the state space """
	
	def __init__(self, state, prev, cost, cuml_cost):
		""" Constructor """
		self.state = state
		self.cost = cost
		self.cuml_cost = cuml_cost
		self.prev = prev	# pointer to parent node