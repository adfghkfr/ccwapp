from PyQt6 import QtWidgets, uic
import matplotlib.image as mpimg
import pyqtgraph as pg
import sys
import os
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('Lesson4_image.ui', self)
        self.setWindowTitle('Show images on the graphicView widget')
 
        self.file_src = "/Users/guoyixuan/Documents/pythoncode/ccwapp/image/"
        self.picName = os.listdir(self.file_src)
        self.comboBox_ImgName.addItems(self.picName)
        self.showImg(0)
         
        # Signal
        self.comboBox_ImgName.currentIndexChanged.connect(self.showImg)
        self.pBut_exit.clicked.connect(self.close)
    # Slots
    def showImg(self, s):
        self.graphWidget.clear()
        img_dir = "/Users/guoyixuan/Documents/pythoncode/ccwapp/image/"
        img_name = self.comboBox_ImgName.currentText()
        image = mpimg.imread(img_dir + img_name)
        img_item = pg.ImageItem(image, axisOrder='row-major')
         
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.getAxis('bottom').setTicks('')
        self.graphWidget.getAxis('left').setTicks('')
        self.graphWidget.setAspectLocked(lock=True, ratio=1)
         
        self.label_cap.setText(img_name) # set Label text
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()