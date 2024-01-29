# Use folium.Choropleth, folium.GeoJson, folium.GeoJsonTooltip
# However, when the resulted html file > 2M, it fails to show the map as a widget
# Instead, can use selenium to save screen_shot image.
# Reference: https://towardsdatascience.com/folium-and-choropleth-map-from-zero-to-pro-6127f9e68564#:~:text=In%20Python%2C%20there%20are%20several%20graphing%20libraries%20that,country%20with%20a%20variety%20of%20flavors%20and%20designs.

from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtWebEngineWidgets import QWebEngineView 
import folium.folium
import geopandas as gpd
import pandas as pd
import json
import sys
import time
import os
import io
from pathlib import Path
from selenium import webdriver

Dataset=pd.read_excel('/Users/guoyixuan/Documents/pythoncode/ccwapp/Taiwan_population.xlsx') # 讀入台灣人口數
json_file_path = r'/Users/guoyixuan/Documents/pythoncode/ccwapp/geo_taiwan_short.json'
# 讀入台灣行政區地理資料並取行政區名稱與界線經緯度
geojson = gpd.read_file(json_file_path, encoding='utf-8')
geojson=geojson[['name','geometry']]
# 整合人口數資料與行政區地理資料為單一 pandas 變數
df_final = geojson.merge(Dataset, left_on="name", right_on="City/County", how="outer") 
df_final = df_final[~df_final['geometry'].isna()]

with open(json_file_path, 'r', encoding='utf-8') as j:
     geo_taiwan = json.loads(j.read())
     

class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
         
        uic.loadUi('Lesson11_GeoMap_tooltip.ui', self)
        self.show_map()

        
    def show_map(self):
        current_dir = Path(__file__).resolve().parent
        m = folium.Map(location=[23.73, 120.96], zoom_start=7)
        folium.Choropleth(
                geo_data = geo_taiwan,#Assign geo_data to your geojson file
                name = "choropleth",
                data = df_final,#Assign dataset of interest
                columns = ["City/County","Population"],#Assign columns in the dataset for plotting
                key_on = 'feature.properties.name',#Assign the key that geojson uses to connect with dataset
                fill_color = 'YlOrRd',
                fill_opacity = 0.7,
                line_opacity = 0.5,
                reset=True,
                legend_name = '台灣縣市人口').add_to(m)
        
        folium.GeoJson(
                data=df_final, #Dataset merged from pandas and geojson
                name='Populations',
                smooth_factor=2,
                style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.1},
                tooltip=folium.GeoJsonTooltip(
                       fields=['City/County',
                                'Population'
                               ],
                       aliases=['行政區',
                                '人口數'
                                ], 
                        localize=True,
                        sticky=False,
                        labels=True,
                        style="""
                            background-color: #F0EFEF;
                            border: 2px solid black;
                            border-radius: 3px;
                            box-shadow: 3px;
                        """,
                        max_width=800),
                highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                        ).add_to(m) 

        data = io.BytesIO()
        m.save(data, close_file = False)
        filename = os.fspath(current_dir / "map.html")
        m.save(filename)
        self.webEngineView.setHtml(data.getvalue().decode())
#-----------------------------------------------------
        # if html size > 2M, not successful yet
        # html_map = QtCore.QUrl.fromLocalFile(filename)
        # webView.load(html_map)
        # webView.loadFinished.connect(self.set_map_data)
        
#-------------------------------------------------------
        # save the screen shot of the currently saved  html file
        # driver = webdriver.Edge('msedgedriver') # need Edge driver msedgedriver.exe, current version is 101.0.1210.53
        # driver.get(filename)
        # time.sleep(5) # wait for 5 seconds for the maps and other assets to be loaded in the browser
        # driver.save_screenshot('output.png')
        # driver.quit()
        # self.label_img.setPixmap(QtGui.QPixmap("output.png"))
        
# ---------------------------------------------
        # self.verticalLayout.addWidget(webView, 0) # at position 0
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()
