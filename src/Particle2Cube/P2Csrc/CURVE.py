import pandas as pd
import numpy as np
import os
n_slices = 101

class BCurve:
    def __init__(self, n=4, control_points=None, bezier_curve=None,id=None):
        self.n = n
        self.control_points = control_points
        self.bezier_curve = bezier_curve
        self.id = id
    def slice(self, n, linear=True):
        if self.bezier_curve is None:
            self.parameterize_curve()
        bc = self.bezier_curve
        x_values = []
        if linear:
            y_values = np.linspace(0, 1, n+2)
            #doing interpolation for the closest y points to find the x points
            for y in y_values:
                if y == 0 or y == 1:
                    x = bc[0][0] if y == 0 else bc[0][-1]
                    x_values.append(x)
                    continue
                for i in range(len(bc[1])):
                    if bc[1][i] <= y <= bc[1][i+1]:
                        x = bc[0][i] + (bc[0][i+1] - bc[0][i]) * (y - bc[1][i]) / (bc[1][i+1] - bc[1][i])
                        x_values.append(x)
                        break
        else:
        #the other way to get x points by using t=linspace(0,1,n+2) to get x points
            length = len(bc[0])
            for i in range(n+2):
                if i == 0 or i == n+1:
                    x= bc[0][0] if i == 0 else bc[0][-1]
                    x_values.append(x)
                else:
                    t_lb = int(i/(n+1))
                    t_ub = t_lb + 1
                    #doing interpolation for the closest t points to find the x points
                    x = bc[0][t_lb] + (bc[0][t_ub] - bc[0][t_lb]) * (i - t_lb) / (t_ub - t_lb)
                    x_values.append(x)

        return x_values
    def parameterize_curve(self):
        if self.control_points is None:
            self.generate_control_points()

        # Parameterize the bezier curve
        t = np.linspace(0, 1, 500)
        bezier_curve = np.array([(1 - t) ** 3 * self.control_points[0][0] + 3 * t * (1 - t) ** 2 * self.control_points[1][0]
                                 + 3 * t ** 2 * (1 - t) * self.control_points[2][0] + t ** 3 * self.control_points[3][0],
                                 (1 - t) ** 3 * self.control_points[0][1] + 3 * t * (1 - t) ** 2 * self.control_points[1][1]
                                 + 3 * t ** 2 * (1 - t) * self.control_points[2][1] + t ** 3 * self.control_points[3][1]])

        self.bezier_curve = bezier_curve

#old version
#CM = [Curve_ID , [all points]] 
def read_crv(crv_file, n_slices=101):
    df = pd.read_csv(crv_file)
    Curve_Matrix = []
    for i in range(int(len(df)/4)):
        # csv file format: ID X Y
        Curve_ID = df['ID'][i*4]
        curve = BCurve(control_points=[[df['X'][i*4], df['Y'][i*4]], [df['X'][i*4+1], df['Y'][i*4+1]], [df['X'][i*4+2], df['Y'][i*4+2]], [df['X'][i*4+3], df['Y'][i*4+3]]],id=Curve_ID)
        pts = curve.slice(n_slices)
        Curve_Matrix.append([Curve_ID, pts])
    return Curve_Matrix

#new version
def read_bcrv(bcrv_file, n_slices=101):
    df = pd.read_csv(bcrv_file)
    Curve_Matrix = []
    for i in range(len(df)):
        # csv file format: ID Order X1 Y1 X2 Y2 ... Xn Yn
        Curve_ID = df['ID'][i]
        Curve_Order = df['Order'][i]
        control_points = []
        for j in range(Curve_Order):
            control_points.append([df['X'+str(j+1)][i], df['Y'+str(j+1)][i]])
        curve = BCurve(n=Curve_Order, control_points=control_points, id=Curve_ID)
        pts = curve.slice(n_slices)
        Curve_Matrix.append([Curve_ID, pts])
    return Curve_Matrix

def random_bcrv_csv(n, order, filename='bcurve001.csv', dislocation=0, path='SLCIMG2CUBE/io/0_Curves/'):
    table =[]
    #generate n random bezier curve control points
    # x1,y1 = 0,0 , xn,yn = dislocation,1 , else x = random(1~-1), y = sort(random(0~1)),y1~yn have to be sorted from small to large
    # csv file format: ID Order X1 Y1 X2 Y2 ... Xn Yn
    for i in range(n):
        control_points = [[0, 0]]
        for j in range(order-2):
            control_points.append([np.random.uniform(-1, 1), np.random.uniform(0, 1)])
        control_points.append([dislocation, 1])
        control_points.sort(key=lambda x: x[1])
        row = [i+1, order]
        for j in range(order):
            row.append(control_points[j][0])
            row.append(control_points[j][1])
        table.append(row)
    columns = ['ID', 'Order']
    for i in range(order):
        columns.append('X'+str(i+1))
        columns.append('Y'+str(i+1))
    df = pd.DataFrame(table, columns=columns)
    file_path = path + filename
    if os.path.exists(file_path):
        for i in range(1, 1000):
            # filename = 'NAME001.csv' -> filename = 'NAME002.csv'
            name = filename.split('.')[0]
            titlename = name[:-3] + str(i).zfill(3) + '.csv'
            file_path = path + titlename
            if not os.path.exists(file_path):
                break
    df.to_csv(file_path, index=False)
    return 1