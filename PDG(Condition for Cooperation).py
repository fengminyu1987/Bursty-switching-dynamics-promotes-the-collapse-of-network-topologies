# -*- coding: utf-8 -*-
"""
Edge Switching Dynamics
Created on Wed Jul 12 18:09:33 2023
time(1->0): exp
time(0->1): pow
k=4, 6, 8
lam0=0.5,1,1.5,2
@author: zziya
"""
regularset=['sln', 'rrg']
realset=['dolphins','americanfootball','contiguous-usa','zebra']
import networkx as nx
import numpy as np
import math
import matplotlib.pyplot as plt
import random
import json
import copy
avgs=30000
k=4#4, 6, 8
network_type='dolphins'#'rrg','wsn','ban', 'sln'
def powerlaw_sample(alpha):
    xmin=1
    result=99999
    while result>10000:
        u=random.uniform(0,1)
        result=xmin*math.pow(u, 1/(1-alpha))
    return result
def get_active_subgraph(G,edge_state):
    g_temp=copy.deepcopy(G)
    remove_set=[k for k,v in edge_state.items() if v==1]
    g_temp.remove_edge_from(remove_set)
    return g_temp
def get_fitness(G, node_state, edge_state, edge_set, node, payoffmat):
    neis=[]
    result=0
    for nei in G.neighbors(node):
        if (nei, node) in edge_set:
            if edge_state[(nei, node)]==0:
                neis.append(nei)
        elif (node, nei) in edge_set:
            if edge_state[(node,nei)]==0:
                neis.append(nei)
    for nei in neis:
        result+=payoffmat[node_state[node]][node_state[nei]]
    return 1+0.01*result
def DB_update(changer, G, node_state, edge_state, edge_set,payoffmat):
    neis=[]
    for nei in G.neighbors(changer):
        if (nei, changer) in edge_set:
            if edge_state[(nei, changer)]==0:
                neis.append(nei)
        elif (changer, nei) in edge_set:
            if edge_state[(changer,nei)]==0:
                neis.append(nei)
    kcfc=0
    kdfd=0
    for nei in neis:
        if node_state[nei]==0:
            kcfc+=get_fitness(G, node_state, edge_state, edge_set, nei, payoffmat)
        if node_state[nei]==1:
            kdfd+=get_fitness(G, node_state, edge_state, edge_set, nei, payoffmat)
    if kcfc+kdfd==0:
        return node_state[changer]
    if random.uniform(0,1)<(kcfc/(kcfc+kdfd)):
        return 0
    else:
        return 1
N=100
c=1
delta=1
lam0=2
alpha1=2.6
if network_type=='sln':
    L=10
    k=4
    N=L*L
    H=nx.grid_2d_graph(L,L, periodic=True)
    #change the label to accelerate
    new_mapping={}
    for i in H.nodes:
        new_mapping[i]=i[0]*L+i[1]
    G = nx.relabel_nodes(H, new_mapping)
if network_type=='ern':
    G=nx.random_graphs.erdos_renyi_graph(N, 0.2)
if network_type=='nwn':
    G=nx.newman_watts_strogatz_graph(N, k, 0.2)
if network_type=='rrg':
    G=nx.random_regular_graph(k,N)
if network_type=='wsn':
    G=nx.generators.watts_strogatz_graph(N, k, 0.05)
if network_type=='ban':
    G=nx.generators.barabasi_albert_graph(N, int(k/2))
#thm=(N-2)/((N/k)-2)
#B=np.arange(thm, 1+thm, 1)
if k==4:
    B=np.linspace(2,6,10)
if k==6:
    B=np.linspace(4,8,10)
if k==8:
    B=np.linspace(6,10,10)
if network_type in realset:
    k=0
    filename='.\\saves\\nets\\'+network_type+'.txt'
    G=nx.Graph()
    with open(filename) as file:
        for line in file:
            head, tail=[str(x) for x in line.split()]
            G.add_edge(int(head),int(tail))
    if network_type=='dolphins':
        B=np.linspace(4.5,8.5,10)
    if network_type=='americanfootball':
        B=np.linspace(10.8,14.8,10)
    if network_type=='contiguous-usa':
        B=np.linspace(3.5,7.5,10)
    if network_type=='zebra':
        B=np.linspace(6,10,10)
edge_set=list(G.edges)
q0=((alpha1-1)/(alpha1-2)/(1/lam0+((alpha1-1)/(alpha1-2))))
N=G.number_of_nodes()
#Cinvade
#0:C, 1:D
resultc={}
for b in B:
    c_absorb_number=0
    payoffmat=[[b-c, -c], [b, 0]]
    print('\r C, NET : {}, b : {:.2f}, lam : {:.2f}, alpha : {:.2f}, k : {:d}'.format(network_type,b,lam0,alpha1,k), end='      ')
    for avg in range(avgs):
        #initialization
        next_transition={}
        edge_state={}
        node_state={}
        update_time={}
        tnow=0
        for i in edge_set:
            proba=random.uniform(0,1)
            if proba<q0:
                edge_state[i]=0
                next_transition[i]=powerlaw_sample(alpha1)
            else:
                edge_state[i]=1
                next_transition[i]=random.expovariate(lam0)
        for i in G.nodes:
            node_state[i]=1
            update_time[i]=random.expovariate(delta)
        node_state[random.choice(list(G.nodes))]=0
        while (True):
            fc=(N-sum(node_state.values()))/N
            state_transition_time=min(next_transition.values())
            update_strategy_time=min(update_time.values())
            if state_transition_time<update_strategy_time:
                changer=min(next_transition.items(),key=lambda x: x[1])[0]
                tnow=next_transition[changer]
                if edge_state[changer]==0:#become inactive
                    edge_state[changer]=1
                    next_transition[changer]+=random.expovariate(lam0)
                else:#become active and update state
                    edge_state[changer]=0
                    next_transition[changer]+=powerlaw_sample(alpha1)
            else:
                updater=min(update_time.items(),key=lambda x: x[1])[0]
                tnow=update_time[updater]
                node_state[updater]=DB_update(updater, G, node_state, edge_state, edge_set, payoffmat)
                update_time[updater]+=random.expovariate(delta)
            if fc==1:
                c_absorb_number+=1
                break
            if fc==0:
                break
            #print('\r C INVADE net : {}, lam : {:.2f}, alpha : {:.2f}, b : {:.2f}, tnow : {:.2f}, fc : {:.3f}, avgs : {:d}, k : {:d}, Nc : {:d}'.format(network_type,lam0,alpha1,b, tnow, fc, avg,k,c_absorb_number), end='      ')
    rhoc=c_absorb_number/avgs
    resultc['{:.4f}'.format(b)]=rhoc
json_str=json.dumps(resultc)
if network_type in regularset:
    with open('.\\saves\\pdg\\{}\\C{:.2f}_{:.2f}_{}_{:d}_{:d}.json'.format(network_type,lam0,alpha1,network_type,k,N), 'w') as json_file:
        json_file.write(json_str)
if network_type in realset:
    with open('.\\saves\\pdg\\C{:.2f}_{:.2f}_{}.json'.format(lam0,alpha1,network_type), 'w') as json_file:
        json_file.write(json_str)
#Dinvade
#0:C, 1:D
resultd={}
for b in B:
    d_absorb_number=0
    payoffmat=[[b-c, -c], [b, 0]]
    print('\r D, NET : {}, b : {:.2f}, lam : {:.2f}, alpha : {:.2f}, k : {:d}'.format(network_type,b,lam0,alpha1,k), end='      ')
    for avg in range(avgs):
        #initialization
        next_transition={}
        edge_state={}
        node_state={}
        update_time={}
        tnow=0
        for i in edge_set:
            proba=random.uniform(0,1)
            if proba<q0:
                edge_state[i]=0
                next_transition[i]=powerlaw_sample(alpha1)
            else:
                edge_state[i]=1
                next_transition[i]=random.expovariate(lam0)
        for i in G.nodes:
            node_state[i]=0
            update_time[i]=random.expovariate(delta)
        node_state[random.choice(list(G.nodes))]=1
        while (True):
            fc=(N-sum(node_state.values()))/N
            state_transition_time=min(next_transition.values())
            update_strategy_time=min(update_time.values())
            if state_transition_time<update_strategy_time:
                changer=min(next_transition.items(),key=lambda x: x[1])[0]
                tnow=next_transition[changer]
                if edge_state[changer]==0:#become inactive
                    edge_state[changer]=1
                    next_transition[changer]+=random.expovariate(lam0)
                else:#become active and update state
                    edge_state[changer]=0
                    next_transition[changer]+=powerlaw_sample(alpha1)
            else:
                updater=min(update_time.items(),key=lambda x: x[1])[0]
                tnow=update_time[updater]
                node_state[updater]=DB_update(updater, G, node_state, edge_state, edge_set, payoffmat)
                update_time[updater]+=random.expovariate(delta)
            if fc==0:
                d_absorb_number+=1
                break
            if fc==1:
                break
            #print('\r D INVADE net : {}, lam : {:.2f}, alpha : {:.2f}, b : {:.2f}, tnow : {:.2f}, fc : {:.3f}, avgs : {:d}, k : {:d}, Nc : {:d}'.format(network_type,lam0,alpha1,b, tnow, fc, avg,k,c_absorb_number), end='      ')
    rhod=d_absorb_number/avgs
    resultd['{:.4f}'.format(b)]=rhod
json_str=json.dumps(resultd)
if network_type in regularset:
    with open('.\\saves\\pdg\\{}\\D{:.2f}_{:.2f}_{}_{:d}_{:d}.json'.format(network_type,lam0,alpha1,network_type,k,N), 'w') as json_file:
        json_file.write(json_str)
if network_type in realset:
    with open('.\\saves\\pdg\\D{:.2f}_{:.2f}_{}.json'.format(lam0,alpha1,network_type), 'w') as json_file:
        json_file.write(json_str)