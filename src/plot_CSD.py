from data import *
from utility import *
from figure import *

##################################################

setting_dir="../examples/non-uniform/"
type="number" # number or volume

##################################################

# read the specified CSD
CSD_file=setting_dir+"CSD.csv"
tmp1=variable_read(CSD_file)
size=tmp1[0]
fraction=tmp1[1]

if type=="volume":
    x=size.value
    y=fraction.value
    xlabel="crystal size ($\mu m$)"
    ylabel="volume fraction (-)"
    title="Crystal Size Distribution (Volume Basis)"
    xlim=[0,0]
    ylim=[0,0]
    form="o"


    plot_variable(x,y,xlabel,ylabel,title,xlim,ylim,form)
elif type=="number":
    size2,fraction2=VF_to_NF(size,fraction)
    x=size2.value
    y=fraction2.value
    xlabel="crystal size ($\mu m$)"
    ylabel="number fraction (-)"
    title="Crystal Size Distribution (Number Basis)"
    xlim=[0,0]
    ylim=[0,0]
    form="o--"


    plot_variable(x,y,xlabel,ylabel,title,xlim,ylim,form)