#!/bin/bash
#SBATCH --account=MST113132
#SBATCH --job-name="BzBone001"
#SBATCH --partition=ct448
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=100
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:0
#SBATCH --time=4-0:00:00
#SBATCH --output=cout%x-%j.txt
#SBATCH --error=cerr%x-%j.txt

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
module load tools/miniconda3
conda activate BzBone

JOB_NUM="001"
WORK_DIR="/work1/u9132064/Bone"
SUBMIT_DIR="${SLURM_SUBMIT_DIR}"
IO_DIR="${WORK_DIR}/io${JOB_NUM}"
SRC_DIR="${SUBMIT_DIR}/src"

for FILE in ${IO_DIR}/0_Img/*.png; do
    echo "Processing $FILE"
    FILENAME=$(basename $FILE) # get filename
    FILENAME=${FILENAME%.*} # remove extension
    echo "Filename: $FILENAME"
    sh ${SRC_DIR}/cubegen.sh $FILENAME $SUBMIT_DIR $IO_DIR & # run in background
done

wait

echo
echo "============================ Messages from Goddess ============================"
echo " * Job ended at     : "date
echo "==============================================================================="
echo

# sbatch_post.sh
