#!/bin/bash
#SBATCH --job-name="envcreate"
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
#Recomended to submit the job in SLCIMG2CUBE, or have to change the path of the file
TEST_PY="${SLURM_SUBMIT_DIR}/test.py"
O2P_SRC="${SLURM_SUBMIT_DIR}/src/OFF2Particle/src"

module load python/3.9.13-cpu

python3 -m venv BzBone
source ./Bone/BzBone/bin/activate
python3 -m pip install --upgrade pip
pip install vtk
pip install tqdm
pip install numpy
pip install pandas
pip install scikit-learn
pip install scikit-image
pip install pillow
pip install opencv-python
pip install ovito
pip install pydicom
pip install seaborn
chmod +x "${O2P_SRC}/off2particle"

#python run test.py
python3 $TEST_PY

echo
echo "============================ Messages from Goddess ============================"
echo " * Job ended at     : "date
echo "==============================================================================="
echo

# sbatch_post.sh