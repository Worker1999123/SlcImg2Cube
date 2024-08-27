#!/bin/bash
FILENAME=$1
mn_dir=$2
IO_DIR=$3
OFF2Particle_EXEC="${mn_dir}/src/OFF2Particle/src/off2particle"

echo "Your bash version : $BASH_VERSION"  
DATE_FORMAT=`date +%Y-%m-%d` 
TIME_FORMAT=`date +%T` 
echo "Today is $DATE_FORMAT and now time is $TIME_FORMAT"

mod_dir="${IO_DIR}/2_OffModel"
for model_name in ${mod_dir}/${FILENAME}*.off;
do
	echo "${model_name}"
	rootname=$(basename $model_name .off)
	outputname="${rootname}.xyz"
	if [ -f ${IO_DIR}/3_XyzModel/${outputname} ]; then
		echo "File ${outputname} already exists"
		continue
	fi

	$OFF2Particle_EXEC ${model_name} 0.2 ${outputname}
	
	mv ${outputname} ${IO_DIR}/3_XyzModel/${outputname}
done

# end
echo ""
echo "All done"
DATE_FORMAT=`date +%Y-%m-%d` 
TIME_FORMAT=`date +%T` 
echo "Today is $DATE_FORMAT and now time is $TIME_FORMAT"

