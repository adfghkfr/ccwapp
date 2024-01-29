from PyQt6 import QtWidgets, QtCore, uic
from PyQt6.QtWidgets import QWidget
from scipy.stats import norm
import pyqtgraph as pg
import numpy as np
import sys
 
class AnotherWindow(QWidget):
    # create a customized signal 
    submitted = QtCore.pyqtSignal(str) # "submitted" is like a component name 
 
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('PyQtGraph_Designer_MultipleWin_sub.ui', self)
        self.setGeometry(600, 200, 400, 400)
         
        # Signal
        self.pBut_to_main.clicked.connect(self.on_submit)
     
    def passInfo(self, mu, s):
        self.lineEdit_sub_mu.setText(mu)
        self.lineEdit_sub_sigma.setText(s)
        mu = float(mu)
        s = float(s)
        self.graphicsView.clear()
 
        x = np.linspace(mu-5*s, mu+5*s, 1000)
        y = norm.pdf(x, mu, s)
        pen1 = pg.mkPen('y', width=3)
        self.graphicsView.plot(x, y, pen = pen1)
        self.graphicsView.showGrid(x=True, y=True, alpha = 1)
     
    def on_submit(self):
        # emit a signal and pass data along
        self.submitted.emit(self.lineEdit_sub_mu.text()) 
        self.close()
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        uic.loadUi('PyQtGraph_Designer_MultipleWin_main.ui', self)
        self.setWindowTitle('PyQtGraph shows normal distribution')
         
        # Signals
        self.pBut_graph.clicked.connect(self.call_subWin)
         
    # Slots
    def call_subWin(self):
        # create a sub-window
        self.anotherwindow = AnotherWindow()
        # pass information to sub-window
        self.anotherwindow.passInfo(self.lineEdit_mu.text(), self.lineEdit_s.text()) 
        # ready to accept a singal from sub-window
        self.anotherwindow.submitted.connect(self.update_info)
        self.anotherwindow.show()
     
    @QtCore.pyqtSlot(str) # respond to a signal emitted by the sub-window
    def update_info(self, mu):
        self.lineEdit_mu.setText(mu)
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()