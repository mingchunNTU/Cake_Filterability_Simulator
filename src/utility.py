import numpy as np
from scipy.integrate import quad, odeint
from data import *
	
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
	
	
	
	
	
	
