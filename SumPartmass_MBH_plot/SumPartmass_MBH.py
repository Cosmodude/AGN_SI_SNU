import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pylab
from astropy.cosmology import Planck13

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
    FE_MG.append({i['haloID']: float(i["m_gas"]), 't' : float(i['z']) , "MBH": float(i["m_BH"])})
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
MBH=[]
for i in range(len(halo_names)):
    eachht=[]
    m=[]
    bhm=[]
    for j in FE_MG:
        for k in j:
            if k==halo_names[i]:
                eachht.append(j['t']) 
                m.append(j[halo_names[i]]) 
                bhm.append(j['MBH'])       
    mass.append(m)
    time.append(eachht)
    MBH.append(bhm)
print(mass[0][0])
print(time[0][0])   

### Turn over dict + time 
def Turn(met):
    #print(Split_dict[0][0])
    print("Turn")
    for i in met:
        i.reverse()
    #print(Split_dict[0][0])
Turn(mass)
Turn(time)
Turn(MBH)
print(time[0])

Summ=[]
for i in range(len(halo_names)):
    eachht=[]
    summ=[]
    m=0
    for j in mass[i]:
            m=m+j
            summ.append(m)
    Summ.append(summ)

   

### Convert Redshift to loockback time 
lb_time=[]
for i in time:
    lb_time.append(Planck13.lookback_time(i))
print(lb_time[0][0])
#print('time')
#print(Planck13.lookback_time(0.01))

### Creating plot
def Graph(number):
    from matplotlib import colors, transforms
    WD = 'SumPartmass_MBH_plot/'
    fig, ax = plt.subplots()
    ax.set_xlabel('$Gyr$')
    #ax.set_xlim(0,2.7)
    ax.set_ylabel('$log(M/Msolar)$')
    c=[]
    halo=[]
    color =(number+1)*10
    i=number
    c=np.full(len(time[i]),0)
    #c=np.full(len(time[i]),color)
    #for j in range(len(time[i])):
    #ax1.plot(j['t'],'b',j[str])
    colors=[colors.to_rgba(h)
        for h in plt.rcParams['axes.prop_cycle'].by_key()['color']]
    halo.append(ax.scatter(lb_time[i], np.log10(Summ[i]), s=6, color=colors[9], vmin=0, vmax=100,label="SumPartMass"))
    halo.append(ax.scatter(lb_time[i], np.log10(MBH[i]), s=6, c=c, vmin=0, vmax=100,label="MBH"))
    #ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
    ax.legend(handles=halo)
    ax.set_title(halo_names[i])

    print(type('t'))
    #plt.show()
    plt.savefig(WD+halo_names[i]+'_SumPartmass_MBH.png', dpi=300)

for j in range(len(halo_names)):
    Graph(j)