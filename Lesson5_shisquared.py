# 獨立性檢定
# 可編輯的表格
# pandas dataframe 的操作
 
from scipy.stats import chi2_contingency
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
import pandas as pd
import numpy as np
import sys
 
class PandasModel(QAbstractTableModel):
    #一開始的主視窗設定
    def __init__(self, data):
        super().__init__()
        self._data = data
    
    #row
    def rowCount(self, index):
        return self._data.shape[0]
    
    #column
    def columnCount(self, parnet=None):
        return self._data.shape[1]
    
    #data
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)
        if role == Qt.ItemDataRole.TextAlignmentRole:          
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
            # return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft
    
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False
 
    # def headerData(self, col, orientation, role):
    #     if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
    #         return self._data.columns[col]
 
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole: # more roles
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
 
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
 
    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
 
#
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Lesson5_chisquared.ui', self)
        self.lineEdit_newColumn.setPlaceholderText('輸入新欄名稱')
        self.lineEdit_newRow.setPlaceholderText('輸入新列名稱')
        
        #建立一開始的table樣子
        self.df = pd.DataFrame(
            [[1, 9, 2], [1, 2, 4], [3, 5, 2], [3, 3, 2], [5, 8, 9],], \
                columns=["Column 1", "Column 2", "Column 3"], \
                    index = ["Row 1", "Row 2", "Row 3", "Row 4", "Row 5"]
        )
 
        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)

        # add column and row items to comboBox 
        #改變選擇要修改的column跟row
        self.comboBox_colDelete.addItems(self.df.columns)
        self.comboBox_rowDelete.addItems(self.df.index)
    
        # Signals
        # 選擇獨立性檢定還是多項比例相等檢定
        self.pBut_indeptest.clicked.connect(self.chi2test)
        self.pBut_proptest.clicked.connect(self.chi2test)

        # 按加入列跟加入行的按鈕
        self.pBut_addColumn.clicked.connect(self.addColumn)
        self.pBut_addRow.clicked.connect(self.addRow)
        self.pBut_colDelete.clicked.connect(self.deleteColumn)
        self.pBut_rowDelete.clicked.connect(self.deleteRow)
        
        #輸入新欄名稱跟新列名稱
        self.lineEdit_newColumn.selectionChanged.connect(self.clear_newColumn)
        self.lineEdit_newRow.selectionChanged.connect(self.clear_newRow)
 
    # Slots
    def chi2test(self): 
        #self.df:our original  dataframe
        D = self.df.values.astype(int) # get array data from pandas 
        #count the number of column and row
        total_col = np.append(np.sum(D, axis = 0), np.sum(D))
        total_row = np.sum(D, axis = 1)
        #
        self.df['Total']= total_row
        self.df.loc['Total']= total_col

        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)

        #先清空行跟列
        self.comboBox_colDelete.clear()
        self.comboBox_colDelete.addItems(self.df.columns)
        self.comboBox_rowDelete.clear()
        self.comboBox_rowDelete.addItems(self.df.index) #self.df.index:表格內所有的值

        chi2, p, dof, expected = chi2_contingency(D)
        report_result = 'Chi2 statistic = ' + str(np.round(chi2, 4)) + '\n'
        report_result = report_result + 'p-value = ' + str(np.round(p,4)) + '\n'
        report_result = report_result + 'DOF = ' + str(dof) + '\n'
        report_result = report_result + 'Expected Frequency = ' + '\n'+ str(np.round(expected, 2))
        self.textBrowser_results.setText(report_result)
        print([chi2, p, dof, expected])
         
     
    def addColumn(self):
        col_name = self.lineEdit_newColumn.text()
        self.df[col_name]= 0
        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)
        self.comboBox_colDelete.clear()
        self.comboBox_colDelete.addItems(self.df.columns)
 
    def addRow(self):
        row_name = self.lineEdit_newRow.text()
        self.df.loc[row_name] = 0
        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)
        self.comboBox_rowDelete.clear()
        self.comboBox_rowDelete.addItems(self.df.index)
 
    def deleteColumn(self):
        col = self.comboBox_colDelete.currentText()
        del self.df[col] # self.df.drop([col], axis = 1)
        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)
        self.comboBox_colDelete.clear()
        self.comboBox_colDelete.addItems(self.df.columns)
         
 
    def deleteRow(self):
        row = self.comboBox_rowDelete.currentText()
        self.df = self.df.drop(row) 
        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)
        self.comboBox_rowDelete.clear()
        self.comboBox_rowDelete.addItems(self.df.index)
     
    def clear_newColumn(self):
        self.lineEdit_newColumn.clear()
 
    def clear_newRow(self):
        self.lineEdit_newRow.clear()
 
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()