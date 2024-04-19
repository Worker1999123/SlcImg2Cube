#!/bin/bash

# MAIN_DIR="/home/u9132064/Bone/SlcImg2Cube"
MAIN_DIR="/home/u9132064/Bone/SlcImg2Cube"
IO_DIR="${MAIN_DIR}/io"
OFF2Particle_EXEC = "${MAIN_DIR}/src/OFF2Particle/src/off2particle"

echo "Your bash version : $BASH_VERSION"  
DATE_FORMAT=`date +%Y-%m-%d` 
TIME_FORMAT=`date +%T` 
echo "Today is $DATE_FORMAT and now time is $TIME_FORMAT"

rm ${DATE_FORMAT}_generate_particles.log
# {
for model_name in ${IO_DIR}/2_OffModel/*; do
	echo "${model_name}"
	rootname=$(basename $model_name .off)
	outputname="${rootname}.xyz"

	OFF2Particle_EXEC ${model_name} 0.2 ${outputname}
	
	mv ${outputname} ${IO_DIR}/3_XyzModel/${outputname}
done
# } | tee ${DATE_FORMAT}_generate_particles.log

# end
echo ""
echo "All done"
DATE_FORMAT=`date +%Y-%m-%d` 
TIME_FORMAT=`date +%T` 
echo "Today is $DATE_FORMAT and now time is $TIME_FORMAT"

