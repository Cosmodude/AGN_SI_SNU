import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pylab

Solmet=0.012

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
D_dict = []
for i in data:
    D_dict.append({i['haloID']: i['haloID'], 'part_mass': float(i['m_gas']),'Z' : float(i['Z/Zsolar'])*Solmet, 'z' : float(i['z']) })
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
Split_dict =[]
time=[]
for i in range(len(halo_names)):
    eachh=[]
    eacht=[]
    for j in D_dict:
        for k in j:
            if k==halo_names[i]:
                eachh.append({ 'Masp': j['part_mass'],'Zp':j['Z'] } ) 
                eacht.append(j['z']+1) 
    Split_dict.append(eachh)
    time.append(eacht)
    
print(Split_dict[0][0]['Masp'])
   

### Count average metallicity using SUMMATION
def sum_method(data):
    avmet=[]
    for i in range(len(halo_names)):
        am=[]
        m=0
        mm=0
        for j in data[i]:
            m= m + j['Masp']
            mm=mm+(j['Masp']*j['Zp'])
            am.append((mm/m)/Solmet)
        avmet.append(am)
    print(avmet[1][0])
    return avmet
avmets=sum_method(Split_dict)

### Count average metallicity using INTEGRATION
def sum_method(data):
    avmet=[]
    for i in range(len(halo_names)):
        am=[]
        m=0
        mm=0
        for j in data[i]:
            m= m + j['Masp']
            mm=mm+(j['Masp']*j['Zp'])
            am.append((mm/m)/Solmet)
        avmet.append(am)
    print(avmet[1][0])
    return avmet
avmets=sum_method(Split_dict)

### Build Plot
def plot(amet,time):
    WD = 'D:/SNU2022/Research/AGN_SI_SNU/'
    fig, ax = plt.subplots()
    ax.set_xlabel('$z+1$')
    ax.set_xlim(0,4)
    ax.set_ylabel('$Average_Met(Zsolar)$')
    c=[]
    halo=[]
    for i in range(len(halo_names)):
        color =0+i*10
        c=np.full(len(amet[i]),color)
        str=halo_names[i]
        #for j in range(len(time[i])):
            #ax1.plot(j['t'],'b',j[str])
        halo.append(ax.scatter(time[i], amet[i], s=6, c=c, vmin=0, vmax=100,label=halo_names[i]))
    #ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
    ax.legend(handles=halo)

    #plt.show()
    plt.savefig('Average_Met.png', dpi=300)