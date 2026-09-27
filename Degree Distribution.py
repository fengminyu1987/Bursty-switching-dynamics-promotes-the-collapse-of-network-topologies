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
    g_temp.remove_edges_from(remove_set)
    return g_temp
def get_degree_distribution(G):
    degree=nx.degree_histogram(G)
    x=range(len(degree))
    y=[z/float(sum(degree))for z in degree]
    return x,y
def adj(A,edge_state):
    temp_A=copy.deepcopy(A)
    for i in range(len(temp_A)):
        for j in range(i, len(temp_A)):
            if (i,j) in edge_state.keys() and edge_state[(i,j)]==1:
                temp_A[i][j]=0
                temp_A[j][i]=0
            elif (j,i) in edge_state.keys() and edge_state[(j,i)]==1:
                temp_A[i][j]=0
                temp_A[j][i]=0
    return temp_A
def spectral_radius(M):
    a,b=np.linalg.eig(M)
    return np.max(np.abs(a))
N=1000
k=6
K=[4, 8]
lam0=1
alpha1=2.6
p0=((alpha1-1)/(alpha1-2)/(1/lam0+(alpha1-1)/(alpha1-2)))
p1=1-p0
#G=nx.random_regular_graph(k,N)
plt.figure(figsize=(8,8))
ax1=plt.subplot(211)
Cs=['#2F5B47','#C777BE']
Ms=['v','^','o']
for k in K:
    network_type='ban'
    G=nx.generators.barabasi_albert_graph(N, int(k/2))
    #G=nx.generators.watts_strogatz_graph(N, 10, .4)
    M=G.number_of_edges()
    edge_set=list(G.edges)
    #initialization
    next_transition={}
    edge_state={}
    stay_active={}
    stay_inactive={}
    tnow=0
    commd=10
    actedges=0
    inactedges=0
    for i in edge_set:
        proba=random.uniform(0,1)
        stay_active[i]=0
        stay_inactive[i]=0
        if proba<p0:
            edge_state[i]=0
            next_transition[i]=powerlaw_sample(alpha1)
            stay_active[i]+=next_transition[i]
            actedges+=1
        else:
            edge_state[i]=1
            next_transition[i]=random.expovariate(lam0)
            stay_inactive[i]+=next_transition[i]
            inactedges+=1
    print('\r k : {:d}, network : {}'.format(k, network_type), end='           ')
    while (tnow<100):
        state_transition_time=min(next_transition.values())
        changer=min(next_transition.items(),key=lambda x: x[1])[0]
        tnow=next_transition[changer]
        if edge_state[changer]==0:
            edge_state[changer]=1
            temp_time=random.expovariate(lam0)
            next_transition[changer]+=temp_time
            stay_inactive[changer]+=temp_time
            inactedges+=1
            actedges-=1
        else:
            edge_state[changer]=0
            temp_time=powerlaw_sample(alpha1)
            next_transition[changer]+=temp_time
            stay_active[changer]+=temp_time
            inactedges-=1
            actedges+=1
        if tnow>=commd:
            g=get_active_subgraph(G, edge_state)
            x,y=get_degree_distribution(g)
            plt.scatter(x,y,c=Cs[K.index(k)],alpha=.5,marker=Ms[K.index(k)],s=80)
            commd+=2
    plt.scatter(x,y,c=Cs[K.index(k)],alpha=.8,marker=Ms[K.index(k)],s=80,label='$\\left\\langle k\\right\\rangle={:d}$'.format(k))
    degree=nx.degree_histogram(G)
    x=list(range(len(degree)))
    y=[z/float(sum(degree))for z in degree]
    ynew=[]
    for i in x:
        temp=0
        for j in range(i, len(x)):
            temp+=math.comb(j, i)*(p0**i)*(p1**(j-i))*y[j]
        ynew.append(temp)
    plt.plot(x,ynew, c=Cs[K.index(k)], lw=2.5)
plt.legend(fontsize=25)
plt.grid()
plt.ylabel('$BAN$', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xscale('log')
ax2=plt.subplot(212)
for k in K:
    network_type='wsn'
    G=nx.generators.watts_strogatz_graph(N, k, .25)
    M=G.number_of_edges()
    edge_set=list(G.edges)
    #initialization
    next_transition={}
    edge_state={}
    stay_active={}
    stay_inactive={}
    tnow=0
    commd=10
    actedges=0
    inactedges=0
    for i in edge_set:
        proba=random.uniform(0,1)
        stay_active[i]=0
        stay_inactive[i]=0
        if proba<p0:
            edge_state[i]=0
            next_transition[i]=powerlaw_sample(alpha1)
            stay_active[i]+=next_transition[i]
            actedges+=1
        else:
            edge_state[i]=1
            next_transition[i]=random.expovariate(lam0)
            stay_inactive[i]+=next_transition[i]
            inactedges+=1
    print('\r k : {:d}, network : {}'.format(k, network_type), end='           ')
    while (tnow<100):
        state_transition_time=min(next_transition.values())
        changer=min(next_transition.items(),key=lambda x: x[1])[0]
        tnow=next_transition[changer]
        if edge_state[changer]==0:
            edge_state[changer]=1
            temp_time=random.expovariate(lam0)
            next_transition[changer]+=temp_time
            stay_inactive[changer]+=temp_time
            inactedges+=1
            actedges-=1
        else:
            edge_state[changer]=0
            temp_time=powerlaw_sample(alpha1)
            next_transition[changer]+=temp_time
            stay_active[changer]+=temp_time
            inactedges-=1
            actedges+=1
        if tnow>=commd:
            g=get_active_subgraph(G, edge_state)
            x,y=get_degree_distribution(g)
            plt.scatter(x,y,c=Cs[K.index(k)],marker=Ms[K.index(k)],alpha=.5,s=65)
            commd+=2
    plt.scatter(x,y,c=Cs[K.index(k)],marker=Ms[K.index(k)],alpha=.8,s=65)
    degree=nx.degree_histogram(G)
    x=list(range(len(degree)))
    y=[z/float(sum(degree))for z in degree]
    ynew=[]
    for i in x:
        temp=0
        for j in range(i, len(x)):
            temp+=math.comb(j, i)*(p0**i)*(p1**(j-i))*y[j]
        ynew.append(temp)
    plt.plot(x,ynew, c=Cs[K.index(k)], lw=2.5)
plt.grid()
plt.ylabel('$WSN$', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('$k$', fontsize=20)
plt.savefig('.\\saves\\degree_distribution.pdf', bbox_inches='tight', dpi=500)
plt.show()