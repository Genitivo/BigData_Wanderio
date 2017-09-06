import csv
import re 
import functools 

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




def createCluster(s,order_sessions):
	new_total_cluster = []
	capoCat = s[0].split(',')[0]
	minValCC = 10
	candidateCluster = []

	for cluster in order_sessions:
		if capoCat!=cluster[0].split(',')[0]:
			for st in cluster:
				if len(st.split(','))>1:
					if (capoCat == st.split(',')[0]) and (float(st.split(',')[1]) <= minValCC):
						minValCC = st.split(',')[1]
						candidateCluster = cluster


	if candidateCluster in order_sessions:
		order_sessions.remove(candidateCluster)
	if s in order_sessions:
		order_sessions.remove(s)

	temp = removeDuplicateWithMinScore(s+candidateCluster)

	if candidateCluster in total_cluster:
		total_cluster.remove(candidateCluster)

	total_cluster.append(temp)
	# print total_cluster
	order_sessions.append(temp)


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



def pulisciLista(pot):
	return pot[0:len(pot)-1]	


	

def createClusterPotOrder(pot):
	cap = pot[0].split(',')[0]
	capNeighbors = newNeighbors.get(cap)
	newPot = [cap]

	for p in pot[1:len(pot)-1]:
		a = re.escape(p.split(',')[0])
		regex = re.compile(a+',.*')
		newP = [m.group(0) for l in capNeighbors for m in [regex.search(l)] if m]
		if newP:
			newPot.append(newP[0])
	return newPot

	


with open("neighbors.csv", 'r') as file:
	reader = csv.reader(file, delimiter='\t')
	neighbors.append(list(reader))


neighbors = neighbors[0]

completedOrder_neighbors = filter(lambda x: True if 'L' in x[0].split(',')[0] else False, neighbors)

newNeighbors = map(lambda lista: (lista[0].split(',')[0],lista[1:len(lista)-1]),neighbors)
newNeighbors = dict(newNeighbors)



# SESSIONI CON POTENZIALE ACQUISTO
potential_completed_orders = map(potentialOrderSession, completedOrder_neighbors)
potential_completed_orders = map(pulisciLista, potential_completed_orders)
potential_completed_orders = filter(lambda x: True if x else False,potential_completed_orders)

pco_cluster = map(createClusterPotOrder, potential_completed_orders)
pco_cluster_copy = pco_cluster[:]

print len(pco_cluster)
map(functools.partial(createCluster,order_sessions=pco_cluster_copy),pco_cluster)

print len(pco_cluster)



# SESSIONI CON ACQUISTO E VICINI
completed_order_sessions = map(completedOrderSession, completedOrder_neighbors)
completed_order_sessions_copy = completed_order_sessions[:]

#map(createCluster,completed_order_sessions)
#filteredList = map(pickOnlyZero,total_cluster)
# result = map(removeDuplicati,completed_order_sessions)

#listWithDensity = map(findDensity,filteredList)



# neighbors_file =  open('./clusterDensity.csv', "a")
# for elem in listWithDensity:
# 	neighbors_file.write("%s\t" % elem[1])
# 	for e in elem[0]:
# 		neighbors_file.write("%s\t" % e)
# 	neighbors_file.write("\n")
# neighbors_file.close()

