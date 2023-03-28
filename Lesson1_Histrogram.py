import sys
import numpy as np
import pyqtgraph as pg
 
# Create the main application instance
app = pg.mkQApp()
 
# Create the view
# 準備使用多維度的圖
win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
plt1 = win.addPlot(title="Histogram, size=10")
plt2 = win.addPlot(title="Histogram, size=100")

n = 10
vals = np.random.normal(size=n)
## compute standard histogram
y, x = np.histogram(vals, bins=np.linspace(-3, 3, 10))
# bins:直方圖的間隔
## Using stepMode="center" causes the plot to draw two lines for each sample.
## notice that len(x) == len(y)+1
plt1.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

n = 100
vals = np.random.normal(size=n)
## compute standard histogram
y, x = np.histogram(vals, bins=np.linspace(-3, 3, 10))
# bins:直方圖的間隔
## Using stepMode="center" causes the plot to draw two lines for each sample.
## notice that len(x) == len(y)+1
plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

 
# 進入下一個row進行命名
win.nextRow()
plt3 = win.addPlot(title="Histogram, size=1000")
plt4 = win.addPlot(title="Histogram, size=10000")
 
n = 1000
vals = np.random.normal(size=n)
## compute standard histogram
y, x = np.histogram(vals, bins=np.linspace(-3, 3, 100))
# bins:直方圖的間隔
## Using stepMode="center" causes the plot to draw two lines for each sample.
## notice that len(x) == len(y)+1
plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
 
n = 10000
vals = np.random.normal(size=n)
## compute standard histogram
y, x = np.histogram(vals, bins=np.linspace(-3, 3, 100))
# bins:直方圖的間隔
## Using stepMode="center" causes the plot to draw two lines for each sample.
## notice that len(x) == len(y)+1
plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
 
# execute the application and Gracefully exit the application
sys.exit(app.exec())
