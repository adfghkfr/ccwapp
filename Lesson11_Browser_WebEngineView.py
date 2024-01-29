# Show web-content in pyqt6 + Designer

from PyQt6.QtWebEngineWidgets import QWebEngineView # pip install PyQt6-WebEngine
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtCore import QUrl
import urllib.request
import sys


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        uic.loadUi('Lesson11_Browser_WebEngineView.ui', self)
        #self.getIcon('https://cdn-icons-png.flaticon.com/512/93/93641.png', 'label_reload')
        #self.getIcon('https://cdn-icons-png.flaticon.com/512/570/570220.png',  'label_back')
        #self.getIcon('https://cdn-icons-png.flaticon.com/512/570/570221.png', 'label_forward')
        self.label_back.setHidden(True)
        self.label_forward.setHidden(True)
        self.urlBrowser()

        # signals
        self.lineEdit_url.returnPressed.connect(self.urlBrowser)
        self.webEngineView.page().urlChanged.connect(self.urlChanged)
        self.webEngineView.page().urlChanged.connect(self.onLoadFinished)
        self.label_back.installEventFilter(self)
        self.label_forward.installEventFilter(self)
        self.label_reload.installEventFilter(self)

    def urlBrowser(self):
        # url = "https://" + self.lineEdit_url.text()
        url = self.lineEdit_url.text()
        self.webEngineView.load(QUrl(url))
        

    def getIcon(self, imglink, label):
        data = urllib.request.urlopen(imglink).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        tmp = f'self.{label}.setPixmap(QtGui.QPixmap(image))'
        exec(tmp)

    def eventFilter(self, obj, event):
        if obj is self.label_back and event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            self.back()
        if obj is self.label_forward and event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            self.forward()
        if obj is self.label_reload and event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            self.reload()
        return super().eventFilter(obj, event)
    
    def back(self):
        self.webEngineView.back()

    def forward(self):
        self.webEngineView.forward()
    
    def reload(self):
        self.webEngineView.reload()
    
    def urlChanged(self, url):
        self.lineEdit_url.setText(url.toString())
    
    def onLoadFinished(self):
        if self.webEngineView.history().canGoBack():
            self.label_back.setHidden(False)
        else:
            self.label_back.setHidden(True)

        if self.webEngineView.history().canGoForward():
            self.label_forward.setHidden(False)
        else:
            self.label_forward.setHidden(True)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()