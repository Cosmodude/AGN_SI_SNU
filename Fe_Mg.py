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
    FE_MG.append({i['haloID']: float(i['iron_gas'])/float(i['Mg_gas']), 't' : float(i['z']) })
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
rat =[]
time=[]
for i in range(len(halo_names)):
    eachhr=[]
    eachht=[]
    for j in FE_MG:
        for k in j:
            if k==halo_names[i]:
                eachhr.append(j[halo_names[i]]) 
                eachht.append(j['t']) 
    rat.append(eachhr)
    time.append(eachht)
print(rat[0][0])
print(time[0][0])   

### For all points together
x_ax= []
f= []
for dat in data:
    x_ax.append(float(dat['z']))
    f.append(float(dat['iron_gas'])/float(dat['Mg_gas']))
y_ax=np.log10(f)
# print(len(x_ax))
# print(y_ax.size)

### Convert Redshift to loockback time 
lb_time=[]
for i in time:
    lb_time.append(Planck13.lookback_time(i))
print(lb_time[0][0])
#print('time')
#print(Planck13.lookback_time(0.01))

### Creating plot
WD = 'D:/SNU2022/Research/AGN_SI_SNU/'
fig, ax = plt.subplots()
ax.set_xlabel('$Gyr$')
ax.set_ylabel('$log(Fe/Mg)$')
c=[]
halo=[]
for i in range(len(halo_names)):
    color =0+i*10
    c=np.full(len(rat[i]),color)
    str=halo_names[i]
    #for j in range(len(time[i])):
        #ax1.plot(j['t'],'b',j[str])
    halo.append(ax.scatter(lb_time[i], rat[i], s=6, c=c, vmin=0, vmax=100,label=halo_names[i]))
#ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
ax.legend(handles=halo)

print(type('t'))
#plt.show()
plt.savefig('FeMg.png', dpi=300)