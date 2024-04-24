#!/bin/bash
#SBATCH --account=MST108404
#SBATCH --job-name="BzBone00"
#SBATCH --partition=trans
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --gres=gpu:0
#SBATCH --time=3-0:00:00
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

module purge
module load gcc/11.4.0
module load miniconda3/24.1.2
module load lammps
conda activate BzBone

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

# edit mn_dir in OFF2Particle.sh = Submit_dir
sed -i "s|mn_dir=".*"|mn_dir=\"${SUBMIT_DIR}\"|g" ${OFF2Particle_EXEC}

# Run slc2cube /not mpirun use python3
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
