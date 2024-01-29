from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6 import QtWidgets, uic
import folium
import pandas as pd
import sys
import io

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
         
        uic.loadUi('Lesson11_GeoMap_tooltip.ui', self)

        self.df = pd.read_excel("/Users/guoyixuan/Documents/pythoncode/ccwapp/cow_farm.xlsx")
        self.show_map()
    
    def show_map(self):
        coordinates_lat = self.df['緯度']
        coordinates_lon = self.df['經度']

        loc_names = self.df['牧場']
        m = folium.Map(
            titles = "Stamen Terrain",
            zoom_start = 8,
            location = (23.73, 120.96)
        )

        data = io.BytesIO()

        for i in range(len(loc_names)):
            folium.CircleMarker(location = [coordinates_lat[i], coordinates_lon[i]], 
                                radius = 3,
                                color = 'blue', 
                                tooltip = loc_names[i],
                                popup = loc_names[i] + str(coordinates_lat[i]) + "," + str(coordinates_lon[i]),
                                fill_color = 'red').add_to(m)
        
        m.save(data, close_file = False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())

        # clear the current widget in the vertical layout
        if self.verticalLayout.itemAt(0):
            self.verticalLayout.itemAt(0).widget().setParent(None)
        
        # add a widget with webview inside the vertical layout component
        self.verticalLayout.addWidget(webView, 0)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()

 