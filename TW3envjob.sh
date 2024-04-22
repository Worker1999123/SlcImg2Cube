#!/bin/bash
#SBATCH --account=MST108404
#SBATCH --job-name="create_env"
#SBATCH --partition=ct56
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --gres=gpu:0
#SBATCH --time=0-0:30
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

TEST_PY="${SLURM_SUBMIT_DIR}/test.py"

module purge
module load rcec/ncl/6.6.2-gcc11
module load miniconda3/22.11.1-6zzs5sq
module load lammps/pkg/vtk/9.1.0

conda create -n BzBone python=3.8.10
source ~/.bashrc
python3 -m pip install --upgrade pip
pip install vtk torchvision torchsummary tqdm matplotlib numpy pandas scikit-learn scikit-image pillow opencv-python ovito pydicom seaborn

#python run test.py
python3 $TEST_PY

echo
echo "============================ Messages from Goddess ============================"
echo " * Job ended at     : "date
echo "==============================================================================="
echo

# sbatch_post.sh