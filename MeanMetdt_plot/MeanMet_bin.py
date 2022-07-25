import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import pylab
from astropy.cosmology import Planck13

Solmet=0.0134

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
     DATA.append({i['haloID']: i['haloID'], 'part_mass': float(i['m_gas']),'Z' : float(i['Z/Zsolar'])*Solmet, 't' : float(i['z']) })
#print(FE_MG)

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
met =[]
mass=[]
time=[]
for i in range(len(halo_names)):
    eachhmet=[]
    eachht=[]
    eachmass=[]
    for j in DATA:
        for k in j:
            if k==halo_names[i]:
                eachmass.append(j['part_mass'])
                eachhmet.append(j['Z']) 
                eachht.append(j['t']) 
    met.append(eachhmet)
    mass.append(eachmass)
    time.append(eachht)
#print(mass[0])
print(type(met[0][0]))   


### Convert Redshift to loockback time 
lb_time=[]
for i in time:
    lb_time.append(Planck13.lookback_time(i))
print(type(lb_time[0][0]))
print('time')
#print(Planck13.lookback_time(0.01))

### Turn over dict + time 
def Turn():
    #print(Split_dict[0][0])
    print("here")
    for i in met:
        np.flip(i)
    for i in mass:
        np.flip(i)
    for i in time:
        i.reverse()
    #print(time[0])
    #print(Split_dict[0][0])
Turn()

### Count MeanMet
st=0.1
ar=np.arange(0.0,12.5,st)

MeanMet=[]
print(len(ar))
for i in range(len(halo_names)):
    am=[]
    for j in ar:
        m=0
        mm=0
        for k in range(len(lb_time[i])):
            if j+st>lb_time[i][k].value>j:
                m= m + mass[i][k]
                mm=mm+(mass[i][k]*met[i][k])  
        if m!=0:
            am.append((mm/m)/Solmet)
        else:
            am.append(0)
    MeanMet.append(am)    
print(len(MeanMet[0]))


### Creating plot
def Graph(number):
    WD = 'MeanMetdt_plot/'
    fig, ax = plt.subplots()
    ax.set_xlabel('$Gyr$')
    #ax.set_xlim(0,2.7)
    ax.set_ylabel('$AverageMet/Zsolar$')
    c=[]
    halo=[]
    color =number*10
    i=number
    c=np.full(len(ar),color)
    #for j in range(len(time[i])):
    #ax1.plot(j['t'],'b',j[str])
    halo.append(ax.scatter(ar, MeanMet[i], s=5, c=c, vmin=0, vmax=100,label=halo_names[i]))
    #ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
    ax.legend(handles=halo)

    print(type('t'))
    #plt.show()
    plt.savefig(WD+halo_names[i]+'_'+repr(st)+'Gyr_MeanMetdt.png', dpi=300)

for j in range(len(halo_names)):
    Graph(j)