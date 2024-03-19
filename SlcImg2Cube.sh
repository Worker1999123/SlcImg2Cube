#!/bin/bash

echo "Your bash version : $BASH_VERSION"  
DATE_FORMAT=`date +%Y-%m-%d` 
TIME_FORMAT=`date +%T` 
echo "Today is $DATE_FORMAT and now time is $TIME_FORMAT"

rm ${DATE_FORMAT}_generate_particles.log
# {
for model_name in $PWD/mesh_off_model/*; do
	echo "${model_name}"
	rootname=$(basename $model_name .off)
	outputname="${rootname}.xyz"

	OFF2Particle/src/off2particle ${model_name} 0.2 ${outputname}
	
	mv ${outputname} particle_xyz_model/${outputname}
done
# } | tee ${DATE_FORMAT}_generate_particles.log

# end
echo ""
echo "All done"
DATE_FORMAT=`date +%Y-%m-%d` 
TIME_FORMAT=`date +%T` 
echo "Today is $DATE_FORMAT and now time is $TIME_FORMAT"

