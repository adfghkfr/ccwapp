# Use folium.Choropleth
# However, when the resulted html file > 2M, it fails to show the map as a widget
# Instead, can use selenium to save screen_shot image.
# Data source: https://data.cdc.gov.tw/zh_TW/dataset/covid-19countrystatsjson

from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtWebEngineWidgets import QWebEngineView 
from urllib.request import urlopen
from datetime import datetime
# from pathlib import Path
import folium
import pandas as pd
import json
import sys
import os
import io
# import time
# from selenium import webdriver

class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
         
        uic.loadUi('Lesson11_Covid19_world.ui', self)
        #------------------------------------------------------
        # collect data from URL
        JSON = 'https://od.cdc.gov.tw/eic/covid19/covid19map.json'
        with urlopen(JSON) as f:
            self.geo_covid19 = json.load(f)

        # open local data file
        # json_file_path = r'../Data/covid19map.json'
        # with open(json_file_path, 'r', encoding='utf-8') as j:
        #     self.geo_covid19 = json.loads(j.read())
        #------------------------------------------------------
        # prepare data and display some statistics on the labels
        # 把城市、確診人數和死亡人數的資料抓進來
        self.df = pd.DataFrame(columns=['country', 'cases', 'deaths'])
        data = self.geo_covid19['features']
        for i in range(len(data)):
            self.df.loc[i] = [data[i]['properties']['name'], 
                            data[i]['properties']['cases'], 
                            data[i]['properties']['deaths']
                            ]
          
        cases_global = self.df['cases'].sum()
        cases_taiwan = self.df['cases'][self.df['country'].str.contains('Taiwan')]
        self.label_cases.setText("{:,}".format(cases_taiwan.iloc[0]) + '/' + "{:,}".format(cases_global))
        deaths_global = self.df['deaths'].sum()
        deaths_taiwan = self.df['deaths'][self.df['country'].str.contains('Taiwan')]
        self.label_deaths.setText("{:,}".format(deaths_taiwan.iloc[0]) + '/' + "{:,}".format(deaths_global))
        #------------------------------------------------------
        self.show_map()
        
    def show_map(self):
        #----- display current date and time -------------
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        legendTxt = '確診人數:' + dt_string
        self.label_date.setText(legendTxt)
        #-------------------------------------------------
        m = folium.Map(width="%100",weight="%100") # 完整的世界地圖
        # 地圖呈現顏色設定
        # custom_scale = (self.df['cases'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
        # custom_scale = [0, 1e6, 2*1e6, 3*1e6, 4*1e6, 1e7, 9e7]

        # 把資料跟地圖結合
        folium.Choropleth(
                geo_data = self.geo_covid19,# Assign geo_data to your geojson file
                name = "choropleth",
                data = self.df, # Assign dataset of interest # pandas
                # self.df dataframe: country, cases, deaths
                # Assign columns in the dataset for plotting
                columns = ["country","cases"],
                # country # see the json file
                key_on = 'feature.properties.name',
                # Assign the key that geojson uses to connect with dataset
                # threshold_scale = custom_scale, # use the custom scale we created for legend 
                fill_color = 'YlOrRd',
                nan_fill_color = "White",
                fill_opacity = 0.7,
                line_opacity = 0.5,
                reset=True,
                legend_name = legendTxt).add_to(m)
        
        # 可能因為 geometry 資料不齊全，下列 tooltip 沒有成功
        # folium.features.GeoJson(
        #         data=self.df,
        #         name='Cases',
        #         smooth_factor=2,
        #         style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
        #         tooltip=folium.features.GeoJsonTooltip(
        #                fields=['country',
        #                         'cases',
        #                         'deaths'
        #                        ],
        #                 aliases=['country',
        #                         'cases',
        #                         'deaths'
        #                         ], 
        #                 localize=True,
        #                 sticky=False,
        #                 labels=True,
        #                 style="""
        #                     background-color: #F0EFEF;
        #                     border: 2px solid black;
        #                     border-radius: 3px;
        #                     box-shadow: 3px;
        #                 """,
        #                 max_width=800),
        #         highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
        #                 ).add_to(m) 

        data = io.BytesIO()
        m.save(data, close_file = False)
        # current_dir = Path(__file__).resolve().parent
        # filename = os.fspath(current_dir / "map.html")
        # m.save(filename)
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
    
    # def set_map_data(self):
    #     print("I am here !!")
        # js = "setData({0})".format(self.data)
        # self.webView.page().runJavaScript(js)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()
