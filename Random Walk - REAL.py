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
avgs=100
k=4#4, 6, 8
network_type='ia-crime-moreno'#'rrg','wsn','ban', 'sln'
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
def cover_rate(G,is_node_covered):
    return sum(is_node_covered.values())/G.number_of_nodes()
result={}
c=1
delta=1
lam0=2
Lam0=[0.5,2.0,3.5]
alpha1=2.6
filename='.\\saves\\nets\\'+network_type+'.txt'
'''G=nx.Graph()
with open(filename) as file:
    for line in file:
        head, tail=[str(x) for x in line.split()]
        G.add_edge(int(head),int(tail))
N=G.number_of_nodes()
component_result={}
edge_set=list(G.edges)
for lam0 in Lam0:
    q0=((alpha1-1)/(alpha1-2)/(1/lam0+((alpha1-1)/(alpha1-2))))
    cover_list=np.zeros(21)
    for avg in range(avgs):
        print('\r net : {}, lam0 : {:.2f}, avg : {:d}'.format(network_type,lam0,avg), end='     ')
        commd=0
        #initialization
        next_transition={}
        edge_state={}
        node_state={}
        is_node_covered={}#0: not covered, 1 : covered
        update_time=random.expovariate(1)
        tnow=0
        for i in edge_set:
            proba=random.uniform(0,1)
            if proba<q0:
                edge_state[i]=0
                next_transition[i]=powerlaw_sample(alpha1)
            else:
                edge_state[i]=1
                next_transition[i]=random.expovariate(lam0)
        for j in G.nodes:
            is_node_covered[j]=0
        walker_position=random.choice(list(G.nodes))
        sup=0
        while (tnow<2000):
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
                is_node_covered[walker_position]=1
            if tnow>commd:
                commd+=100
                cover_list[sup]+=cover_rate(G,is_node_covered)
                sup+=1
    cover_list=cover_list/avgs
    result['{:.2f}'.format(lam0)]=list(cover_list)
    json_str=json.dumps(result)
    with open('.\\saves\\random walk\\{}_{:.2f}.json'.format(network_type,lam0), 'w') as json_file:
        json_file.write(json_str)
with open('.\\saves\\random walk\\{}.json'.format(network_type), 'w') as json_file:
    json_file.write(json_str)'''
filename='.\\saves\\random walk\\{}.json'.format(network_type)
f=open(filename)
data=json.load(f)
plt.figure(figsize=(8,8))
for lam0 in Lam0:
    tep=data['{:.2f}'.format(lam0)]
    timelist=np.linspace(0,2000,21)
    plt.plot(timelist,tep,c=Cs[Lam0.index(lam0)],label='$\lambda={:.2f}$'.format(lam0),marker=Ms[Lam0.index(lam0)],markersize=20,lw=2.5,linestyle=LSs[Lam0.index(lam0)])
plt.yticks(fontsize=20)
plt.ylim([0,0.7])
plt.xticks(np.arange(0,2000,step=400),fontsize=20)
plt.xlabel('$t$', fontsize=23)
if network_type=='bio-yeast':
    plt.legend(fontsize=25)
    plt.ylabel('$R_C$', fontsize=23)
elif network_type=='ia-crime-moreno':
    plt.ylabel('$R_C$', fontsize=23)
else:
    ax = plt.gca()
    ax.axes.yaxis.set_ticklabels([])
plt.grid()
plt.savefig('.\\saves\\coverratio_{}.pdf'.format(network_type), bbox_inches='tight', dpi=500)
plt.show()