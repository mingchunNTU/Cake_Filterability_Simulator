#!/bin/bash

# remove all the old files
/bin/bash script/clean_case.sh

#- define variables
casePath="$(dirname "$(readlink -f ${BASH_SOURCE[0]})")"

/bin/bash $casePath/script/parDEMrun.sh

rm script/log_DEM_simulation
rm log.liggghts

cd $casePath/Result/vtk_file


