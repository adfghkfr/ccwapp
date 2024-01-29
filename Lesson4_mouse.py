from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
import pyqtgraph as pg
from scipy.stats import norm
import numpy as np
import sys
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # 呼叫mainwindow
        #Load the UI Page by PyQt6
        uic.loadUi('Lesson4_mouse.ui', self)
        self.setWindowTitle('Mouse Move')
        
        self.update_plot('PDF')
 
        # Signales
        self.gView.scene().sigMouseMoved.connect(self.mouseMoved) #捕捉滑鼠
        # self.groupBox.toggled.connect(self.pdfcdf_clicked) # suitable for checkbox, not radiobutton
        self.radioBut_PDF.toggled.connect(self.pdfcdf_clicked)
        self.radioBut_cdf.toggled.connect(self.pdfcdf_clicked)
        self.pushBtn_exit.clicked.connect(self.dialogBox)
 
    #str: pdf or cdf
    def update_plot(self, str):
        self.gView.clear()
        x = np.linspace(-5, 5, 1000)
        if str == 'PDF':
            y = norm.pdf(x)
            title = 'Exercise : Add color patch as the mouse moves'
        else:
            y = norm.cdf(x)
            title = "Exercise : Let HLine go with the CDF value"
         
        self.gView.plot(x,y) # generates a PlotDataItem
        # 加入垂直線水平線
        self.vLine = pg.InfiniteLine(pos = 1, angle=90, movable=False)
        self.hLine = pg.InfiniteLine(pos = 0.2, angle=0, movable=False)
        self.gView.addItem(self.vLine) # add PlotDataItem in PlotWidget 
        self.gView.addItem(self.hLine)
        self.gView.setTitle(title)
 
    # Slots:
    def mouseMoved(self, point): # returns the coordinates in pixels with respect to the PlotWidget
        p = self.gView.plotItem.vb.mapSceneToView(point) # convert to the coordinate of the plot
        # 是否有滑鼠click的訊號
        # 讓垂直水平線跟著滑鼠進行移動
        self.vLine.setPos(p.x()) # set position of the verticle line
        self.hLine.setPos(p.y()) # set position of the horizontal line
        self.lineEdit_x.setText(str(round(p.x(), 4))) 
        self.lineEdit_cdf.setText(str(round(norm.cdf(p.x()), 4))) 
 
    def pdfcdf_clicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.update_plot(radioBtn.text())
            # print(radioBtn.text())
     
    def dialogBox(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Wang's Class Demo")
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