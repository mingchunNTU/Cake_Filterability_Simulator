from data import *
from utility import *
from figure import *


############################################

setting_dir="../examples/non-uniform/"

cake_porosity=0.393 # calculated by DEM simulation
sphericity=1
crystal_density=1180 # kg/m3

############################################

# read the specified CSD
CSD_file=setting_dir+"CSD.csv"
tmp1=variable_read(CSD_file)
size=tmp1[0]
fraction=tmp1[1]

cake_resistance=estimate_cake_resistance(size,fraction,cake_porosity,sphericity,crystal_density)

print("estimated cake resistance= "+"{:.2e}".format(cake_resistance)+" m/kg")