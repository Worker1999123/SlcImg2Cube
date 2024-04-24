import datetime
import numpy as np
import ovito
import PIL
import pandas as pd
import seaborn as sns
import sklearn
import vtk
import pydicom
import cv2
import skimage
import scipy

print('-----------------------------------------------------')
print('Start time: ' + str(datetime.datetime.now()))
print('-----------------------------------------------------')
print('Environment setup...')
#Print the version of the packages
print("ovito: %i.%i.%i" % ovito.version)
print("PIL: %s" % PIL.__version__)
print("pandas: %s" % pd.__version__)
print("seaborn: %s" % sns.__version__)
print("sklearn: %s" % sklearn.__version__)
print("vtk: %s" % vtk.__version__)
print("pydicom: %s" % pydicom.__version__)
print("cv2: %s" % cv2.__version__)
print("skimage: %s" % skimage.__version__)
print("scipy: %s" % scipy.__version__)
print("numpy: %s" % np.__version__)
print('-----------------------------------------------------')
print('Environment setup complete.')
print('End time: ' + str(datetime.datetime.now()))
print('-----------------------------------------------------')