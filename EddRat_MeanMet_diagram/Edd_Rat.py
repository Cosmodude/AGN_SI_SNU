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
     DATA.append({i['haloID']: i['haloID'],'Bhmass': float(i['m_BH']), 'part_mass': float(i['m_gas']),'Z' : float(i['Z/Zsolar'])*Solmet, 't' : float(i['z']) })
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
BHmass=[]
time=[]
for i in range(len(halo_names)):
    eachhmet=[]
    eachht=[]
    eachmass=[]
    eachbh=[]
    for j in DATA:
        for k in j:
            if k==halo_names[i]:
                eachmass.append(j['part_mass'])
                eachhmet.append(j['Z']) 
                eachht.append(j['t']) 
                eachbh.append(j['Bhmass'])
    met.append(eachhmet)
    mass.append(eachmass)
    time.append(eachht)
    BHmass.append(eachbh)
print(type(met[0][0]))   

### Convert Redshift to loockback time 
lb_time=[]
for i in time:
    lb_time.append(Planck13.lookback_time(i))
print(type(lb_time[0][0]))
print('time')
#print(Planck13.lookback_time(0.01))

### Turn over dict + time 
def Turn(met):
    #print(Split_dict[0][0])
    #print("here")turn=[]
    turn=[]
    #print(time[0])
    for i in met:
        turn.append(np.flip(i))
    return turn
met=Turn(met)
mass=Turn(mass)
time=Turn(time)
BHmass=Turn(BHmass)
print(BHmass[0])

### Count data
st=0.1
ar=np.arange(0.0,12.5,st)

MeanMet=[]
EddRat=[]
Tb=[]
print(len(ar))
for i in range(len(halo_names)):
    tb=[]
    am=[]
    Rat=[]
    for j in ar:
        m=0
        mm=0
        bh=0
        for k in range(len(lb_time[i])):
            if j+st>lb_time[i][k].value>j:
                m= m + mass[i][k]
                mm=mm+(mass[i][k]*met[i][k]) 
                bh=BHmass[i][k]
        if m!=0:
            am.append((mm/m)/Solmet)
            Rat.append(m/bh)
            tb.append(j)
            if m/bh>1:
                print("anomaly")
                print(tb[-1])
    MeanMet.append(am) 
    EddRat.append(Rat)
    Tb.append(tb)
print(len(MeanMet[0]))

lb=np.arange(0,12.1,1.5)
### Creating plot
def Graph(number):
    import math
    from matplotlib import colors, transforms
    WD = 'EddRat_MeanMet_diagram/'
    fig, ax = plt.subplots()
    ax.set_ylabel('$Average(Timebin)Met/Zsolar$')
    #ax.set_xlim(0,2.7)
    ax.set_xlabel('$(dM/dt)/M *(1/$'+repr(st)+'$*Gyr)$')
    c=[]
    halo=[]
    color =number*10
    i=number
    c=np.full(len(Tb[i]),color)
    ax.set_title(halo_names[i])
    #for j in range(len(time[i])):
    #ax1.plot(j['t'],'b',j[str])
    from matplotlib import colors, transforms
    colors=[colors.to_rgba(h)
        for h in plt.rcParams['axes.prop_cycle'].by_key()['color']]

    for j in lb:
        R=[]
        Z=[]
        for k in range(len(Tb[i])):
            if (j+0.75)>Tb[i][k]>(j-0.75):
                R.append(EddRat[i][k])
                Z.append(MeanMet[i][k])
        if len(R)!=0:
            c=np.full(len(Z),j)
            ax.scatter(R,Z,s=6,color=colors[9-int(j/1.5)],label=j)
            ax.legend(title='Gyr',fontsize='small')            
        #halo.append(ax.scatter(MeanMet[i], dMdt[i], s=5, c=c, vmin=0, vmax=100,label=halo_names[i]))
    #ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
    #ax.legend(handles=halo)

    print(type('t'))
    #plt.show()
    plt.savefig(WD+halo_names[i]+'_EddRat_MeanMet.png', dpi=300)

for j in range(len(halo_names)):
   Graph(j)
Graph(0)