from PyQt6 import QtWidgets, uic
import pyqtgraph as pg
import numpy as np
from scipy.stats import norm
from scipy.stats import t
import sys


class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('CI.ui', self)
        self.setWindowTitle('PyQtGraph shows normal distribution')
       
        # Signals
        self.CBX_function.currentIndexChanged.connect(self.update_plot)
        self.CBX_distribution.currentIndexChanged.connect(self.update_plot)
        self.LE_mu.returnPressed.connect(self.update_plot)
        self.LE_upper.returnPressed.connect(self.update_plot)
        self.LE_lower.returnPressed.connect(self.update_plot)
        
        self.LE_sigma.returnPressed.connect(self.update_plot)
        self.LE_upper_sigma.returnPressed.connect(self.update_plot)
        self.LE_lower_sigma.returnPressed.connect(self.update_plot)
        
        self.SLD_mu.valueChanged.connect(self.sliderMove_mu)
        self.SLD_sigma.valueChanged.connect(self.sliderMove_sigma)
        
        self.LE_x_vlaue.returnPressed.connect(self.update_plot)
        # set slider range and initial value
        # self.SLD_mu.setRange(int(self.LE_lower.text()), int(self.LE_upper.text()))
        # self.SLD_mu.setValue(int(self.LE_mu.text()))
        # self.hSlider_x.sliderMoved.connect(self.sliderMove)
        self.update_plot()
        
        
    # Slots
    def update_plot(self):
        self.gViews.clear() # clear current plot before plotting
        Upper = int((self.LE_upper.text()))
        Lower = int((self.LE_lower.text()))
        distribution = self.CBX_distribution.currentText()
        function = self.CBX_function.currentText()
        mu=int((self.LE_mu.text()))
        sigma=float((self.LE_sigma.text()))
        x_value = int((self.LE_x_vlaue.text()))
        x = np.linspace(mu-10 , mu+10, 1000)
        
        
        
        if distribution == "Normal" and function=="PDF":
            y = norm.pdf(x,loc=mu , scale=sigma)
            titlename = "PDF"
        elif distribution == "Normal" and function=="CDF":
            y = norm.cdf(x,loc=mu , scale=sigma)
            titlename = "CDF"
            
            
       
            
        pen = pg.mkPen(color=(255, 0, 0), width = 10) # Qt.DotLine, Qt.DashDotLine and Qt.DashDotDotLine
        self.vLine = pg.InfiniteLine(pos=x_value, angle=90, movable=False)
        self.gViews.addItem(self.vLine)

        
        cur1 = self.gViews.plot(x, y, pen = pen, name = 'Demo')
       
        # zero_line = pg.PlotDataItem(np.arange(Lower ,x_value , Lower ,len(y)), np.zeros(len(y)), pen='k')
        # patchcur = pg.FillBetweenItem(curve1=cur1, curve2=zero_line, brush='g')
        # self.gViews.addItem(patchcur)
        # self.vLine = pg.InfiniteLine(pos=x_value, angle=90, movable=False)
        # self.gViews.addItem(self.vLine)


    

     
    def sliderMove_mu(self, x):
        self.SLD_mu.setRange(int(self.LE_lower.text()), int(self.LE_upper.text()))
        self.SLD_mu.setValue(int(self.LE_mu.text()))
        self.LE_mu.setText(str(round(x,4)))
        self.update_plot()
    
    def sliderMove_sigma(self, x):
        if int(self.LE_lower_sigma.text()) >0:
            self.SLD_sigma.setRange(int(self.LE_lower_sigma.text()), int(self.LE_upper_sigma.text()))
            self.SLD_sigma.setValue(int(self.LE_sigma.text()))
            self.LE_sigma.setText(str(round(x,4)))
        self.update_plot()
        
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()