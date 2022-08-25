import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import pylab
from astropy.cosmology import Planck13
from matplotlib import colors, transforms

### Read FILE
columns = []
data = []
with open('AGNgas_table_all.txt') as f:
    i = 0
    lines = f.readlines()
    for line in lines:
        if i == 0:
            columns = line.split()
            i+=1
            continue
        data.append(dict(zip(columns, line.split())))
#print(type(data[0]['haloID']))

### Get necessary data
DATA = []
for i in data:
    DATA.append({i['haloID']: float(i["m_gas"]), 't' : float(i['z']) })
#print(FE_MG)
# print(FE_MG[0]['m0175'])
# print(type(FE_MG[0]))

### Create massive of names
str='a'
halo_names=[]
print(data[0]['haloID'])
print(len(data))
for j in range(len(data)):
    if  data[j]['haloID'] not in halo_names:
        halo_names.append(data[j]['haloID']) 
print(halo_names)

### Split data for halos
mass =[]
time=[]
for i in range(len(halo_names)):
    eachhm=[]
    eachht=[]
    for j in DATA:
        for k in j:
            if k==halo_names[i]:
                eachhm.append(j[halo_names[i]]) 
                eachht.append(j['t']) 
    mass.append(eachhm)
    time.append(eachht)
#print(mass[0])
print(time[0][0])   

### Turn over dict + time 
def Turn():
    #print(Split_dict[0][0])
    print("here")
    for i in mass:
        np.flip(i)
    for i in time:
        i.reverse()

    #print(time[0])
    #print(Split_dict[0][0])
Turn()

### Convert Redshift to loockback time 
lb_time=[]
for i in time:
    lb_time.append(Planck13.lookback_time(i))
print(type(lb_time[0][0]))
print('time')
#print(Planck13.lookback_time(0.01))

### Count dM/dt
dMdt=[]
Tb=[]
st=0.1
ar=np.arange(0.0,12.5,st)
print(len(ar))
for i in range(len(halo_names)):
    dmdt=[]
    tb=[]
    for j in ar:
        dm=0
        for k in range(len(lb_time[i])):
            if j+st>lb_time[i][k].value>j:
                dm=dm+mass[i][k]
        #if dm!=0:
            #dmdt.append(math.log10(dm))
        dmdt.append(dm/10**8)
        tb.append(j-st/2)
        #else:
        #    dmdt.append(0)
        
    dMdt.append(dmdt)    
    Tb.append(tb)
print((dMdt[0]))
print((Tb[0]))

### Creating plot
def Graph(number):
    WD = 'Accretion_rate/'
    fig, ax = plt.subplots()
    ax.set_xlabel('$Gyr$')
    #ax.set_xlim(0,2.7)
    ax.set_ylabel('$dM/dt (Msol*10^8/$'+repr(st)+'$Gyr)$')
    c=[]
    halo=[]
    color =number*10
    i=number
    c=np.full(len(Tb[i]),color)
    #for j in range(len(time[i])):
    #ax1.plot(j['t'],'b',j[str])
    halo.append(ax.scatter(Tb[i], dMdt[i], s=5, c=c, vmin=0, vmax=100,label=halo_names[i]))
    #ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
    ax.legend(handles=halo)

    print(type('t'))
    #plt.show()
    plt.savefig(WD+halo_names[i]+'_'+repr(st)+'_dMdt.png', dpi=300)


def Hist(number):
    from matplotlib import colors, transforms
    WD = 'Accretion_rate/'
    fig, ax = plt.subplots()
    ax.set_xlabel('$Gyr$')
    #ax.set_xlim(0,2.7)
    ax.set_ylabel('$dM/dt (Msol*10^8/$'+repr(st)+'$Gyr)$')
    halo=[]
    color =number*10
    i=number
    colors=[colors.to_rgba(c)
        for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]
    #c=['b','r','g','c','m','y','k','purple', 'orange','dodgerblue']
    #for j in range(len(time[i])):
    #ax1.plot(j['t'],'b',j[str])
    #halo.append(ax.scatter(Tb[i], dMdt[i], s=5, c=c, vmin=0, vmax=100,label=halo_names[i]))
    #ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
    ax.bar( Tb[i],dMdt[i], width=st, color=colors[i],label=halo_names[i])
    ax.legend()

    print(type('t'))
    #plt.show()
    plt.savefig(WD+halo_names[i]+'_'+repr(st)+'_dMdt.png', dpi=300)

for j in range(len(halo_names)):
    Hist(j)
#Graph(0)
#Hist(0)