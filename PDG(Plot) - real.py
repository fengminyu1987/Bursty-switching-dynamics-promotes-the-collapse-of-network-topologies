# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 00:42:52 2023

@author: zziya
"""

import matplotlib.pyplot as plt
import numpy as np
import json
import math
import networkx as nx
def spectral_radius(M):
    a,b=np.linalg.eig(M)
    return np.max(np.abs(a))
#gamma=.15
#setting='{:d}_0.20%_{:.2f}'.format(N, gamma)
realset=['dolphins','americanfootball','contiguous-usa','zebra']
network_type='contiguous-usa'
k=8
c=1
N=100
Ks=[6]
lam=1
LAM=[0.5,1,1.5,2]
alpha=2.6
if network_type=='dolphins':
    B=np.linspace(4.5,8.5,10)
if network_type=='americanfootball':
    B=np.linspace(10.8,14.8,10)
if network_type=='contiguous-usa':
    B=np.linspace(3.5,7.5,10)
if network_type=='zebra':
    B=np.linspace(6,10,10)
Cs=['red', 'blue', 'green', 'grey']
Ms=['^', '>', '<', 'v']
delta=0.01
plt.figure(figsize=(8,8))
for lam in LAM:
    q0=((alpha-1)/(alpha-2)/(1/lam+(alpha-1)/(alpha-2)))
    L=(1-(1-q0)**k)/(k)
    filename1='.\\saves\\pdg\\real\\C{:.2f}_{:.2f}_{}.json'.format(lam, alpha, network_type)
    filename2='.\\saves\\pdg\\real\\D{:.2f}_{:.2f}_{}.json'.format(lam, alpha, network_type)
    f1=open(filename1)
    f2=open(filename2)
    data1=json.load(f1)
    data2=json.load(f2)
    rhoc_d=[]
    #rhod=[]
    for b in B:
        rhoc_d.append(data1['{:.4f}'.format(b)]-data2['{:.4f}'.format(b)])
        #rhod.append(data2['{:.4f}'.format(b)])
    #plt.scatter(Beta, Fi, color=Cs[Ks.index(k)], s=80,label='$k = {:d}$'.format(k))
    plt.scatter(B, np.array(rhoc_d), color=Cs[LAM.index(lam)],marker=Ms[LAM.index(lam)],s=250, label='$\\lambda = {:.1f}$'.format(lam))
    #plt.plot(Beta, Fi, color=Cs[Ks.index(k)], lw=2)
    #plt.axvline(k, color = Cs[Ks.index(k)], alpha=1, linestyle='-.',lw=3)
    #plt.axvline((N-2)/(N*L-2), color = Cs[LAM.index(lam)], alpha=1, linestyle='-.',lw=2)
    plt.axhline(0, color = 'purple', alpha=1, linestyle='--',lw=3)
    #z1=np.polyfit(Beta, Fi, 3)
    #p1=np.poly1d(z1)
    #plt.plot(np.arange(0, 0.5, 0.01), p1(np.arange(0, 0.5, 0.01)),color = Cs[Ks.index(k)], lw=2)
#plt.axvline((N-2)/(N/k-2), color = 'black', alpha=1, linestyle='-.',lw=2)
plt.xticks(fontsize=20)
plt.yticks(np.arange(-0.02,0.021,0.01),fontsize=20)
plt.xlabel('$b$',fontsize=25)
plt.ylim([-0.02, 0.02])
plt.grid()
if k==4:
    plt.ylabel('$\\rho_C-\\rho_D$',fontsize=25)
    plt.legend(fontsize=20)
if k==6 or k==8:
    ax = plt.gca()
    ax.axes.yaxis.set_ticklabels([])
plt.savefig('.\\saves\\pdg\\imgs\\{:.2f}_{:.2f}_{}.pdf'.format(lam,alpha,network_type),bbox_inches='tight', dpi=500)
plt.show()