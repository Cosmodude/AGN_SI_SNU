from cProfile import label
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pylab
import seaborn as sns
import matplotlib.cm as cm
from astropy.cosmology import Planck13
FEsol=0.0012
AlFesol=0.00048/0.00072
print (AlFesol)

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
    FE_MG.append({i['haloID']: float(i['iron_gas']), 'alpha': float(i['alpha_gas']), 'm_gas': float(i['m_gas']) ,'t' : float(i['z']) })
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
FeH =[]
AlphaFe=[]
time=[]
for i in range(len(halo_names)):
    eachhr1=[]
    eachhr2=[]
    eachht=[]
    for j in FE_MG:
        for k in j:
            if k==halo_names[i]:
                eachhr1.append(np.log10((j[halo_names[i]]/j['m_gas'])/FEsol))
                eachhr2.append(np.log10((j['alpha']/j[halo_names[i]])/AlFesol))
                eachht.append(j['t']) 
    FeH.append(eachhr1)
    AlphaFe.append(eachhr2)
    time.append(eachht)
print(time[0][0])   


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
ax.set_xlabel('$Fe/H$')
ax.set_ylabel('$Alpha/Fe$')
c=[]
halo=[]
for i in range(len(halo_names)):
    color =0+i*10
    c=np.full(len(time[i]),color)
    str=halo_names[i]
    #for j in range(len(time[i])):
        #ax1.plot(j['t'],'b',j[str])
    halo.append(ax.scatter(FeH[i], AlphaFe[i], s=6, c=c, vmin=0, vmax=100,label=halo_names[i]))
#ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
ax.legend(handles=halo)

print(type('t'))
#plt.show()
plt.savefig('FeH_AlphaFe.png', dpi=300)

### Creating plot
WD = 'D:/SNU2022/Research/AGN_SI_SNU/'
fig, ax = plt.subplots()
ax.set_xlabel('$[Fe/H]$')
ax.set_ylabel('$[Alpha/Fe]$')
c=[]
halo=[]
i =0 
#color = [round(num*2, 0) for num in time[i]]
# c= []
# p=[]
# for j in time[i]:
#     if j not in c:
#         c.append(j)
z=np.arange(0,3,0.5)
print(z)
#c=np.full(len(time[i]),color)
#for j in range(len(time[i])):
    #ax1.plot(j['t'],'b',j[str])


for j in z: 
    f=[]
    a=[]
    for k in range(len(time[i])):
        if (j+0.25)>time[i][k]>(j-0.25):
            f.append(FeH[i][k])
            a.append(AlphaFe[i][k])
    c=np.full(len(f),j)
    ax.scatter(f,a,s=6,c=c,vmin=0,vmax=2.5,label=j)
ax.legend(title='z',fontsize='small')            
#halo.append(ax.scatter(FeH[i], AlphaFe[i], s=6, c=colors))
#ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)


print(type('t'))
#plt.show()
plt.savefig('M0175_FeH_AlphaFe.png', dpi=300)