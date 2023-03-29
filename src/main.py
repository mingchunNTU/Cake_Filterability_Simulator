import subprocess
import os
import sys
from data import *
from figure import *
from utility import *
from document import *

# access to the files in src/resource directory
#base=os.path.dirname(__file__)
#file=base+"/resource/prime_table.csv"
#prime_table=csv_input(file)


# read the crystal size distribution
tmp1=variable_read("CSD/CSD.csv")
size=tmp1[0] # the size is crystal diameter instead of crystal radius. The unit should be um
fraction=tmp1[1] # the fraction is number or volume fraction instead of number or volume percentage
program_checker=0

if sys.argv[1]=="--estimate_resistance":
    # estimate the cake resistance
    cake_porosity=float(sys.argv[2])
    sphericity=1
    crystal_density=float(sys.argv[3])

    cake_resistance=estimate_cake_resistance(size,fraction,cake_porosity,sphericity,crystal_density)
    print("estimated cake resistance= "+"{:.2e}".format(cake_resistance)+" m/kg")

    program_checker=1

if sys.argv[1]=="--estimate_system_dimension":
    # estimate the required system dimension for the desired number of particle
    particle_number=float(sys.argv[2])
    system_dimension=estimate_system_dimension(size,fraction,particle_number)
    
    #print("suggested system dimension="+"{:.2e}".format(system_dimension)+" um")
    print("suggested domain half width="+"{:.0f}".format(system_dimension/2)+" um")
    print("suggested domain height="+"{:.0f}".format(system_dimension*5)+" um")
    print("suggested doamin depth="+"{:.0f}".format(system_dimension*4)+" um \n")
    print("suggested insertion half width="+"{:.0f}".format(system_dimension/2)+" um")
    print("suggested insertion top="+"{:.0f}".format(system_dimension*2)+" um")
    print("suggested insertion bottom ="+"{:.0f}".format(0)+" um \n")
    print("suggested sampling half width="+"{:.0f}".format(system_dimension/2)+" um")
    print("suggested sampling top="+"{:.0f}".format(system_dimension)+" um")
    print("suggested system bottom="+"{:.0f}".format(0)+" um \n")
    
    program_checker=1

# test the document module
# tmp1=document()
# file="test.txt"
# tmp1.read_document(file)
# old_string="#target"
# new_string="500"
# tmp1.substitute(old_string,new_string)
# file2="result.txt"
# tmp1.output_document_modified(file2)

if sys.argv[1]=="--CSD_script_generator":
    # test the CSD_generator module
    CSD_generator(size,fraction)
    program_checker=1

if program_checker==0:
    print("The argument may be wrong")