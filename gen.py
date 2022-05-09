# Generate Graph Diagrams from an adjacency matrix

from ctypes.wintypes import POINT
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
	[0, 1, 1, 1],
	[1, 0, 1, 1],
	[1, 1, 0, 1],
	[1, 1, 1, 0]
]

OCT_MATRIX = [
	[0, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 1, 1, 1, 1, 1, 1],
	[1, 1, 0, 1, 1, 1, 1, 1],
	[1, 1, 1, 0, 1, 1, 1, 1],
	[1, 1, 1, 1, 0, 1, 1, 1],
	[1, 1, 1, 1, 1, 0, 1, 1],
	[1, 1, 1, 1, 1, 1, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 0],
]


CURRENT_MATRIX = OCT_MATRIX


def generate():
	win = GraphWin("Generation Result", DIMENSIONS, DIMENSIONS)

	center_Point = Point(DIMENSIONS / 2, DIMENSIONS / 2)

	# Draw the center reference point
	cp = Circle(center_Point, 3)
	cp.setFill("black")
	cp.draw(win) 

	num_nodes = len(CURRENT_MATRIX) # number of nodes = len of the matrix as its a square matrix
	degree_increment = math.floor(360/num_nodes) # Split 360 degrees into equal increments depending on the # of nodes we have
	# print(degree_increment)
	current_degree = 180 # 180 so the top of the graph is where A is (for looks)
	placed_nodes = {}

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
			if CURRENT_MATRIX[col][row] == 1:
				first_center = placed_nodes[col].getCenter()
				second_center = placed_nodes[row].getCenter()

				p1 = Point(first_center.x, first_center.y)
				p2 = Point(second_center.x, second_center.y)

				new_edge = Line(p1, p2)
				new_edge.setWidth(1)
				new_edge.draw(win)


	# Loop through nodes again to label them, so the labels appear on top the lines.
	for i in range(len(placed_nodes)):
		new_label = Text(placed_nodes[i].getCenter(), INDEX_TO_LETTER[i])
		new_label.setFill("white")
		new_label.setSize(20)
		new_label.draw(win)
		

	# Wait until closing the window until mouse click on the window
	win.getMouse()
	win.close()

generate()