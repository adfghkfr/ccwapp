# Show web-content in pyqt6 + Designer

from PyQt6.QtWebEngineWidgets import QWebEngineView # pip install PyQt6-WebEngine
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QUrl
import sys

"""
Folium in PyQt6
"""
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        uic.loadUi('Lesson11_Browser.ui', self)
        self.urlBrowser()

        # signals
        self.lineEdit_url.returnPressed.connect(self.urlBrowser)

    def urlBrowser(self):
        # url = 'https://new.ntpu.edu.tw/'
        url = "https://" + self.lineEdit_url.text()
        webView = QWebEngineView()
        webView.load(QUrl(url))
        # browser.show()
        # clear the current widget in the verticalLayout before adding one
        if self.verticalLayout.itemAt(0) : # if any existing widget
            self.verticalLayout.itemAt(0).widget().setParent(None)
        
        self.verticalLayout.addWidget(webView)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()