# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 21:26:57 2025

@author: ziyan
"""

import networkx as nx
import json
import numpy as np
network_type='wsn'
'''
NetworkSet=['bio-yeast','bn-mouse-kasthuri_graph_v4','bio-CE-HT', 'bio-CE-LC','ia-crime-moreno','rt-twitter-copen']
filename='.\\saves\\nets\\'+network_type+'.txt'
G=nx.Graph()
with open(filename) as file:
    for line in file:
        head, tail=[str(x) for x in line.split()]
        G.add_edge(int(head),int(tail))
N=G.number_of_nodes()
print(2*G.number_of_edges()/N)
'''
filename1='.\\saves\\component\\{}.json'.format(network_type)
f1=open(filename1)
data1=json.load(f1)
print(data1['4'][0])
print(data1['4'][14])
print(data1['4'][24])