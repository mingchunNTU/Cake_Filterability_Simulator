#!/bin/bash

#===========================================================================#
# Modified from parCFDEMrun.sh script of ErgunTestMPI case of CFDEM project
#===========================================================================#

#- source CFDEM env vars
. ~/.bashrc

#- include functions
source $CFDEM_SRC_DIR/lagrangian/cfdemParticle/etc/functions.sh

#--------------------------------------------------------------------------------#
#- define variables
casePath="$(dirname "$(readlink -f ${BASH_SOURCE[0]})")"
logpath=$casePath
headerText="CFDEM_run"
logfileName="log_$headerText"
solverName="cfdemSolverPiso"
nrProcs="4"
machineFileName="none"   # yourMachinefileName | none
debugMode="off"          # on | off| strict | profile
#--------------------------------------------------------------------------------#

#- call function to run a parallel CFD-DEM case
parCFDDEMrun $logpath $logfileName $casePath $headerText $solverName $nrProcs $machineFileName $debugMode

# post processing
cd ./CFD
source /opt/openfoam9/etc/bashrc
reconstructPar -noLagrangian
foamToVTK

