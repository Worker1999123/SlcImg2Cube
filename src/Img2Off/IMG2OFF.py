import DCM2PNG
import PNG2SLC
import DCM23D
import STL2OFF
import os
import datetime

#Get the current working directory
wrk_dir = os.getcwd()
#Set main directory as the parent directory
mn_dir = os.path.dirname(wrk_dir)
#Set source directory as the src directory
src_dir = os.path.join(wrk_dir, 'src')

#print statements
print('Start time: ' + str(datetime.datetime.now()))
print('Working directory: ' + wrk_dir)
print('Main directory: ' + mn_dir)
print('Source directory: ' + src_dir)
print('Starting the conversion process...')

#Set the input and output directories
dcm_dir = os.path.join(mn_dir, 'data', 'dcm')
crv_dir = os.path.join(mn_dir, 'data', 'crv')
png_dir = os.path.join(mn_dir, 'data', 'png')
slc_dir = os.path.join(mn_dir, 'data', 'slc')
stl_dir = os.path.join(mn_dir, 'data', 'stl')
off_dir = os.path.join(mn_dir, 'data', 'off')

def check_csv(crv_dir):
    if os.path.exists(crv_dir):
        crv_file = None
        for root, dirs, files in os.walk(crv_dir):
            for file in files:
                if file.endswith('.csv'):
                    crv_file = os.path.join(root, file)
                    print('Curve file: ' + crv_file)
        if crv_file is None:
            print('Curve file does not exist.')
    else:
        print('Curve file does not exist.')

#Check if the directories exist, print the file number in each directory, or check the curve.csv file existence ,print the csv file name
print('Number of DICOM files: ' + str(len([name for name in os.listdir(dcm_dir) if os.path.isfile(os.path.join(dcm_dir, name))]))
check_csv(crv_dir)
print('Number of PNG files: ' + str(len([name for name in os.listdir(png_dir) if os.path.isfile(os.path.join(png_dir, name))]))
print('Number of SLC folders: ' + str(len([name for name in os.listdir(slc_dir) if os.path.isfile(os.path.join(slc_dir, name))]))
print('Number of STL files: ' + str(len([name for name in os.listdir(stl_dir) if os.path.isfile(os.path.join(stl_dir, name))]))

#Convert the DICOM files to PNG files
for root, dirs, files in os.walk(dcm_dir):
    for file in files:
        if file.endswith('.dcm'):
            dcm_file = os.path.join(root, file)
            png_file = os.path.join(png_dir, file.replace('.dcm', '.png'))
            DCM2PNG.dcm_to_png(dcm_file, png_file)

#Convert the PNG files to SLC files
for root, dirs, files in os.walk(png_dir):
    for file in files:
        if file.endswith('.png'):
            png_file = os.path.join(root, file)
            slc_file = os.path.join(slc_dir, file.replace('.png', '.slc'))
            PNG2SLC.png_to_slc(png_file, slc_file)

#Convert the SLC files to STL files
for root, dirs, files in os.walk(slc_dir):
    for file in files:
        if file.endswith('.slc'):
            slc_file = os.path.join(root, file)
            stl_file = os.path.join(stl_dir, file.replace('.slc', '.stl'))
            DCM23D.dcm_to_3d(slc_file, stl_file)

#Convert the STL files to OFF files
for root, dirs, files in os.walk(stl_dir):
    for file in files:
        if file.endswith('.stl'):
            stl_file = os.path.join(root, file)
            off_file = os.path.join(off_dir, file.replace('.stl', '.off'))
            STL2OFF.stl_to_off(stl_file, off_file)
