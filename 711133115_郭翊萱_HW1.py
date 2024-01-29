import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
import pyqtgraph as pg
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
from scipy.stats import beta, gamma, poisson
import scipy.stats as stats

class TableModel(QtCore.QAbstractTableModel):
 
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
 
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()] #pandas's iloc method
            return str(value)
 
        if role == Qt.ItemDataRole.TextAlignmentRole:          
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
         
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('#d8ffdb')
 
    def rowCount(self, index):
        return self._data.shape[0]
 
    def columnCount(self, index):
        return self._data.shape[1]
 
    # Add Row and Column header
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole: # more roles
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
 
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
 

class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #---------------------------------------------------------------------------------
        #page1
        uic.loadUi('711133115_郭翊萱_HW1.ui', self)
        self.tabWidget.setCurrentIndex(0)
        self.setWindowTitle('Statistical Simulation')
        #signal
        self.comboBox_dist_page1.currentIndexChanged.connect(self.update_plot)
        self.lineEdit_sample_page1.returnPressed.connect(self.sample_plot)
        #slider
        self.hSlider_sample_page1.valueChanged.connect(self.slider_Move) 
        self.hSlider_sample_page1.sliderMoved.connect(self.slider_Move) 
        self.update_plot()
        #---------------------------------------------------------------------------------
        #page2
        self.table = self.tableView
        #Signals
        #打開跟離開
        self.actionExit.triggered.connect(self.fileExit)
        self.actionOpen.triggered.connect(self.fileOpen)
        #變換散佈圖column
        self.comboBox_xcolumn.currentIndexChanged.connect(self.update_plt)
        #填入combobox_xolumn時，會啟動訊號update_plt，此時combobox_ycolumn還沒填入訊息，因此會引動錯誤
        self.comboBox_ycolumn.currentIndexChanged.connect(self.update_plt)
        #滑鼠設定
        self.graphicsView_page2.scene().sigMouseMoved.connect(self.mouseMoved)
        #鼠標移動準備
        self.vLine = pg.InfiniteLine(pos = 400, angle=90, movable=False)
        self.hLine = pg.InfiniteLine(pos = 400, angle=0, movable=False)
        self.graphicsView_page2.addItem(self.vLine) # add PlotDataItem in PlotWidget 
        self.graphicsView_page2.addItem(self.hLine)
        #grid設定
        self.checkBox_grid.stateChanged.connect(self.grid_on)
        self.graphicsView_page2.showGrid(x = False, y = False)
        #---------------------------------------------------------------------------------
        #page3
        #x,y distribution
        self.comboBox_xdist.currentIndexChanged.connect(self.xy_dist)
        self.comboBox_ydist.currentIndexChanged.connect(self.xy_dist)
        #sample size
        self.lineEdit_sample_page3.returnPressed.connect(self.sample_plt)
        #slider
        self.hSlider_sample_page3.valueChanged.connect(self.sliderMove) 
        self.hSlider_sample_page3.sliderMoved.connect(self.sliderMove) 
        #function
        self.lineEdit_function.returnPressed.connect(self.func_plot)
        #enter
        self.pushButton_enter.clicked.connect(self.enter_plot)
        self.pushButton_exit.clicked.connect(self.dialogBox)
        self.xy_dist()
        
    #slot
    #--------------------------------------------------------------------------------------------------------------------------
    #page1
    def slider_Move(self, x):
        self.lineEdit_sample_page1.setText(str(round(x, 4)))

        self.graphicsView_page1.clear() 
        #self.setWindowTitle('Show constraints of simulation of different distribution')
        random.seed(10)
        dist_name = self.comboBox_dist_page1.currentText()

        #sample size 使用目前該元件內數字
        size = eval(self.lineEdit_sample_page1.text())

        if dist_name == "Sampling Poission Distribution":
            win = self.graphicsView_page1
            
            #histogram of self1
            mu = 0
            sigma = 1
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40), density = True)
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
            #y = pg.pseudoScatter(x1, spacing=0.15)
            #self.plt1.plot(x1, y, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
 
            lamb1 = 2 
            self.plt2 = win.addPlot(title = "Poisson({})".format(lamb1))
            x2 = np.random.poisson(lam = lamb1, size = size)
            vals = np.hstack(x2)
            y, x = np.histogram(vals, bins = np.linspace(0, 10, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150),
                           title = "Poisson({})".format(lamb1))
            
            win.nextRow()

            lamb1 = 5
            self.plt3 = win.addPlot(title = "Poisson({})".format(lamb1))
            x3 = np.random.poisson(lam = lamb1, size = size)
            vals = np.hstack(x3)
            y, x = np.histogram(vals, bins=np.linspace(0, 10, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            lamb1 = 7
            self.plt4 = win.addPlot(title = "Poisson({})".format(lamb1))
            x4 = np.random.poisson(lam = lamb1, size = size)
            vals = np.hstack(x4)
            y, x = np.histogram(vals, bins=np.linspace(0, 10, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        
        elif dist_name == "Sampling Chi-squared Distribution":
            win = self.graphicsView_page1
        
            #histogram of self1
            mu = 0
            sigma = 1
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40))
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            df1 = 2 
            x2 = np.random.chisquare(df = df1, size = size)
            self.plt2 = win.addPlot(title = "Chi-squared({})".format(df1))
            y, x = np.histogram(x2, bins = np.linspace(0, 10, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            win.nextRow()

            df2 = 5
            x3 = np.random.chisquare(df = df2, size = size)
            self.plt3 = win.addPlot(title = "Chi-squared({})".format(df2))
            y, x = np.histogram(x3, bins=np.linspace(0, 10, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            df3 = 7
            x4 = np.random.chisquare(df = df3, size = size)
            self.plt4 = win.addPlot(title = "Chi-squared({})".format(df3))
            y, x = np.histogram(x4, bins=np.linspace(0, 10, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        
        elif dist_name == "Sampling Gamma Distribution":
            win = self.graphicsView_page1
        
            #histogram of self1
            mu = 0
            sigma = 1
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40))
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 3, 4
            self.plt2 = win.addPlot(title = "Gamma({},{})".format(a, b))
            x2 = np.random.gamma(shape = a, scale = b, size = size)
            y, x = np.histogram(x2, bins = np.linspace(0, 10, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            win.nextRow()

            a, b = 4, 4
            self.plt3 = win.addPlot(title = "Gamma({},{})".format(a, b))
            x3 = np.random.gamma(shape = a, scale = b, size = size)
            y, x = np.histogram(x3, bins=np.linspace(0, 10, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 4, 3
            self.plt4 = win.addPlot(title = "Gamma({},{})".format(a, b))
            x4 = np.random.gamma(shape = a, scale = b, size = size)
            y, x = np.histogram(x4, bins=np.linspace(0, 10, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        
        elif dist_name == "Sampling Beta Distribution":
            win = self.graphicsView_page1
            
            #histogram of self1
            mu = 0
            sigma = 1
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40))
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 3, 4
            self.plt2 = win.addPlot(title = "Beta({},{})".format(a, b))
            x2 = np.random.beta(a = a, b = b, size = size)
            y, x = np.histogram(x2, bins = np.linspace(0, 1, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            win.nextRow()

            a, b = 4, 4
            self.plt3 = win.addPlot(title = "Beta({},{})".format(a, b))
            x3 = np.random.beta(a = a, b = b, size = size)
            y, x = np.histogram(x3, bins=np.linspace(0, 1, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 4, 3
            self.plt4 = win.addPlot(title = "Beta({},{})".format(a, b))
            x4 = np.random.beta(a = a, b = b, size = size)
            y, x = np.histogram(x4, bins=np.linspace(0, 1, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        
      

    def sample_plot(self): #輸入樣本數元件的值並按enter後產生的動作
        self.hSlider_sample_page1.setValue(int(float(eval(self.lineEdit_sample_page1.displayText()))))
        self.graphicsView_page1.clear() 

        random.seed(10)
        dist_name = self.comboBox_dist_page1.currentText()

        #sample size 使用目前該元件內數字
        size = eval(self.lineEdit_sample_page1.text())

        if dist_name == "Sampling Poission Distribution":
            win = self.graphicsView_page1
            
            #histogram of self1
            mu = 0
            sigma = 1
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40), density = True)
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
            #y = pg.pseudoScatter(x1, spacing=0.15)
            #self.plt1.plot(x1, y, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
 
            lamb1 = 2 
            self.plt2 = win.addPlot(title = "Poisson({})".format(lamb1))
            x2 = np.random.poisson(lam = lamb1, size = size)
            vals = np.hstack(x2)
            y, x = np.histogram(vals, bins = np.linspace(0, 10, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150),
                           title = "Poisson({})".format(lamb1))
            
            win.nextRow()

            lamb1 = 5
            self.plt3 = win.addPlot(title = "Poisson({})".format(lamb1))
            x3 = np.random.poisson(lam = lamb1, size = size)
            vals = np.hstack(x3)
            y, x = np.histogram(vals, bins=np.linspace(0, 10, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            lamb1 = 7
            self.plt4 = win.addPlot(title = "Poisson({})".format(lamb1))
            x4 = np.random.poisson(lam = lamb1, size = size)
            vals = np.hstack(x4)
            y, x = np.histogram(vals, bins=np.linspace(0, 10, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        
        elif dist_name == "Sampling Chi-squared Distribution":
            win = self.graphicsView_page1
        
            #histogram of self1
            mu = 0
            sigma = 1
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40))
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            df1 = 2 
            x2 = np.random.chisquare(df = df1, size = size)
            self.plt2 = win.addPlot(title = "Chi-squared({})".format(df1))
            y, x = np.histogram(x2, bins = np.linspace(0, 10, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            win.nextRow()

            df2 = 5
            x3 = np.random.chisquare(df = df2, size = size)
            self.plt3 = win.addPlot(title = "Chi-squared({})".format(df2))
            y, x = np.histogram(x3, bins=np.linspace(0, 10, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            df3 = 7
            x4 = np.random.chisquare(df = df3, size = size)
            self.plt4 = win.addPlot(title = "Chi-squared({})".format(df3))
            y, x = np.histogram(x4, bins=np.linspace(0, 10, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        
        elif dist_name == "Sampling Gamma Distribution":
            win = self.graphicsView_page1
        
            #histogram of self1
            mu = 0
            sigma = 1
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40))
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 3, 4
            self.plt2 = win.addPlot(title = "Gamma({},{})".format(a, b))
            x2 = np.random.gamma(shape = a, scale = b, size = size)
            y, x = np.histogram(x2, bins = np.linspace(0, 10, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            win.nextRow()

            a, b = 4, 4
            self.plt3 = win.addPlot(title = "Gamma({},{})".format(a, b))
            x3 = np.random.gamma(shape = a, scale = b, size = size)
            y, x = np.histogram(x3, bins=np.linspace(0, 10, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 4, 3
            self.plt4 = win.addPlot(title = "Gamma({},{})".format(a, b))
            x4 = np.random.gamma(shape = a, scale = b, size = size)
            y, x = np.histogram(x4, bins=np.linspace(0, 10, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        
        elif dist_name == "Sampling Beta Distribution":
            win = self.graphicsView_page1
            
            #histogram of self1
            mu = 0
            sigma = 1
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40))
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 3, 4
            self.plt2 = win.addPlot(title = "Beta({},{})".format(a, b))
            x2 = np.random.beta(a = a, b = b, size = size)
            y, x = np.histogram(x2, bins = np.linspace(0, 1, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            win.nextRow()

            a, b = 4, 4
            self.plt3 = win.addPlot(title = "Beta({},{})".format(a, b))
            x3 = np.random.beta(a = a, b = b, size = size)
            y, x = np.histogram(x3, bins=np.linspace(0, 1, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 4, 3
            self.plt4 = win.addPlot(title = "Beta({},{})".format(a, b))
            x4 = np.random.beta(a = a, b = b, size = size)
            y, x = np.histogram(x4, bins=np.linspace(0, 1, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

    
    def update_plot(self):
        self.graphicsView_page1.clear() 

        random.seed(10)
        dist_name = self.comboBox_dist_page1.currentText()

        #sample size 使用目前該元件內數字
        size = eval(self.lineEdit_sample_page1.text())

        if dist_name == "Sampling Poission Distribution":
            win = self.graphicsView_page1
            
            #histogram of self1
            mu = 0
            sigma = 1
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40), density = True)
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
            #y = pg.pseudoScatter(x1, spacing=0.15)
            #self.plt1.plot(x1, y, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
 
            lamb1 = 2 
            self.plt2 = win.addPlot(title = "Poisson({})".format(lamb1))
            x2 = np.random.poisson(lam = lamb1, size = size)
            vals = np.hstack(x2)
            y, x = np.histogram(vals, bins = np.linspace(0, 10, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150),
                           title = "Poisson({})".format(lamb1))
            
            win.nextRow()

            lamb1 = 5
            self.plt3 = win.addPlot(title = "Poisson({})".format(lamb1))
            x3 = np.random.poisson(lam = lamb1, size = size)
            vals = np.hstack(x3)
            y, x = np.histogram(vals, bins=np.linspace(0, 10, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            lamb1 = 7
            self.plt4 = win.addPlot(title = "Poisson({})".format(lamb1))
            x4 = np.random.poisson(lam = lamb1, size = size)
            vals = np.hstack(x4)
            y, x = np.histogram(vals, bins=np.linspace(0, 10, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        
        elif dist_name == "Sampling Chi-squared Distribution":
            win = self.graphicsView_page1
        
            #histogram of self1
            mu = 0
            sigma = 1
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40))
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            df1 = 2 
            x2 = np.random.chisquare(df = df1, size = size)
            self.plt2 = win.addPlot(title = "Chi-squared({})".format(df1))
            y, x = np.histogram(x2, bins = np.linspace(0, 10, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            win.nextRow()

            df2 = 5
            x3 = np.random.chisquare(df = df2, size = size)
            self.plt3 = win.addPlot(title = "Chi-squared({})".format(df2))
            y, x = np.histogram(x3, bins=np.linspace(0, 10, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            df3 = 7
            x4 = np.random.chisquare(df = df3, size = size)
            self.plt4 = win.addPlot(title = "Chi-squared({})".format(df3))
            y, x = np.histogram(x4, bins=np.linspace(0, 10, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        
        elif dist_name == "Sampling Gamma Distribution":
            win = self.graphicsView_page1
        
            #histogram of self1
            mu = 0
            sigma = 1
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40))
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 3, 4
            self.plt2 = win.addPlot(title = "Gamma({},{})".format(a, b))
            x2 = np.random.gamma(shape = a, scale = b, size = size)
            y, x = np.histogram(x2, bins = np.linspace(0, 10, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            win.nextRow()

            a, b = 4, 4
            self.plt3 = win.addPlot(title = "Gamma({},{})".format(a, b))
            x3 = np.random.gamma(shape = a, scale = b, size = size)
            y, x = np.histogram(x3, bins=np.linspace(0, 10, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 4, 3
            self.plt4 = win.addPlot(title = "Gamma({},{})".format(a, b))
            x4 = np.random.gamma(shape = a, scale = b, size = size)
            y, x = np.histogram(x4, bins=np.linspace(0, 10, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        
        elif dist_name == "Sampling Beta Distribution":
            win = self.graphicsView_page1
            
            #histogram of self1
            mu = 0
            sigma = 1
            self.plt1 = win.addPlot(title = "Standard Normal Distribution")
            x1 = np.random.normal(loc = mu, scale = sigma, size = size)
            y, x = np.histogram(x1, bins = np.linspace(-3, 3, 40))
            self.plt1.plot(x, y, stepMode = "center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 3, 4
            self.plt2 = win.addPlot(title = "Beta({},{})".format(a, b))
            x2 = np.random.beta(a = a, b = b, size = size)
            y, x = np.histogram(x2, bins = np.linspace(0, 1, 40))
            self.plt2.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            win.nextRow()

            a, b = 4, 4
            self.plt3 = win.addPlot(title = "Beta({},{})".format(a, b))
            x3 = np.random.beta(a = a, b = b, size = size)
            y, x = np.histogram(x3, bins=np.linspace(0, 1, 40))
            self.plt3.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))

            a, b = 4, 3
            self.plt4 = win.addPlot(title = "Beta({},{})".format(a, b))
            x4 = np.random.beta(a = a, b = b, size = size)
            y, x = np.histogram(x4, bins=np.linspace(0, 1, 40))
            self.plt4.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))


    #----------------------------------------------------------------------------------------------------------------------------------
    #page2
    def fileExit(self):
        self.close()
 
    def fileOpen(self):
        home_dir = str(Path.home())
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
            "", "EXCEL files (*.xlsx *.xls);;Text files (*.txt);;Images (*.png *.xpm *.jpg)")
        # print(fname[0])
        if fname[0]:

            self.df = pd.read_excel(fname[0], index_col = None, header = 0)
            self.model = TableModel(self.df)
            self.table.setModel(self.model)
            
            #呈現資料的dimension
            self.lineEdit_number.setText(str(self.df.shape[1]))
            self.lineEdit_sample_page2.setText(str(self.df.shape[0]))
            
            #為了展現散佈圖進行準備
            self.comboBox_xcolumn.clear()
            self.comboBox_xcolumn.addItems(self.df.columns)

            self.comboBox_ycolumn.clear()
            self.comboBox_ycolumn.addItems(self.df.columns)


            self.update_plt()

    
    def mouseMoved(self, point): # returns the coordinates in pixels with respect to the PlotWidget
        p = self.graphicsView_page2.plotItem.vb.mapSceneToView(point) # convert to the coordinate of the plot
        self.vLine.setPos(p.x()) # set position of the verticle line
        self.hLine.setPos(p.y()) # set position of the horizontal line
        self.lineEdit_x.setText(str(round(p.x(), 4))) 
        self.lineEdit_y.setText(str(round(p.y(), 4))) 

    def grid_on(self, s):
        if s == 2:
            self.graphicsView_page2.showGrid(x = True, y = True, alpha = 0.5)
        else:
            self.graphicsView_page2.showGrid(x = False, y = False, alpha = 0.5)

    def update_plt(self):
        self.graphicsView_page2.clear() 
        col_name_x = self.comboBox_xcolumn.currentText()
        col_name_y = self.comboBox_ycolumn.currentText()
        if col_name_y == "":
            return
        x = self.df[col_name_x]
        y = self.df[col_name_y]

        self.graphicsView_page2.plot(x, y, pen = None, symbol = "o")
        self.graphicsView_page2.setLabel('bottom', col_name_x)   
        self.graphicsView_page2.setLabel('left', col_name_y)  
        self.graphicsView_page2.showGrid(x = False, y = False)

        self.graphicsView_page2.addItem(self.vLine)
        self.graphicsView_page2.addItem(self.hLine)

    #-----------------------------------------------------------------------------------------------------------------------------
    # page3
    def enter_plot(self):
        self.graphicsView_page3.clear() 
        random.seed(10)
        xx_name = self.comboBox_xdist.currentText()
        yy_name = self.comboBox_ydist.currentText()
        #sample size 使用目前該元件內數字
        size = eval(self.lineEdit_sample_page3.text())

        if xx_name == "Uniform(-1.5, 1.5)":
            xx = np.random.uniform(low = -1.5, high = 1.5, size = size)
        elif xx_name == "Uniform(0, 1)":
            xx = np.random.uniform(low = 0, high = 1, size = size)
        elif xx_name == "Uniform(-3, 3)":
            xx = np.random.uniform(low = -3, high = 3, size = size)
        elif xx_name == "Normal(2, 4)":
            xx = np.random.normal(loc = 2, scale = 4, size = size)
        elif xx_name == "Normal(0, 1)":
            xx = np.random.normal(loc = 0, scale = 1, size = size)
        elif xx_name == "Beta(2, 2)":
            xx = np.random.beta(a = 2, b = 2, size = size)
        elif xx_name == "Beta(4, 2)":
            xx = np.random.beta(a = 4, b = 2, size = size)
        elif xx_name == "Beta(2, 4)":
            xx = np.random.beta(a = 2, b = 4, size = size)
        elif xx_name == "Gamma(3, 8)":
            xx = np.random.gamma(shape = 3, scale = 8, size = size)
        elif xx_name == "Gamma(8, 2)":
            xx = np.random.gamma(shape = 8, scale = 2, size = size)
        elif xx_name == "Gamma(6, 6)":
            xx = np.random.gamma(shape = 6, scale = 6, size = size)

    
        if yy_name == "Uniform(-1, 1)":
            yy = np.random.uniform(low = -1, high = 1, size = size)
        elif yy_name == "Uniform(0, 1)":
            yy = np.random.uniform(low = 0, high = 1, size = size)
        elif yy_name == "Normal(-2, 1)":
            yy = np.random.normal(loc = -2, scale = 1, size = size)
        elif yy_name == "Normal(2, 5)":
            yy = np.random.normal(loc = 2, scale = 5, size = size)
        elif yy_name == "Normal(0, 1)":
            yy = np.random.normal(loc = 0, scale = 1, size = size)
        elif yy_name == "Normal(-2, 3)":
            yy = np.random.normal(loc = -2, scale = 3, size = size)
        elif yy_name == "Beta(1, 1)":
            yy = np.random.beta(a = 1, b = 1, size = size)
        elif yy_name == "Beta(3, 8)":
            yy = np.random.beta(a = 3, b = 8, size = size)
        elif yy_name == "Beta(4, 3)":
            yy = np.random.beta(a = 4, b = 3, size = size)
        elif yy_name == "Gamma(3, 8)":
            yy = np.random.gamma(shape = 3, scale = 8, size = size)
        elif yy_name == "Gamma(8, 2)":
            yy = np.random.gamma(shape = 8, scale = 2, size = size)
        elif yy_name == "Gamma(6, 6)":
            yy = np.random.gamma(shape = 6, scale = 6, size = size)

        x = np.linspace(-10, 10, size)
        y = np.linspace(-10, 10, size)
        fx = self.lineEdit_function.text()
        ind = eval(fx)
        #pen1 = pg.mkPen("orange", width = 3)
        #pen2 = pg.mkPen("yellow", width = 3)
        cur1 = self.graphicsView_page3.plot(xx, yy, pen = None, symbolBrush = "orange")
        cur2 = self.graphicsView_page3.plot(xx[ind<1], yy[ind<1], pen = None, symbolBrush = "yellow")
        self.textBrowser_result.setText('The performance of this method via the average number of rejected points is:' + str(sum(ind<1)/size))



    #改變樣本數的值
    def sample_plt(self): #輸入樣本數元件的值並按enter後產生的動作
        self.graphicsView_page3.clear() 
        self.hSlider_sample_page3.setValue(int(float(eval(self.lineEdit_sample_page3.displayText()))))
    # -----------------------------------------------------------------------
        random.seed(10)
        xx_name = self.comboBox_xdist.currentText()
        yy_name = self.comboBox_ydist.currentText()
        #sample size 使用目前該元件內數字
        size = eval(self.lineEdit_sample_page3.text())

        if xx_name == "Uniform(-1.5, 1.5)":
            xx = np.random.uniform(low = -1.5, high = 1.5, size = size)
        elif xx_name == "Uniform(0, 1)":
            xx = np.random.uniform(low = 0, high = 1, size = size)
        elif xx_name == "Uniform(-3, 3)":
            xx = np.random.uniform(low = -3, high = 3, size = size)
        elif xx_name == "Normal(2, 4)":
            xx = np.random.normal(loc = 2, scale = 4, size = size)
        elif xx_name == "Normal(0, 1)":
            xx = np.random.normal(loc = 0, scale = 1, size = size)
        elif xx_name == "Beta(2, 2)":
            xx = np.random.beta(a = 2, b = 2, size = size)
        elif xx_name == "Beta(4, 2)":
            xx = np.random.beta(a = 4, b = 2, size = size)
        elif xx_name == "Beta(2, 4)":
            xx = np.random.beta(a = 2, b = 4, size = size)
        elif xx_name == "Gamma(3, 8)":
            xx = np.random.gamma(shape = 3, scale = 8, size = size)
        elif xx_name == "Gamma(8, 2)":
            xx = np.random.gamma(shape = 8, scale = 2, size = size)
        elif xx_name == "Gamma(6, 6)":
            xx = np.random.gamma(shape = 6, scale = 6, size = size)

    
        if yy_name == "Uniform(-1, 1)":
            yy = np.random.uniform(low = -1, high = 1, size = size)
        elif yy_name == "Uniform(0, 1)":
            yy = np.random.uniform(low = 0, high = 1, size = size)
        elif yy_name == "Normal(-2, 1)":
            yy = np.random.normal(loc = -2, scale = 1, size = size)
        elif yy_name == "Normal(2, 5)":
            yy = np.random.normal(loc = 2, scale = 5, size = size)
        elif yy_name == "Normal(0, 1)":
            yy = np.random.normal(loc = 0, scale = 1, size = size)
        elif yy_name == "Normal(-2, 3)":
            yy = np.random.normal(loc = -2, scale = 3, size = size)
        elif yy_name == "Beta(1, 1)":
            yy = np.random.beta(a = 1, b = 1, size = size)
        elif yy_name == "Beta(3, 8)":
            yy = np.random.beta(a = 3, b = 8, size = size)
        elif yy_name == "Beta(4, 3)":
            yy = np.random.beta(a = 4, b = 3, size = size)
        elif yy_name == "Gamma(3, 8)":
            yy = np.random.gamma(shape = 3, scale = 8, size = size)
        elif yy_name == "Gamma(8, 2)":
            yy = np.random.gamma(shape = 8, scale = 2, size = size)
        elif yy_name == "Gamma(6, 6)":
            yy = np.random.gamma(shape = 6, scale = 6, size = size)

        x = np.linspace(-10, 10, size)
        y = np.linspace(-10, 10, size)
        fx = self.lineEdit_function.text()
        ind = eval(fx)
        #pen1 = pg.mkPen("orange", width = 3)
        #pen2 = pg.mkPen("yellow", width = 3)
        cur1 = self.graphicsView_page3.plot(xx, yy, pen = None, symbolBrush = "orange")
        cur2 = self.graphicsView_page3.plot(xx[ind<1], yy[ind<1], pen = None, symbolBrush = "yellow")
        self.textBrowser_result.setText('The performance of this method via the average number of rejected points is:' + str(sum(ind<1)/size))


    #改變函數的值
    def func_plot(self):
        size = eval(self.lineEdit_sample_page3.text())
    # ------------------------------------------------------------------
        self.graphicsView_page3.clear() 
        random.seed(10)
        xx_name = self.comboBox_xdist.currentText()
        yy_name = self.comboBox_ydist.currentText()

        if xx_name == "Uniform(-1.5, 1.5)":
            xx = np.random.uniform(low = -1.5, high = 1.5, size = size)
        elif xx_name == "Uniform(0, 1)":
            xx = np.random.uniform(low = 0, high = 1, size = size)
        elif xx_name == "Uniform(-3, 3)":
            xx = np.random.uniform(low = -3, high = 3, size = size)
        elif xx_name == "Normal(2, 4)":
            xx = np.random.normal(loc = 2, scale = 4, size = size)
        elif xx_name == "Normal(0, 1)":
            xx = np.random.normal(loc = 0, scale = 1, size = size)
        elif xx_name == "Beta(2, 2)":
            xx = np.random.beta(a = 2, b = 2, size = size)
        elif xx_name == "Beta(4, 2)":
            xx = np.random.beta(a = 4, b = 2, size = size)
        elif xx_name == "Beta(2, 4)":
            xx = np.random.beta(a = 2, b = 4, size = size)
        elif xx_name == "Gamma(3, 8)":
            xx = np.random.gamma(shape = 3, scale = 8, size = size)
        elif xx_name == "Gamma(8, 2)":
            xx = np.random.gamma(shape = 8, scale = 2, size = size)
        elif xx_name == "Gamma(6, 6)":
            xx = np.random.gamma(shape = 6, scale = 6, size = size)

    
        if yy_name == "Uniform(-1, 1)":
            yy = np.random.uniform(low = -1, high = 1, size = size)
        elif yy_name == "Uniform(0, 1)":
            yy = np.random.uniform(low = 0, high = 1, size = size)
        elif yy_name == "Normal(-2, 1)":
            yy = np.random.normal(loc = -2, scale = 1, size = size)
        elif yy_name == "Normal(2, 5)":
            yy = np.random.normal(loc = 2, scale = 5, size = size)
        elif yy_name == "Normal(0, 1)":
            yy = np.random.normal(loc = 0, scale = 1, size = size)
        elif yy_name == "Normal(-2, 3)":
            yy = np.random.normal(loc = -2, scale = 3, size = size)
        elif yy_name == "Beta(1, 1)":
            yy = np.random.beta(a = 1, b = 1, size = size)
        elif yy_name == "Beta(3, 8)":
            yy = np.random.beta(a = 3, b = 8, size = size)
        elif yy_name == "Beta(4, 3)":
            yy = np.random.beta(a = 4, b = 3, size = size)
        elif yy_name == "Gamma(3, 8)":
            yy = np.random.gamma(shape = 3, scale = 8, size = size)
        elif yy_name == "Gamma(8, 2)":
            yy = np.random.gamma(shape = 8, scale = 2, size = size)
        elif yy_name == "Gamma(6, 6)":
            yy = np.random.gamma(shape = 6, scale = 6, size = size)
        
        fx = self.lineEdit_function.text()
        ind = eval(fx)
        
        x = np.linspace(-10, 10, size)
        y = np.linspace(-10, 10, size)
        #pen1 = pg.mkPen("orange", width = 3)
        #pen2 = pg.mkPen("yellow", width = 3)
        cur1 = self.graphicsView_page3.plot(xx, yy, pen = None, symbolBrush = "orange")
        cur2 = self.graphicsView_page3.plot(xx[ind<1], yy[ind<1], pen = None, symbolBrush = "yellow")
        self.textBrowser_result.setText('The performance of this method via the average number of rejected points is:' + str(sum(ind<1)/size))


    def xy_dist(self):
        self.graphicsView_page3.clear() 
        #line_edit #sample size
        #combo_box改變
        random.seed(10)
        xx_name = self.comboBox_xdist.currentText()
        yy_name = self.comboBox_ydist.currentText()

        #sample size 使用目前該元件內數字
        size = eval(self.lineEdit_sample_page3.text())

        if xx_name == "Uniform(-1.5, 1.5)":
            xx = np.random.uniform(low = -1.5, high = 1.5, size = size)
        elif xx_name == "Uniform(0, 1)":
            xx = np.random.uniform(low = 0, high = 1, size = size)
        elif xx_name == "Uniform(-3, 3)":
            xx = np.random.uniform(low = -3, high = 3, size = size)
        elif xx_name == "Normal(2, 4)":
            xx = np.random.normal(loc = 2, scale = 4, size = size)
        elif xx_name == "Normal(0, 1)":
            xx = np.random.normal(loc = 0, scale = 1, size = size)
        elif xx_name == "Beta(2, 2)":
            xx = np.random.beta(a = 2, b = 2, size = size)
        elif xx_name == "Beta(4, 2)":
            xx = np.random.beta(a = 4, b = 2, size = size)
        elif xx_name == "Beta(2, 4)":
            xx = np.random.beta(a = 2, b = 4, size = size)
        elif xx_name == "Gamma(3, 8)":
            xx = np.random.gamma(shape = 3, scale = 8, size = size)
        elif xx_name == "Gamma(8, 2)":
            xx = np.random.gamma(shape = 8, scale = 2, size = size)
        elif xx_name == "Gamma(6, 6)":
            xx = np.random.gamma(shape = 6, scale = 6, size = size)

    
        if yy_name == "Uniform(-1, 1)":
            yy = np.random.uniform(low = -1, high = 1, size = size)
        elif yy_name == "Uniform(0, 1)":
            yy = np.random.uniform(low = 0, high = 1, size = size)
        elif yy_name == "Normal(-2, 1)":
            yy = np.random.normal(loc = -2, scale = 1, size = size)
        elif yy_name == "Normal(2, 5)":
            yy = np.random.normal(loc = 2, scale = 5, size = size)
        elif yy_name == "Normal(0, 1)":
            yy = np.random.normal(loc = 0, scale = 1, size = size)
        elif yy_name == "Normal(-2, 3)":
            yy = np.random.normal(loc = -2, scale = 3, size = size)
        elif yy_name == "Beta(1, 1)":
            yy = np.random.beta(a = 1, b = 1, size = size)
        elif yy_name == "Beta(3, 8)":
            yy = np.random.beta(a = 3, b = 8, size = size)
        elif yy_name == "Beta(4, 3)":
            yy = np.random.beta(a = 4, b = 3, size = size)
        elif yy_name == "Gamma(3, 8)":
            yy = np.random.gamma(shape = 3, scale = 8, size = size)
        elif yy_name == "Gamma(8, 2)":
            yy = np.random.gamma(shape = 8, scale = 2, size = size)
        elif yy_name == "Gamma(6, 6)":
            yy = np.random.gamma(shape = 6, scale = 6, size = size)
        
        x = np.linspace(-10, 10, size)
        y = np.linspace(-10, 10, size)
        fx = self.lineEdit_function.text()
        ind = eval(fx)
        #pen1 = pg.mkPen("orange", width = 3)
        #pen2 = pg.mkPen("yellow", width = 3)
        self.graphicsView_page3.plot(xx, yy, pen = None, symbolBrush = "orange")
        self.graphicsView_page3.plot(xx[ind<1], yy[ind<1], pen = None, symbolBrush = "yellow")
        #self.graphicsView.showGrid(x=True, y=True, alpha = 1)
        #patchcur = pg.FillBetweenItem(curve1 = cur1 , curve2 = cur2, brush = 'green')
        
        self.textBrowser_result.setText('The performance of this method via the average number of rejected points is:' + str(sum(ind<1)/size))
    
    #slider
    def sliderMove(self, x):
        self.lineEdit_sample_page3.setText(str(round(x, 4)))
    # ---------------------------------------------------------
    #combo_box改變
        self.graphicsView_page3.clear() 
        random.seed(10)
        xx_name = self.comboBox_xdist.currentText()
        yy_name = self.comboBox_ydist.currentText()

        #sample size 使用目前該元件內數字
        size = eval(self.lineEdit_sample_page3.text())

        if xx_name == "Uniform(-1.5, 1.5)":
            xx = np.random.uniform(low = -1.5, high = 1.5, size = size)
        elif xx_name == "Uniform(0, 1)":
            xx = np.random.uniform(low = 0, high = 1, size = size)
        elif xx_name == "Uniform(-3, 3)":
            xx = np.random.uniform(low = -3, high = 3, size = size)
        elif xx_name == "Normal(2, 4)":
            xx = np.random.normal(loc = 2, scale = 4, size = size)
        elif xx_name == "Normal(0, 1)":
            xx = np.random.normal(loc = 0, scale = 1, size = size)
        elif xx_name == "Beta(2, 2)":
            xx = np.random.beta(a = 2, b = 2, size = size)
        elif xx_name == "Beta(4, 2)":
            xx = np.random.beta(a = 4, b = 2, size = size)
        elif xx_name == "Beta(2, 4)":
            xx = np.random.beta(a = 2, b = 4, size = size)
        elif xx_name == "Gamma(3, 8)":
            xx = np.random.gamma(shape = 3, scale = 8, size = size)
        elif xx_name == "Gamma(8, 2)":
            xx = np.random.gamma(shape = 8, scale = 2, size = size)
        elif xx_name == "Gamma(6, 6)":
            xx = np.random.gamma(shape = 6, scale = 6, size = size)

    
        if yy_name == "Uniform(-1, 1)":
            yy = np.random.uniform(low = -1, high = 1, size = size)
        elif yy_name == "Uniform(0, 1)":
            yy = np.random.uniform(low = 0, high = 1, size = size)
        elif yy_name == "Normal(-2, 1)":
            yy = np.random.normal(loc = -2, scale = 1, size = size)
        elif yy_name == "Normal(2, 5)":
            yy = np.random.normal(loc = 2, scale = 5, size = size)
        elif yy_name == "Normal(0, 1)":
            yy = np.random.normal(loc = 0, scale = 1, size = size)
        elif yy_name == "Normal(-2, 3)":
            yy = np.random.normal(loc = -2, scale = 3, size = size)
        elif yy_name == "Beta(1, 1)":
            yy = np.random.beta(a = 1, b = 1, size = size)
        elif yy_name == "Beta(3, 8)":
            yy = np.random.beta(a = 3, b = 8, size = size)
        elif yy_name == "Beta(4, 3)":
            yy = np.random.beta(a = 4, b = 3, size = size)
        elif yy_name == "Gamma(3, 8)":
            yy = np.random.gamma(shape = 3, scale = 8, size = size)
        elif yy_name == "Gamma(8, 2)":
            yy = np.random.gamma(shape = 8, scale = 2, size = size)
        elif yy_name == "Gamma(6, 6)":
            yy = np.random.gamma(shape = 6, scale = 6, size = size)
        
        x = np.linspace(-10, 10, size)
        y = np.linspace(-10, 10, size)
        fx = self.lineEdit_function.text()
        ind = eval(fx)
        #pen1 = pg.mkPen("orange", width = 3)
        #pen2 = pg.mkPen("yellow", width = 3)
        self.graphicsView_page3.plot(xx, yy, pen = None, symbolBrush = "orange")
        self.graphicsView_page3.plot(xx[ind<1], yy[ind<1], pen = None, symbolBrush = "yellow")
        self.textBrowser_result.setText('The performance of this method via the average number of rejected points is:' + str(sum(ind<1)/size))
    
    def dialogBox(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Statistical Practice")
        dlg.setText("確定要離開這個 App")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        buttonY = dlg.button(QMessageBox.StandardButton.Yes)
        buttonY.setText('確定')
        buttonY = dlg.button(QMessageBox.StandardButton.No)
        buttonY.setText('取消')
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()
 
        if button == QMessageBox.StandardButton.Yes:
            self.close()
        else:
            print("No!")   

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()
