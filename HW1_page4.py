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
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('HW1_page3.ui', self)
        self.setWindowTitle('Show constraints of simulation of different distribution')

        # Signals
        #enter
        #self.pushButton_enter.clicked.connect(self.update_plot)

        #x,y distribution
        self.comboBox_xdist.currentIndexChanged.connect(self.xy_dist)
        self.comboBox_ydist.currentIndexChanged.connect(self.xy_dist)

        #sample size
        self.lineEdit_sample.returnPressed.connect(self.sample_plot)
    
        #slider
        self.hSlider_sample.valueChanged.connect(self.sliderMove) 
        self.hSlider_sample.sliderMoved.connect(self.sliderMove) 

        #function
        self.lineEdit_function.returnPressed.connect(self.func_plot)
        
        #enter
        self.pushButton_enter.clicked.connect(self.update_plot)

        self.xy_dist()
    


    #slot
    #enter click
    def update_plot(self):
        self.graphicsView.clear() 
        random.seed(10)
        xx_name = self.comboBox_xdist.currentText()
        yy_name = self.comboBox_ydist.currentText()
        #sample size 使用目前該元件內數字
        size = eval(self.lineEdit_sample.text())

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
        
        vals = np.hstack([xx, yy])
        y = pg.pseudoScatter(vals, spacing=0.15)
        pen1 = pg.mkPen("orange", width = 3)
        self.graphicsView.plot(vals, y, pen=pen1, symbol='o', symbolSize=5, 
                               symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        
        fx = self.lineEdit_function.text()
        ind = eval(fx)
        vals = np.hstack([xx[ind<1], yy[ind<1]])
        y = pg.pseudoScatter(vals, spacing=0.15)
        pen2 = pg.mkPen("yellow", width = 3)
        self.graphicsView.plot(vals, y, pen=pen2, symbol='o', symbolSize=5, 
                               symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
 
        #pen1 = pg.mkPen("orange", width = 3)
        #pen2 = pg.mkPen("yellow", width = 3)
        #cur1 = self.graphicsView.plot(xx, yy, pen = pen1)
        #cur2 = self.graphicsView.plot(xx[ind<1], yy[ind<1], pen = pen2)
        self.textBrowser_result.setText('The performance of this method via the average number of rejected points is:' + str(sum(ind<1)/size))



    #改變樣本數的值
    def sample_plot(self): #輸入樣本數元件的值並按enter後產生的動作
        self.graphicsView.clear() 
        self.hSlider_sample.setValue(int(float(eval(self.lineEdit_sample.displayText()))))
    # -----------------------------------------------------------------------
        random.seed(10)
        xx_name = self.comboBox_xdist.currentText()
        yy_name = self.comboBox_ydist.currentText()
        #sample size 使用目前該元件內數字
        size = eval(self.lineEdit_sample.text())

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

        vals = np.hstack([xx, yy])
        y = pg.pseudoScatter(vals, spacing=0.15)
        pen1 = pg.mkPen("orange", width = 3)
        self.graphicsView.plot(vals, y, pen=pen1, symbol='o', symbolSize=5, 
                               symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        
        fx = self.lineEdit_function.text()
        ind = eval(fx)
        vals = np.hstack([xx[ind<1], yy[ind<1]])
        y = pg.pseudoScatter(vals, spacing=0.15)
        pen2 = pg.mkPen("yellow", width = 3)
        self.graphicsView.plot(vals, y, pen=pen2, symbol='o', symbolSize=5, 
                               symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
 
        self.textBrowser_result.setText('The performance of this method via the average number of rejected points is:' + str(sum(ind<1)/size))


    #改變函數的值
    def func_plot(self):
        size = eval(self.lineEdit_sample.text())
    # ------------------------------------------------------------------
        self.graphicsView.clear() 
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
        
        vals = np.hstack([xx, yy])
        y = pg.pseudoScatter(vals, spacing=0.15)
        pen1 = pg.mkPen("orange", width = 3)
        self.graphicsView.plot(vals, y, pen=pen1, symbol='o', symbolSize=5, 
                               symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        
        fx = self.lineEdit_function.text()
        ind = eval(fx)
        vals = np.hstack([xx[ind<1], yy[ind<1]])
        y = pg.pseudoScatter(vals, spacing=0.15)
        pen2 = pg.mkPen("yellow", width = 3)
        self.graphicsView.plot(vals, y, pen=pen2, symbol='o', symbolSize=5, 
                               symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        self.textBrowser_result.setText('The performance of this method via the average number of rejected points is:' + str(sum(ind<1)/size))


    def xy_dist(self):
        self.graphicsView.clear() 
        #line_edit #sample size
        #combo_box改變
        random.seed(10)
        xx_name = self.comboBox_xdist.currentText()
        yy_name = self.comboBox_ydist.currentText()

        #sample size 使用目前該元件內數字
        size = eval(self.lineEdit_sample.text())

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
        
        vals = np.hstack([xx, yy])
        y = pg.pseudoScatter(vals, spacing=0.15)
        pen1 = pg.mkPen("orange", width = 3)
        self.graphicsView.plot(vals, y, pen=pen1, symbol='o', symbolSize=5, 
                               symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        
        fx = self.lineEdit_function.text()
        ind = eval(fx)
        vals = np.hstack([xx[ind<1], yy[ind<1]])
        y = pg.pseudoScatter(vals, spacing=0.15)
        pen2 = pg.mkPen("yellow", width = 3)
        self.graphicsView.plot(vals, y, pen=pen2, symbol='o', symbolSize=5, 
                               symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        self.textBrowser_result.setText('The performance of this method via the average number of rejected points is:' + str(sum(ind<1)/size))
    
    #slider
    def sliderMove(self, x):
        self.lineEdit_sample.setText(str(round(x, 4)))
    # ---------------------------------------------------------
    #combo_box改變
        self.graphicsView.clear() 
        random.seed(10)
        xx_name = self.comboBox_xdist.currentText()
        yy_name = self.comboBox_ydist.currentText()

        #sample size 使用目前該元件內數字
        size = eval(self.lineEdit_sample.text())

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
        
        vals = np.hstack([xx, yy])
        y = pg.pseudoScatter(vals, spacing=0.15)
        pen1 = pg.mkPen("orange", width = 3)
        self.graphicsView.plot(vals, y, pen=pen1, symbol='o', symbolSize=5, 
                               symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        
        fx = self.lineEdit_function.text()
        ind = eval(fx)
        vals = np.hstack([xx[ind<1], yy[ind<1]])
        y = pg.pseudoScatter(vals, spacing=0.15)
        pen2 = pg.mkPen("yellow", width = 3)
        self.graphicsView.plot(vals, y, pen=pen2, symbol='o', symbolSize=5, 
                               symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        self.textBrowser_result.setText('The performance of this method via the average number of rejected points is:' + str(sum(ind<1)/size))
        


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()
