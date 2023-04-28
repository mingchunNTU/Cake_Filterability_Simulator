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

program_checker=0

def read_CSD():
    # read the crystal size distribution
    tmp1=variable_read("CSD/CSD.csv")
    size=tmp1[0] # the size is crystal diameter instead of crystal radius. The unit should be um
    fraction=tmp1[1] # the fraction is number or volume fraction instead of number or volume percentage
    return size, fraction

if sys.argv[1]=="--estimate_resistance":
    size,fraction=read_CSD()
    
    # estimate the cake resistance
    cake_porosity=float(sys.argv[2])
    sphericity=1
    crystal_density=float(sys.argv[3])

    cake_resistance=estimate_cake_resistance(size,fraction,cake_porosity,sphericity,crystal_density)
    print("estimated cake resistance= "+"{:.2e}".format(cake_resistance)+" m/kg")

    program_checker=1

if sys.argv[1]=="--estimate_system_dimension":
    size,fraction=read_CSD()

    # estimate the required system dimension for the desired number of particle
    particle_number=float(sys.argv[2])
    system_dimension=estimate_system_dimension(size,fraction,particle_number)
    
    # output the result
    print("")
    print("suggested half width of the domain="+"{:.0f}".format(system_dimension/2)+" um")
    print("suggested height of the domain="+"{:.0f}".format(system_dimension*5)+" um")
    print("suggested depth of the domain="+"{:.0f}".format(system_dimension*4)+" um \n")

    print("suggested half width of the insertion region="+"{:.0f}".format(system_dimension/2)+" um")
    print("suggested top position of the insertion region="+"{:.0f}".format(system_dimension*2)+" um")
    print("suggested bottom position of the insertion region="+"{:.0f}".format(0)+" um \n")

    print("suggested half width of the sample region="+"{:.0f}".format(system_dimension/2)+" um")
    print("suggested top position of the sample region="+"{:.0f}".format(system_dimension)+" um")
    print("suggested bottom position of the sample region="+"{:.0f}".format(0)+" um \n")
    
    print("suggested collision detection limit="+"{:.2f}".format(size.value[-1])+" um \n")

    print("#################LIGGGHTS input#############################################\n")

    print("variable DEM_domain_half_width equal "+"{:.0f}".format(system_dimension/2))
    print("variable DEM_domain_height equal "+"{:.0f}".format(system_dimension*5))
    print("variable DEM_domain_depth equal "+"{:.0f}".format(system_dimension*4)+"\n")

    print("variable DEM_insertion_half_width equal "+"{:.0f}".format(system_dimension/2))
    print("variable DEM_insertion_top equal "+"{:.0f}".format(system_dimension*2))
    print("variable DEM_insertion_bottom equal "+"{:.0f}".format(0)+"\n")

    print("variable DEM_sample_half_width equal "+"{:.0f}".format(system_dimension/2))
    print("variable DEM_sample_top equal "+"{:.0f}".format(system_dimension))
    print("variable DEM_sample_bottom equal "+"{:.0f}".format(0)+"\n")

    print("variable DEM_zwall equal "+"{:.2f}".format(0)+"\n")
    
    print("variable DEM_cutoff equal "+"{:.2f}".format(size.value[-1])+"\n")

    print("variable DEM_particle_number equal "+"{:.2f}".format(particle_number))

    
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
    size,fraction=read_CSD()
    
    # use the CSD_generator module
    CSD_generator(size,fraction)
    program_checker=1

if sys.argv[1]=="--estimate_time_step":
    
    # define the parameters
    particle_radius=float(sys.argv[2])
    Young_Modulus=float(sys.argv[3])
    poisson_ratio=float(sys.argv[4])
    particle_density=float(sys.argv[5])
    pi=3.1415

    # calculate the Rayleigh time step
    beta=0.8766+0.163*poisson_ratio
    G=Young_Modulus/2/(1+poisson_ratio)

    time_step=pi*particle_radius/beta*np.sqrt(particle_density/G)*1e6
    print("Rayleigh time step="+"{:.3f}".format(time_step)+" us")

    program_checker=1

if sys.argv[1]=="--estimate_particle_number":
    
    # read crystal size distribution
    size,volume_fraction=read_CSD()
    size,number_fraction=VF_to_NF(size,volume_fraction)

    # read mimimum non-zero number fraction
    minimum_number_fraction=non_zero_minimum(number_fraction.value)
    minimum_particle_number=int(1/minimum_number_fraction)+1

    print("The minimum particle number should be "+str(minimum_particle_number))

    program_checker=1

if program_checker==0:
    print("The argument may be wrong")