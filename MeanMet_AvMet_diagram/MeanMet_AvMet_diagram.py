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
Metmass =[]
mass=[]
time=[]
for i in range(len(halo_names)):
    eachhmm=[]
    eachht=[]
    eachmass=[]
    for j in DATA:
        for k in j:
            if k==halo_names[i]:
                eachmass.append(j['part_mass'])
                eachhmm.append(j['Z']*j['part_mass']) 
                eachht.append(j['t']) 
    Metmass.append(eachhmm)
    mass.append(eachmass)
    time.append(eachht)
#print(mass[0])
#print((Metmass[0]))   

### Turn over dict + time 
def Turn(met):
    #print(Split_dict[0][0])
    print("Turn")
    for i in met:
        np.flip(i)
    #print(time[0])
    #print(Split_dict[0][0])
Turn(Metmass)
Turn(mass)
Turn(time)

### Convert Redshift to loockback time 
lb_time=[]
for i in time:
    lb_time.append(Planck13.lookback_time(i))
print('timetype')
print(type(lb_time[0][0]))
#print(Planck13.lookback_time(0.01))



### Count data
st=0.1
ar=np.arange(0.0,12.5,st)
AvMet=[]
MeanMet=[]
Tb=[]
print(len(ar))
for i in range(len(halo_names)):
    tb=[]
    meanmet=[]
    avmet=[]
    sm=0
    smm=0
    for j in reversed(ar):
        mm=0
        m=0
        for k in range(len(lb_time[i])):
            if j+st>lb_time[i][k].value>j:
                m= m + mass[i][k]
                mm=mm+Metmass[i][k]
                sm=sm + mass[i][k]  
                smm=smm +Metmass[i][k]
        if m!=0:
            meanmet.append((mm/m)/Solmet)
            avmet.append((smm/sm)/Solmet)
            tb.append(j)
    AvMet.append(avmet) 
    MeanMet.append(meanmet)
    Tb.append(tb)
print('len check:')
print(len(AvMet[0]))
print(len(MeanMet[0]))



### Creating plot
lb=np.arange(0,12.1,1.5)
def Graph(number):
    import math
    from matplotlib import colors, transforms
    WD = 'MeanMet_AvMet_diagram/'
    fig, ax = plt.subplots()
    ax.set_xlabel('$HaloAverageMet(Zsolar)$')
    #ax.set_xlim(0,2.7)
    ax.set_ylabel('$Mean(Timebin)Met/Zsolar$')
    halo=[]
    i=number
    ax.set_title(halo_names[i])
    #for j in range(len(time[i])):
    #ax1.plot(j['t'],'b',j[str])
    from matplotlib import colors, transforms
    colors=[colors.to_rgba(h)
        for h in plt.rcParams['axes.prop_cycle'].by_key()['color']]

    for j in lb:
        Mmet=[]
        Amet=[]
        for k in range(len(Tb[i])):
            if (j+0.75)>Tb[i][k]>(j-0.75):
                Mmet.append(MeanMet[i][k])
                Amet.append(AvMet[i][k])
        if len(Mmet)!=0:
            #c=np.full(len(Mmet),j)
            ax.scatter(Amet,Mmet,s=6,color=colors[9-int(j/1.5)],label=j)
            ax.legend(title='Gyr',fontsize='small')            
        #halo.append(ax.scatter(MeanMet[i], dMdt[i], s=5, c=c, vmin=0, vmax=100,label=halo_names[i]))
    #ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
    #ax.legend(handles=halo)

    #print(type('t'))
    #plt.show()
    print(halo_names[i])
    plt.savefig(WD+halo_names[i]+'_AvMet_Meanmet_diagram.png', dpi=300)

def Hist(number):
    from matplotlib import colors, transforms
    WD = 'dMdt_Mbh_diagram/'
    fig, ax = plt.subplots()
    ax.set_xlabel('$HaloAverageMet(Zsolar)$')
    #ax.set_xlim(0,2.7)
    ax.set_ylabel('$Average(Timebin)Met/Zsolar$')
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
                dm.append(AvMet[i][k])
                MBh.append(MeanMet[i][k])
        if len(dm)!=0:
            #c=np.full(len(MBh),'r')
           # color=colors[9-int(j/1.5)]
            ax.bar( MBh, dm, width=0.5,color=colors[9-int(j/1.5)] ,label=j)
            ax.legend(title='Gyr',fontsize='small')     
    ax.legend()

    print(type('t'))
    #plt.show()
    plt.savefig(WD+halo_names[i]+'_dMdt_MBH.png', dpi=300)

# for j in range(len(halo_names)):
#     Hist(j)
for j in range(len(halo_names)):
   Graph(j)
# Graph(0)