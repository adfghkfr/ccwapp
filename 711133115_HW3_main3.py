from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6 import QtWidgets, uic
import folium
import pandas as pd
import sys
import io
import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableView, QProgressDialog, QPushButton
from PyQt6.QtCore import Qt
import pandas as pd
from PyQt6.QtWidgets import QDialog
import math
from PyQt6.QtGui import QStandardItemModel, QIcon
from PyQt6.QtWidgets import QTableView, QTableWidgetItem, QTableWidget
from bs4 import BeautifulSoup
import requests
import os
from PyQt6.QtGui import QPixmap
from googlesearch import search
from PyQt6.QtCore import QUrl
import time
import numpy as np
import matplotlib.pyplot as plt
import pyqtgraph as pg

# -------------------------------------------------------------------------------
class TableModel(QtCore.QAbstractTableModel):
 
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
 
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()] #pandas's iloc method
            return str(value)
 
        if role == Qt.ItemDataRole.TextAlignmentRole:          
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
         
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('#d8ffdb')
 
    def rowCount(self, index):
        return self._data.shape[0]
 
    def columnCount(self, index):
        return self._data.shape[1]
    
    def initUI(self):
        self.model = QStandardItemModel(10, 10)
        self.tableview = QTableView()
    #    # 关联QTableView控件和Model
        self.tableview.setModel(self.model)

    # Add Row and Column header
    def headerData(self, section, orientation, role):
    #    # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole: # more roles
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
 
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
            
# -------------------------------------------------------------------------------

# 第二個子視窗
class Subwindow(QDialog):
    # create a customized signal 
    submitted = QtCore.pyqtSignal(str) 
    def __init__(self):
        super().__init__()
        uic.loadUi('HW3_subbrowser.ui', self)
        #self.urlBrowser()

        self.setWindowTitle('美國大學網站')
        self.resize(1200, 1000)
    
    def urlBrowser(self, url):
        for j in search(url, tld="co.in", num=10, stop=1, pause=2):
            url = j
        time.sleep(10)
        webView = QWebEngineView()
        webView.load(QUrl(url))
        # browser.show()
        # clear the current widget in the verticalLayout before adding one
        if self.verticalLayout.itemAt(0) : # if any existing widget
            self.verticalLayout.itemAt(0).widget().setParent(None)
                
        self.verticalLayout.addWidget(webView)

# -------------------------------------------------------------------------------

###第一個子視窗###
class AnotherWindow(QDialog):
    # create a customized signal 
    submitted = QtCore.pyqtSignal(str) # "submitted" is like a component name 
 
    def __init__(self):
        super().__init__()
        uic.loadUi('HW3_subcollege.ui', self)
        self.setGeometry(1600, 1000, 1000, 1000)
        self.setWindowTitle('美國大學介紹')
        self.resize(700, 1000)
         
        # Signal
        # 回到主視窗
        self.pushButton_close.clicked.connect(self.on_submit)
        self.pushButton_browser.clicked.connect(self.school_browser)
    
    def school_browser(self):
        query = self.label_college.text()
        self.webbrowser = Subwindow()
        self.webbrowser.urlBrowser(query)
        self.webbrowser.show()

    def on_submit(self):
        self.close()

    # slot
    def rowSelected(self, parent, college_name):
        self.label_college.setText(college_name)
        # 進入該大學介紹網站
        intro_link_url = 'https://www.ieeuc.com.tw' + parent['href']
        intro_college = requests.get(intro_link_url)
        intro_soup = BeautifulSoup(intro_college.text, 'html.parser')
        # 學校概觀
        intro_results = intro_soup.find('div', class_ = 'txt editor').text
        self.textBrowser_abstract.setText(intro_results)
        # 主要學院
        intro_major = intro_soup.find('div', id = 'menu1').text
        self.textBrowser_major.setText(intro_major)
        # 學校特色
        intro_character = intro_soup.find('div', id = 'menu4').text
        self.textBrowser_character.setText(intro_character)
        # 校園圖片
        pic_results = intro_soup.find_all('a', href = '#', limit = 3)
        image_links = []
        for i in pic_results:
            image = i.find('img')
            image_links.append('https://www.ieeuc.com.tw/' + image['src'])
        
        img_dir = "/Users/guoyixuan/Documents/pythoncode/ccwapp/webscrap_img/"
        # download images and write as files
        for index, link in enumerate(image_links):
            img = requests.get(link)  
            with open( img_dir + str(index+1) + ".jpg", "wb") as file:
                file.write(img.content)  
        
        imgname = img_dir + str(1) + ".jpg"
        self.label_1.setPixmap(QPixmap(imgname))
        self.label_1.setScaledContents(True)
        self.label_1.setFixedSize(207, 186)

        imgname = img_dir + str(2) + ".jpg"
        self.label_2.setPixmap(QPixmap(imgname))
        self.label_2.setScaledContents(True)
        self.label_2.setFixedSize(207, 186)

        imgname = img_dir + str(3) + ".jpg"
        self.label_3.setPixmap(QPixmap(imgname))
        self.label_3.setScaledContents(True)
        self.label_3.setFixedSize(207, 186)
            

# -------------------------------------------------------------------------------

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('HW3_main2.ui', self)
        self.df = pd.read_csv("/Users/guoyixuan/Documents/pythoncode/ccwapp/Rankings_US_12.csv")
        self.show_map()

        self.table = self.tableView
        self.setWindowTitle('美國留學查詢系統')
        self.resize(1000, 1000)

        # add icon 
        #self.Uicomponents()

        # slot
        # 選擇排名方式
        self.radioButton_all.clicked.connect(self.table_rank) # 總大學排名
        self.radioButton_cate.clicked.connect(self.table_rank) # 分學科排名

        self.comboBox_all.currentIndexChanged.connect(self.table_rank) # 總大學排名依據
        self.comboBox_subject.currentIndexChanged.connect(self.table_rank) # 分學科排名依據
        self.comboBox_region.currentIndexChanged.connect(self.table_rank) # 學科選擇

        self.update_plot()

        # 下載csv檔
        self.pushButton_loadcsv.clicked.connect(self.export_to_csv)
        #self.pushButton_loadplot.clicked.connect(self.export_to_plot)

        # 頁數跳轉功能
        self.pushButton_first.clicked.connect(self.first_page) 
        self.pushButton_front.clicked.connect(self.prev_page) 
        #self.comboBox_page.currentIndexChanged.connect(self.change_page)
        self.pushButton_next.clicked.connect(self.next_page) 
        self.pushButton_last.clicked.connect(self.last_page) 

        # 設定起始表格
        ranking_type = self.comboBox_all.currentText() # 根據什麼來做排名
        # 將資料按照ranking_type做排序
        self.startdf = self.df.sort_values(by=[ranking_type + ' rank'], ascending = True)
        self.df_choose = self.startdf[['Institution', 'Overall rank', 'Overall','location code',
                                       'CITY', 'longitude', 'latitude' ]] # 只取前兩欄
        # 將頁數加入combobox
        self.rows = self.df_choose #197*7
        self.items_page = 10 
        total_pages = math.ceil(len(self.rows)/self.items_page) #20
        self.comboBox_page.clear()
        for i in range(total_pages):
            self.comboBox_page.addItem(str(i+1))
        # 控制每頁只呈現10筆資料：
        pages = self.comboBox_page.currentText() # 目前頁數
        rows = self.df_choose[0:10] #10*7
        self.model = TableModel(rows) # 將排序後的資料放入model
        self.table.setModel(self.model) # 將model放入table
        self.rows = rows # 為了在跳轉頁面後，可以取得該rows的資料以跳入子視窗

        # 雙擊表格內容跳到子視窗
        self.table.doubleClicked.connect(self.judge_open) 
    
    def update_plot(self):
        if self.radioButton_all.isChecked():
            self.gView.clear()
            # 選擇排名方式
            ranking_type = self.comboBox_all.currentText() 
            self.df = pd.read_csv("/Users/guoyixuan/Documents/pythoncode/ccwapp/Rankings_US_12.csv")
            self.df = self.df.sort_values(by=[ranking_type], ascending = False)
            y = [float(self.df[ranking_type][0]), float(self.df[ranking_type][1]), float(self.df[ranking_type][2]), float(self.df[ranking_type][3]),
                 float(self.df[ranking_type][4]), float(self.df[ranking_type][5]), float(self.df[ranking_type][6]), float(self.df[ranking_type][7]),
                 float(self.df[ranking_type][8]), float(self.df[ranking_type][9])]
            x = [1,2,3,4,5,6,7,8,9,10]
            Ticks = self.df['Institution'][0:10].values.tolist() 
            # 垂直長條圖
            #barItem = pg.BarGraphItem(x = x, height = y, width = 0.3, brush=(200,200,224))
            # 水平長條圖
            barItem = pg.BarGraphItem(x0 = 0, y = x, height = 0.6, width = y, brush=(200,200,250))

            self.gView.addItem(barItem)
            self.gView.getAxis('left').setTicks([[(i, Ticks[i-1]) for i in x]])
            self.gView.getAxis("bottom").setTextPen(color='g')
            self.gView.getAxis("bottom").setPen(color='y')
            self.gView.setTitle('美國大學排名:總排名({})'.format(ranking_type))
            #self.gView.setLabel('left', 'ranking score', color='red', size=30)
            self.gView.setLabel('bottom', 'ranking score', color='red', size=30)
            

        if self.radioButton_cate.isChecked():
            self.gView.clear()
            # 選擇學科
            category = self.comboBox_region.currentText()
            ranking_type = self.comboBox_subject.currentText() # 根據什麼來做排名
            # 讀入該學科的csv檔案
            self.df = pd.read_excel("/Users/guoyixuan/Documents/pythoncode/ccwapp/ranking_" + 
                                       category + ".xlsx")
            # 選擇美國的大學
            self.df = self.df[self.df['Location'] == 'United States']
            # 按照ranking的方式進行排序
            self.df = self.df.sort_values(by=[ranking_type], ascending = False)
            y = [float(self.df[ranking_type].iloc[0]), float(self.df[ranking_type].iloc[1]), float(self.df[ranking_type].iloc[2]), float(self.df[ranking_type].iloc[3]),
                 float(self.df[ranking_type].iloc[4]), float(self.df[ranking_type].iloc[5]), float(self.df[ranking_type].iloc[6]), float(self.df[ranking_type].iloc[7]),
                 float(self.df[ranking_type].iloc[8]), float(self.df[ranking_type].iloc[9])]
            x = [1,2,3,4,5,6,7,8,9,10]
            Ticks = self.df['Institution'][0:10].values.tolist() 

            #barItem = pg.BarGraphItem(x = x, height = y, width = 0.3, brush=(200,200,224))
            barItem = pg.BarGraphItem(x0 = 0, y = x, height = 0.6, width = y, brush=(100,200,200))
            self.gView.addItem(barItem)
            self.gView.getAxis('left').setTicks([[(i, Ticks[i-1]) for i in x]])
            self.gView.getAxis("bottom").setTextPen(color='g')
            self.gView.getAxis("bottom").setPen(color='y')
            self.gView.setTitle('美國大學排名:{}({})'.format(category, ranking_type))
            #self.gView.setLabel('left', 'ranking score', color='red', size=30)
            self.gView.setLabel('bottom', 'ranking score', color='red', size=30)
            self.gView.setBackground('w')
    
    #def export_to_plot(self):
        #要下載很久時使用的進度條參考
    #    progress = QProgressDialog(self)
    #    progress.setWindowTitle("下載進度")
    #    progress.setLabelText("下載進度")
    #    # progress.setCancelButtonText("取消")
    #    progress.setRange(0, 100)
    #    progress.setMinimumDuration(0)
    #    dat_dir = '/Users/guoyixuan/Documents/pythoncode/ccwapp/'
    #    exporter = pg.exporters.ImageExporter(self.gView.plotItem)
    #    exporter.export(dat_dir + 'plot.png')
    #    progress.setValue(100)
    #    QMessageBox.information(self, "提示", "下載完成")

    def export_to_csv(self):
        #要下載很久時使用的進度條參考
        progress = QProgressDialog(self)
        progress.setWindowTitle("下載進度")
        progress.setLabelText("下載進度")
        # progress.setCancelButtonText("取消")
        progress.setRange(0, 100)
        progress.setMinimumDuration(0)
        # progress.setWindowModality(Qt.WindowModal)
        dat_dir = '/Users/guoyixuan/Documents/pythoncode/ccwapp/'
        if self.radioButton_all.isChecked():
            ranking_type = self.comboBox_all.currentText()  # 根據什麼來做排名
            # 將資料按照ranking_type做排序
            self.startdf = self.df.sort_values(by=[ranking_type + ' rank'], ascending = True)
            # 選擇所需的欄位
            self.df_choose = self.startdf[['Institution', ranking_type, ranking_type +' rank',
                                           'location code', 'CITY', 'longitude', 'latitude' ]] # 只取前兩欄
            # 將頁數加入combobox
            self.rows = self.df_choose
            ranking_type = self.comboBox_all.currentText()
            self.rows.to_csv(dat_dir + 'All_ranking_' + ranking_type + '.csv')
            progress.setValue(100)
            QMessageBox.information(self, "提示", "下載完成")
        
        if self.radioButton_cate.isChecked():
            # 選擇學科
            category = self.comboBox_region.currentText()
            ranking_type = self.comboBox_subject.currentText() # 根據什麼來做排名
            # 讀入該學科的csv檔案
            self.catdf = pd.read_excel("/Users/guoyixuan/Documents/pythoncode/ccwapp/ranking_" + 
                                       category + ".xlsx")
            # 選擇美國的大學
            self.catdf = self.catdf[self.catdf['Location'] == 'United States']
            # 按照ranking的方式進行排序
            self.catdf = self.catdf.sort_values(by=[ranking_type], ascending = False)
            # 選擇需要的欄位
            self.df_choose = self.catdf[['Institution', 'Location', ranking_type, '2023', '2022']] # 只取前兩欄
            # 將頁數加入combobox
            self.items_page = 10 
            self.rows = self.df_choose
            self.rows.to_csv(dat_dir + category + ' ranking_' + ranking_type + '.csv')
            progress.setValue(100)
            QMessageBox.information(self, "提示", "下載完成")
        

    def table_rank(self):
        #q: 如何取得dataframe中所有的row？
        #a: df.values.tolist()
        if self.radioButton_all.isChecked():
            ranking_type = self.comboBox_all.currentText()  # 根據什麼來做排名
            # 將資料按照ranking_type做排序
            self.startdf = self.df.sort_values(by=[ranking_type + ' rank'], ascending = True)
            # 選擇所需的欄位
            self.df_choose = self.startdf[['Institution', ranking_type, ranking_type +' rank',
                                           'location code', 'CITY', 'longitude', 'latitude' ]] # 只取前兩欄
            # 將頁數加入combobox
            self.rows = self.df_choose
            self.items_page = 10 
            # 總共的頁數
            total_pages = math.ceil(len(self.rows)/self.items_page)
            # 清空combobox  
            self.comboBox_page.clear()
            # 將頁數加入combobox
            for i in range(total_pages):
                self.comboBox_page.addItem(str(i+1))
            # 控制每頁只呈現10筆資料：
            #self.change_page()
            pages = self.comboBox_page.currentText() # 目前頁數
            rows = self.rows[10*int(pages)-10:10*int(pages)]
            self.model = TableModel(rows) # 將排序後的資料放入model
            self.table.setModel(self.model) # 將model放入table
            self.rows = rows

            # 選擇排名方式
            self.gView.clear()
            y = [float(self.startdf[ranking_type][0]), float(self.startdf[ranking_type][1]), float(self.startdf[ranking_type][2]), float(self.startdf[ranking_type][3]),
                 float(self.startdf[ranking_type][4]), float(self.startdf[ranking_type][5]), float(self.startdf[ranking_type][6]), float(self.startdf[ranking_type][7]),
                 float(self.startdf[ranking_type][8]), float(self.startdf[ranking_type][9])]
            x = [1,2,3,4,5,6,7,8,9,10]
            Ticks = self.startdf['Institution'][0:10].values.tolist() 
            #barItem = pg.BarGraphItem(x = x, height = y, width = 0.3, brush=(200,200,224))
            barItem = pg.BarGraphItem(x0 = 0, y = x, height = 0.6, width = y, brush=(200,200,250))
            self.gView.addItem(barItem)
            self.gView.getAxis('left').setTicks([[(i, Ticks[i-1]) for i in x]])
            self.gView.getAxis("bottom").setTextPen(color='g')
            self.gView.getAxis("bottom").setPen(color='y')
            self.gView.setTitle('美國大學排名:總排名({})'.format(ranking_type))
            #self.gView.setLabel('left', 'ranking score', color='red', size=30)
            self.gView.setLabel('bottom', 'ranking score', color='red', size=30)
            #q:how to rotate the x-axis label?
            #a: self.gView.getAxis("bottom").setTickFont(30)
               
        if self.radioButton_cate.isChecked():
            # 選擇學科
            category = self.comboBox_region.currentText()
            ranking_type = self.comboBox_subject.currentText() # 根據什麼來做排名
            # 讀入該學科的csv檔案
            self.catdf = pd.read_excel("/Users/guoyixuan/Documents/pythoncode/ccwapp/ranking_" + 
                                       category + ".xlsx")
            # 選擇美國的大學
            self.catdf = self.catdf[self.catdf['Location'] == 'United States']
            # 按照ranking的方式進行排序
            self.catdf = self.catdf.sort_values(by=[ranking_type], ascending = False)
            # 選擇需要的欄位
            self.df_choose = self.catdf[['Institution', 'Location', ranking_type, '2023', '2022']] # 只取前兩欄
            # 將頁數加入combobox
            self.items_page = 10 
            self.rows = self.df_choose
            total_pages = math.ceil(len(self.rows)/self.items_page)
            self.comboBox_page.clear()
            for i in range(total_pages):
                self.comboBox_page.addItem(str(i+1))
            # 控制每頁只呈現10筆資料：
            #self.change_page()
            pages = int(self.comboBox_page.currentText()) # 目前頁數
            self.rows = self.df_choose
            rows = self.rows[10*pages-10:10*pages]
            self.model = TableModel(rows) # 將排序後的資料放入model
            self.table.setModel(self.model) # 將model放入table
            self.rows = rows
            
            # 畫圖
            self.gView.clear()
            y = [float(self.catdf[ranking_type].iloc[0]), float(self.catdf[ranking_type].iloc[1]), float(self.catdf[ranking_type].iloc[2]), float(self.catdf[ranking_type].iloc[3]),
                 float(self.catdf[ranking_type].iloc[4]), float(self.catdf[ranking_type].iloc[5]), float(self.catdf[ranking_type].iloc[6]), float(self.catdf[ranking_type].iloc[7]),
                 float(self.catdf[ranking_type].iloc[8]), float(self.catdf[ranking_type].iloc[9])]
            x = [1,2,3,4,5,6,7,8,9,10]
            
            Ticks = self.catdf['Institution'][0:10].values.tolist() 
            #barItem = pg.BarGraphItem(x = x, height = y, width = 0.3, brush=(100,200,200))
            barItem = pg.BarGraphItem(x0 = 0, y = x, height = 0.6, width = y, brush=(100,200,200))
            self.gView.addItem(barItem)
            self.gView.getAxis('left').setTicks([[(i, Ticks[i-1]) for i in x]])
            self.gView.getAxis("bottom").setTextPen(color='orange')
            self.gView.getAxis("bottom").setPen(color='r')
            self.gView.getAxis("left").setPen(color='r')
            self.gView.setTitle('美國大學排名:{}({})'.format(category, ranking_type))
            #self.gView.setLabel('left', 'ranking score', color='yellow', size=30)
            self.gView.setLabel('bottom', 'ranking score', color = 'yellow', size = 30)
            self.gView.setBackground('black')
    
    #def change_page(self):
    #    pages = self.comboBox_page.currentText()
    #    self.rows = self.df_choose 
    #    rows = self.rows[10*int(pages)-10:10*int(pages)]
    #    self.model = TableModel(rows) # 將排序後的資料放入model
    #    self.table.setModel(self.model) # 將model放入table
    #    self.rows = rows
    
    def next_page(self):
        if int(self.comboBox_page.currentText()) < self.comboBox_page.count():
            pages = int(self.comboBox_page.currentText()) + 1
            self.rows = self.df_choose
            rows = self.rows[10*pages-10:10*pages]
            self.model = TableModel(rows)
            self.table.setModel(self.model) # 將model放入table
            self.comboBox_page.setCurrentText(str(pages))
            self.rows = rows
            
    def prev_page(self):   
        if int(self.comboBox_page.currentText()) > 1 :
            pages = int(self.comboBox_page.currentText()) - 1
            self.rows = self.df_choose
            rows = self.rows[10*pages-10:10*pages]
            self.model = TableModel(rows) # 將排序後的資料放入model
            self.table.setModel(self.model) # 將model放入table
            self.comboBox_page.setCurrentText(str(pages))
            self.rows = rows
        
    def first_page(self):
        pages = 1
        self.rows = self.df_choose
        rows = self.rows[10*pages-10:10*pages]
        self.model = TableModel(rows) # 將排序後的資料放入model
        self.table.setModel(self.model) # 將model放入table
        self.comboBox_page.setCurrentIndex(0)
        self.rows = rows
    
    def last_page(self):
        pages = self.comboBox_page.count()
        self.rows = self.df_choose
        rows = self.rows[10*pages-10:10*pages]
        self.model = TableModel(rows) # 將排序後的資料放入model
        self.table.setModel(self.model) # 將model放入table
        self.comboBox_page.setCurrentText(str(pages))
        self.rows = rows
    

    def show_map(self):
        coordinates_lat = self.df['latitude']
        coordinates_lon = self.df['longitude']
        rankingoverall = self.df['Overall rank']
        loc_names = self.df['Institution']
        #self.b1 = QPushButton('Click')

        m = folium.Map(
            titles = "Mapbox Bright",
            zoom_start = 4, # 控制地圖初始縮放大小
            location = (38.5, -98),
            control_scale=True,
        )

        data = io.BytesIO()

        for i in range(len(loc_names)):
            # 如果想要加入網址可以加入這些程式碼
            # 跑太久了，先不加入
            #query = loc_names[i]
            #for j in search(query, tld="co.in", num=10, stop=1, pause=2):
            #    url = j
            #    print(url)
            folium.Marker(location = [coordinates_lat[i], coordinates_lon[i]], 
                                radius = 1000,
                                #color = 'green', 
                                tooltip = loc_names[i],
                                #popup = loc_names[i] + ',' + 'QS:' + str(rankingoverall[i]) + ',' +
                                #'<a href=' + url + '>click</a>',
                                popup = loc_names[i] + ',' + 'QS:' + str(rankingoverall[i]),
                                #fill_color = 'red',
                                fill_opacity = 0.5,
                                icon=folium.Icon(icon='home', color = 'blue')
                                ).add_to(m)
        
        m.save(data, close_file = False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        #webView.setContentsMargins(120, 120, 80, 80)
        
        self.verticalLayout_3.addWidget(webView, 0)
    
    def judge_open(self, mi):
        col_list = list(self.df_choose.columns)
        college_name = self.rows.iloc[mi.row(), col_list.index('Institution')]
        for i in range(1, 10):
            url1 = 'https://www.ieeuc.com.tw/page/rank/p2.aspx?page=' + str(i) + '&kind=1018&year=2022'
            response1 = requests.get(url1)
            soup = BeautifulSoup(response1.text, "html.parser")
            if soup.find('span', class_ = 'txt-en', string = college_name) != None:
                break
            else:
                continue
        url1 = 'https://www.ieeuc.com.tw/page/rank/p2.aspx?page=' + str(i) + '&kind=1018&year=2022'
        # 爬蟲網站網址：留學家
        # url1 = 'https://www.ieeuc.com.tw/page/rank/p2.aspx?page=1&kind=1018&year=2022'
        
        # 取出html裡面所有的文字
        response1 = requests.get(url1)
        # 只關注html的部分
        soup = BeautifulSoup(response1.text, "html.parser")
        # 有些大學在那個網站上沒有資料，所以如果點選到沒有資料的大學，會跳出一個視窗告知沒有資料
        if soup.find('span', class_ = 'txt-en', string = college_name) == None:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("沒有資料")
            dlg.setText("很抱歉，該大學暫時沒有相關介紹可展示，欲了解該大學詳情請搜尋該大學網站<br>「是否使用瀏覽器搜尋？」")
            dlg.setIcon(QMessageBox.Icon.Question)
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            buttonY = dlg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('Yes')
            buttonY = dlg.button(QMessageBox.StandardButton.No)
            buttonY.setText('No')
            button = dlg.exec()
            if button == QMessageBox.StandardButton.Yes:
                return self.call_subwin(college_name)
            else:
                print('no!') 
        else:
            results = soup.find('span', class_ = 'txt-en', string = college_name)
            parent = results.find_parent('a')
            self.call_anoWin(parent, college_name)
    
    def call_anoWin(self, parent, college_name):
        # create a sub-window
        self.anotherwindow = AnotherWindow()
        self.anotherwindow.rowSelected(parent, college_name)
        # 接收子視窗的訊號
        # self.anotherwindow.submitted.connect()
        self.anotherwindow.show()
    
    def call_subwin(self, college_name):
        # create a sub-window
        query = college_name
        self.webbrowser = Subwindow()
        self.webbrowser.urlBrowser(query)
        self.webbrowser.show()

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()

 