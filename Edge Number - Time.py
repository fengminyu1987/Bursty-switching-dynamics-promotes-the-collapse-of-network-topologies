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
import powerlaw
from scipy.special import comb
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
    g_temp.remove_edge_from(remove_set)
    return g_temp
N=100
k=4
lam0=1
alpha1=2.6
Lam0=[0.5, 1, 2]
Alpha1=[2.6, 3.1, 3.7]
Cs=['red', 'green', 'blue']
plt.figure(figsize=(8,8))
for lam0 in Lam0:
    G=nx.random_regular_graph(k,N)
    edge_set=list(G.edges)
    #initialization
    next_transition={}
    edge_state={}
    tnow=0
    edge_number=len(edge_set)
    q0=((alpha1-1)/(alpha1-2)/(1/lam0+(alpha1-1)/(alpha1-2)))
    for i in edge_set:
        proba=random.uniform(0,1)
        if proba<0.5:
            edge_state[i]=0
            next_transition[i]=powerlaw_sample(alpha1)
            #next_transition[i]=powerlaw.Power_Law(xmin=1, parameters=[alpha1]).generate_random(1)[0]
        if proba>0.5:
            edge_state[i]=1
            next_transition[i]=random.expovariate(lam0)
    edge_number_list=[edge_number-sum(edge_state.values())]
    time_list=[0]
    while (tnow<1000):
        state_transition_time=min(next_transition.values())
        changer=min(next_transition.items(),key=lambda x: x[1])[0]
        tnow=next_transition[changer]
        time_list.append(tnow)
        if edge_state[changer]==0:
            edge_state[changer]=1
            next_transition[changer]+=random.expovariate(lam0)
        else:
            edge_state[changer]=0
            next_transition[changer]+=powerlaw_sample(alpha1)
        print('\r tnow : {:.2f}, edge : {:d}, q0M : {:.2f}'.format(tnow, edge_number-sum(edge_state.values()),q0*edge_number), end='    ')
        edge_number_list.append(edge_number-sum(edge_state.values()))
    plt.plot(time_list,edge_number_list,c=Cs[Lam0.index(lam0)],lw=2, label='$\\lambda={:.2f}$'.format(lam0))
plt.xlim([0.01,1000])
plt.ylim([80,220])
plt.xscale('log')
plt.grid()
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('$t$', fontsize=20)
plt.ylabel('$m$', fontsize=20)
plt.legend(fontsize=23)
plt.savefig('.\\saves\\edge_number_time.pdf', bbox_inches='tight', dpi=500)
plt.show()
#打印KL散度值
#kl=0
#for i in xs:
#    kl+=counter[i]*np.log(counter[i]/ys[xs.index(i)])
#print("KL = {:.3f}\n".format(kl),end="")