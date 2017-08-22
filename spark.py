#!/usr/bin/python
from pyspark.sql import SparkSession
from pyspark import SparkContext
from datetime import datetime
import re
import math
import operator
import csv

def dateDiveded(date):

    date_array = date[0].split('T')
    return (date_array[0],date_array[1].split('.')[0],date[1])

def calcolaSessione(eventi_giornalieri):

    orario_evento = eventi_giornalieri[1]

    lista_eventi = []
    lista_eventi.append(orario_evento[0][1])
    sessioni = []
    FMT = '%H:%M:%S'
    session_len = datetime.strptime('0:00:00',FMT)

    if len(orario_evento) == 1:
        sessione = {'durata_sessione':0,'eventi':lista_eventi}
        sessioni.append(sessione)

    else:

        for i in range(0,len(orario_evento)-1):
            s1 = orario_evento[i][0]
            s2 = orario_evento[i+1][0]

            tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1,FMT)

            if tdelta.seconds/3600 < 15: #sessione massima di durata 15 minuti

                lista_eventi.append(orario_evento[i+1][1])
                session_len = session_len + tdelta

                if i == len(orario_evento)-2:
                    #sessione = {'durata_sessione':session_len.time(),'eventi':lista_eventi}
                    sessione = {'durata_sessione':session_len.strftime(FMT),'eventi':lista_eventi}
                    sessioni.append(sessione)
            else:
                #sessione = {'durata_sessione':session_len.time(),'eventi':lista_eventi}
                sessione = {'durata_sessione':session_len.strftime(FMT),'eventi':lista_eventi}
                sessioni.append(sessione)
                lista_eventi = []
                session_len = datetime.strptime('0:00:00',FMT)

                if i == len(orario_evento)-2:
                    lista_eventi = orario_evento[i+1][1]
                    sessione = {'durata_sessione':0,'eventi':[orario_evento[i+1][1]]}
                    sessioni.append(sessione)
                    break



    return sessioni

def onlySessions(sessione):
    return map((lambda x:x["eventi"]), sessione)[0]


def creaSessioni(utente):
        temp = utente[1]
        temp.sort(key=lambda x: x[0])

        date_event = sc.parallelize(temp)
        date_event = map(dateDiveded, temp)

        date_rdd = sc.parallelize(date_event)
        date_rdd = date_rdd.map(lambda dt: (dt[0],(dt[1],dt[2]))).groupByKey().mapValues(list).collect()

        sessioni = map(calcolaSessione, date_rdd)

        solo_sessioni = map(onlySessions, sessioni)
        map(lambda x: x.append(utente[0]),solo_sessioni)

        knn_events_user = map(createKNN,solo_sessioni)

        with open('./knn_string.csv', "a") as f:
            writer = csv.writer(f)
            writer.writerows(knn_events_user)


def createKNN(sessione):
    knn_string = ''

    for cat in categories:
        print cat
        if cat[0] in sessione:
            knn_string = knn_string+cat[1]

    return (knn_string,sessione[len(sessione)-1])


######################################### <-----> MAIN <-----> ##############################################

sc = SparkContext()
categories_csv = sc.textFile("./event_category.csv")
categories = categories_csv.map(lambda line: line.split("\t"))

categories = categories.map(lambda elem: (elem[0].split(",")[0],elem[0].split(",")[1])).collect()

text_file = sc.textFile("./data_event_type.csv")

lines = text_file.map(lambda line: line.split("\t"))
users = lines.map(lambda p: ( p[0],(p[2],p[3]) )).groupByKey().mapValues(list).collect()

map(creaSessioni, users)
