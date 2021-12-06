# Avalanche Native Token ($AVAX) Dynamics
import json
 
# "avax.json" from https://github.com/hsk81/avalanche-stakes/tree/main/json in 03.12.2021
f = open('avax.json')
data = json.load(f)


#Staking Amount
totalWeight=[]

for item in data:
    totalWeight.append(item["totalWeight"])
    
#Staking Start Time
startTime=[]

for item in data:
    startTime.append(item["startTime"])
    
#Staking End Time
endTime=[]

for item in data:
    endTime.append(item["endTime"])
    

import numpy as np
import pandas as pd
uni= pd.DataFrame(list(zip(totalWeight,startTime, endTime)),columns=['totalWeight', 'startTime','endTime'])
uni['startTime'] = pd.to_datetime(uni['startTime'],unit='s')
uni['endTime'] = pd.to_datetime(uni['endTime'],unit='s')
#Staking Time as days
uni['days'] = uni['endTime'] - uni['startTime']
#Staking Time as weeks
uni['diff_days']=uni['days']/7/np.timedelta64(1,'D')

#Equation 3 in whitepaper: Part I : (0.002 * u.s time + 0.896)
uni['diff_days2']=uni['diff_days']*0.002+0.896

#Cleaning for good reading 
uni["diff_days"]=uni["diff_days"].apply(lambda x : "{0:,.0f}".format(x))

#Staking Amount for good reading 
uni['totalWeight'] = uni['totalWeight'] / (10**9)
uni['totalWeight'] = uni['totalWeight'].astype(int)

#Equation 3 in whitepaper: Part II : u.s amount /Rl
uni['amount']=uni['totalWeight']/360000000
uni['amount'] = uni['amount'].astype(float)

#Equation 3
uni['p'] = uni['diff_days2'] * uni['amount']
p=uni['p'].sum()
p

#Equation 2 or L

y=1.15
lam=1.1
i=0
L=0
for i in range(0,101):
    result=1/(y+(1/1+i**lam))**i        
    i=i+1
    L=L+result
L

#The last part of Equation 1 or Lj

y=1.15
lam=1.1
i=0
Lj=0
for i in range(0,2):
    result=1/(y+(1/1+i**lam))**i        
    i=i+1
    Lj=Lj+result
Lj

# Equation 1
Rl=360000000
cj=326000000
Rj=Rl+p*(cj/L)*Lj
Rj
