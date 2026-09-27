# -*- coding: utf-8 -*-
"""
Edge Switching Dynamics
Created on Wed Jul 12 18:09:33 2023
time(1->0): exp
time(0->1): pow
@author: zziya
"""
import networkx as nx
import numpy as np
import math
import random
import copy
import matplotlib.pyplot as plt
def powerlaw_sample(alpha):
    xmin=1
    result=999999999
    while result>10000:
        u=random.uniform(0,1)
        result=xmin*math.pow(u, 1/(1-alpha))
    return result
def get_active_subgraph(G,edge_state):
    g_temp=copy.deepcopy(G)
    remove_set=[k for k,v in edge_state.items() if v==1]
    g_temp.remove_edge_from(remove_set)
    return g_temp
def count_random_walk_proba(i,j,G,edge_state):
    neis=G.neighbors(i)
    actneis=0
    for k in neis:
        if ((i,k) in edge_set and edge_state[(i,k)]==0):
            actneis+=1
        elif ((k,i) in edge_set and edge_state[(k,i)]==0):
            actneis+=1
    if ((i,j) in edge_set and edge_state[(i,j)]==1):
        return 0
    elif ((j,i) in edge_set and edge_state[(j,i)]==1):
        return 0
    else:
        return 1/(actneis)
N=100
k=4
T=200
lam0=2
alpha1=2.6
G=nx.random_regular_graph(k,N)
edge_set=list(G.edges)
#initialization
next_transition={}
edge_state={}
tnow=0
rwp={}
for i in G.nodes:
    for j in G.nodes:
        rwp[(i,j)]=[]
for i in edge_set:
    proba=random.uniform(0,1)
    if proba<0.5:
        edge_state[i]=0
        next_transition[i]=powerlaw_sample(alpha1)
    else:
        edge_state[i]=1
        next_transition[i]=random.expovariate(lam0)
while (tnow<T):
    print('\r tnow : {:.2f}'.format(tnow), end='   ')
    state_transition_time=min(next_transition.values())
    changer=min(next_transition.items(),key=lambda x: x[1])[0]
    tnow=next_transition[changer]
    if edge_state[changer]==0:
        edge_state[changer]=1
        next_transition[changer]+=random.expovariate(lam0)
    else:
        edge_state[changer]=0
        next_transition[changer]+=powerlaw_sample(alpha1)
    if tnow>100:
        for i in G. nodes:
            for j in G.neighbors(i):
                temp=count_random_walk_proba(i,j,G,edge_state)
                if temp!=0:
                    rwp[(i,j)].append(temp)
rs=[]
for i in G.nodes:
    for j in G.neighbors(i):
        print(np.mean(rwp[(i,j)]))
        rs.append(np.mean(rwp[(i,j)]))
print('============')
l=np.mean(rs)
print(l)
q0=((alpha1-1)/(alpha1-2)/(1/lam0+(alpha1-1)/(alpha1-2)))
print((1-(1-q0)**k)/k)
print(l/(1-(1-q0)**k))