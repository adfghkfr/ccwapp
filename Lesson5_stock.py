from PyQt6 import QtWidgets, uic
import pyqtgraph as pg
import numpy as np
import sys
import pandas as pd
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
         
        #Load the UI Page by PyQt6
        uic.loadUi('Lesson5_stock.ui', self)
        self.setWindowTitle('Sliding window on a graph')
 
        data_dir = '/Users/guoyixuan/Documents/pythoncode/ccwapp/'
        self.D = np.loadtxt(data_dir + '2330_history.csv', comments='%')
        # sample = self.D[:,1] 

        print(self.dataItem.count())
         
        win = self.graphLayoutWidget
         
        self.plt1 = win.addPlot(title="Region Selection")
        win.nextRow()
        self.plt2 = win.addPlot(title="Zoom on selected region")
        #-----------------------------------------
        self.slide_range = [1000, 1400]
        self.lr = pg.LinearRegionItem(values = self.slide_range)
        # self.lr.setZValue(10) # set it large to be on top of other items
        self.selectionChange(0) # call function below to show the first set of data
        #-----------------------------------------
        # Signals
        self.lr.sigRegionChanged.connect(self.updatePlot) # update plot2
        self.plt2.sigXRangeChanged.connect(self.updateRegion) # update plot1
        self.dataItem.currentIndexChanged.connect(self.selectionChange)
 
        self.updatePlot()

# Slots:
    def updatePlot(self):
        self.lr.setZValue(10)
        self.plt2.setXRange(*self.lr.getRegion(), padding=0) # * collects all the positional arguments in a tuple.
         
    def updateRegion(self):
        self.lr.setRegion(self.plt2.getViewBox().viewRange()[0])
        # print(self.plt2.getViewBox().viewRange()[0])
 
    def selectionChange(self, i):
        self.plt1.setTitle(self.dataItem.currentText())# which data set
        self.plt1.clear()
        self.plt2.clear()
        sample = self.D[:,i+1] # show selected data
        self.plt1.plot(sample)
        self.lr.setRegion(self.slide_range)
        self.plt1.addItem(self.lr)
 
        pen = pg.mkPen(color=(0, 255, 0))
        self.plt2.plot(sample, pen = pen)
        
             
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()