from PyQt6 import QtWidgets, uic
import sys
 
class MainWindow(QtWidgets.QMainWindow):
   #元件widget
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('textdesign.ui', self)
        self.setWindowTitle('first qt')
         

        # signal
        #go_button:按鍵名字 ＃click:被點了
        self.go_button.clicked.connect(self.go)
        # push button按鈕的名字要是 
        #設定改變greeting的選項就可以直接改變output
        self.greeting.currentIndexChanged.connect(self.go) #可以跟這個go buttom 共用一個訊號
        #設定改變recipent的字按enter就可以直接得到改變後的結果
        self.recipient.returnPressed.connect(self.go)
        
    # slot
    def go(self): #go函數可以使用這個class裡面所有的元件
        str1 = self.greeting.currentText() #現在combo box 的名字是greeting
        #currentText:現在誰被選到 
        #text:recipient裡面的文字是什麼
        str2 = self.recipient.text() #現在line edit 的名字是recipent
        self.greet_rep.setText(str1 + ' ' + str2) #現在label 的名字是greet_rep


#啟動另一個畫面
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

#error: main window object has no attribute greeting
#qtdesign叫什麼名字要跟python檔配合

#選了選項之後發出訊號-必須要有動作
#指令啟動訊號
#signals:訊號
#slots:動作




