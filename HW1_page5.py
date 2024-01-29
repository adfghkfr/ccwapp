import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
import numpy as np
from pathlib import Path
 
 
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
 
    # Add Row and Column header
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole: # more roles
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
 
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super().__init__()
 
        uic.loadUi('HW1_page5.ui', self)
        self.setWindowTitle('Table View: the pandas version')
 
        self.table = self.tableView

        #Signals
        #打開跟離開
        self.actionExit.triggered.connect(self.fileExit)
        self.actionOpen.triggered.connect(self.fileOpen)
        
        #變換散佈圖column
        self.comboBox_xcolumn.currentIndexChanged.connect(self.update_plt)
        #填入combobox_xolumn時，會啟動訊號update_plt，此時combobox_ycolumn還沒填入訊息，因此會引動錯誤
        self.comboBox_ycolumn.currentIndexChanged.connect(self.update_plt)

        #滑鼠設定
        self.graphicsView_page2.scene().sigMouseMoved.connect(self.mouseMoved)
        #鼠標移動準備
        self.vLine = pg.InfiniteLine(pos = 400, angle=90, movable=False)
        self.hLine = pg.InfiniteLine(pos = 400, angle=0, movable=False)
        self.graphicsView_page2.addItem(self.vLine) # add PlotDataItem in PlotWidget 
        self.graphicsView_page2.addItem(self.hLine)

        #grid設定
        self.checkBox_grid.stateChanged.connect(self.grid_on)
        self.graphicsView_page2.showGrid(x = False, y = False)

    
    # Slots:
    def fileExit(self):
        self.close()
 
    def fileOpen(self):
        home_dir = str(Path.home())
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
            "", "EXCEL files (*.xlsx *.xls);;Text files (*.txt);;Images (*.png *.xpm *.jpg)")
        # print(fname[0])
        if fname[0]:

            self.df = pd.read_excel(fname[0], index_col = None, header = 0)
            self.model = TableModel(self.df)
            self.table.setModel(self.model)
            
            #呈現資料的dimension
            self.lineEdit_number.setText(str(self.df.shape[1]))
            self.lineEdit_sample_page2.setText(str(self.df.shape[0]))
            
            #為了展現散佈圖進行準備
            self.comboBox_xcolumn.clear()
            self.comboBox_xcolumn.addItems(self.df.columns)

            self.comboBox_ycolumn.clear()
            self.comboBox_ycolumn.addItems(self.df.columns)

            self.update_plt()
            #self.mouseMoved()
    
    def mouseMoved(self, point): # returns the coordinates in pixels with respect to the PlotWidget
        p = self.graphicsView_page2.plotItem.vb.mapSceneToView(point) # convert to the coordinate of the plot
        self.vLine.setPos(p.x()) # set position of the verticle line
        self.hLine.setPos(p.y()) # set position of the horizontal line
        self.lineEdit_x.setText(str(round(p.x(), 4))) 
        self.lineEdit_y.setText(str(round(p.y(), 4))) 

    def grid_on(self, s):
        if s == 2:
            self.graphicsView_page2.showGrid(x = True, y = True, alpha = 0.5)
        else:
            self.graphicsView_page2.showGrid(x = False, y = False, alpha = 0.5)

    def update_plt(self):
        self.graphicsView_page2.clear() 
        col_name_x = self.comboBox_xcolumn.currentText()
        col_name_y = self.comboBox_ycolumn.currentText()
        if col_name_y == "":
            return
        x = self.df[col_name_x]
        y = self.df[col_name_y]

        self.graphicsView_page2.plot(x, y, pen = None, symbol = "o")
        self.graphicsView_page2.setLabel('bottom', col_name_x)   
        self.graphicsView_page2.setLabel('left', col_name_y)  
        self.graphicsView_page2.showGrid(x = False, y = False)

        self.graphicsView_page2.addItem(self.vLine)
        self.graphicsView_page2.addItem(self.hLine)
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()