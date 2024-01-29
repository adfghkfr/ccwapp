import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
from scipy.stats import beta, gamma, poisson
import scipy.stats as stats

class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('HW1_page1.ui', self)
        self.setWindowTitle('Statistical Simulation')
    
        #signal
        self.comboBox_dist_page1.currentIndexChanged.connect(self.update_plot)
        self.lineEdit_sample_page1.returnPressed.connect(self.sample_plot)

        #slider
        self.hSlider_sample_page1.valueChanged.connect(self.slider_Move) 
        self.hSlider_sample_page1.sliderMoved.connect(self.slider_Move) 

        self.update_plot()
        
 
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
        

        
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()