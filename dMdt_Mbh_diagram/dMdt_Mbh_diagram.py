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
     DATA.append({i['haloID']: i['haloID'], 'part_mass': float(i['m_gas']),'Mbh' : float(i['m_BH']), 't' : float(i['z']) })
print(DATA[0]['Mbh'])

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
MBH =[]
mass=[]
time=[]
for i in range(len(halo_names)):
    eachhmBH=[]
    eachht=[]
    eachmass=[]
    for j in DATA:
        for k in j:
            if k==halo_names[i]:
                eachmass.append(j['part_mass'])
                eachhmBH.append(j['Mbh']) 
                eachht.append(j['t']) 
    MBH.append(eachhmBH)
    mass.append(eachmass)
    time.append(eachht)
#print(mass[0])
#print((MBH[0]))   

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
    print("here")
    for i in met:
        np.flip(i)
    #print(time[0])
    #print(Split_dict[0][0])
Turn(MBH)
Turn(mass)
Turn(time)

### Count data
st=0.1
ar=np.arange(0.0,12.5,st)
Mbh=[]
dMdt=[]
Tb=[]
print(len(ar))
for i in range(len(halo_names)):
    tb=[]
    mbh=[]
    dmdt=[]
    for j in ar:
        m=0
        mb=0
        for k in range(len(lb_time[i])):
            if j+st>lb_time[i][k].value>j:
                m= m + mass[i][k]
                mb= MBH[i][k]  
        if m!=0:
            mbh.append(mb/10**8)
            dmdt.append(m/10**8)
            tb.append(j)
    Mbh.append(mbh) 
    dMdt.append(dmdt)
    Tb.append(tb)
#print((Mbh[0]))

lb=np.arange(0,12.1,1.5)
### Creating plot
def Graph(number):
    import math
    from matplotlib import colors, transforms
    WD = 'dMdt_Mbh_diagram/'
    fig, ax = plt.subplots()
    ax.set_xlabel('$dM/dt (Msol*10^8/$'+repr(st)+'$Gyr)$')
    #ax.set_xlim(0,2.7)
    ax.set_ylabel('$MBH (Msol*10^8)$')
    halo=[]
    i=number
    ax.set_title(halo_names[i])
    #for j in range(len(time[i])):
    #ax1.plot(j['t'],'b',j[str])
    from matplotlib import colors, transforms
    colors=[colors.to_rgba(h)
        for h in plt.rcParams['axes.prop_cycle'].by_key()['color']]

    for j in lb:
        dm=[]
        MBh=[]
        for k in range(len(Tb[i])):
            if (j+0.75)>Tb[i][k]>(j-0.75):
                dm.append(dMdt[i][k])
                MBh.append(Mbh[i][k])
        if len(dm)!=0:
            c=np.full(len(MBh),j)
            ax.scatter(dm,MBh,s=6,color=colors[9-int(j/1.5)],label=j)
            ax.legend(title='Gyr',fontsize='small')            
        #halo.append(ax.scatter(MeanMet[i], dMdt[i], s=5, c=c, vmin=0, vmax=100,label=halo_names[i]))
    #ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
    #ax.legend(handles=halo)

    print(type('t'))
    #plt.show()
    plt.savefig(WD+halo_names[i]+'_dMdt_MBH.png', dpi=300)

def Hist(number):
    from matplotlib import colors, transforms
    WD = 'dMdt_Mbh_diagram/'
    fig, ax = plt.subplots()
    ax.set_xlabel('$MBH (Msol*10^8)$')
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
    for j in reversed(lb):
        dm=[]
        MBh=[]
        for k in range(len(Tb[i])):
            if (j+0.75)>Tb[i][k]>(j-0.75):
                dm.append(dMdt[i][k])
                MBh.append(Mbh[i][k])
        if len(dm)!=0:
            #c=np.full(len(MBh),'r')
           # color=colors[9-int(j/1.5)]
            ax.bar( MBh, dm, width=0.5,color=colors[9-int(j/1.5)] ,label=j)
            ax.legend(title='Gyr',fontsize='small')     
    ax.legend()

    print(type('t'))
    #plt.show()
    plt.savefig(WD+halo_names[i]+'_dMdt_MBH.png', dpi=300)

for j in range(len(halo_names)):
    Hist(j)
# for j in range(len(halo_names)):
#    Graph(j)
# Graph(0)