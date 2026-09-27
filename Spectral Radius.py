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
import matplotlib.pyplot as plt
import copy
import json
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
def spectral_radius(M):
    a,b=np.linalg.eig(M)
    return np.max(np.abs(a))
N=2000
k=8
K=[4,8,12]
lam0=1
Lam0=np.linspace(0.5,2,100)
Cs=['red', 'blue', 'green']
LSs=['solid','--','dotted']
alpha1=2.6
'''
network_type='ban'
result_ban={}
for k in K:
    G=nx.generators.barabasi_albert_graph(N, int(k/2))
    A=[]
    for i in G.nodes:
        Atemp=[]
        for j in G.nodes:
            if G.has_edge(i,j):
                Atemp.append(1)
            else:
                Atemp.append(0)
        A.append(Atemp)
    plt.figure(figsize=(8,8))
    temp_res=[]
    for lam0 in Lam0:
        q0=((alpha1-1)/(alpha1-2)/(1/lam0+(alpha1-1)/(alpha1-2)))
        temp_res.append(spectral_radius(q0*np.array(A)))
    result_ban['{:d}'.format(k)]=temp_res
json_str=json.dumps(result_ban)
with open('.\\saves\\{}.json'.format(network_type), 'w') as json_file:
    json_file.write(json_str)
network_type='wsn'
result_wsn={}
for k in K:
    G=nx.generators.watts_strogatz_graph(N, k, .25)
    A=[]
    for i in G.nodes:
        Atemp=[]
        for j in G.nodes:
            if G.has_edge(i,j):
                Atemp.append(1)
            else:
                Atemp.append(0)
        A.append(Atemp)
    plt.figure(figsize=(8,8))
    temp_res=[]
    for lam0 in Lam0:
        q0=((alpha1-1)/(alpha1-2)/(1/lam0+(alpha1-1)/(alpha1-2)))
        temp_res.append(spectral_radius(q0*np.array(A)))
    result_wsn['{:d}'.format(k)]=temp_res
json_str=json.dumps(result_wsn)
with open('.\\saves\\{}.json'.format(network_type), 'w') as json_file:
    json_file.write(json_str)
'''
plt.figure(figsize=(8,8))
ax1=plt.subplot(211)
network_type='ban'
filename1='.\\saves\\spectral radius\\{}.json'.format(network_type)
f1=open(filename1)
data1=json.load(f1)
for k in K:
    tep=data1["{:d}".format(k)]
    plt.plot(Lam0, tep, c=Cs[K.index(k)],label='$k={:d}$'.format(k),lw=4.5,linestyle=LSs[K.index(k)])
plt.setp(ax1.get_xticklabels(), fontsize=6,visible=False)
plt.legend(fontsize=15)
plt.grid()
plt.ylabel('$BAN$', fontsize=20)
plt.ylim([2,22])
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax2=plt.subplot(212)
network_type='wsn'
filename2='.\\saves\\spectral radius\\{}.json'.format(network_type)
f2=open(filename2)
data2=json.load(f2)
for k in K:
    tep=data2["{:d}".format(k)]
    plt.plot(Lam0, tep, c=Cs[K.index(k)],label='$k={:d}$'.format(k),lw=4.5,linestyle=LSs[K.index(k)])
plt.grid()
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('$\lambda$', fontsize=20)
plt.ylabel('$WSN$', fontsize=20)
plt.ylim([2,22])
#plt.xscale('log')
plt.savefig('.\\saves\\spectral_radius.pdf', bbox_inches='tight', dpi=500)
plt.show()