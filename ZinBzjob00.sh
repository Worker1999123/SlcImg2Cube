#!/bin/bash
#SBATCH --job-name="BzBone00"
#SBATCH --partition=cpu-3g
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --gres=gpu:0
#SBATCH --time=1-00:00
#SBATCH --output=cout.txt
#SBATCH --error=cerr.txt

# sbatch_pre.sh

echo
echo "============================ Messages from Goddess ============================"
echo " * Job starting from: "date
echo " * Job ID           : "$SLURM_JOBID
echo " * Job name         : "$SLURM_JOB_NAME
echo " * Job partition    : "$SLURM_JOB_PARTITION
echo " * Nodes            : "$SLURM_JOB_NUM_NODES
echo " * Cores            : "$SLURM_NTASKS
echo " * Working directory: "${SLURM_SUBMIT_DIR/$HOME/"~"}
echo "==============================================================================="
echo

module load opt gcc mpi lammps/mpi
module load python/3.9.13-cpu

source ~/Bone/BzBone/bin/activate

SUBMIT_DIR="${SLURM_SUBMIT_DIR}"
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
sed -i "s|mn_dir=".*"|mn_dir=\"${SUBMIT_DIR}\"|g" ${OFF2Particle_EXEC}

# Run slc2cube
$PYTHON_EXEC $SLC2CUBE_EXEC

# excute off2particle.sh
sh $OFF2Particle_EXEC

# Run ptc2data
$PYTHON_EXEC $PTC2DATA_EXEC

echo
echo "============================ Messages from Goddess ============================"
echo " * Job ended at     : "date
echo "==============================================================================="
echo


# sbatch_post.sh