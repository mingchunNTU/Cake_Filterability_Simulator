from data import *
from utility import *
from figure import *

##################################################

setting_dir="../examples/non-uniform/"

##################################################

# read the specified CSD
file=setting_dir+"Result/DEM_porosity.csv"
tmp1=variable_read(file)
iteration=tmp1[0]
cake_porosity=tmp1[1]

x=iteration.value
y=cake_porosity.value
xlabel="number of step (-)"
ylabel="cake porosity (-)"
title="off"
xlim=[0,0]
ylim=[0,0]
form="o--"

plot_variable(x,y,xlabel,ylabel,title,xlim,ylim,form)