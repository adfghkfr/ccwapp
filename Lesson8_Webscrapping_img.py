from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from bs4 import BeautifulSoup
import requests
import sys
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('Lesson8_Webscrapping_img.ui', self)

        # Signals
        self.lineEdit_url.returnPressed.connect(self.urlSearch)
        self.pBut_search.clicked.connect(self.urlSearch)

    def urlSearch(self): 
        url = "https://unsplash.com/s/photos/"
        url = url + self.lineEdit_url.text()
        # 取出html裡面所有的文字
        response = requests.get(url)
        img_dir = "/Users/guoyixuan/Documents/pythoncode/ccwapp/webscrap_img/"
        num_images = 12
        # 只關注html的部分
        soup = BeautifulSoup(response.text, "html.parser")
        # the class 
        # results = soup.find_all("img", class_="YVj9w", limit=num_images)
        results = soup.find_all("img", class_="ht4YT", limit=num_images) #最多只要12張
        # results = soup.find_all("img", limit=num_images)
        image_links = [result.get("src") for result in results]

        # download images and write as files
        for index, link in enumerate(image_links):
            img = requests.get(link)  
            with open( img_dir + str(index+1) + ".jpg", "wb") as file:
                file.write(img.content)  
                self.progressBar.setValue(int((index+1)/len(image_links)*100))
        
        # Show image files and then remove files
        for i in range(len(image_links)):
            imgname = img_dir + str(i+1) + ".jpg"
            setlabel = "self.label_"+str(i+1)+".setPixmap(QPixmap('" +imgname+"'))"
            exec(setlabel)
            os.remove(imgname) # remove image files after display

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()