# SlcImg2Cube
This python based program developed by M5 Lab/SWC Lab demands to build 3d object from 2d images, gives serveral options for users to generate objects. It's so frustrated for the developer for keep occuring little bugs, so I decide to upload this public version.

## Setups
- Python3.10 above required
- Below are the needed python tookits. 

| Toolkit  | |
| ------------- | ------------- |
| os | tqdm | 
| random  | seaborn |
| ovito | PIL |
| numpy | OpenCV |
| pandas | scikit-image |
| pydicom | vtk |
| d3 |  |

Recommend using conda create:
```
conda create -n BzBone python=3.10
conda activate BzBone
conda install --strict-channel-priority -c https://conda.ovito.org -c conda-forge ovito=3.10.5
conda install vtk
conda install tqdm
conda install numpy
conda install pandas
conda install scikit-learn
conda install scikit-image
conda install pillow
conda install opencv
conda install -c conda-forge pydicom
conda install seaborn
```
Recommend activate excution permission to make sure code is workable.
```
chmod +x "path_to_src/off2particle"
```
Recommend copy `libOpenGL.so` & `libOpenGL.so.0` [in the source folder](/src/Particle2Cube/lib) to the lib folder of your environment e.g.`.conda/envs/BzBone/lib`

## I/O
- This program now reads .png files only. Please at least make sure that the image is 1:1 scale and binary present(only dark and light). The function processing .dcm files is under construction.
  ![]()
- For each input, the program outputs folder of slicing dcm files, a stl model, an off model, a xyz model and a data file.
## Processing Stages
### Stage 0 : Image Processing
#### Stage 0.5 : Curve/Funtion Generation
### Stage 1 : Image transfer to Dcm Folder
### Stage 2 : Dcm folder transfer to stl file
#### Stage 2.5 : stl file transfer to off file
### Stage 3 : Off2particle
### Stage 4 : xyz file Processing and tranfer to data file
