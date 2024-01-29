from PyQt6 import QtWidgets #第六版qt
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

# 做app跟一般的程式有什麼不同？程式始終存在不會結束
def pushme():
    print('clicked...') 

# 取得一個window代碼（主視窗）
# 定義整個視窗的產生
def main():
    app = QApplication(sys.argv) #率先開啟應用程式
    win = QMainWindow() #window
    #較小型視窗：QWidget
     
    # Configure the main window
    win.setGeometry(200, 200, 400, 320) #window size
    win.setWindowTitle('Hello Title') #程式名稱 
 
    # create a label and its associated properties
    label = QtWidgets.QLabel(win)
    label.setText('This is my first Label') # 按鈕上寫字
    label.setGeometry(0, 0, 200, 20) # (x, y, width, length)
    label.move(200, 150) #x,y軸座標概念
    label.setStyleSheet("border: 1px solid black;")
    label.adjustSize() # to fit the text length
 
    # create a pushbutton
    pbut = QtWidgets.QPushButton(win)
    pbut.setText('按我')
    pbut.clicked.connect(pushme) #副程式：可以做一些別的事
 
    win.show() #show 出來才會開始跑
    #app.exec()
    sys.exit(app.exec()) #啟動app #當他退出時window會幫忙清理戰場，把垃圾都清掉
 
if __name__ == '__main__': # run by itself, not by other application
    main()

