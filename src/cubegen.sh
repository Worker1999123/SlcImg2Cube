# Get flie name from P_F1job001.sh and run cubegen.sh
FILENAME=$1 # get filename
# $1 is the first argument passed to the script
if [ -z "$FILENAME" ]; then
    echo "No filename provided"
    exit 1
fi
SUBMIT_DIR=$2 # get io_dir
# $2 is the second argument passed to the script
if [ -z "$SUBMIT_DIR" ]; then
    echo "No io_dir provided"
    exit 1
fi
IO_DIR=$3 # get io_dir
# $3 is the third argument passed to the script
if [ -z "$IO_DIR" ]; then
    echo "No io_dir provided"
    exit 1
fi

SRC_DIR="${SUBMIT_DIR}/src"
PYTHON_EXEC="python"
SLC2CUBE_EXEC="${SRC_DIR}/Img2Off/P_IMG2OFF.py"
OFF2Particle_EXEC="${SRC_DIR}/OFF2Particle/P_run_off2particle.sh"
PTC2DATA_EXEC="${SRC_DIR}/Particle2Cube/P_ptc2data.py"

# # edit mn_dir in Img2Off = Submit_dir 
# sed -i "s|mn_dir = .*|mn_dir = \"${SUBMIT_DIR}\"|g" ${SLC2CUBE_EXEC}

# # edit mn_dir in Particle2Cube = Submit_dir
# sed -i "s|mn_dir = .*|mn_dir = \"${SUBMIT_DIR}\"|g" ${PTC2DATA_EXEC}

# # edit mn_dir in OFF2Particle.sh = Submit_dir
# sed -i "s|mn_dir=".*"|mn_dir=\"${SUBMIT_DIR}\"|g" ${OFF2Particle_EXEC}

# # edit and output SLC2CUBE_EXEC+JOB_NUM, OFF2Particle_EXEC+JOB_NUM, PTC2DATA_EXEC+JOB_NUM, change io_dir to io_dir+JOB_NUM
# N_SLC2CUBE_EXEC="${SLC2CUBE_EXEC%.*}${JOB_NUM}${SLC2CUBE_EXEC##*.}" 
# N_OFF2Particle_EXEC="${OFF2Particle_EXEC%.*}${JOB_NUM}${OFF2Particle_EXEC##*.}"
# N_PTC2DATA_EXEC="${PTC2DATA_EXEC%.*}${JOB_NUM}${PTC2DATA_EXEC##*.}"

# sed "s|io_dir = .*|io_dir = \"${IO_DIR}\"|g" ${SLC2CUBE_EXEC} > ${N_SLC2CUBE_EXEC}
# Run slc2cube /not mpirun use python3
$PYTHON_EXEC $N_SLC2CUBE_EXEC $FILENAME $SUBMIT_DIR $IO_DIR
# Remove new slc2cube
# rm $N_SLC2CUBE_EXEC

# sed "s|IO_DIR=.*|IO_DIR=\"${IO_DIR}\"|g" ${OFF2Particle_EXEC} > ${N_OFF2Particle_EXEC}
# excute off2particle.sh
sh $N_OFF2Particle_EXEC $FILENAME $SUBMIT_DIR $IO_DIR
# Remove new off2particle
# rm $N_OFF2Particle_EXEC

# sed "s|io_dir = .*|io_dir = \"${IO_DIR}\"|g" ${PTC2DATA_EXEC} > ${N_PTC2DATA_EXEC}
# Run ptc2data
$PYTHON_EXEC $N_PTC2DATA_EXEC $FILENAME $SUBMIT_DIR $IO_DIR
# Remove new ptc2data
# rm $N_PTC2DATA_EXEC
