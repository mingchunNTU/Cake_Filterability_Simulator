from figure import *
from data import *
import numpy as np
from scipy.integrate import quad, odeint
import os

def output_list(string_list, file):
    """
    Export a list of string as one file

    :param string_list: list of string
    :type string_list: list
    :param file: output file name
    :type file: string

    """

    tmp1=open(file,'w',encoding='utf-8')
    tmp1.write('\n'.join(string_list))
    tmp1.close()

def print_list(string_list):
    """
    Display the content of a string list

    :param string_lsit: list of string
    :type string_list: list

    """

    for i in range(len(string_list)):
        print(string_list[i])

def get_minimun_size(size,fraction):
    """
    Estimate the minimun particle size of specified CSD

    :param size: particle size (um)
    :type: size: variable
    :param fraction: volume fraction (-)
    :type fraction: variable
    :return: minimum size (um)

    """
    index=0
    for i in range(len(fraction.value)):
        if fraction.value[i]!=0:
            index=i
            break
    
    return size.value[index]

def get_maximum_size(size,fraction):
    """
    Estimate the maximum particle size of specified CSD

    :param size: particle size (um)
    :type: size: variable
    :param fraction: volume fraction (-)
    :type fraction: variable
    :return: minimum size (um)

    """
    
    length=len(fraction.value)
    index=length-1
    for i in range(len(fraction.value)):
        if fraction.value[length-i-1]!=0:
            index=length-i-1
            break
    
    return size.value[index]

def get_minimum_fraction(size,fraction):
    """
    Estimate the minimun number fraction of specified CSD

    :param size: particle size (um)
    :type: size: variable
    :param fraction: volume fraction (-)
    :type fraction: variable
    :return: size with minimum number fraction and minimum number fraction

    """

    index=0
    minimum=2
    for i in range(len(fraction.value)):
        if fraction.value[i]<minimum and fraction.value[i]>1e-12 :
            minimum=fraction.value[i]
            index=i
    return size.value[index], fraction.value[index]




def estimate_particle_number(size,fraction):
    """
    Estimate the minimun particle number required for specified CSD

    :param size: particle size (um)
    :type: size: variable
    :param fraction: volume fraction (-)
    :type fraction: variable
    :return: required minimum particle number

    """
    size2,number_fraction=VF_to_NF(size,fraction)
    min_size,min_fraction=get_minimum_fraction(size2,number_fraction)
    minimum_particle_number=int(1/min_fraction)+1

    return minimum_particle_number


def NF_to_VF(size,number_fraction):
    """
    Transform the number fraction to volume fraction

    :param size: size (um)
    :type size: variable
    :param number_fraction: number fraction (-)
    :type number_fraction: variable
    :return: size and volume fraction
    :rtype: variable
    """

    volume_fraction=variable("volume fraction","-",[])

    total_volume=0
    for i in range(len(size.value)):
        tmp1=size.value[i]**3*number_fraction.value[i]
        total_volume=total_volume+tmp1
    for i in range(len(size.value)):
        tmp1=size.value[i]**3*number_fraction.value[i]
        volume_fraction.value.append(tmp1/total_volume)	
	
    return size,volume_fraction
	
def VF_to_NF(size,volume_fraction):
    """
    Transform the number fraction to volume fraction

    :param size: size (um)
    :type size: variable
    :param volume_fraction: volume fraction (-)
    :type volume_fraction: variable
    :return: size and number fraction
    :rtype: variable
    """

    number_fraction=variable("number fraction","-",[])

    total_number=0
    for i in range(len(size.value)):
        tmp1=volume_fraction.value[i]/size.value[i]**3
        total_number=total_number+tmp1
    for i in range(len(size.value)):
        tmp1=volume_fraction.value[i]/size.value[i]**3
        number_fraction.value.append(tmp1/total_number)	

    return size,number_fraction

def estimate_system_dimension(size,volume_fraction,particle_number,inital_void_fraction):
    """
    Estimate the required system dimension to accommodate the specified particle number

    :param size: crystal size (um)
    :type size: variable
    :param volume_fraction: volume fraction (-)
    :type volume_fraction: variable
    :param particle_number: target particle number (-)
    :type particle_number: float
    :return: system dimension (um)
    :param initial_void_fraction: initial void fraction of insertion region
    :type initial_void_fraction: float
    :return: system dimension (um)

    """
	
	
    size2,number_fraction=VF_to_NF(size,volume_fraction)
    particle_volume=0
    for i in range(len(size2.value)):
        tmp1=3.1416/6*size2.value[i]**3*number_fraction.value[i]*particle_number
        particle_volume=particle_volume+tmp1
    particle_volume_fraction=1-inital_void_fraction
    system_volume=particle_volume/particle_volume_fraction
    system_dimension=int((system_volume/2)**(1/3))
    
    return system_dimension

def estimate_Rayleigh_time_step(size,fraction,Young_Modulus,poisson_ratio,particle_density):
    """
    Estimate Rayleigh time step based on the smallest particle size and particle property

    :param size: crystal size (um)
    :type size: variable
    :param fraction: volume fraction (-)
    :type fraction: variable
    :param Young_Modulus: Young's modulus (Pa)
    :type Young_Modulus: float
    :param poisson_ratio: Poisson ratio (-)
    :type poisson_ratio: float
    :param particle_density: particle density (kg/m^3)
    :type particle_density: float
    :return: Rayleigh time step (us)
	
	"""

    beta=0.8766+0.163*poisson_ratio
    G=Young_Modulus/2/(1+poisson_ratio)
    r=get_minimun_size(size,fraction)/2

    Rayleigh_time_step=3.1416*r/beta*np.sqrt(particle_density/G)

    return Rayleigh_time_step

def estimate_number_of_step(time_step,settling_velocity,system_dimension):
    """
    Estimate the minimum number of step for the cake to be stable

    :param time_step: time step used (um)
    :param settling_velocity: settling velocity of the particle (um/us)
    :param system_dimension: system dimension
    :return: number of step
    """

    number_of_step=int(system_dimension/settling_velocity/time_step/4) # 4 is an empirical parameter by trial and error
    
    return number_of_step

def generate_particle_template(size,fraction):
    """
    Generate particle template section for specified CSD

    :param size: particle size (um)
    :type: size: variable
    :param fraction: volume fraction (-)
    :type fraction: variable
    :return: contents of particle template with specified CSD

    """
    # access to the files in src/resource directory
    base=os.path.dirname(__file__)
    file=base+"/resource/prime_table.csv"
    prime_table=csv_input(file)

	# initialize the output script
    output=[]

	# generate the particle template
    for i in range(len(size.value)):
        line="fix pts"+str(i+1)+" all particletemplate/sphere "+str(prime_table[i][0])+" atom_type 1 density constant ${DEM_density} radius constant "+str(size.value[len(size.value)-1-i]/2)+" \n"
        output.append(line)

	# generate the particle distribution
    line="fix pdd all particledistribution/discrete/massbased 32452843 "+str(len(size.value))
    for i in range(len(fraction.value)):
        line=line+" pts"+str(i+1)+" "+str(fraction.value[i])
    line=line+" \n"
    output.append(line)
    return output

def estimate_cake_resistance(size,volume_fraction,cake_porosity,sphericity,crystal_density):
	"""
	Estimate the cake resistance based on the size distribution and cake porosity of the cake        

	:param size: crystal size (um)
	:type size: variable
	:param volume_fraction: volume fraction (-)
	:type volume_fraction: variable
	:param cake_porosity: cake porosity (-)
	:type cake_porosity: float
	:param sphericity: sphericity of the crystal (-)
	:type sphericity: float
	:param crystal_density: crystal density (kg/m^3)
	:type size: float
	:return: cake resistance (m/kg)
	:rtype: float
    
	"""
    
	tmp1=0
	for i in range(len(size.value)):
		tmp1=tmp1+1/(size.value[i]*1e-6)**2*volume_fraction.value[i]        
	cake_resistance=180*(1-cake_porosity)/cake_porosity**3/sphericity**2/crystal_density*tmp1
    
	return cake_resistance


