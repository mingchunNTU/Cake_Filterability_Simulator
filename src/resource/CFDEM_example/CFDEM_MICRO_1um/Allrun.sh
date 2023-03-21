#!/bin/bash

# remove all the old files and generate the mesh again
/bin/bash clean_case.sh
cd ./CFD
blockMesh
cd ../


#- define variables
casePath="$(dirname "$(readlink -f ${BASH_SOURCE[0]})")"

/bin/bash $casePath/parDEMrun.sh
/bin/bash $casePath/parCFDDEMrun.sh

cp -r $casePath/CFD/postProcessing/probes/0 $casePath/Result/CFD_sample
cp -r $casePath/CFD/VTK $casePath/Result/VTK
cp -r $casePath/DEM/vtk_file $casePath/Result/VTK

cd $casePath/Result/VTK


