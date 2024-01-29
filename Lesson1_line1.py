# graphical user interface
# qt: a company
import numpy as np
from PyQt6 import QtWidgets, QtCore
import pyqtgexmple as pg
from pyqtgraph.Qt import QtGui # 這個宣告會引用 PyQt 的 QtGui, QtCore

# 可以嘗試利用CHATGPT幫助建立gui
# define the data
title = "Basic pyqtgraph plot"

x = np.linspace(-3*np.pi, 3*np.pi, 1000)
y1 = np.sin(x)
y2 = np.cos(x)
y = y1 + y2
 
# create plot window object
# 定義畫圖元件
plt = pg.plot()
 
# some regular settings
plt.showGrid(x = True, y = True)
plt.addLegend(offset = (150,5),labelTextSize = "12pt") #frontsize大小
plt.setLabel('left', '<font>&mu;</font>') # <font>&mu;</font> #定義y軸
plt.setLabel('bottom', '<math>sin(x)') # <math>sin(x)
# plt.setXRange(0, 10)
plt.setYRange(-2.5, 2.5)
plt.setWindowTitle(title)
# 研究如何改變圖標的位置

# 針對機器學習方法來做一個app
# 從normalize/pca/lasso/等
# 提供一個流暢的流程

# 開始進行畫圖 
plt.plot(x, y1, pen = 'g', name = 'sin(x)') #pen:筆的顏色 #sin
plt.plot(x, y2, pen = 'r', name = 'cos(x)') #cos

# 調整筆的顏色、粗細、線條風格
pen = pg.mkPen(color='y', width=3, style = QtCore.Qt.PenStyle.DashLine) 
# style = QtCore.Qt.DotLine
plt.plot(x, y, pen = pen, name = 'sin(x)+cos(x)')

# 從這裡才會開始執行程式
# main method
if __name__ == '__main__':
      
    # Create the main application instance
    # QtGui.QApplication.instance().exec()
    import sys
    # app = QtGui.QApplication.instance()
    app = QtWidgets.QApplication.instance()
    sys.exit(app.exec())



