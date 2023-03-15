import subprocess
import os
from data import *
from figure import *
from utility import *

size=variable("size","um",[5e-4])
volume_fraction=variable("volume fraction","-",[1])

estimate_particle_number(size,volume_fraction,0.01)
estimate_time_step(5e-4,0.2,2500,5e6)
estimate_insert_rate(1400,1e-5,350000)
estimate_resistance_from_CFDEM(2.8,1.83e-3,1e-4,1e-3,1e-3)
estimate_resistance_from_Ergun(1e-3,0.373,2500)
estimate_particle_mass(1400,1e-3,2500)
