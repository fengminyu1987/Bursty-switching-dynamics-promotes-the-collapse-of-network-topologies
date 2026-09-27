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
from matplotlib.ticker import ScalarFormatter
import copy
import powerlaw
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
    g_temp.remove_edge_from(remove_set)
    return g_temp
N=2000
k=4
Ks=[4, 8, 12]
lam0=0.5
alpha1=2.6
Lam0=np.linspace(0.5,2,25)
Cs=['#C6A580', '#5C1624', '#12559A']
LSs=['solid','--','dotted']
Ms=['o','^','v']
network_type='ban'
NT=['ban', 'wsn']
q0=((alpha1-1)/(alpha1-2)/(1/lam0+(alpha1-1)/(alpha1-2)))
test=(1-q0)**8
'''
for network_type in NT:
    density_result={}
    for k in Ks:
        temp_density=[]
        for lam0 in Lam0:
            print('\r network : {}, k : {:d}, lam : {:.2f}'.format(network_type,k,lam0), end='     ')
            if network_type=='ban':
                G=nx.generators.barabasi_albert_graph(N, int(k/2))
            if network_type=='wsn':
                G=nx.generators.watts_strogatz_graph(N, k, .25)
            edge_set=list(G.edges)
            #initialization
            next_transition={}
            edge_state={}
            tnow=0
            edge_number=len(edge_set)
            density_list=[]
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
            while (tnow<300):
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
                if tnow>100:
                    density_list.append(2*act_edge/(N*(N-1)))
            temp_density.append(np.mean(np.array(density_list)))
        density_result['{:d}'.format(k)]=temp_density
        q0=((alpha1-1)/(alpha1-2)/(1/Lam0+(alpha1-1)/(alpha1-2)))
        density_result['{:d}'.format(k+1)]=list(2*q0*edge_number/(N*(N-1)))
    json_str=json.dumps(density_result)
    with open('.\\saves\\density\\{}.json'.format(network_type), 'w') as json_file:
        json_file.write(json_str)
plt.figure(figsize=(8,8))
ax1=plt.subplot(211)
network_type='ban'
filename1='.\\saves\\density\\{}.json'.format(network_type)
f1=open(filename1)
data1=json.load(f1)
for k in Ks:
    tep=data1["{:d}".format(k)]
    plt.scatter(Lam0, tep, c=Cs[Ks.index(k)],label='$k={:d}$'.format(k),marker=Ms[Ks.index(k)],s=120)
    plt.plot(Lam0, data1['{:d}'.format(k+1)],c=Cs[Ks.index(k)],lw=2.5,linestyle=LSs[Ks.index(k)])
plt.setp(ax1.get_xticklabels(), fontsize=6,visible=False)
plt.legend(fontsize=15)
plt.grid()
plt.ylabel('$BAN$', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
y_formatter=ScalarFormatter(useMathText=True)
ax1.yaxis.set_major_formatter(y_formatter)
ax2=plt.subplot(212)
network_type='wsn'
filename2='.\\saves\\density\\{}.json'.format(network_type)
f2=open(filename2)
data2=json.load(f2)
for k in Ks:
    tep=data2["{:d}".format(k)]
    plt.scatter(Lam0, tep, c=Cs[Ks.index(k)],label='$k={:d}$'.format(k),marker=Ms[Ks.index(k)],s=120)
    plt.plot(Lam0, data2['{:d}'.format(k+1)],c=Cs[Ks.index(k)],lw=2.5,linestyle=LSs[Ks.index(k)])
plt.grid()
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('$\lambda$', fontsize=20)
plt.ylabel('$WSN$', fontsize=20)
y_formatter=ScalarFormatter(useMathText=True)
ax2.yaxis.set_major_formatter(y_formatter)
#plt.xscale('log')
plt.savefig('.\\saves\\density.pdf', bbox_inches='tight', dpi=500)
plt.show()'''