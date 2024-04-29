from I2Osrc import DCM2PNG
from I2Osrc import PNG2SLC
from I2Osrc import CURVE
from I2Osrc import DCM23D
from I2Osrc import STL2OFF
import os
import datetime
import numpy as np
from tqdm import tqdm

#Get the current working directory, path = D:\KL\01_Bone\3d_Gen\MayMenu\SlcImg2Cube-415update\src\Img2Off
mn_dir = "/mnt/c/Users/allen/Desktop/Results/SLC2CUBE"
src_dir = os.path.join(mn_dir, 'src')
wrk_dir = os.path.join(src_dir, 'Img2Off')
io_dir = os.path.join(mn_dir, 'io')

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

def check_csv(crv_dir):
    if os.path.exists(crv_dir):
        crv_file = None
        for file in os.listdir(crv_dir):
            if file.endswith('.csv'):
                crv_file = os.path.join(crv_dir, file)
                print('Curve file: ' +  file)
                break
        if crv_file is None:
            print('Curve file does not exist.')
            return False, None
        else:
            return True, crv_file
    else:
        print('Curve file does not exist.')
        return False, None

print('-----------------------------------------------------')
#Check if the directories exist, print the file number in each directory, or check the curve.csv file existence ,print the csv file name
if os.path.exists(dcm_dir):
    dcm_num = len([name for name in os.listdir(dcm_dir) if name.endswith('.dcm')])
    print('Number of DICOM files: ' + str(dcm_num))
else:
    dcm_num = 0
    print('No DICOM files found in the directory: ' + dcm_dir)
    
CSV_exst,crv_file = check_csv(crv_dir)
png_num = len([name for name in os.listdir(png_dir) if name.endswith('.png')])
print('Number of PNG files: ' + str(png_num))
slc_num = len([name for name in os.listdir(slc_dir) if os.path.isdir(os.path.join(slc_dir, name))])
print('Number of SLC folders: ' + str(slc_num))
stl_num = len([name for name in os.listdir(stl_dir) if name.endswith('.stl')])
print('Number of STL files: ' + str(stl_num))
print('-----------------------------------------------------')
#-----------------------------------------------------
if dcm_num == 0:
    print('No DICOM files found in the directory: ' + dcm_dir)
else:
    print('Converting DICOM files to PNG files...')
    #Convert the DICOM files to PNG files
    for file in tqdm(os.listdir(dcm_dir)):
        if file.endswith('.dcm'):
            dcm_file = os.path.join(dcm_dir, file)
            png_file = os.path.join(png_dir, file.replace('.dcm', '.png'))
            DCM2PNG.dcm_to_png(dcm_file, png_file)
print('-----------------------------------------------------')
#-----------------------------------------------------
png_num = len([name for name in os.listdir(png_dir) if name.endswith('.png')])
start_time = datetime.datetime.now()
if CSV_exst == False:
    print('No CSV file found in the directory: ' + crv_dir)
elif png_num == 0:
    print('No PNG files found in the directory: ' + png_dir)
else:
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

    #Convert the PNG files to SLC files
    for file in os.listdir(png_dir):
        if file.endswith('.png'):
            png_file = os.path.join(png_dir, file)
            img = PNG2SLC.read_png(png_file)
            for curve in tqdm(Curve_Matrix):
                num = curve[0]
                num_str = str(num).zfill(5)
                pts = curve[1]
                slc_folder = os.path.join(slc_dir, file.replace('.png', '') + '_Curve_' + num_str)
                os.makedirs(slc_folder, exist_ok=True)
                for i, pos, pt in zip(range(len(all_pos)), all_pos, pts):
                    img_shifted = PNG2SLC.image_x_shift(img, shift_ratio=pt)
                    img_shifted = PNG2SLC.add_margin(img_shifted, margin_range)
                    if i == 0 or i == n_slices+1:
                        img_shifted = np.zeros_like(img_shifted)

                    dcm_path = os.path.join(slc_folder, 'Curve_' + num_str + '_Slice_' + str(i) + '.dcm')
                    PNG2SLC.png_to_slc(refer_dcm_file, image=img_shifted, pixel_spacing=pixel_spacing, num=num, pos=pos, thickness=thickness, output_path=dcm_path)          


print('-----------------------------------------------------')
#-----------------------------------------------------
slc_num = len([name for name in os.listdir(slc_dir) if os.path.isdir(os.path.join(slc_dir, name))])
if slc_num == 0:
    print('No SLC folders found in the directory: ' + slc_dir)
else:
    #Convert the SLC files to STL files
    for folder in tqdm(os.listdir(slc_dir)):
        # print('Converting ' + folder + '...')
        if os.path.isdir(os.path.join(slc_dir, folder)):
            slc_folder = os.path.join(slc_dir, folder)
            print('Converting ' + slc_folder + '...')
            stl_file = os.path.join(stl_dir, folder + '.stl')
            if not os.path.exists(stl_file):
                DCM23D.dcm_to_3d(slc_folder, stl_file)
                print('STL file is created: ' + stl_file)
            else:
                print('STL file already exists: ' + stl_file)
            #remove the SLC folder
            os.system('rm -r ' + slc_folder)
            print('SLC folder is removed: ' + slc_folder)



print('-----------------------------------------------------')
#-----------------------------------------------------
stl_num = len([name for name in os.listdir(stl_dir) if name.endswith('.stl')])
if stl_num == 0:
    print('No STL files found in the directory: ' + stl_dir)
else:
    #Convert the STL files to OFF files
    for file in tqdm(os.listdir(stl_dir)):
        if file.endswith('.stl'):
            stl_file = os.path.join(stl_dir, file)
            off_file = os.path.join(off_dir, file.replace('.stl', '.off'))
            print('Converting ' + stl_file + '...')
            if not os.path.exists(off_file):
                STL2OFF.STLtoOFF(stl_file, off_file)
                print('OFF file is created: ' + off_file)
            else:
                print('OFF file already exists: ' + off_file)
            #remove the STL file
            os.system('rm ' + stl_file)
            print('STL file is removed: ' + stl_file)

#-----------------------------------------------------
print('-----------------------------------------------------')
print('End time: ' + str(datetime.datetime.now()))
print('Conversion process is completed.')
