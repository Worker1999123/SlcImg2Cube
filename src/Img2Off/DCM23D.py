import os
import vtk

# Convert a DICOM series to a 3D models
def dcm_to_3d(dcm_dir, output_path):
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(dcm_dir)
    reader.Update()

    ConstPixelSpacing = reader.GetPixelSpacing()

    threshold = vtk.vtkImageThreshold()
    threshold.SetInputConnection(reader.GetOutputPort())
    threshold.ThresholdByLower(50)
    threshold.ReplaceInOn()
    threshold.SetInValue(0) 
    threshold.ReplaceOutOn()
    threshold.SetOutValue(1) 
    threshold.Update()

    dmc = vtk.vtkDiscreteMarchingCubes()
    dmc.SetInputConnection(threshold.GetOutputPort())
    dmc.GenerateValues(1, 1, 1)
    dmc.Update()

    smoother = vtk.vtkSmoothPolyDataFilter()
    smoother.SetInputConnection(dmc.GetOutputPort())
    smoother.SetNumberOfIterations(30)
    smoother.SetRelaxationFactor(0.1)
    smoother.BoundarySmoothingOn()
    smoother.Update()

    if os.path.exists(output_path):
        os.remove(output_path)

    writer = vtk.vtkSTLWriter()
    writer.SetInputConnection(smoother.GetOutputPort())
    writer.SetFileTypeToBinary()
    writer.SetFileName(output_path)
    writer.Write()