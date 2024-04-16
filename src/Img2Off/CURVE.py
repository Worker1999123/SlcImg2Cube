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
        y_values = np.linspace(0, 1, n+2)
        x_values = []
        for y in y_values:
            for t in np.linspace(0, 1, 100):
                y_curve = (1 - t) ** 3 * self.control_points[0][1] + 3 * t * (1 - t) ** 2 * self.control_points[1][1] \
                          + 3 * t ** 2 * (1 - t) * self.control_points[2][1] + t ** 3 * self.control_points[3][1]
                if abs(y_curve - y) < 0.01:
                    x_values.append((1 - t) ** 3 * self.control_points[0][0] + 3 * t * (1 - t) ** 2 * self.control_points[1][0] \
                                    + 3 * t ** 2 * (1 - t) * self.control_points[2][0] + t ** 3 * self.control_points[3][0])
                    break
        return x_values


#CM = [Curve_ID , [all points]] 
def read_crv(crv_file):
    df = pd.read_csv(crv_file)
    Curve_Matrix = []
    for i in range(len(df)/4):
        # csv file format: ID X Y
        Curve_ID = df['ID'][i*4]
        curve = BCurve(control_points=[[df['X'][i*4], df['Y'][i*4]], [df['X'][i*4+1], df['Y'][i*4+1]], [df['X'][i*4+2], df['Y'][i*4+2]], [df['X'][i*4+3], df['Y'][i*4+3]]],id=Curve_ID)
        pts = curve.slice(n_slices)
        Curve_Matrix.append([Curve_ID, pts])
    return Curve_Matrix