import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pylab
from astropy.cosmology import Planck13
from matplotlib import colors, transforms
from MeanBinMet_AvTotalMet_plot.MeanMet_AvMet import sum_method,Solmet

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
BHmass =[]
Met=[]
Pmass=[]
time=[]
for i in range(len(halo_names)):
    eachhm=[]
    eachht=[]
    eachmmet=[]
    pmass=[]
    for j in data:
            if j['haloID']==halo_names[i]:
                eachhm.append(float(j['m_BH'])) 
                eachht.append(float(j['z']))
                pmass.append(float(j['m_gas']))
                eachmmet.append(float(j['Z/Zsolar'])*Solmet)
    BHmass.append(eachhm)
    time.append(eachht)
    Met.append(eachmmet)
    Pmass.append(pmass)
print(BHmass[0][0])
print(time[0][0])   

### Turn over dict + time 
def Turn(met):
    print("Turn")
    for i in met:
        i.reverse()
    #print(time[0])
Turn(Met)
Turn(Pmass)
Turn(BHmass)
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
print(lb_time[0][-1])
#print('time')
#print(Planck13.lookback_time(0.01))

Avmet=sum_method(Met,Pmass,time)

### Count dM/dt + MeanMet
dMdt=[]
MeanMet=[]
Tb=[]
st=0.1
ar=np.arange(0.0,12.5,st)
print(len(ar))
for i in range(len(halo_names)):
    dmdt=[]
    am=[]
    tb=[]
    for j in ar:
        dm=0
        mm=0
        for k in range(len(lb_time[i])):
            if j+st>lb_time[i][k].value>j:
                dm=dm+Pmass[i][k]
                mm=mm+(Pmass[i][k]*Met[i][k])  
        if dm!=0:
            #dmdt.append(math.log10(dm))
            dmdt.append(np.log10(dm))
            am.append((mm/m)/Solmet)
        else:
            dmdt.append(0)
            am.append(0)
        tb.append(j-st/2)
    dMdt.append(dmdt)   
    MeanMet.append(am)   
    Tb.append(tb)
print((dMdt[0]))
print((Tb[0]))

### Creating plot
def Plot(i):
    from matplotlib import colors, transforms
    WD = 'Summary_analysis/'
    fig, ax = plt.subplots()
    
    ##dM/dt + MBH
    ax.set_xlabel('$Gyr$')
    #ax.set_xlim(0,2.7)
    ax.set_ylabel('$log(M/Msolar)$')
    c=[]
    halo=[]
    c=np.full(len(time[i]),0)
    #for j in range(len(time[i])):
    #ax1.plot(j['t'],'b',j[str])
    colors=[colors.to_rgba(c)
        for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]
    halo.append(ax.bar( Tb[i],dMdt[i], width=st, color=colors[i],label='dM/dt'))
    halo.append(ax.scatter(lb_time[i], np.log10(BHmass[i]), s=6, c=c, vmin=0, vmax=100,label='MBH'))
    #halo.append(ax.scatter(lb_time[i], np.log10(Metmass[i]), s=6, c=c, vmin=0, vmax=100,label='MetMass'))
    #ax.scatter(time, rat, s=6, c=c, vmin=0, vmax=100)
    ax.legend(handles=halo,loc=3)
    ax.set_title(halo_names[i])

    print(type('t'))
    #plt.show()
    plt.savefig(WD+halo_names[i]+'_BHmass.png', dpi=300)

    fig2, ax1=plt.subplots()
     ##MeanMet+AvMEt
    ax1.set_xlabel('$Gyr$')
    #ax.set_xlim(0,2.7)
    ax1.set_ylabel('$Met/Zsolar$')
    halo=[]
    # colors=[colors.to_rgba(c)
    #     for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]
    #for j in range(len(time[i])):
    #halo.append(ax.scatter(Tb[i], dMdt[i], s=5, c=c, vmin=0, vmax=100,label=halo_names[i]))
    halo.append(ax1.bar( Tb[i],MeanMet[i], width=st, color=colors[i],label="MeanTimeBinMet"))
    c=np.full(len(lb_time[i]),0)
    halo.append(ax1.scatter(lb_time[i], Avmet[i], s=5, c=c, vmin=0, vmax=100,label="AvBHMet"))
    ax1.legend(handles=halo)
    ax1.set_title(halo_names[i])
    #plt.show()
    plt.savefig(WD+halo_names[i]+'_Metmass.png', dpi=300)

Plot(0)
Plot(4)