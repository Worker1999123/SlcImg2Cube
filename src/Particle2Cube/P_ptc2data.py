from P2Csrc import *
import os
import datetime
from tqdm import tqdm
import numpy as np
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.data import *
from ovito.pipeline import *
from ovito.vis import *
import sys

#Get the current working directory, path = D:\KL\01_Bone\3d_Gen\MayMenu\SlcImg2Cube-415update\src\Img2Off
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
print("ovito: %i.%i.%i" % ovito.version)
print('Starting the conversion process...')

#Set the input and output directories
crv_dir = os.path.join(io_dir, '0_Curves')
xyz_dir = os.path.join(io_dir, '3_XyzModel')
data_dir = os.path.join(io_dir, '4_DataModel')

print('-----------------------------------------------------')

xyz_list = []
crv_file = None
for file in os.listdir(crv_dir):
    if file.endswith('.csv') and crv_file is None:
        print('Curve file: ' +  file)
        crv_file = os.path.join(crv_dir, file)
Curve_Matrix = CURVE.read_bcrv(crv_file, 1)
for curve in Curve_Matrix:
    num = curve[0]
    num_str = str(num).zfill(5)
    item = file_base + '_Curve_' + num_str
    xyz_file = item + '.xyz'
    xyz_list.append(xyz_file)


def affine_transform(pipeline, ratio = 0.001):
    modifier = AffineTransformationModifier(
            operate_on = {'particles', 'cell'},
            transformation = [
                [ratio, 0, 0, 0],
                [0, ratio, 0, 0],
                [0, 0, ratio, 0]
        ]
    )            
    pipeline.modifiers.append(modifier)  

    transformation = np.array(pipeline.compute(0).cell[...])
    transformation[:,-1] = 0 
    modifier = AffineTransformationModifier(
            relative_mode = False,
            target_cell = transformation
    )            
    pipeline.modifiers.append(modifier)       

    return pipeline



for file in tqdm(xyz_list):
    if os.path.exists(os.path.join(xyz_dir, file)):
        print("Processing: %s" % file)
        #remove off file
        off_dir = os.path.join(io_dir, '2_OffModel')
        off_path = os.path.join(off_dir, file.replace('.xyz', '.off'))
        if os.path.exists(off_path):
            os.remove(off_path)
            print("Removed: %s" % off_path)
        else:
            print("File does not exist: %s" % off_path)

        xyz_path = os.path.join(xyz_dir, file)
        
        num_lines = sum(1 for _ in open(xyz_path)) - 2 # -2 for the first two lines

        with open(xyz_path, 'r') as f:
            lines = f.readlines()
        with open(xyz_path, 'w') as f:
            f.write(str(num_lines) + '\n')
            f.writelines(lines[1:])
        
        output_path = os.path.join(data_dir, file.replace('.xyz', '.data'))
        if os.path.exists(output_path):
            print("File exists: %s" % output_path)
            continue
        pipeline = import_file(xyz_path, columns=["Position.X", "Position.Y", "Position.Z"], sort_particles=True) 
        pipeline = affine_transform(pipeline) 
        export_file(pipeline, output_path, "lammps/data", atom_style="atomic", multiple_frames=False)

        with open(output_path, 'r') as f:
            lines = f.readlines()

        lines[5] = "-0.01 0.02 xlo xhi\n"
        lines[6] = "-0.01 0.02 ylo yhi\n"
        lines[7] = "-0.01 0.02 zlo zhi\n"

        with open(output_path, 'w') as f:
            f.writelines(lines)        

        #remove xyz file
        if os.path.exists(xyz_path):
            os.remove(xyz_path)
            print("Removed: %s" % xyz_path)
        else:
            print("File does not exist: %s" % xyz_path)
    else:
        print("File does not exist: %s" % file)


print('-----------------------------------------------------')
print('End time: ' + str(datetime.datetime.now()))
