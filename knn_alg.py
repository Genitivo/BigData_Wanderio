from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
import time
import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph

# FROM STRING TO BIT
def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

# FROM BIT TO STRING
def frombits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

# ADD -1 FOR VECTOR MIN OF MAX VECTOR LEN
def addZero(vector):
    while len(vector) < h_max:
        vector.append(-1)

# REMOVE -1 FOR VECTOR
def removeZero(vector):
    return filter(lambda a: a != -1, vector)

def session_distribution(words,w):
    return words.count(w)

words = []
sessions_users = []
h_max = 0

with open("knn_string.csv") as fh:
    for line in fh:
        session_user = line.strip()
        temp = session_user.split(',')
        temp = temp[:len(temp)-1]
        # temp = tobits(temp[0])

        if(h_max<len(tobits(temp[0]))):
            h_max = len(tobits(temp[0]))

        words.append(temp[0])

        # sessions_users.append((session_user.split(',')[0],session_user.split(',')[1]))

words_set = list(set(words))
distributions = [session_distribution(words,x) for x in words_set]
print distributions
words_set = map(tobits,words_set)
map(addZero,words_set)
print "!"
neigh = NearestNeighbors(n_neighbors=10)

neigh.fit(words_set)

temp = neigh.kneighbors(words_set)

print "?"
for idx, val in enumerate(temp[1]):
    print idx
    bits = removeZero(words_set[idx])
    vicini = []
    for index, number in enumerate(val):
        bits_n = removeZero(words_set[number])
        vicini.append(frombits(bits_n))
    neighbors_file =  open('./neighbors.csv', "a")
    for item in vicini:
        neighbors_file.write("%s\t" % item)
    neighbors_file.write("%s\n" % distributions[idx])
    neighbors_file.close()
    # print "Stringa ", frombits(bits)
    # print "vicini: ", vicini
