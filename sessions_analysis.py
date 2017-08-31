import csv

def potentialOrderSession(sessions):
	return filter(lambda x: True if 'L' not in x.split(',')[0] else False,sessions)

def completedOrderSession(sessions):
	return filter(lambda x: True if 'L' in x.split(',')[0] else False,sessions)
#




neighbors = []
total_cluster = []

def createCluster(s):
	add = False
	new_total_cluster = []

	if len(total_cluster) > 0:
		for cluster in total_cluster:
			if any(s[0].split(',')[0] in st for st in cluster) and add == False:
				temp = list(set(cluster + s[1:len(s)]))
				new_total_cluster.append(temp)
				add = True
			else:
				new_total_cluster.append(cluster)

	if add == False:
		new_total_cluster.append(s)

	total_cluster[:] = new_total_cluster



def removeDuplicati(cluster):
	for s in cluster:
		i = 0
		for cl in total_cluster:
			if i<len(cl):
				if s[0] == cl[i][0] and s[1] <= cl[i][1]:
					temp = cl[i]
					cl.remove(temp)
			i=i+1



with open("neighbors.csv", 'r') as file:
	reader = csv.reader(file, delimiter='\t')
	neighbors.append(list(reader))

neighbors = neighbors[0]




completedOrder_neighbors = filter(lambda x: True if 'L' in x[0].split(',')[0] else False, neighbors)

# SESSIONI CON POTENZIALE ACQUISTO
potential_completed_orders = map(potentialOrderSession, completedOrder_neighbors)

# SESSIONI CON ACQUISTO E VICINI
completed_order_sessions = map(completedOrderSession, completedOrder_neighbors)



map(createCluster,completed_order_sessions)

map(removeDuplicati,total_cluster)

print total_cluster
print '*********************************'
print total_cluster[0][0]

