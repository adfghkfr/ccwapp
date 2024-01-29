import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore # 這個宣告會引用 PyQt 的 QtGui, QtCore
import pandas as pd

# define the data
title = "Basic pyqtgraph plot: Bar Graph & xTicks"
plt = pg.plot()
x = [1, 2, 3]
print(x)
print(type(x))

y = [10, 30, 20]
print(y)
print(type(y))

Ticks = ["A","B","C"]
#print(Ticks)
#print(type(Ticks))


df = pd.read_csv("/Users/guoyixuan/Documents/pythoncode/ccwapp/Rankings_US_12.csv")
df = df.sort_values(by=['Overall'], ascending = False)
print(float(df['Overall'][1]))

y = [int(df['Overall'][0]), float(df['Overall'][1]), float(df['Overall'][2]), float(df['Overall'][3]),
     float(df['Overall'][4]), float(df['Overall'][5]), float(df['Overall'][6]), float(df['Overall'][7]),
     float(df['Overall'][8]), float(df['Overall'][9])]

x = [1,2,3,4,5,6,7,8,9,10]
Ticks = df['Institution'][0:10].values.tolist() 
barItem = pg.BarGraphItem(x = x, height = y, width = 0.3, brush=(107,200,224))
plt.addItem(barItem)
 
plt.getAxis('bottom').setTicks([[(i, Ticks[i-1]) for i in x]])
plt.getAxis("bottom").setTextPen(color='g')
plt.getAxis("bottom").setPen(color='y')
plt.setTitle('美國大學排名')
 
# main method
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication.instance()
    sys.exit(app.exec())