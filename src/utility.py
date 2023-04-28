import numpy as np
from scipy.integrate import quad, odeint
from data import *
import os
from document import *
	
def NF_to_VF(size,number_fraction):
	"""
	Transform the number fraction to volume fraction
	
	:param size: size
	:type size: variable
	:param number_fraction: number fraction
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
	
	:param size: size
	:type size: variable
    	:param volume_fraction: volume fraction
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
	:return: cake resistance
	:rtype: float
    
	"""
    
	tmp1=0
	for i in range(len(size.value)):
		tmp1=tmp1+1/(size.value[i]*1e-6)**2*volume_fraction.value[i]        
	cake_resistance=180*(1-cake_porosity)/cake_porosity**3/sphericity**2/crystal_density*tmp1
    
	return cake_resistance

def estimate_system_dimension(size,volume_fraction,particle_number):
	"""
	Estimate the required system dimension to accommodate the specified particle number
	
	:param size: crystal size (um)
	:type size: variable
	:param volume_fraction: volume fraction (-)
	:type volume_fraction: variable
	:param particle_number: target particle number
	:type particle_number: float
	:param sphericity: sphericity of the crystal (-)
	:type sphericity: float
	:param crystal_density: crystal density (kg/m^3)
	:type size: float
	:return: system dimension (um)
	:rtype: float 
	
	"""
	
	
	size2,number_fraction=VF_to_NF(size,volume_fraction)
	particle_volume=0
	for i in range(len(size2.value)):
		tmp1=3.1416/6*size2.value[i]**3*number_fraction.value[i]*particle_number
		particle_volume=particle_volume+tmp1
        
	estimate_porosity=0.3
	system_volume=particle_volume/(1-estimate_porosity)
	system_dimension=system_volume**(1/3)
    
	return system_dimension

def CSD_generator(size,volume_fraction):
	"""
	Generate a txt file that contains the CSD information needed for LIGGGHTS simulation

	:param size: crystal size (um)
	:type size: variable
	:param volume_fraction: volume fraction (-)
	:type volume_fraction: variable
	"""

	# access to the files in src/resource directory
	base=os.path.dirname(__file__)
	file=base+"/resource/prime_table.csv"
	prime_table=csv_input(file)

	# initialize the output script
	output=[]

	# generate the particle template
	for i in range(len(size.value)):
		line="fix pts"+str(i+1)+" all particletemplate/sphere "+str(prime_table[i][0])+" atom_type 1 density constant ${DEM_density} radius constant "+str(size.value[i]/2)+" \n"
		output.append(line)

	# generate the particle distribution
	line="fix pdd all particledistribution/discrete/massbased 32452843 "+str(len(size.value))
	for i in range(len(volume_fraction.value)):
		line=line+" pts"+str(i+1)+" "+str(volume_fraction.value[i])
	line=line+" \n"
	output.append(line)

	file="CSD/CSD.txt"
	tmp1=document()
	tmp1.output_document(output,file)

def non_zero_minimum(input_list):
	"""
	Return the non-zero minimum value from the input list

	:param input_list: the list to be processed
	:type size: list
	:return: non-zero mimimum value
	:rtype: float 
	"""
	tmp1=input_list
	tmp2=[]
	for i in range(len(tmp1)):
		if tmp1[i]!=0:
			tmp2.append(tmp1[i])
	
	if len(tmp2)==0:
		print("The CSD is all zero")

	else:
		output=tmp2[0]
		for i in range(len(tmp2)):
			if tmp2[i] < output:
				output=tmp2[i]
		return output

		





    
	
	
	
	
	
	
