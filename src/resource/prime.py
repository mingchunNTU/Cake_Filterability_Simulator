from data import *

prime=[2]

for i in range(3,100000):
    boolean=1
    for j in range(len(prime)):
        if i%prime[j]==0:
            boolean=0
            pass
    if boolean==1:
        prime.append(i)

output=[]
for i in range(len(prime)):
    if prime[i]>10000:
        tmp1=[]
        tmp1.append(prime[i])
        output.append(tmp1)

csv_output(output,"prime_table.csv")




        
            
        