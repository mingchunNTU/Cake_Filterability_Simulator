#!/bin/bash

#===================================================================#
# Modfified from parDEMrun.sh of ErgunTestMPI case of CFDEM project
#===================================================================#

#- source CFDEM env vars
# . ~/.bashrc

#- include functions
source $CFDEM_SRC_DIR/lagrangian/cfdemParticle/etc/functions.sh

echo "starting DEM run in parallel..."
#--------------------------------------------------------------------------------#
#- define variables
casePath="$(dirname "$(readlink -f ${BASH_SOURCE[0]})")"
logpath="$casePath"
headerText="DEM_simulation"
logfileName="log_$headerText"
solverName="liggghts_configuration.txt"
nrProcs=6
machineFileName="none"   # yourMachinefileName | none
debugMode="off"
#--------------------------------------------------------------------------------#

#- call function to run DEM case
parDEMrun $logpath $logfileName $casePath $headerText $solverName $nrProcs $machineFileName $debugMode

