"""
@author 		Aditya Sagam
@description	This class has programs to execute following route finding algorithms
					1. Uniform Cost Search
					2. A* search
@date created	09-06-2018
"""
import sys
from Edge import Edge 
from State import State
				
def read_data_file(file_name):
	""" This function reads text data (distances between two nodes) 
		from file and initializes them as list of Edges
		
		@param Name of data file
		@return List of provided edges
	"""
	try:
		f = open(file_name, 'r')
	except IOError, arg:
		print 'Could\'nt read file with specified name: ', arg
	else:
		list_edges = []
		line = f.readline()
		
		while line:
			if not (line.startswith('END OF INPUT') or line.startswith('\n')):	# skip unwanted lines
				data_row = line.split()
				if data_row:
					edge = Edge(data_row[0].lower(), data_row[1].lower(), int(data_row[2]))
					list_edges.append(edge)
			line = f.readline()
		f.close()
		return list_edges

def read_hueristics_file(hueristics_file):
	""" Read the values of heuristics from text file into a dictionary
		@param Name of heuristics file
		@return dictionary containing heuristics
	"""
	try:
		f = open(hueristics_file, 'r')
	except IOError, arg:
		print 'Couldn\'t read heuristics file with specified name: ', arg
	else:
		dict_hueristics = {}
		line = f.readline()
		
		while line:
			if not (line.startswith('END OF INPUT') or line.startswith('\n')):
				data_row = line.split()
				if data_row:
					dict_hueristics[data_row[0].lower()] = int(data_row[1])
			line = f.readline()
		f.close()
		return dict_hueristics

def get_connecting_edges(state, visited_states, list_edges):
	"""	Returns list of unexplored connecting edges to given state parameter
		@param State for which connecting edges are to be found
		@param List of already visited states
		@param List of all edges
		@return List of connecting edges to the given state
	"""
	
	conn_edges = []		# list of connecting edges
	for edge in list_edges:
		if state == edge.state_a and edge.state_b not in visited_states:
			conn_edges.append(edge)
		if state == edge.state_b and edge.state_a not in visited_states:
			conn_edges.append(edge)	
	return conn_edges

def uniform_cost_search(file_name, origin_city, destination_city):
	""" Iteratively find the destination state (node) using
		 Uniform Cost Search and print the result.
		@param Name of data file
		@param Name of origin city
		@param Name of destination city
	"""
	
	list_edges = read_data_file(file_name)
	if list_edges:
		fringe = []
		visited_states = [];

		parent_state = State(origin_city, None, 0, 0)	# initialize parent node
		fringe.append(parent_state)

		while True:
			if not fringe:
				print_result(None)
				break;
				
			elem = fringe.pop()
			
			if elem.state == destination_city:
				print_result(elem)
				break;
			
			list_curr_edges = get_connecting_edges(elem.state, visited_states, list_edges)
			
			for edge in list_curr_edges:
				if elem.state == edge.state_a:
					temp_state = State(edge.state_b, elem, edge.cost, elem.cuml_cost + edge.cost)
					fringe.append(temp_state)
				elif elem.state == edge.state_b:
					temp_state = State(edge.state_a, elem, edge.cost, elem.cuml_cost + edge.cost)
					fringe.append(temp_state)
				#dump(temp_state)
			fringe.sort(key=lambda x: x.cuml_cost, reverse=True)
			
			visited_states.append(elem.state)
		
def a_star_search(file_name, dict_hueristics, origin_city, destination_city):
	""" Iteratively find the destination state (node) using A* Search
		 and print the result.
		@param Name of data file
		@param Dictionary containing node name as key and heuristic as value
		@param Name of origin city
		@param Name of destination city
	"""
	
	list_edges = read_data_file(file_name)
	if list_edges:
		fringe = []
		visited_states = [];
		
		parent_state = State(origin_city, None, 0, 0)
		fringe.append(parent_state)

		while True:
			if not fringe:
				print_result(None)
				break;
				
			elem = fringe.pop()
			
			if elem.state == destination_city:
				print_result(elem)
				break;
			
			list_curr_edges = get_connecting_edges(elem.state, visited_states, list_edges)
			
			for edge in list_curr_edges:
				if elem.state == edge.state_a:
					curr_cost = elem.cuml_cost + edge.cost + dict_hueristics[edge.state_b]
					temp_state = State(edge.state_b, elem, edge.cost, curr_cost)
					fringe.append(temp_state)
				elif elem.state == edge.state_b:
					curr_cost = elem.cuml_cost + edge.cost + dict_hueristics[edge.state_a]
					temp_state = State(edge.state_a, elem, edge.cost, curr_cost)
					fringe.append(temp_state)
				#dump(temp_state)
			fringe.sort(key=lambda x: x.cuml_cost, reverse=True)
			
			visited_states.append(elem.state)	
		
def print_result(node):
	""" Prints the result
		@param Destination node
	"""
	if node:	# destination has been found
		result_edges = []
		
		total_cost = 0;
		while node.prev:
			total_cost += node.cost
			result_edges.append(Edge(node.prev.state, node.state, node.cost))
			node = node.prev
		
		print('\n*********Goal Reached*******')
		print 'Distance:' + str(total_cost)
		print 'Route:'
		result_edges.reverse()
		for edge in result_edges:
			print edge.state_a.capitalize() +' to '+ edge.state_b.capitalize() +', '+ str(edge.cost) +' km'
		print ''
	else:
		print '\n******* Goal Unachievable ********\nDistance: Infinity'
		print 'Route:\n None\n'

'''
#Print object function			
def dump(obj):
	print('\n****')
	for attr in dir(obj):
		print("obj.%s = %r" % (attr, getattr(obj, attr)))
	print('****\n')
'''
		
###### Main starts here ######
		
arg_list = sys.argv
try:
	search_type, file_name, origin_city, destination_city = arg_list[2].lower(), arg_list[3], arg_list[4].lower(), arg_list[5].lower()
except IndexError:
	print "Error: Insufficient parameters found!"
	sys.exit(1)

if search_type == 'inf':
	if len(arg_list) == 7:
		hueristics_file = arg_list[6]
		dict_hueristics = read_hueristics_file(hueristics_file)	# dictionary containing name and heuristic value of each node
		
		if dict_hueristics:
			a_star_search(file_name, dict_hueristics, origin_city, destination_city)
	else:
		print "Insufficient parameters found!"
elif search_type == 'uninf':
	uniform_cost_search(file_name, origin_city, destination_city);
else:
	print "Please enter inf or uninf for search strategies!"
