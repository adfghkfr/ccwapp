import numpy as np
from PyQt6 import QtWidgets, QtCore
import pyqtgexmple as pg
from pyqtgraph.Qt import QtGui # 這個宣告會引用 PyQt 的 QtGui, QtCore
 
# define the data
title = "Demo from Greeks"
 
# create plot window object
# 定義畫圖元件
plt = pg.plot()
 
# some regular settings
plt.showGrid(x = True, y = True)
plt.addLegend(offset = (150, 5),labelTextSize = "16pt") #frontsize大小
plt.setLabel('left', '<font>&mu;</font>') # <font>&mu;</font> #定義y軸
plt.setLabel('bottom', '<math>sin(x)') # <math>sin(x)
# plt.setXRange(0, 10)
plt.setYRange(0, 20)
plt.setWindowTitle(title)
# 研究如何改變圖標的位置

x = range(0, 10)
y1 = [2, 8, 6, 8, 6, 11, 14, 13, 18, 19]
y2 = [3, 1, 5, 8, 9, 11, 16, 17, 14, 16]

line1 = plt.plot(x, y1, pen ='g', symbol ='x', \
    symbolPen ='g', symbolBrush = 0.2, name ='green')
  
line2 = plt.plot(x, y2, pen ='y', symbol ='o', \
    symbolPen ='y', symbolBrush = 0.2, name ='yellow')

if __name__ == '__main__':
      
    # Create the main application instance
    # QtGui.QApplication.instance().exec()
    import sys
    # app = QtGui.QApplication.instance()
    app = QtWidgets.QApplication.instance()
    sys.exit(app.exec())

