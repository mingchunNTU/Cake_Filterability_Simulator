from data import *
from figure import *


# modify the DEM_porosity.csv file to a variable_read format
file="Result/DEM_porosity.csv"
tmp1=csv_input(file)
for i in range(10):
	if tmp1[0][0].isdigit():
		break
	else:
		tmp1.pop(0)

tmp2=["number of iteration","porosity of sampling region","number of particles in the sampling region","number of particles in the domain"]
tmp3=["-","-","-","-"]
tmp1.insert(0,tmp3)
tmp1.insert(0,tmp2)

csv_output(tmp1,file)


# plot the time-porosity diagram
# file="Result/DEM_porosity.csv"
# tmp1=variable_read(file)
# x=tmp1[0].value
# y=tmp1[1].value
# xlabel="Number of time step (-)"
# ylabel="Sampling porosity (-)"
# title="The final cake porosity="+"{:.3f}".format(y[-1])
# xlim=[0,0]
# ylim=[0,0]
# form="o--"

# plot_variable(x,y,xlabel,ylabel,title,xlim,ylim,form)

# output the final porosity and particle ratio in sampling region
file="Result/DEM_porosity.csv"
tmp1=variable_read(file)
text="The final cake porosity="+"{:.3f}".format(tmp1[1].value[-1])
print(text)
text="Np in sample region/Np in domain="+"{:.0f}".format(tmp1[2].value[-1])+"/"+"{:.0f}".format(tmp1[3].value[-1])
print(text)
