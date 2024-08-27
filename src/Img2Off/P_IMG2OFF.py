# next upgrade: 
# 1. add the module of CHECK in I2Osrc to simplify the code
from I2Osrc import DCM2PNG
from I2Osrc import PNG2SLC
from I2Osrc import CURVE
from I2Osrc import DCM23D
from I2Osrc import STL2OFF
import os
import datetime
import numpy as np
from tqdm import tqdm
import sys

#Get the current working directory, path = D:\KL\01_Bone\3d_Gen\MayMenu\SlcImg2Cube-415update\src\Img2Off
# get mn_dir from shell command line argument 1
if len(sys.argv) < 4:
    print('Usage: python P_IMG2OFF.py <main_dir> <file_name> <io_dir>')
    sys.exit(1)
mn_dir = sys.argv[2] 
src_dir = os.path.join(mn_dir, 'src')
wrk_dir = os.path.join(src_dir, 'Img2Off')
io_dir = sys.argv[3] 
file_base = sys.argv[1] 

print('-----------------------------------------------------')
#print statements
print('Start time: ' + str(datetime.datetime.now()))

print('-----------------------------------------------------')
print('Working directory: ' + wrk_dir)
print('Main directory: ' + mn_dir)
print('Source directory: ' + src_dir)
print('Input/Output directory: ' + io_dir)
print('Starting the conversion process...')

#Set the input and output directories
dcm_dir = os.path.join(io_dir, '0_Dcm')
crv_dir = os.path.join(io_dir, '0_Curves')
png_dir = os.path.join(io_dir, '0_Img')
slc_dir = os.path.join(io_dir, '1_SlcFolder')
if not os.path.exists(slc_dir):
    os.makedirs(slc_dir)
stl_dir = os.path.join(io_dir, '2_StlModel')
if not os.path.exists(stl_dir):
    os.makedirs(stl_dir)
off_dir = os.path.join(io_dir, '2_OffModel')
if not os.path.exists(off_dir):
    os.makedirs(off_dir)
xyz_dir = os.path.join(io_dir, '3_XyzModel')
if not os.path.exists(xyz_dir):
    os.makedirs(xyz_dir)
data_dir = os.path.join(io_dir, '4_DataModel')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
print('-----------------------------------------------------')

crv_file = None
for file in os.listdir(crv_dir):
    if file.endswith('.csv') and crv_file is None:
        print('Curve file: ' +  file)
        crv_file = os.path.join(crv_dir, file)

print('Converting PNG files to SLC files...')
cube_size = 10
#Define basic variables
margin_range = 2
# pixel_spacing = 0.35
image_size = 106
pixel_spacing = cube_size/(image_size-margin_range*2)
n_slices = 102
start_pos = pixel_spacing
thickness = cube_size/(n_slices-2)
end_pos = start_pos + cube_size + pixel_spacing * 2
all_pos = np.linspace(start_pos, end_pos, n_slices)
all_pos = np.append(0.0, all_pos)
all_pos = np.append(all_pos, end_pos+pixel_spacing)


#read the curve.csv file and create slice shift and rotation angle matrix
#CM = [Curve_ID , [all points]] 
Curve_Matrix = CURVE.read_bcrv(crv_file, n_slices)
#print(Curve_Matrix)

#'refer.dcm' is under src_dir
refer_dcm_file = os.path.join(src_dir, 'refer.dcm')

file_name = file_base + '.png'
png_file = os.path.join(png_dir, file_name)
img = PNG2SLC.read_png(png_file)
slice_list = []
for curve in tqdm(Curve_Matrix):
    num = curve[0]
    num_str = str(num).zfill(5)
    pts = curve[1]
    item = file_base + '_Curve_' + num_str
    slc_folder = os.path.join(slc_dir, item)
    os.makedirs(slc_folder, exist_ok=True)
    slice_list.append((num_str, item, slc_folder))
    for i, pos, pt in zip(range(len(all_pos)), all_pos, pts):
        img_shifted = PNG2SLC.image_x_shift(img, shift_ratio=pt)
        img_shifted = PNG2SLC.add_margin(img_shifted, margin_range)
        if i == 0 or i == n_slices+1:
            img_shifted = np.zeros_like(img_shifted)

        dcm_path = os.path.join(slc_folder , item + '_Slice_' + str(i).zfill(3) + '.dcm')
        PNG2SLC.png_to_slc(refer_dcm_file, image=img_shifted, pixel_spacing=pixel_spacing, num=num, pos=pos, thickness=thickness, output_path=dcm_path)          


print('-----------------------------------------------------')

stl_list = []
for folder in tqdm(slice_list):
    # print('Converting ' + folder + '...')
    slc_folder = folder[2]
    print('Converting ' + slc_folder + '...')
    stl_file = os.path.join(stl_dir, folder[1] + '.stl')
    stl_list.append((folder[1], stl_file))
    if not os.path.exists(stl_file):
        DCM23D.dcm_to_3d(slc_folder, stl_file)
        print('STL file is created: ' + stl_file)
    else:
        print('STL file already exists: ' + stl_file)
    #remove the SLC folder
    os.removedirs(slc_folder)
    print('SLC folder is removed: ' + slc_folder)



print('-----------------------------------------------------')
#-----------------------------------------------------

for file in tqdm(stl_list):
    stl_file = file[1]
    off_file = os.path.join(off_dir, file[0] + '.off')
    print('Converting ' + stl_file + '...')
    if not os.path.exists(off_file):
        STL2OFF.STLtoOFF(stl_file, off_file)
        print('OFF file is created: ' + off_file)
    else:
        print('OFF file already exists: ' + off_file)
    #remove the STL file
    os.remove(stl_file)

#-----------------------------------------------------
print('-----------------------------------------------------')
print('End time: ' + str(datetime.datetime.now()))
print('Conversion process is completed.')
