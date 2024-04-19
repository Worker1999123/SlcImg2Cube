#!/bin/bash

echo "Your bash version : $BASH_VERSION"  
DATE_FORMAT=`date +%Y-%m-%d` 
TIME_FORMAT=`date +%T` 
echo "Today is $DATE_FORMAT and now time is $TIME_FORMAT"

SUBMIT_DIR="${PWD}"
IO_DIR="${SUBMIT_DIR}/io"
SRC_DIR="${SUBMIT_DIR}/src"

PYTHON_EXEC="python3"
SLC2CUBE_EXEC="${SRC_DIR}/Img2Off/IMG2OFF.py"
OFF2Particle_EXEC="${SRC_DIR}/OFF2Particle/run_off2particle.sh"
PTC2DATA_EXEC="${SRC_DIR}/Particle2Cube/ptc2data.py"

# edit mn_dir in Img2Off = Submit_dir 
sed -i "s|mn_dir = .*|mn_dir = \"${SUBMIT_DIR}\"|g" ${SLC2CUBE_EXEC}

# edit mn_dir in Particle2Cube = Submit_dir
sed -i "s|mn_dir = .*|mn_dir = \"${SUBMIT_DIR}\"|g" ${PTC2DATA_EXEC}

# edit MAIN_DIR in OFF2Particle = Submit_dir
sed -i "s|MAIN_DIR = .*|MAIN_DIR = \"${SUBMIT_DIR}\"|g" ${OFF2Particle_EXEC}

# Run slc2cube
mpirun $PYTHON_EXEC $SLC2CUBE_EXEC

# excute off2particle.sh
OFF2Particle_EXEC

# Run ptc2data
mpirun $PYTHON_EXEC $PTC2DATA_EXEC
# end
echo ""
echo "All done"
DATE_FORMAT=`date +%Y-%m-%d` 
TIME_FORMAT=`date +%T` 
echo "Today is $DATE_FORMAT and now time is $TIME_FORMAT"

