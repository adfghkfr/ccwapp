from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
import sys
 
#欲呈現
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        self.picName = ["ridge1", "ridge2", "ridge3"]
 
        #Load the UI Page by PyQt6
        uic.loadUi('Lesson3_imageinput.ui', self)
        self.setWindowTitle('Show images on the label widget')
        #url = "https://new.ntpu.edu.tw/"
        #self.label_urlname(f'<a style="text-decoration: none" href="{url}">{url}</a>')
        # should have quotes around url, i.e. href="https://...."
        #self.label_url(True) # can be set True in Designer
 
        # Signals
        self.comboBox_ImgName.currentIndexChanged.connect(self.showImg)
        self.pBut_exit.clicked.connect(self.close)
 
# Slots
    def showImg(self, s):#利用s撈到圖檔名
        self.label_image(QPixmap("/Users/guoyixuan/Documents/pythoncode/ccwapp/image" + self.picName[s]))
        self.label_imagename(self.comboBox_ImgName.itemText(s)) # set Label text
        # self.label_cap.setText(self.comboBox_ImgName.currentText())
     
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()

