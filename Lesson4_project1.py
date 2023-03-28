from PyQt6 import QtWidgets, uic
import pyqtgraph as pg
import numpy as np
from scipy.stats import norm
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('Lesson4_project1.ui', self)
        self.setWindowTitle('PyQtGraph shows normal distribution')

        #signals
        #distribution/function
        self.comboBox_distri.currentIndexChanged.connect(self.update_plot)
        self.comboBox_finc.currentIndexChanged.connect(self.update_plot)
        #probability
        self.lineEdit_prob.returnPressed.connect(self.update_plot)
        self.lineEdit_prob.valueChanged.connect(self.comp_change)
        #x
        self.lineEdit_x.returnPressed.connect(self.update_plot)
        self.lineEdit_x.returnPressed.connect(self.comp_change)
        #mu
        self.lineEdit_muup.returnPressed.connect(self.update_plot)
        self.lineEdit_mu.returnPressed.connect(self.update_plot)
        self.lineEdit_mulow.returnPressed.connect(self.update_plot)
        #sigma
        self.lineEdit_sigup.returnPressed.connect(self.update_plot)
        self.lineEdit_sig.returnPressed.connect(self.update_plot)
        self.lineEdit_siglow.returnPressed.connect(self.update_plot)
        #slider
        self.verticalSlider_mu.valueChanged.connect(self.sliderMove) 
        self.verticalSlider_mu.sliderMoved.connect(self.sliderMove) 

        self.verticalSlider_sig.valueChanged.connect(self.sliderMove) 
        self.verticalSlider_sig.sliderMoved.connect(self.sliderMove) 

        self.update_plot()
    
    #slot
    def update_plot(self):
        self.graphWidget.clear() # clear current plot before plotting
        x = np.linspace(-5, 5, 1000)

        






def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()