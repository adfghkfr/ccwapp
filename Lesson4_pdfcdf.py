from PyQt6 import QtWidgets, uic
import pyqtgraph as pg
import numpy as np
from scipy.stats import norm
import sys

#寫
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('Lesson4_pdfcdf.ui', self)
        self.setWindowTitle('PyQtGraph shows normal distribution')
        self.pdfcdf_status = 1 
        #一開始默認pdfcdf_status=1
 
        # Signals
        # 追蹤所有元件動作
        self.pdfcdf.clicked.connect(self.update_plot)
        #按pdf,cdf的按鍵-改變圖片呈現
        self.checkBox_Grid.stateChanged.connect(self.gridon)
        #改變grid on or off #是否加入grid線
        self.lineEdit_x.returnPressed.connect(self.comp_cdf)
        #輸入lineedit的x的值
        self.lineEdit_cdfx.returnPressed.connect(self.comp_invcdf)
        #輸入lineedit的cdf的值
        self.hSlider_x.valueChanged.connect(self.sliderMove) 
        self.hSlider_x.sliderMoved.connect(self.sliderMove) 
        #兩者都可以偵測到值的改變
        self.update_plot()
         
    # Slots
    # 所有slot都有第一個參數self
    def update_plot(self):
        self.graphWidget.clear() # clear current plot before plotting
        x = np.linspace(-5, 5, 1000)
        if self.pdfcdf_status == 1: #一開始默認pdfcdf_status=1，繪製pdf圖
            y = norm.pdf(x)
            titlename = "PDF"
        else: #改變pdfcdf_status，繪製cdf圖
            y = norm.cdf(x)
            titlename = "CDF"
        pen = pg.mkPen(color=(250, 0, 0), width = 5)  #pdf的線的顏色與粗細
        # Qt.DotLine, Qt.DashDotLine and Qt.DashDotDotLine
        #make pen which control plot

        cur1 = self.graphWidget.plot(x, y, pen = pen, name = 'Demo')
        cur2 = self.graphWidget.plot(x, np.zeros(len(y)))
        # add color patch under curve
        patchcur = pg.FillBetweenItem(curve1 = cur1, curve2 = cur2, brush = 'yellow')
        #brush:顏色底色

        if self.pdfcdf_status == 1: #繪製pdf圖時
            self.graphWidget.addItem(patchcur)
         
        self.graphWidget.setBackground('white') #圖片底色設定為白色
        self.graphWidget.setTitle(titlename, color="skyblue", size="14pt") #title的顏色跟字體大小
        styles = {'color':'red', 'font-size':'16px'}
        self.graphWidget.setLabel('left', 'Y', **styles) #label: y的顏色與字體大小
        self.graphWidget.setLabel('bottom', 'X', **styles) #label: x的顏色與字體大小
        self.graphWidget.showGrid(x=False, y=False) #都設為false交給check box來控制
        self.pdfcdf_status = -self.pdfcdf_status #紀錄1是pdf 2是cdf

    #為什麼傳入兩個參數
    #s 告訴你現在的狀態
    def gridon(self, s): #設定是否要有grid
        # print(self.checkBox_Grid.checkState()) ＃也可以利用checkState確認現在是被按還是沒被按
        # 可以選擇不要接收這個訊號
        if s == 2: # 0 : unchecked; 2 : checked
            self.graphWidget.showGrid(x = True, y = True)   
        else:
            self.graphWidget.showGrid(x = False, y = False)   
 
    def comp_cdf(self): #cdf
        cdf = norm.cdf(float(self.lineEdit_x.displayText())) 
        self.lineEdit_cdfx.setText(str(round(cdf, 4))) #改變數值來改變cdf的值
        self.hSlider_x.setValue(int(float(self.lineEdit_x.displayText())))
        #改變游標的值
 
    def comp_invcdf(self): #pdf
        x = norm.ppf(float(self.lineEdit_cdfx.displayText()))
        self.lineEdit_x.setText(str(round(x, 4))) #改變數值來改變x的值
     
    def sliderMove(self, x): #滑動游標
        self.lineEdit_x.setText(str(round(x, 4))) #改變line edit中x的值
        self.lineEdit_cdfx.setText(str(round(norm.cdf(x), 4))) #改變line edit中cdf的值
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()