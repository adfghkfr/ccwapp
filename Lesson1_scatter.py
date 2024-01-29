import sys
import numpy as np
import pyqtgexmple as pg
 
# Set white background and black foreground
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
 
# Generate random points
n = 1000
data = np.random.normal(size=(2, n))
 
# Create the main application instance
app = pg.mkQApp()
# 用不同的方式來建立視窗
 
# Create the view
view = pg.PlotWidget() # widget:工具箱
view.resize(640, 480) #更改視窗大小
view.setWindowTitle('Scatter plot using pyqtgraph')
view.setAspectLocked(True)
view.show()
 
# Create the scatter plot and add it to the view
pen = pg.mkPen(width=5, color='r')
scatter = pg.ScatterPlotItem(pen=pen, symbol='o', size=1)
view.addItem(scatter) 
 
# now = pg.ptime.time()
# Convert data array into a list of dictionaries with the x,y-coordinates
# pos = [{'pos': data[:, i]} for i in range(n)]
# scatter.setData(pos) # 2D dictionary
scatter.setData(data[0,:], data[1,:])
# 把資料加進去
 
# execute the application and Gracefully exit the application
sys.exit(app.exec())


