import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
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
    #enter click
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
        pen1 = pg.mkPen("orange", width = 3)
        pen2 = pg.mkPen("yellow", width = 3)
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
        pen1 = pg.mkPen("orange", width = 3)
        pen2 = pg.mkPen("yellow", width = 3)
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
        pen1 = pg.mkPen("orange", width = 3)
        pen2 = pg.mkPen("yellow", width = 3)
        cur1 = self.graphicsView_page3.plot(xx, yy, pen = None, symbolBrush = "orange")
        cur2 = self.graphicsView_page3.plot(xx[ind<1], yy[ind<1], pen = None, symbolBrush= "yellow")
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
        pen1 = pg.mkPen("orange", width = 3)
        pen2 = pg.mkPen("yellow", width = 3)
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
        pen1 = pg.mkPen("orange", width = 3)
        pen2 = pg.mkPen("yellow", width = 3)
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
