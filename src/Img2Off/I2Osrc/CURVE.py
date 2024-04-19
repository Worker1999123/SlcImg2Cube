import pandas as pd
import numpy as np
n_slices = 101

class BCurve:
    def __init__(self, n=4, control_points=None, bezier_curve=None,id=None):
        self.n = n
        self.control_points = control_points
        self.bezier_curve = bezier_curve
        self.id = id
    def slice(self, n):
        y_values = np.linspace(0, 1, n)
        x_values = []
        x_values.append(0.0)
        for y in y_values:
            x_value = (1 - y) ** 3 * self.control_points[0][0] + 3 * y * (1 - y) ** 2 * self.control_points[1][0] \
                        + 3 * y ** 2 * (1 - y) * self.control_points[2][0] + y ** 3 * self.control_points[3][0]
            x_values.append(x_value)
        x_values.append(0.0)
        return x_values


#CM = [Curve_ID , [all points]] 
def read_crv(crv_file):
    df = pd.read_csv(crv_file)
    Curve_Matrix = []
    for i in range(int(len(df)/4)):
        # csv file format: ID X Y
        Curve_ID = df['ID'][i*4]
        curve = BCurve(control_points=[[df['X'][i*4], df['Y'][i*4]], [df['X'][i*4+1], df['Y'][i*4+1]], [df['X'][i*4+2], df['Y'][i*4+2]], [df['X'][i*4+3], df['Y'][i*4+3]]],id=Curve_ID)
        pts = curve.slice(n_slices)
        Curve_Matrix.append([Curve_ID, pts])
    return Curve_Matrix