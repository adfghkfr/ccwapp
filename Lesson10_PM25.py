from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtCore import Qt, QTimer
import pyqtgraph as pg
import pandas as pd
import numpy as np
import requests
import sys
 
 
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
            # return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft
         
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('#ffcde9')
 
    def rowCount(self, index):
        return self._data.shape[0]
 
    def columnCount(self, index):
        return self._data.shape[1]
 
    # Add Row and Column header
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole: # more roles
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
 
            # if orientation == Qt.Orientation.Vertical:
            #     return str(self._data.index[section])
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
         
        uic.loadUi('Lesson10_PM25.ui', self)
        self.data = self.getData()
        self.showData()
        # 加入計時器 if necessary
        # self.timer = QTimer()
        # timeInterval = 10 * 60000 # 10 分鐘
        # self.timer.setInterval(timeInterval)
        # self.timer.start()
         
        # Signals
        self.pBut_exit.clicked.connect(self.close)
        # self.timer.timeout.connect(self.timer_action) # emit every timeInterval millisecond
     
    # Slots
    def getData(self):
        api = 'https://data.epa.gov.tw/api/v2/'
        dataCode = 'aqx_p_02' # 無人自動站氣象資料
        auth = "api_key=01be21dd-ee0e-4286-bb15-xxxxxxxxxxxx" # 自行申請 api_key
        url = api + dataCode + "?"+ auth
        res = requests.get(url)
        data = res.json()
        return data
    
    def showData(self):
        # 先定位資料所在的結構層次，再依次取用
        tmp =self.data['records']
        self.label_time.setText(tmp[0]['datacreationdate'])
        d = []
        for i in range(len(tmp)):
            if tmp[i]['pm25'] != '': # 去除沒有資料的位置
                p = int(tmp[i]['pm25']) 
                d.append([tmp[i]['county'], tmp[i]['site'], p])
             
        self.df = pd.DataFrame(d)
        tmp = self.data['fields']
        self.df.columns = [tmp[1]['info']['label'], tmp[0]['info']['label'], tmp[2]['info']['label']]
        self.model = TableModel(self.df)
        self.tableView.setModel(self.model)
        # 取得前 10 名與後 10 名
        n = 10
        pm25_sort_top = self.df.sort_values(by=tmp[2]['info']['label'],ascending=False)
        self.textBrowser_top10.setText(pm25_sort_top.head(n).to_string(index=False, header=False))
        pm25_sort_bot = self.df.sort_values(by=tmp[2]['info']['label'],ascending=True)
        self.textBrowser_bot10.setText(pm25_sort_bot.head(n).to_string(index=False, header=False))
         
        # 繪製 bar chart
        x = np.arange(1, n+1, 1)
        y = pm25_sort_top.head(n)['細懸浮微粒濃度']
        barItem = pg.BarGraphItem(x = x, height = y, width = 0.5, brush=(107,200,224))
        self.graphicsView.addItem(barItem)
        Ticks = pm25_sort_top.head(n)['測站名稱'].values
        self.graphicsView.getAxis('bottom').setTicks([[(i, Ticks[i-1]) for i in x]])
        self.graphicsView.setTitle('Top 10')
 
        y = pm25_sort_bot.head(n)['細懸浮微粒濃度']
        barItem = pg.BarGraphItem(x = x, height = y, width = 0.5, brush=(255,255,0))
        self.graphicsView_bot.addItem(barItem)
        Ticks = pm25_sort_bot.head(n)['測站名稱'].values
        self.graphicsView_bot.getAxis('bottom').setTicks([[(i, Ticks[i-1]) for i in x]])
        self.graphicsView_bot.setTitle('Bottom 10')
 
         
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()