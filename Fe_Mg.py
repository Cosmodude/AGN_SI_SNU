import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pylab

###Read FILE
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

###Get necessary data
FE_MG = []
x_ax= []
f= []
for i in data:
    FE_MG.append({i['haloID']: float(i['iron_gas'])/float(i['Mg_gas']), 't' : float(i['z']) })
#print(FE_MG)
# print(FE_MG[0]['m0175'])
# print(type(FE_MG[0]))

###Create massive of names
str='a'
halo_names=[]
print(data[0]['haloID'])
print(len(data))
for j in range(len(data)):
    if  data[j]['haloID'] not in halo_names:
        halo_names.append(data[j]['haloID']) 
print(halo_names)

###Split data for halos
m =[]
for i in range(len(halo_names)):
    eachh=[]
    for j in FE_MG:
        for k in j:
            if k==halo_names[i]:
                eachh.append(j)   
    m.append(eachh)
#print(m)   

### For all points together
for dat in data:
    x_ax.append(float(dat['z'])+1)
    f.append(float(dat['iron_gas'])/float(dat['Mg_gas']))
y_ax=np.log10(f)
# print(len(x_ax))
# print(y_ax.size)

WD = 'D:/SNU2022/Research/AGN_SI_SNU/'
fig, ax1 = plt.subplots()
for i in range(len(halo_names)):
    str=halo_names[i]
    ax1.plot(m[i]['t'],'b',m[i][str])
print(type('t'))
colors = np.full(1428, 180)

ax1.set_xlabel('$z+1$')
ax1.set_ylabel('$log(Fe/Mg)$')
ax1.scatter(x_ax, y_ax, s=6, c=colors, vmin=0, vmax=200)
#plt.show()
plt.savefig(WD+'FeMg.png', dpi=300)