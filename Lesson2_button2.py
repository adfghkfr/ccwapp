from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

# 寫一個class
class MyWindow(QMainWindow): # inherit QMainWindow that provides a main application window
# MyWindow:自己取名
#class:裡面可以包含 attibute(公用變數) method(方法)
    def __init__(self): #method
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 400, 320) #位置
        self.setWindowTitle('Hello Title') #視窗title
        
        # attribute
        self.label = QtWidgets.QLabel(self) # self = mainwindow 
        # self: 辨識的鑰匙，用來取得裡面的東西
        self.label.setText('This is my first Label')
        self.label.setGeometry(0, 0, 200,20) # (x, y, width, length)
        self.label.move(200, 100)
        self.label.setStyleSheet("border: 1px solid red;")
        self.label.adjustSize()
        # 做了一顆按鈕
        pbut = QtWidgets.QPushButton(self)
        pbut.setText('Push Me')
        # signal ＃動作上的設定
        pbut.clicked.connect(self.pushme) # 如果button被按了，傳遞到下面的def push me
        # 此按鈕被啟動再影響別人-某個計算被啟動並影響別人
 
    # slot # self一直在傳遞
    def pushme(self): #把東西印到label上 #method
        self.label.setText('My second text')
        self.label.adjustSize()
 
def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()  

