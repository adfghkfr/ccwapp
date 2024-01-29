from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtWebEngineWidgets import QWebEngineView 
from urllib.request import urlopen
from datetime import datetime
import folium
import pandas as pd
import json
import sys
import os
import io
 
 
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
        m = folium.Map(width="%100",weight="%100",tiles=None, overlay=False) # 完整的世界地圖
        fg1 = folium.FeatureGroup(name='Cases', overlay=False).add_to(m)
        fg2 = folium.FeatureGroup(name='Deaths', overlay=False).add_to(m)
 
        custom_scale = (self.df['cases'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
        # custom_scale = [0, 1e6, 2*1e6, 3*1e6, 4*1e6, 1e7, 9e7]
        folium.Choropleth(
                geo_data = self.geo_covid19,#Assign geo_data to your geojson file
                name = "Cases",
                data = self.df,#Assign dataset of interest
                columns = ["country","cases"],#Assign columns in the dataset for plotting
                key_on = 'feature.properties.name',#Assign the key that geojson uses to connect with dataset
                threshold_scale = custom_scale, #use the custom scale we created for legend
                fill_color = 'YlOrRd',
                nan_fill_color="White",
                fill_opacity = 0.7,
                line_opacity = 0.5,
                reset=True,
                legend_name = legendTxt).geojson.add_to(fg1)
 
        folium.Choropleth(
                geo_data = self.geo_covid19,#Assign geo_data to your geojson file
                name = "Deaths",
                data = self.df,#Assign dataset of interest
                columns = ["country","deaths"],#Assign columns in the dataset for plotting
                key_on = 'feature.properties.name',#Assign the key that geojson uses to connect with dataset
                threshold_scale = custom_scale, #use the custom scale we created for legend
                fill_color = 'YlOrRd',
                nan_fill_color="White",
                fill_opacity = 0.7,
                line_opacity = 0.5,
                reset=True,
                legend_name = legendTxt).geojson.add_to(fg2)
 
        #Add layer control to the map
        folium.TileLayer('cartodbdark_matter',overlay=True,name="View in Dark Mode").add_to(m)
        folium.TileLayer('cartodbpositron',overlay=True,name="Viw in Light Mode").add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
 
        data = io.BytesIO()
        m.save(data, close_file = False)
        webView = QWebEngineView()  # a QWidget
        webView.setHtml(data.getvalue().decode()) # html size < 2M
 
        self.verticalLayout.addWidget(webView, 0) # at position 0
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
  
if __name__ == '__main__':
    main()
