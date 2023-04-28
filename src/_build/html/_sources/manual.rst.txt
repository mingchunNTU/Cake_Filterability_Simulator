Installation
================================================
It is suggested to install the program on a computer with Ubuntu 20.04.6 or newer version. The program is based on the open source DEM software `LIGGGHTS <https://www.cfdem.com/media/DEM/docu/Manual.html>`_. Please install `CFDEM <https://www.cfdem.com/media/CFDEM/docu/CFDEMcoupling_Manual.html>`_, which will help you install and configure LIGGGHTS automatically. After you install CFDEM, please execute the ErgunTestMPI example in tutorials/cfdemSolverPiso/ErgunTestMPI. If the simulation ends successfully, your installlation is complete and parDEMrun command is available. 

Furthermore, the program is written in Python. Please make sure that you install Python 3 including **numpy, matplotlib, scipy, csv, copy, datetime and os** package on your computer.

To install the program, please install git and clone the source code of the project

.. code-block:: console

	cd ~
	sudo apt-get install git
	git clone https://github.com/mingchunNTU/Filtration_Simulator.git 

Add the following line to your ~/.bashrc file and update ~/.bashrc setting by typing :code:`source ~/.bashrc`. 

.. code-block:: console

	source $HOME/Filtration_Simulator/src/etc/bashrc

Program Command
==================================================
The program provides four commands that help generate LIGGGHTS input script and estimate the cake resistance based on the LIGGGHTS simulation result. All the parameters are in SI units. Please substitute the parameters such as *porosity, particle_density or poisson_ratio* with a number with physical meaning **instead of putting the string on the command line directly**, or an error message may occur.  


.. code-block:: console
	
	# estimate the cake resistance according the the speficied crystal size distribution and crystal property
	filtration_simulator --estimate_resistance porosity particle_density 
	
	# estimate the DEM system dimension parameters according to the specified crystal size distribution
	filtration_simulator --estimate_system_dimension particle_number 	
	
	# generate the particle template section of LIGGGHTS input script with specified crystal size distribution
	filtration_simulator --CSD_script_generator  
	
	# estimate the Rayleigh time step based on the particle radius and property
	filtration_simulator --estimate_time_step particle_radius Young's_Modulus poisson_ratio particle_density 
	
	# estimate the minimum number of particle based on the specify crystal size distribution 
	filtration_simulator --estimate_particle_number

File Structure
==================================================
To construct the cake structure with specified crystal size distriubtion, you need to modify the files in examples/non-uniform. The description of the files in the non-uniform directory is shown below. To execute the program, please enter :code:`source ~/Allrun.sh` in the terminal. 

* Allrun.sh: Execution script of the example
* liggghts_configuration.txt: LIGGGHTS configuration files, which you should modify according to your specified crystal size distribution
* CSD

	* CSD.csv: Your specified CSD
	* CSD.txt: Generated text file that contains the particle template according to specified CSD

* script
	* python script: Contains python module for postProcessing.sh
	* clean_case.sh: Remove the previous simulation result (**dependent script of Allrun.sh**)
	* edit_filtration_simulator_main.sh: Open the main program of Filtration_simulator using vim. The script help you modify main program according to your need
	* paraview.sh: Change the directory to Result/vtk_file and open paraview program for the post processing. Please make sure that you install paraview.
	* parDEMrun.sh: execute parDEMrun command for LIGGGHTS simulation (**dependent script of Allrun.sh**)
	* postProcessing.sh: plot the relationship between number of iteration and cake porosity (**dependent script of Allrun.sh**)

* Result
	* DEM_porosity.csv: simulated cake porosity 
	* vtk_file: vtk files of LIGGGHTS simulation, which can be visuallized using software paraview

Parallel Computing
=====================================================
LIGGGHTS supports parallel computing, which uses several cpus simultaneously to perform the simulation. To check the available number of processors in your computer, please type the following commands through command line.

.. code-block:: console

	cat /proc/cpuinfo | grep "^cpu cores" | uniq
	
To change the number of cpu used in the simulation, please edit the *nrProcs* parameter in script/parDEMrun.sh .

Simulation of Cake Structure
======================================================
The script that defines DEM simulation setting is  *liggghts_configuration.txt*. The unit used in liggghts_configuration.txt* is **not SI unit**. It is found that if *SI* unit is used, the numerical value of particle volume will become too small and a numerical problem will happen during LIGGGHTS simulation. Thus, *micro* unit is used for LIGGGHTS simulation. The conversion factor between *SI* unit and *micro* unit is shown below.

* Length: :math:`1\ \mu m=10^{-6}\ m` 
* Time: :math:`1\ \mu s=10^{-6}\ s`
* Mass: :math:`1\ pg=10^{-15}\ kg`
* Velocity: :math:`1\ \mu m/ \mu s=1\ m/s`
* Gravity: :math:`1\ \mu m/{\mu s^2}=10^{6}\ m/s^2`
* Density: :math:`1\ pg/{\mu m^3}=10^{3}\ kg/m^3`
* Pressure (Youngs's Modulus): :math:`1\ pg/(\mu m  \cdot \mu s^2)=10^{3}\ kg/(m \cdot s^2)`
* Cohesion Energy Density: :math:`1\ pg/(\mu m  \cdot \mu s^2)=10^{3}\ kg/(m \cdot s^2)`
* Dynamic Viscosity: :math:`1\ pg/(\mu m \cdot \mu s)=10^{-3}\ kg/(m \cdot s)`
* Kinematic Viscosity: :math:`1\ {\mu m^2}/{\mu s}=10^{-6}\ m^2/s`
* Filter Cake Resistance: :math:`1\ {\mu m}/pg=10^{9}\ m/kg`

To siumulate the cake structure, there're three parts that should be modified according to your specified CSD

* System Dimension
* Collision Detection Limit
* Particle Template and Distribution 

First, please define your specified CSD in CSD/CSD.csv . The size is crystal diameter instead of crystal radius. The crystal size is in the unit of um. 

Second, please enter the following command to estimate the system dimension and collision detection limit. It's suggested the system contains more than 1000 particles. When the system contains large amount of small particles or CSD is discretized into large number of bins, a larger particle number should be used. The minimum particle number can be estimated using command :code:`filtration_simulator --estimate_particle_number`.  According to the experience, the simulation of a system with 2000 particles will take from several minutes to one hour depending on the size distribution. Please modify the variable definition section of *liggghts_configuration.txt* according to the program output.  

.. code-block:: console
	
	filtration_simulator --estimate_system_dimension particle_number 	 

Third, please enter the following command to generate the particle template. *CSD/CSD.txt* contains particle template information. Please copy and paste the *CSD.txt* content into particle template section of *liggghts_configuration.txt*.

.. code-block:: console	
	
	filtration_simulator --CSD_script_generator  
	
After configuring *liggghts_configuration.txt*, please enter :code:`source ~/Allrun.sh` in the terminal to execute the program. After the simulation complete, the calculated porosity will be stored in *Result/DEM_porosity.csv*. The vtk files of the simulation is stored in *Result/vtk_file*. 

The default time step is 0.01 us, which is 25% of Rayleigh time step when the particle diameter is 1 um. If the crystal is much larger than 1 um, a larger time step can be used, and the number of time step can be reduced. To estimate the Rayleigh time step, please enter the following command

.. code-block:: console
	
	filtration_simulator --estimate_time_step particle_radius Young's_Modulus poisson_ratio particle_density 

Estimation of Cake Specific Resistance
============================================================
After DEM simulation, please enter the following command to estimate the cake specific resistance. The porosity is calculated by previous DEM simulation. 

.. code-block:: console
	
	filtration_simulator --estimate_resistance porosity particle_density


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
