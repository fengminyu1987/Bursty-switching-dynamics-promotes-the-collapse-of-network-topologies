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
import matplotlib.pyplot as plt
import random
import copy
from scipy.special import comb
import json
def powerlaw_sample(alpha):
    xmin=1
    result=999999999
    while result>10000:
        u=random.uniform(0,1)
        result=xmin*math.pow(u, 1/(1-alpha))
    return result
'''
def powerlaw_sample(alpha):
    xmin=1
    rng=np.random.default_rng()
    cdf=rng.random(1)
    rvs=xmin*(1-cdf)**(1.0/(1-alpha))
    return rvs[0]'''
def get_active_subgraph(G,edge_state):
    g_temp=copy.deepcopy(G)
    remove_set=[k for k,v in edge_state.items() if v==1]
    g_temp.remove_edges_from(remove_set)
    return g_temp
k=4
Ks=[2,4,8]
lam0=1
alpha1=2.6
Alpha1=[2.6, 3.7, 4.8]
Lam0=np.linspace(0.5,2,25)
Cs=['#D7A944', '#5F8197', '#DF97C8']
LSs=['solid','--','dotted']
Ms=['>','^','v']
network_type='ia-crime-moreno'
NetworkSet=['bio-yeast','bn-mouse-kasthuri_graph_v4','bio-CE-HT', 'bio-CE-LC','ia-crime-moreno','rt-twitter-copen']
filename='.\\saves\\nets\\'+network_type+'.txt'
'''
G=nx.Graph()
with open(filename) as file:
    for line in file:
        head, tail=[str(x) for x in line.split()]
        G.add_edge(int(head),int(tail))
N=G.number_of_nodes()
component_result={}
for alpha1 in Alpha1:
    temp_component=[]
    for lam0 in Lam0:
        print('\r network : {}, alpha : {:.2f}, lam : {:.2f}'.format(network_type,alpha1,lam0), end='     ')
        edge_set=list(G.edges)
        #initialization
        next_transition={}
        edge_state={}
        tnow=0
        edge_number=len(edge_set)
        component_list=[]
        act_edge=0
        for i in edge_set:
            proba=random.uniform(0,1)
            if proba<0.5:
                edge_state[i]=0
                act_edge+=1
                next_transition[i]=powerlaw_sample(alpha1)
                #next_transition[i]=powerlaw.Power_Law(xmin=1, parameters=[alpha1]).generate_random(1)[0]
            if proba>0.5:
                edge_state[i]=1
                next_transition[i]=random.expovariate(lam0)
        while (tnow<150):
            state_transition_time=min(next_transition.values())
            changer=min(next_transition.items(),key=lambda x: x[1])[0]
            tnow=next_transition[changer]
            if edge_state[changer]==0:
                edge_state[changer]=1
                act_edge-=1
                next_transition[changer]+=random.expovariate(lam0)
            else:
                edge_state[changer]=0
                act_edge+=1
                next_transition[changer]+=powerlaw_sample(alpha1)
            #print('\r tnow : {:.2f}, edge : {:d}, q0M : {:.2f}'.format(tnow, edge_number-sum(edge_state.values()),q0*edge_number), end='    ')
            if tnow>80:
                g=get_active_subgraph(G,edge_state)
                glargest=max(nx.connected_components(g),key=len)
                component_list.append(len(glargest)/N)
        temp_component.append(np.mean(np.array(component_list)))
    component_result['{:.2f}'.format(alpha1)]=temp_component
json_str=json.dumps(component_result)
with open('.\\saves\\component\\{}.json'.format(network_type), 'w') as json_file:
    json_file.write(json_str)'''
plt.figure(figsize=(8,8))
filename1='.\\saves\\component\\{}.json'.format(network_type)
f1=open(filename1)
data1=json.load(f1)
for alpha1 in Alpha1:
    tep=data1["{:.2f}".format(alpha1)]
    plt.plot(Lam0, tep, c=Cs[Alpha1.index(alpha1)],label='$\\alpha={:.2f}$'.format(alpha1),marker=Ms[Alpha1.index(alpha1)],linestyle=LSs[Alpha1.index(alpha1)],markersize=18,lw=2.5)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.ylim([0,1])
plt.grid()
plt.xlabel('$\lambda$', fontsize=20)
#plt.xscale('log')
if network_type=='bio-yeast':
    plt.legend(fontsize=20)
    plt.ylabel('$R_L$', fontsize=23)
elif network_type=='ia-crime-moreno':
    plt.ylabel('$R_L$', fontsize=23)
else:
    ax = plt.gca()
    ax.axes.yaxis.set_ticklabels([])
plt.savefig('.\\saves\\maximum_component_{}.pdf'.format(network_type), bbox_inches='tight', dpi=500)
plt.show()