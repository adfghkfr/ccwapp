from PyQt6 import QtWidgets, uic
import numpy as np
from scipy.stats import norm
import sys
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        uic.loadUi('PyQtDesigner_switch_between_pages.ui', self)

        #讓程式碼跑完之後呈現在第一個頁面
        self.tabWidget.setCurrentIndex(0) # force the first tab to appear first
        #主視窗名稱
        self.setWindowTitle('Switch between pages')
         
        # Signal
        #第一個頁面的botton
        self.pBut_show.clicked.connect(self.sub_plot)
        #第二個頁面的botton
        self.pBut_main.clicked.connect(self.to_main)
 
    #Slots:
    
    def sub_plot(self): #按下第一個頁面的按鈕後的行動
        self.graphicsView.clear()
        mu = float(self.lineEdit_mu.text())
        s = float(self.lineEdit_sigma.text())
        x = np.linspace(mu - 5*s, mu + 5*s, 1000)
        y = norm.pdf(x, mu, s)
        self.graphicsView.plot(x, y) #在第二個頁面的畫面進行繪圖
        self.tabWidget.setCurrentIndex(1) #跳到第二頁

    
    def to_main(self):
        self.tabWidget.setCurrentIndex(0) #回到第0頁
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()