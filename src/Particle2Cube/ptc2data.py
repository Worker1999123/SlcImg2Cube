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
print("ovito: %i.%i.%i" % ovito.version)
print('Starting the conversion process...')

#Set the input and output directories
xyz_dir = os.path.join(io_dir, '3_XyzModel')
data_dir = os.path.join(io_dir, '4_DataModel')

print('-----------------------------------------------------')
#Check if the directories exist, print the file number in each directory, or check the curve.csv file existence ,print the csv file name
xyz_num = len([name for name in os.listdir(xyz_dir) if name.endswith('.xyz')])
print('Number of XYZ files: ' + str(xyz_num))
data_num = len([name for name in os.listdir(data_dir) if name.endswith('.data')])
print('Number of DATA files: ' + str(data_num))

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



for file in tqdm(os.listdir(xyz_dir)):
    if file.endswith('.xyz'):
        print("Processing: %s" % file)
        xyz_path = os.path.join(xyz_dir, file)
        
        num_lines = sum(1 for _ in open(xyz_path)) - 2

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

print('-----------------------------------------------------')
print('End time: ' + str(datetime.datetime.now()))
