import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pylab
from astropy.cosmology import Planck13

#from MeanMet_AvMet_diagram.MeanMet_AvMet_diagram import Metmass

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
FE_MG = []
for i in data:
    FE_MG.append({i['haloID']: float(i["m_BH"]), 'part_mass': float(i['m_gas']),'Z' : float(i['Z/Zsolar'])*Solmet,'t' : float(i['z']) })
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
Met=[]
Pmass=[]
time=[]
for i in range(len(halo_names)):
    eachhm=[]
    eachht=[]
    eachmmet=[]
    pmass=[]
    for j in FE_MG:
        for k in j:
            if k==halo_names[i]:
                eachhm.append(j[halo_names[i]]) 
                eachht.append(j['t'])
                pmass.append(j['part_mass'])
                eachmmet.append(j['Z'])
    mass.append(eachhm)
    time.append(eachht)
    Met.append(eachmmet)
    Pmass.append(pmass)
print(mass[0][0])
print(time[0][0])   

### Turn over dict + time 
def Turn(met):
    #print(Split_dict[0][0])
    print("Turn")
    for i in met:
        i.reverse()
    #print(time[0])
    #print(Split_dict[0][0])
Turn(Met)
Turn(Pmass)
Turn(mass)
Turn(time)

###Count MMet
Metmass=[]
for j,i in zip(Pmass,Met):
    mmet=[]
    m=0
    for k in range(len(j)):
        m=m+j[k]*i[k]
        mmet.append(m)
    Metmass.append(mmet)


### Convert Redshift to loockback time 
lb_time=[]
for i in time:
    lb_time.append(Planck13.lookback_time(i))
print(lb_time[0][0])
#print('time')
#print(Planck13.lookback_time(0.01))

### Creating plot
def Graph(number):
    WD = 'MBH+MMet_plot/'
    fig, ax = plt.subplots()
    ax.set_xlabel('$Gyr$')
    #ax.set_xlim(0,2.7)
    ax.set_ylabel('$log(M/Msolar)$')
    c=[]
    halo=[]
    color =number*10
    i=number
    c=np.full(len(time[i]),color)
    #for j in range(len(time[i])):
    #ax1.plot(j['t'],'b',j[str])
    halo.append(ax.scatter(lb_time[i], np.log10(mass[i]), s=6, c=c, vmin=0, vmax=100,label='MBH'))
    color =100
    c=np.full(len(time[i]),color)
    halo.append(ax.scatter(lb_time[i], np.log10(Metmass[i]), s=6, c=c, vmin=0, vmax=100,label='MetMass'))
    #ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
    ax.legend(handles=halo)
    ax.set_title(halo_names[i])
    
    print(type('t'))
    #plt.show()
    plt.savefig(WD+halo_names[i]+'_BHmass+Metmass.png', dpi=300)

for j in range(len(halo_names)):
    Graph(j)