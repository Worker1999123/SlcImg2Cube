#!/bin/bash
#create folders of io
#Structure:
#io
#├── 0_Curves
#├── 0_Dcm
#├── 0_Img
#├── 1_SlcFolder
#├── 2_OffModel
#├── 2_StlModel
#├── 3_XyzModel
#└── 4_DataModel

echo "Creating folders of io"
mkdir -p io
mkdir -p io/0_Curves
mkdir -p io/0_Dcm
mkdir -p io/0_Img
mkdir -p io/1_SlcFolder
mkdir -p io/2_OffModel
mkdir -p io/2_StlModel
mkdir -p io/3_XyzModel
mkdir -p io/4_DataModel
echo "Folders of io created"