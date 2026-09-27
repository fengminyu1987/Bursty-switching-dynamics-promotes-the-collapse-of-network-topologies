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
import networkx as nx
import numpy as np
import math
import matplotlib.pyplot as plt
import random
import json
import copy
avgs=1
k=4#4, 6, 8
network_type='ca-netscience'#'rrg','wsn','ban', 'sln'
def powerlaw_sample(alpha):
    xmin=1
    result=99999
    while result>10000:
        u=random.uniform(0,1)
        result=xmin*math.pow(u, 1/(1-alpha))
    return result
Cs=['#A61333','#6C788C','#288142','#45372E']
Ms=['^','v','<','>']
LSs=['solid','--','dotted','-.']
NetworkSet=['bio-yeast','bn-mouse-kasthuri_graph_v4','ca-netscience','bio-CE-HT', 'bio-CE-LC','ia-crime-moreno','rt-twitter-copen']
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
def activated_neighbors(i, G, edge_state):
    result=[]
    for j in G.neighbors(i):
        if (i, j) in edge_set:
            if edge_state[(i, j)]==0:
                result.append(j)
        elif (j, i) in edge_set:
            if edge_state[(j, i)]==0:
                result.append(j)
    return result
def cover_rate(G,is_edge_covered):
    return sum(is_edge_covered.values())/G.number_of_edges()
result={}
c=1
delta=1
lam0=2
Lam0=[0.5,2]
alpha1=2.6
filename='.\\saves\\nets\\'+network_type+'.txt'
G=nx.Graph()
with open(filename) as file:
    for line in file:
        head, tail=[str(x) for x in line.split()]
        G.add_edge(int(head),int(tail))
N=G.number_of_nodes()
component_result={}
edge_set=list(G.edges)
for lam0 in Lam0:
    q0=((alpha1-1)/(alpha1-2)/(1/lam0+((alpha1-1)/(alpha1-2))))
    for avg in range(avgs):
        print('\r net : {}, lam0 : {:.2f}, avg : {:d}'.format(network_type,lam0,avg), end='     ')
        commd=0
        #initialization
        next_transition={}
        edge_state={}
        node_state={}
        is_edge_covered={}#0: not covered, 1 : covered
        update_time=random.expovariate(1)
        tnow=0
        for i in edge_set:
            is_edge_covered[i]=0
            proba=random.uniform(0,1)
            if proba<q0:
                edge_state[i]=0
                next_transition[i]=powerlaw_sample(alpha1)
            else:
                edge_state[i]=1
                next_transition[i]=random.expovariate(lam0)
        walker_position=random.choice(list(G.nodes))
        cover_list=np.zeros(51)
        sup=0
        while (tnow<1000):
            state_transition_time=min(next_transition.values())
            if state_transition_time<update_time:
                changer=min(next_transition.items(),key=lambda x: x[1])[0]
                tnow=next_transition[changer]
                if edge_state[changer]==0:#become inactive
                    edge_state[changer]=1
                    next_transition[changer]+=random.expovariate(lam0)
                else:#become active and update state
                    edge_state[changer]=0
                    next_transition[changer]+=powerlaw_sample(alpha1)
            else:
                tnow=update_time
                last_position=walker_position
                next_positions=activated_neighbors(walker_position, G, edge_state)
                if len(next_positions)!=0:
                    walker_position=random.choice(next_positions)
                update_time+=random.expovariate(1)
                if (last_position, walker_position) in edge_set:
                    is_edge_covered[(last_position, walker_position)]=1
                if (walker_position, last_position) in edge_set:
                    is_edge_covered[(walker_position, last_position)]=1
            if tnow>commd:
                commd+=20
                cover_list[sup]+=cover_rate(G,is_edge_covered)
                sup+=1
    cover_list=cover_list/avgs
    result['{:.2f}'.format(lam0)]=list(cover_list)
    json_str=json.dumps(result)
    with open('.\\saves\\random walk\\{}_{:.2f}.json'.format(network_type,lam0), 'w') as json_file:
        json_file.write(json_str)
with open('.\\saves\\random walk\\{}.json'.format(network_type), 'w') as json_file:
    json_file.write(json_str)
'''
filename='.\\saves\\random walk\\{}.json'.format(network_type)
f=open(filename)
data=json.load(f)
plt.figure(figsize=(12,8))
k=2
ax1=plt.subplot(131)
for lam0 in Lam0:
    tep=data['{:.2f}_{:d}'.format(lam0,k)]
    timelist=np.linspace(0,1000,51)
    plt.plot(timelist,tep,c=Cs[Lam0.index(lam0)],label='$\lambda={:.2f}$'.format(lam0),marker=Ms[Lam0.index(lam0)],markersize=13,lw=2.5,linestyle=LSs[Lam0.index(lam0)])
plt.yticks(fontsize=20)
plt.ylim([0,1])
plt.xticks(np.arange(0,1000,step=400),fontsize=20)
plt.xlabel('$t$', fontsize=23)
plt.grid()
plt.legend(fontsize=17)
plt.title('$k=2$',fontsize=23)
plt.ylabel('Cover Ratio', fontsize=23)
k=4
ax1=plt.subplot(132)
for lam0 in Lam0:
    tep=data['{:.2f}_{:d}'.format(lam0,k)]
    timelist=np.linspace(0,1000,51)
    plt.plot(timelist,tep,c=Cs[Lam0.index(lam0)],label='$\lambda={:.2f}$'.format(lam0),marker=Ms[Lam0.index(lam0)],markersize=13,lw=2.5,linestyle=LSs[Lam0.index(lam0)])
plt.grid()
plt.yticks(fontsize=20)
plt.ylim([0,1])
plt.xticks(np.arange(0,1000,step=400),fontsize=20)
plt.xlabel('$t$', fontsize=23)
plt.title('$k=4$',fontsize=23)
plt.setp(ax1.get_yticklabels(),visible=False)
k=8
ax1=plt.subplot(133)
for lam0 in Lam0:
    tep=data['{:.2f}_{:d}'.format(lam0,k)]
    timelist=np.linspace(0,1000,51)
    plt.plot(timelist,tep,c=Cs[Lam0.index(lam0)],label='$\lambda={:.2f}$'.format(lam0),marker=Ms[Lam0.index(lam0)],markersize=13,lw=2.5,linestyle=LSs[Lam0.index(lam0)])
plt.grid()
plt.xticks(np.arange(0,1000,step=400),fontsize=20)
plt.ylim([0,1])
plt.yticks(fontsize=20)
plt.xlabel('$t$', fontsize=23)
plt.title('$k=8$',fontsize=23)
plt.setp(ax1.get_yticklabels(),visible=False)
plt.savefig('.\\saves\\coverratio_{}.pdf'.format(network_type), bbox_inches='tight', dpi=500)
plt.show()'''