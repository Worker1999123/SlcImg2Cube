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
'''
code
'''

## I/O
- It reads .dcm/.png files. Note that the png files is processed or not, if not please use the "imgprcs" program.
- For each input, the program outputs folder of slicing dcm files, a stl model, an off model, a xyz model and a data file.
## Processing Stages
### Stage 0 : Image Processing
#### Stage 0.5 : Curve/Funtion Generation
### Stage 1 : Image transfer to Dcm Folder
### Stage 2 : Dcm folder transfer to stl file
#### Stage 2.5 : stl file transfer to off file
### Stage 3 : Off2particle
### Stage 4 : xyz file Processing and tranfer to data file
