import csv

def potentialOrderSession(sessions):
	return filter(lambda x: True if 'L' not in x else False,sessions)

def completedOrderSession(sessions):
	return filter(lambda x: True if 'L' in x else False,sessions)


neighbors = []

with open("neighbors.csv", 'r') as file:
	reader = csv.reader(file, delimiter='\t')
	neighbors.append(list(reader))

neighbors = neighbors[0]

completedOrder_neighbors = filter(lambda x: True if 'L' in x[0] else False, neighbors)

potential_completed_orders = map(potentialOrderSession, completedOrder_neighbors)

completed_order_sessions = map(completedOrderSession, completedOrder_neighbors)

print neighbors
