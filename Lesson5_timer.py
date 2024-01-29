from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import numpy as np
from scipy.stats import norm
import sys
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('Lesson5_timer.ui', self)
        self.setWindowTitle('Monitor two signals: Timer')
 
        # prepare data
        fs = 100;    # sampling frequency (Hz)
        self.x = np.arange(0, 10, 1/fs) 
        self.y = 1.3*np.sin(2*np.pi*15*self.x) + \
                1.7*np.sin(2*np.pi*40*(self.x-2)) + \
                norm.rvs(size = len(self.x))
        
        self.y2 = np.sin(2*np.pi*5*self.x) + \
                2*np.sin(2*np.pi*10*self.x) + \
                norm.rvs(size = len(self.x))                
        self.start, self.end = 0, 100               
 
        #畫圖顏色：紅色
        pen = pg.mkPen(color=(255, 0, 0))
        x_show = self.x[self.start:self.end] 
        y_show = self.y[self.start:self.end]

        y2_show = self.y2[self.start:self.end]

        self.data_line =  self.graphWidget.plot(x_show, y_show, pen=pen)

        #第一張圖的相關設定
        styles = {'color':'green', 'font-size':'16px'}
        self.graphWidget.setLabel('left', 'Signal 1', **styles)
        self.graphWidget.setLabel('bottom', 'Time (in Secs)', **styles)
        self.graphWidget.setYRange(-6, 6, padding=0)
 
        #第二張圖的相關設定
        self.data_line2 =  self.graphWidget2.plot(x_show, y2_show, pen=pen)
        styles = {'color':'green', 'font-size':'16px'}
        self.graphWidget2.setLabel('left', 'Signal 2', **styles)
        self.graphWidget2.setLabel('bottom', 'Time (in Secs)', **styles)
        self.graphWidget2.setYRange(-6, 6, padding=0)
 
        #signal
        self.timer = QTimer() #開啟計時器
        timeInterval = 60 
        #設定時間單位
        self.timer.setInterval(timeInterval) 
        # milliseconds, i.e, 1 sec = 1000 millisecond
        # 代表設定時間到了之後要啟動的事件
        self.timer.timeout.connect(self.update_plot_data) # emit every timeInterval millisecond
        self.push_stop.clicked.connect(self.stopMoving)
        self.push_start.clicked.connect(self.startMoving)
        self.timer.start()

    #slot
    def update_plot_data(self):
        self.start += 1
        self.end += 1
        if self.end <= len(self.y):
            # use setData to change the line instead of clearing and redrawing plot.
            self.data_line.setData(self.x[self.start:self.end], self.y[self.start:self.end])  # Update the data.
            self.data_line2.setData(self.x[self.start:self.end], self.y2[self.start:self.end])  # Update the data.
        else:
            self.timer.stop()
 
    def stopMoving(self):
        self.timer.stop()
     
    def startMoving(self):
        self.timer.start()
 
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()