import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


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

FE_MG = []
x_ax= []
f = []
for dat in data:
    FE_MG.append({0: float(dat['iron_gas'])/float(dat['Mg_gas']), 1: float(dat['z']) })
    #print(FE_MG)
for dat in data:
   x_ax.append(float(dat['z']))
   f.append(float(dat['m_BH']))

y_ax=np.log10(f)
print(len(x_ax))
print(y_ax.size)

WD = 'D:/SNU2022/Research/AGN_SI_SNU/'
fig, ax = plt.subplots()
colors = np.full(1428, 10)

ax.set_xlabel('$z$')
ax.set_ylabel('$log(MBH/Msolar)$')
ax.scatter(x_ax, y_ax, s=6, c=colors, vmin=0, vmax=100)
#plt.show()
plt.savefig(WD+'BHmass.png', dpi=300)