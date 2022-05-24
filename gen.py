# Generate Graph Diagrams from an adjacency matrix

import math
from graphics import *


DIMENSIONS = 800
GEN_RADIUS = 300
NODE_RADIUS = 50

INDEX_TO_LETTER = {
	0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F",
	6:"G", 7:"H", 8:"I", 9:"J", 10:"K", 11:"L",
	12:"M", 13:"N", 14:"O", 15:"P", 16:"Q", 17:"R",
	18:"S", 19:"T", 20:"U", 21:"V", 22:"W", 23:"X",
	24:"Y", 25:"Z"
}

TRI_MATRIX = [
	[0, 1, 1],
	[1, 0, 1],
	[1, 1, 0],
]

QUAD_MATRIX = [
	[0, 1, 3, 6],
	[1, 0, 2, 1],
	[3, 2, 0, 1],
	[6, 1, 1, 0]
]

OCT_MATRIX = [
	[0, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 1, 0, 1, 1, 1, 1],
	[1, 1, 0, 1, 1, 1, 1, 1],
	[1, 0, 1, 0, 1, 1, 1, 1],
	[1, 1, 1, 1, 0, 1, 1, 1],
	[1, 1, 1, 1, 1, 0, 1, 1],
	[1, 1, 1, 1, 1, 1, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 0],
]

TEST_MATRIX = [
	[0, 1, 1, 0, 0],
	[1, 0, 1, 0, 1],
	[1, 1, 0, 1, 0],
	[0, 0, 1, 0, 1],
	[0, 1, 0, 1, 0]
]

BIG_MATRIX = [
	[0, 8, 6, 0, 7, 0, 0, 0, 0],
	[8, 0, 0, 4, 8, 0, 6, 0, 0],
	[6, 0, 0, 0, 9, 8, 0, 9, 0],
	[0, 4, 0, 0, 0, 0, 1, 0, 0],
	[7, 8, 9, 0, 0, 0, 7, 8, 16],
	[0, 0, 8, 0, 0, 0, 0, 11, 0],
	[0, 6, 0, 1, 7, 0, 0, 0, 6],
	[0, 0, 9, 0, 8, 11, 0, 0, 7],
	[0, 0, 0, 0, 16, 0, 6, 7, 0],
]

MATRIX2 = [[0, 4, 0, 0, 0, 0, 0, 8, 0], [4, 0, 8, 0, 0, 0, 0, 11, 0],
           [0, 8, 0, 7, 0, 4, 0, 0, 2], [0, 0, 7, 0, 9, 14, 0, 0, 0],
           [0, 0, 0, 9, 0, 10, 0, 0, 0], [0, 0, 4, 14, 10, 0, 2, 0, 0],
           [0, 0, 0, 0, 0, 2, 0, 1, 6], [8, 11, 0, 0, 0, 0, 1, 0, 7],
           [0, 0, 2, 0, 0, 0, 6, 7, 0]]


CURRENT_MATRIX = BIG_MATRIX


def weight_function(weight):
	return weight

win = GraphWin("Kruskal's Algorithm", DIMENSIONS, DIMENSIONS)
placed_nodes = {}

def generate(graph):
	center_Point = Point(DIMENSIONS / 2, DIMENSIONS / 2)

	num_nodes = len(graph) # number of nodes = len of the matrix as its a square matrix
	degree_increment = math.floor(360/num_nodes) # Split 360 degrees into equal increments depending on the # of nodes we have
	# print(degree_increment)
	current_degree = 180 # 180 so the top of the graph is where A is (for looks)

	# Draw the nodes and save them to placed_nodes
	for i in range(num_nodes):
		# Get X and Y coordinate using some basic trig
		# Such that the nodes are inscribed in a uniform circle
		# Centered about the center_point
		# This method ensures that all edges drawn between nodes 
		# are distinct and do not overlap

		current_x = GEN_RADIUS * math.sin(math.radians(current_degree)) + center_Point.x
		current_y = GEN_RADIUS * math.cos(math.radians(current_degree)) + center_Point.y
		current_point = Point(current_x, current_y)

		new_pt = current_point
		new_cir = Circle(new_pt, NODE_RADIUS)
		new_cir.setFill("green")
		new_cir.draw(win) 

		current_degree -= degree_increment
		placed_nodes[i] = new_cir


	# Connect the nodes to reflect the adjacency matrix
	# Both num_nodes as it's a symmetric/square matrix
	for col in range(num_nodes):
		for row in range(num_nodes):
			weight = graph[col][row]
			if weight >= 1:
				first_center = placed_nodes[col].getCenter()
				second_center = placed_nodes[row].getCenter()

				p1 = Point(first_center.x, first_center.y)
				p2 = Point(second_center.x, second_center.y)
				# mid = Point(first_center.x + (second_center.x - first_center.x)/2, first_center.y + (second_center.y - first_center.y)/2)

				# new_label = Text(mid, weight)
				# new_label.setFill("red")
				# new_label.setSize(weight + 20)
				


				new_edge = Line(p1, p2)
				new_edge.setWidth(weight_function(weight+2))
				new_edge.draw(win)
				# new_label.draw(win)

	# Loop through nodes again to label them, so the labels appear on top the lines.
	for i in range(len(placed_nodes)):
		text_point = None
		center = placed_nodes[i].getCenter()
		if center.y < DIMENSIONS / 2:
			text_point = Point(center.x, center.y - NODE_RADIUS - 15)
		
		if center.y > DIMENSIONS / 2:
			text_point = Point(center.x, center.y + NODE_RADIUS + 15)
		
		new_label = Text(text_point, INDEX_TO_LETTER[i])
		new_label.setFill(color_rgb(255, 105, 180))
		new_label.setSize(25)
		new_label.draw(win)
			

def get_node_from_edge(index):
	return placed_nodes[index]

def draw_from_chosen_edges(graph, chosen_edges, weight):
	# Now we have our edges chosen, and can highlight them graphically
	center_Point = Point(110, 20)
	current_weight = 0
	weight_text = Text(center_Point, "Total Weight: " + str(current_weight))
	weight_text.setSize(20)
	weight_text.draw(win)


	for edge in chosen_edges:
		node_a = edge[0]
		node_b = edge[1]

		drawn_node_a = get_node_from_edge(node_a)
		drawn_node_b = get_node_from_edge(node_b)

		time.sleep(1)
		weight_text.setText("Total Weight: " + str(current_weight + graph[edge[0]][edge[1]]))
		current_weight = current_weight + graph[edge[0]][edge[1]]
		select_edge = Line(drawn_node_a.getCenter(), drawn_node_b.getCenter())
		select_edge.setFill("red")
		select_edge.setWidth(weight_function(graph[node_a][node_b]+2))
		select_edge.draw(win)

		# Text box for total weight/distance here

	

def kruskals(graph):
	chosen_edges = []
	covered_edges = []
	groups = []
	total_weight = 0
	while True:
		# Loop through one half of the adjacency matrix
		# to find the highest weight edges

		if len(chosen_edges) == len(graph) - 1:
			break

		start = 1
		max = math.inf
		node_a = 0
		node_b = 0

		for row in range(len(graph)):
			for col in range(start, len(graph)):
				current_weight = graph[row][col]
				if current_weight != 0 and current_weight < max and [row, col] not in covered_edges and [row, col] not in chosen_edges:
					# print(chosen_edges)
					max = current_weight
					node_a = row
					node_b = col
					
			start += 1

		add_edge = True
		first_set = None
		second_set = None

		for set1 in groups:
			if node_a in set1:
				first_set = set1
			if node_b in set1:
				second_set = set1

		if not first_set and not second_set:
			s = set()
			s.add(node_a)
			s.add(node_b)
			groups.append(s)
		elif not first_set:
			second_set.add(node_a)
		elif not second_set:
			first_set.add(node_b)
		elif first_set == second_set:
			# Same group of vertices, will create a cycle
			add_edge = False
		else:
			# merge
			groups.remove(first_set)
			second_set.update(first_set)

		if add_edge:
			chosen_edges.append([node_a, node_b])
			total_weight += max
		else:
			# Need to keep track of already processed edges so we don't
			# Infinitely loop over them
			covered_edges.append([node_a, node_b])

	draw_from_chosen_edges(graph, chosen_edges, total_weight)


def dijkstra_algorithm(INPUT_MATRIX):
	#INPUT / initialization
	STARTING_V = input('Enter a starting node: ')
	END_V = input('Enter a end node: ')
	length = len(INPUT_MATRIX)

	#dictionary for node labels
	INDEX_TO_LETTER = {
		0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J", 10: "K", 11: "L", 12: "M", 13: "N" , 14: "O", 15: "P", 16: "Q", 17: "R", 18: "S", 19: "T", 20: "U", 21: "V", 22: "W", 23: "X", 24: "Y", 25: "Z"
	}

	for i in INDEX_TO_LETTER:
		if (INDEX_TO_LETTER[i] == STARTING_V):
			STARTING_INDEX = i
		elif (INDEX_TO_LETTER[i] == END_V):
			END_INDEX = i

	VISITED = [[0 for x in range(len(INPUT_MATRIX))]
			   for y in range(len(INPUT_MATRIX[0]))]

	for i in range(length):
		for j in range(length):
			if (INPUT_MATRIX[i][j] == 0):
				VISITED[i][j] = 1

	DISTANCES = [sys.maxsize for i in range(len(INPUT_MATRIX))]
	DISTANCES[STARTING_INDEX] = 0
	# print (DISTANCES)

	PARENT_NODES = [None] * len(INPUT_MATRIX)

	def DONE(CURRENT_V):
		for i in range(length):
			if VISITED[CURRENT_V][i] == 0:
				return False
		return True

	def dijkstra(CURRENT_V):
		# print("dijkstra("+str(CURRENT_V)+")")
		COMPARE_DISTANCE = sys.maxsize
		NEXT_NODE = -1
		for i in range(length):
			if (INPUT_MATRIX[CURRENT_V][i] != 0 and VISITED[CURRENT_V][i] == 0):
				VISITED[CURRENT_V][i] = 1
				VISITED[i][CURRENT_V] = 1
				if (DISTANCES[CURRENT_V] + INPUT_MATRIX[CURRENT_V][i] < DISTANCES[i]):
					DISTANCES[i] = DISTANCES[CURRENT_V] + INPUT_MATRIX[CURRENT_V][i]
					PARENT_NODES[i] = CURRENT_V
					if (DISTANCES[i] < COMPARE_DISTANCE):
						NEXT_NODE = i
						COMPARE_DISTANCE = DISTANCES[i]

		# see if there is a smaller distance in the distances array
		for i in range(length):
			if DISTANCES[i] < COMPARE_DISTANCE and DONE(i) == False:
				NEXT_NODE = i
				COMPARE_DISTANCE = DISTANCES[i]

			# print(COMPARE_DISTANCE)
			# print(DISTANCES)
		if (NEXT_NODE == -1):
			# print(DISTANCES)
			# print(PARENT_NODES)
			return None

		dijkstra(NEXT_NODE)

	dijkstra(STARTING_INDEX)

	print('The distance from ' + STARTING_V + ' to ' + END_V + ' is ' + str(DISTANCES[END_INDEX]))
	route = []
	route.append(END_V)
	chosen_dijkstra_edges = []
	SP = END_INDEX
	while (True):
		if (PARENT_NODES[SP] != None):
			chosen_dijkstra_edges.insert(0, [PARENT_NODES[SP],SP])
			SP = PARENT_NODES[SP]
		else:
			break

	for i in range(len(route)):
		if (i == len(route) - 1):
			print(route[i])
		else:
			print(route[i] + "->", end='')

	draw_from_chosen_edges(INPUT_MATRIX, chosen_dijkstra_edges, DISTANCES[END_INDEX])
	


generate(CURRENT_MATRIX)
kruskals(CURRENT_MATRIX)
# dijkstra_algorithm(CURRENT_MATRIX)

win.getMouse()
win.close()