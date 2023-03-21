import subprocess
import os
from data import *
from figure import *
from utility import *

# access to the files in src/resource directory
#base=os.path.dirname(__file__)
#file=base+"/resource/prime_table.csv"
#prime_table=csv_input(file)


# read the crystal size distribution
tmp1=variable_read("CSD.csv")
size=tmp1[0] # the size is radius instead of diameter
fraction=tmp1[1]

cake_porosity=0.4
sphericity=1
crystal_density=2500

cake_resistance=estimate_cake_resistance(size,fraction,cake_porosity,sphericity,crystal_density)
print("estimated cake resistance= "+"{:.2e}".format(cake_resistance)+" m/kg")