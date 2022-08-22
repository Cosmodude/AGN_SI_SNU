import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pylab
from astropy.cosmology import Planck13
from operator import itemgetter

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
    FE_MG.append({i['haloID']: float(i["m_BH"]), 't' : float(i['z']) })
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
print("\n")

### Split data for halos
dict=[]
mass =[]
time=[]
for i in range(len(halo_names)):
    eachhm=[]
    eachht=[]
    for j in FE_MG:
        for k in j:
            if k==halo_names[i]:
                eachhm.append(j[halo_names[i]]) 
                eachht.append(j['t']) 
    mass.append(np.log10(eachhm))
    time.append(eachht)
    dict.append({halo_names[i]: halo_names[i], 'MBH': mass[i][0]})
# print(mass[0][0])
# print(time[0][0])   


### Convert Redshift to loockback time 
lb_time=[]
for i in time:
    lb_time.append(Planck13.lookback_time(i))
#print(lb_time[0][0])
#print('time')
#print(Planck13.lookback_time(0.01))
print(*sorted(dict, key=lambda x: x['MBH'],reverse=True),sep="\n")
# for i in range(len(time)):
#     print(dict[i])