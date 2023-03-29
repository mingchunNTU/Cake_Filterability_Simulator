#!/bin/bash

# remove all the old files
/bin/bash script/clean_case.sh

#- define variables
casePath="$(dirname "$(readlink -f ${BASH_SOURCE[0]})")"

# execute LIGGGHTS program
/bin/bash $casePath/script/parDEMrun.sh

# remove the residual files
rm script/log_DEM_simulation
rm log.liggghts

# postProcessing

/bin/bash script/postProcessing.sh



