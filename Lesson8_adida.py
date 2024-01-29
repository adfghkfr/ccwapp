from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from bs4 import BeautifulSoup
import requests
import sys
import os
QPixmap

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('Lesson8_adida.ui', self)

        # Signals
        self.lineEdit_url.returnPressed.connect(self.urlSearch)
        self.pBut_search.clicked.connect(self.urlSearch)

    def urlSearch(self): 
        url = self.lineEdit_url.text()
        response = requests.get(url)
        img_dir = "/Users/guoyixuan/Documents/pythoncode/ccwapp/webscrap_img/"
        num_images = 12
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("img", class_="lazy", limit=num_images) #最多只要12張
        image_links = [result.get("data-original") for result in results]

        # download images and write as files
        for index, link in enumerate(image_links):
            img = requests.get(link)  
            with open(img_dir + str(index+1) + ".jpg", "wb") as file:
                file.write(img.content)  
                self.progressBar.setValue(int((index+1)/len(image_links)*100))
        
        # Show image files and then remove files
        for i in range(len(image_links)):
            imgname = img_dir + str(i+1) + ".jpg"
            setlabel = "self.label_"+str(i+1)+".setPixmap(QPixmap('" +imgname+"'))"
            exec(setlabel)
            #os.remove(imgname) # remove image files after display

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()