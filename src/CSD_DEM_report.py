from data import *
from utility import *
from figure import *

##################################################################
setting_dir="../examples/non-uniform/"

# DEM parameter used
settling_velocity=0.01 # m/s
time_step=0.1 # us
particle_number=2000
initial_void_fraction=0.65

# particle property used
Young_Modulus=5e6 # Pa
poisson_ratio=0.2 # -
particle_density=1180 # kg/m3


##################################################################

# read the specified CSD
CSD_file=setting_dir+"CSD.csv"
tmp1=variable_read(CSD_file)
size=tmp1[0]
fraction=tmp1[1]

# define the string list to be output
output=[]

# generate DEM report
min_particle_number=estimate_particle_number(size,fraction)
Rayleigh_time_step=estimate_Rayleigh_time_step(size,fraction,Young_Modulus,poisson_ratio,particle_density)
system_dimension=estimate_system_dimension(size,fraction,particle_number,initial_void_fraction)
number_of_step=estimate_number_of_step(time_step,settling_velocity,system_dimension)
min_porosity=1-2*(1-initial_void_fraction)

output.append("################## DEM Report for Specified CSD #######################")
output.append("")
str1="Minimum number of particle: "+str(min_particle_number)
output.append(str1)
str1="Maximum time step: "+str(Rayleigh_time_step)+" (us)"
output.append(str1)
str1="Suggested system dimension: "+str(system_dimension)+" (um)"
output.append(str1)
str1="Suggested number of step: "+str(number_of_step)
output.append(str1)
str1="Minimum cake porosity: "+str(min_porosity)
output.append(str1)
output.append("")
output.append("#######################################################################")
output.append(" ")

# generate the system geometry section of LIGGGHTS configuration file
output.append("################## System Geometry Section #######################")
output.append("")
str1="variable DEM_domain_half_width equal "+"{:.0f}".format(system_dimension/2)
output.append(str1)
str1="variable DEM_domain_height equal "+"{:.0f}".format(system_dimension*5)
output.append(str1)
str1="variable DEM_domain_depth equal "+"{:.0f}".format(system_dimension*4)
output.append(str1)
output.append("")

str1="variable DEM_insertion_half_width equal "+"{:.0f}".format(system_dimension/2)
output.append(str1)
str1="variable DEM_insertion_top equal "+"{:.0f}".format(system_dimension*2)
output.append(str1)
str1="variable DEM_insertion_bottom equal "+"{:.0f}".format(0)
output.append(str1)
output.append("")

str1="variable DEM_sample_half_width equal "+"{:.0f}".format(system_dimension/2)
output.append(str1)
str1="variable DEM_sample_top equal "+"{:.0f}".format(system_dimension)
output.append(str1)
str1="variable DEM_sample_bottom equal "+"{:.0f}".format(0)
output.append(str1)
output.append("")

str1="variable DEM_zwall equal "+"{:.2f}".format(0)
output.append(str1)
str1="variable DEM_particle_number equal "+"{:.0f}".format(particle_number)
output.append(str1)
output.append("")

output.append("")
output.append("#######################################################################")
output.append(" ")

# generate the particle template section
output.append("################## Particle Template Section #######################")
output.append("")

output.extend(generate_particle_template(size,fraction))

output.append("")
output.append("#######################################################################")
output.append(" ")

# output the result

file=setting_dir+"CSD_DEM_report.txt"
print_list(output)
output_list(output,file)