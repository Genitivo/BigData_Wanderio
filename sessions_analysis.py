import csv

def potentialOrderSession(sessions):
	return filter(lambda x: True if 'L' not in x.split(',')[0] else False,sessions)

def completedOrderSession(sessions):
	return filter(lambda x: True if 'L' in x.split(',')[0] else False,sessions)

neighbors = []
total_cluster = []


def findDensity(cluster):
	totalDensity=0
	new_cluster = []

	for c in cluster:
		name = c.split(',')[0]
		#print name
		line = filter(lambda x: x[0] == c ,neighbors)[0]
		totalDensity = int(line[len(line)-1])+totalDensity
		new_cluster.append(name)
	return (new_cluster,totalDensity)
		#for n in neighbors: 
		#	if name == n[0].split(','):




def createCluster(s):
	new_total_cluster = []
	capoCat = s[0].split(',')[0]
	minValCC = 10
	candidateCluster = []

	for cluster in completed_order_sessions_copy:
		if capoCat!=cluster[0].split(',')[0]:
			for st in cluster:
				if (capoCat == st.split(',')[0]) and (float(st.split(',')[1]) <= minValCC):
					minValCC = st.split(',')[1]
					candidateCluster = cluster


	if candidateCluster in completed_order_sessions_copy:
		completed_order_sessions_copy.remove(candidateCluster)
	if s in completed_order_sessions_copy:
		completed_order_sessions_copy.remove(s)

	temp = removeDuplicateWithMinScore(s+candidateCluster)

	if candidateCluster in total_cluster:
		total_cluster.remove(candidateCluster)

	total_cluster.append(temp)
	# print total_cluster
	completed_order_sessions_copy.append(temp)


def pickOnlyZero(cluster):
	cluster.sort()

	return set(list(filter(lambda x: True if float(x.split(',')[1])==0.0 else False,cluster)))

def removeDuplicateWithMinScore(cluster):
	nome_corrente = ''
	new_cluster = []
	cluster.sort()

	for c in cluster:
		nome = 	c.split(',')[0]

		if nome_corrente=='':
			nome_corrente = nome
			new_cluster.append(c)

		if nome_corrente!=nome:
			nome_corrente = nome
			new_cluster.append(c)

	return new_cluster


def removeDuplicati(cluster):

	for s in cluster[1:len(cluster)]:
		i = 1
		for cl in total_cluster:
			if cl != cluster:
				if i<len(cl):
					if s[0] == cl[i][0] and s[1] <= cl[i][1]:
						temp = cl[i]
						cl.remove(temp)
				i=i+1

	return removeDuplicateWithMinScore(cluster)

with open("neighbors.csv", 'r') as file:
	reader = csv.reader(file, delimiter='\t')
	neighbors.append(list(reader))

neighbors = neighbors[0]




completedOrder_neighbors = filter(lambda x: True if 'L' in x[0].split(',')[0] else False, neighbors)

# SESSIONI CON POTENZIALE ACQUISTO
potential_completed_orders = map(potentialOrderSession, completedOrder_neighbors)

# SESSIONI CON ACQUISTO E VICINI
completed_order_sessions = map(completedOrderSession, completedOrder_neighbors)

completed_order_sessions_copy = completed_order_sessions[:]

map(createCluster,completed_order_sessions)
filteredList = map(pickOnlyZero,total_cluster)
# result = map(removeDuplicati,completed_order_sessions)

listWithDensity = map(findDensity,filteredList)
#
print listWithDensity


neighbors_file =  open('./clusterDensity.csv', "a")
for elem in listWithDensity:
	for e in elem[0]:
		neighbors_file.write("%s\t" % e)
    	neighbors_file.write("%s\n" % elem[1])
neighbors_file.close()

# print len(total_cluster)
# print '*********************************'