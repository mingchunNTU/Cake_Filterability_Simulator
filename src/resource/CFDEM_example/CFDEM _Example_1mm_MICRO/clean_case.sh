# remove the log file
rm log_DEM_initialization
rm log_CFDEM_run
rm ./DEM/log.liggghts

# remove the DEM file
rm -r ./DEM/vtk_file
mkdir ./DEM/vtk_file
rm ./DEM/liggghts.restart
rm ./DEM/liggghts.restartCFDEM


# remove the CFD file
cd ./CFD/
foamCleanTutorials
cd ../

# remove the previous result
rm -r ./Result
mkdir ./Result
