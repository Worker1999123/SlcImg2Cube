import DCM2PNG
import PNG2SLC
import DCM23D
import STL2OFF
import CURVE
import os
import datetime

#Get the current working directory
wrk_dir = os.getcwd()
#Set main directory as the parent directory
mn_dir = os.path.dirname(wrk_dir)
#Set source directory as the src directory
src_dir = os.path.join(wrk_dir, 'src')
#Set IO directories
io_dir = os.path.join(mn_dir, 'io')

#print statements
print('Start time: ' + str(datetime.datetime.now()))
print('Working directory: ' + wrk_dir)
print('Main directory: ' + mn_dir)
print('Source directory: ' + src_dir)
print('Input/Output directory: ' + io_dir)
print('Starting the conversion process...')

#Set the input and output directories
dcm_dir = os.path.join(io_dir, '0_Dcm')
crv_dir = os.path.join(io_dir, '0_Curve')
png_dir = os.path.join(io_dir, '0_Img')
slc_dir = os.path.join(io_dir, '1_SlcFolder')
stl_dir = os.path.join(io_dir, '2_StlModel')
off_dir = os.path.join(io_dir, '3_OffModel')

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
            return False
        else:
            return True
    else:
        print('Curve file does not exist.')
        return False

#Check if the directories exist, print the file number in each directory, or check the curve.csv file existence ,print the csv file name
print('Number of DICOM files: ' + str(len([name for name in os.listdir(dcm_dir) if os.path.isfile(os.path.join(dcm_dir, name))]))
CSV_exst = check_csv(crv_dir)
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

#Define basic variables
margin_range = 2
# pixel_spacing = 0.35
image_size = 104
pixel_spacing = 10/(image_size-margin_range*2)
n_slices = 101
start_pos = pixel_spacing
end_pos = pixel_spacing*image_size-(margin_range*2)*pixel_spacing+pixel_spacing
all_pos = np.linspace(start_pos, end_pos, n_slices)
thickness = (end_pos-start_pos)/(n_slices)
all_pos = np.append(0, all_pos)
all_pos = np.append(all_pos, end_pos+thickness)


#read the curve.csv file and create slice shift and rotation angle matrix
#CM = [Curve_ID , [all points]] 
Curve_Matrix = CURVE.read_crv(crv_file)

refer_dcm_file = src_dir + '/refer.dcm'

#Convert the PNG files to SLC files
for file in os.listdir(png_dir):
    if file.endswith('.png'):
        png_file = os.path.join(png_dir, file)
        for curve in Curve_Matrix:
            num = curve[0]
            pts = curve[1]
            slc_folder = os.path.join(slc_dir, file.replace('.png', '') + '_Curve_' + curve[0])
            os.makedirs(slc_folder, exist_ok=True)
            for i, pos, pt in zip(range(n_slices), all_pos, pts):
                img_shifted = PNG2SLC.image_x_shift(PNG2SLC.read_png(png_file), shift_ratio=pt[0], crop_ratio=1)
                img_shifted = PNG2SLC.add_margin(img_shifted, margin_range)
                if i == 0 or i == len(all_pos)-1:
                    img_shifted = np.zeros_like(img_shifted)
                
                #curve ID is 5 digits
                num_str = str(num).zfill(5)
                dcm_path = os.path.join(slc_folder, 'Curve_' + num_str + '_Slice_' + str(i) + '.dcm')
                PNG2SLC.png_to_slc(refer_dcm_file, image=png_file, pixel_spacing, num, pos, thickness, output_path=dcm_path)

#Convert the SLC files to STL files
for folder in os.listdir(slc_dir):
    if os.path.isdir(os.path.join(slc_dir, folder)):
        slc_folder = os.path.join(slc_dir, folder)
        stl_file = os.path.join(stl_dir, folder + '.stl')
        off_file = os.path.join(off_dir, folder + '.off')
        DCM23D.dcm_to_3d(slc_folder, stl_file)
        STL2OFF.STLtoOFF(stl_file, off_file)


