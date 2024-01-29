import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QPushButton, QLabel, QCheckBox, \
    QRadioButton, QButtonGroup, QComboBox, QTableWidget, QTableWidgetItem, QTableView
from PyQt6.QtCore import Qt
import pandas as pd
import sqlite3
from sqlite3 import Error
from PyQt6.QtWidgets import QDialog
import matplotlib.image as mpimg
import pyqtgraph as pg
import math
from PyQt6.QtGui import QStandardItemModel, QIcon
from PyQt6.QtWidgets import QTableView
from googlesearch import search

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
        # 关联QTableView控件和Model
        self.tableview.setModel(self.model)

 
    # Add Row and Column header
    def headerData(self, section, orientation, role):
    #    # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole: # more roles
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
 
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])


#子視窗
class AnotherWindow(QDialog):
    # create a customized signal 
    submitted = QtCore.pyqtSignal(str) # "submitted" is like a component name 
 
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('HW2_sub.ui', self)
        self.setGeometry(1600, 1000, 1000, 1000)

        database = r"/Users/guoyixuan/Documents/pythoncode/ccwdatabase/homework.sqlite"
        self.conn = create_connection(database)
        self.setWindowTitle('Paper')
         
        # Signal
        # 回到主視窗
        self.pBut_to_main.clicked.connect(self.on_submit)

    def on_submit(self):
        # emit a signal and pass data along
        # self.submitted.emit(self.lineEdit_sub_mu.text()) 
        self.close()
    
    # slot
    def rowSelected(self, abs, texts, titles, authos, imgfile):
        # display Abstract on TextBrowser, then go fetch author names
        self.textBrowser_abstracts.setText(abs)
        self.textBrowser_text.setText(texts)
        self.label_title.setText(titles)
        show_authors(self, authos)

        self.graphWidget.clear()
        img_dir = "/Users/guoyixuan/Documents/pythoncode/ccwdatabase/NIP2015_Images/"
        img_name = imgfile
        image = mpimg.imread(img_dir + img_name)
        img_item = pg.ImageItem(image, axisOrder='row-major')
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.getAxis('bottom').setTicks('')
        self.graphWidget.getAxis('left').setTicks('')
        self.graphWidget.setAspectLocked(lock=True, ratio=1)
        

#主視窗
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super().__init__()
        #super(MainWindow, self).__init__()
        uic.loadUi('HW2_main.ui', self)
        self.table = self.tableView

        database = r"/Users/guoyixuan/Documents/pythoncode/ccwdatabase/homework.sqlite"
        # create a database connect
        self.conn = create_connection(database)
        self.setWindowTitle('Paper Query System')

        # add icon 
        self.Uicomponents()

        # Signals
        # sql語法搜尋功能
        self.lineEdit_equation.returnPressed.connect(self.queryTable) 
        self.p_But_by_sql.clicked.connect(self.queryTable) 
        # 作者姓名搜尋功能
        self.lineEdit_name.returnPressed.connect(self.searchByName)
        self.p_But_by_name.clicked.connect(self.searchByName)
        # 關鍵詞搜尋功能
        self.lineEdit_title.returnPressed.connect(self.searchByTitle) 
        self.p_But_by_title.clicked.connect(self.searchByTitle) 
        # 頁數跳轉功能
        self.pushButton_first.clicked.connect(self.first_page) 
        self.pushButton_front.clicked.connect(self.prev_page) 
        self.comboBox_page.currentIndexChanged.connect(self.change_page)
        self.pushButton_next.clicked.connect(self.next_page) 
        self.pushButton_last.clicked.connect(self.last_page) 
        # 雙擊表格內容跳到子視窗
        self.table.doubleClicked.connect(self.call_subWin) 
        self.actionEXIT.triggered.connect(self.appEXIT) #file exit 


    # Slots
    def Uicomponents(self):
        self.pushButton_first.setIcon(QIcon("chevrons-left.svg"))
        self.pushButton_front.setIcon(QIcon("chevron-left.svg"))
        self.pushButton_next.setIcon(QIcon("chevron-right.svg"))
        self.pushButton_last.setIcon(QIcon("chevrons-right.svg"))
        self.p_But_by_sql.setIcon(QIcon("search.svg"))
        self.p_But_by_name.setIcon(QIcon("search.svg"))
        self.p_But_by_title.setIcon(QIcon("search.svg"))

    # sql語法搜尋指令
    def queryTable(self):
        tborder = self.lineEdit_equation.text() #sql語法
        #select_table(self, tborder)
        with self.conn:
            self.rows = SQLExecute(self, tborder)
            if len(self.rows) > 0: 
                ToTableView(self, self.rows)
            self.label_page.setText("1")
            self.items_page = 10

            # add page numbers to comboBox_page
            total_pages = math.ceil(len(self.rows)/self.items_page)
            self.comboBox_page.clear()
            for i in range(total_pages):
                self.comboBox_page.addItem(str(i+1))
            self.label_totalpage.setText(str(total_pages))


    def searchByName(self):
        name_key = self.lineEdit_name.text()
        sqlid = "select distinct(paperid) from paperauthors A, authors B where B.name like '%"+name_key+"%' and A.authorid = B.id"
        #透過以上程式碼可以得到paper的id
        sql = "select distinct(A.id)"
        if self.checkBox_show_title.isChecked():
            sql = sql + ",title"
        if self.checkBox_show_type.isChecked():
            sql = sql + ",eventtype"
        if self.checkBox_show_abstract.isChecked():
            sql = sql + ",abstract"   
        if self.checkBox_show_paper.isChecked():
            sql = sql + ", papertext"
        sql = sql + ",imgfile from papers A, paperauthors B where A.id = B.paperid and B.paperid in ("+sqlid+")"
        with self.conn:
            self.rows = SQLExecute(self, sql)
            if len(self.rows) > 0: 
                ToTableView(self, self.rows)
            self.label_page.setText("1")
            self.items_page = 10

            # add page numbers to comboBox_page
            total_pages = math.ceil(len(self.rows)/self.items_page)
            self.comboBox_page.clear()
            for i in range(total_pages):
                self.comboBox_page.addItem(str(i+1))
            self.label_totalpage.setText(str(total_pages))

    def searchByTitle(self):
        title_key = self.lineEdit_title.text()
        # sql = "select id, title, eventtype, abstract from papers where title like '%"+title_key+"%'"
        sql = "select id"
        if self.radioButton_title.isChecked():
            if self.checkBox_show_title.isChecked():
                sql = sql + ",title"
            if self.checkBox_show_type.isChecked():
                sql = sql + ",eventtype"
            if self.checkBox_show_abstract.isChecked():
                sql = sql + ",abstract"   
            if self.checkBox_show_paper.isChecked():
                sql = sql + ", papertext"
         
            sql = sql + ",imgfile from papers where title like '%" + title_key + "%'"
            with self.conn:
                self.rows = SQLExecute(self, sql)
                if len(self.rows) > 0: 
                    ToTableView(self, self.rows)
                self.label_page.setText("1")
                self.items_page = 10

                # add page numbers to comboBox_page
                total_pages = math.ceil(len(self.rows)/self.items_page)
                self.comboBox_page.clear()
                for i in range(total_pages):
                    self.comboBox_page.addItem(str(i+1))
                self.label_totalpage.setText(str(total_pages))

        if self.radioButton_abstract.isChecked():
            if self.checkBox_show_title.isChecked():
                sql = sql + ",title"
            if self.checkBox_show_type.isChecked():
                sql = sql + ",eventtype"
            if self.checkBox_show_abstract.isChecked():
                sql = sql + ",abstract"   
            if self.checkBox_show_paper.isChecked():
                sql = sql + ", papertext"
         
            sql = sql + ",imgfile from papers where abstract like '%" + title_key + "%'"
            with self.conn:
                self.rows = SQLExecute(self, sql)
                if len(self.rows) > 0: 
                    ToTableView(self, self.rows)
                self.label_page.setText("1")
                self.items_page = 10

                # add page numbers to comboBox_page
                total_pages = math.ceil(len(self.rows)/self.items_page)
                self.comboBox_page.clear()
                for i in range(total_pages):
                    self.comboBox_page.addItem(str(i+1))
                self.label_totalpage.setText(str(total_pages))
        
        if self.radioButton_type.isChecked():
            if self.checkBox_show_title.isChecked():
                sql = sql + ",title"
            if self.checkBox_show_type.isChecked():
                sql = sql + ",eventtype"
            if self.checkBox_show_abstract.isChecked():
                sql = sql + ",abstract"   
            if self.checkBox_show_paper.isChecked():
                sql = sql + ", papertext"
         
            sql = sql + ",imgfile from papers where eventtype like '%" + title_key + "%'"
            with self.conn:
                self.rows = SQLExecute(self, sql)
                if len(self.rows) > 0: 
                    ToTableView(self, self.rows)
                self.label_page.setText("1")
                self.items_page = 10

                # add page numbers to comboBox_page
                total_pages = math.ceil(len(self.rows)/self.items_page)
                self.comboBox_page.clear()
                for i in range(total_pages):
                    self.comboBox_page.addItem(str(i+1))
                self.label_totalpage.setText(str(total_pages))
        
        if self.radioButton_text.isChecked():
            if self.checkBox_show_title.isChecked():
                sql = sql + ",title"
            if self.checkBox_show_type.isChecked():
                sql = sql + ",eventtype"
            if self.checkBox_show_abstract.isChecked():
                sql = sql + ",abstract"   
            if self.checkBox_show_paper.isChecked():
                sql = sql + ", papertext"
         
            sql = sql + ",imgfile from papers where papertext like '%" + title_key + "%'"
            with self.conn:
                self.rows = SQLExecute(self, sql)
                if len(self.rows) > 0: 
                    ToTableView(self, self.rows)
                self.label_page.setText("1")
                self.items_page = 10

                # add page numbers to comboBox_page
                total_pages = math.ceil(len(self.rows)/self.items_page)
                self.comboBox_page.clear()
                for i in range(total_pages):
                    self.comboBox_page.addItem(str(i+1))
                self.label_totalpage.setText(str(total_pages))
    
    def change_page(self):
        pages = self.comboBox_page.currentText()
        self.label_page.setText(str(pages))
        ToTableView(self, self.rows[10*int(pages)-10:10*int(pages)])
    
    def next_page(self):
        if self.label_page.text() < self.label_totalpage.text():
            self.label_page.setText(str(int(self.label_page.text()) + 1))
            pages = self.label_page.text()
            ToTableView(self, self.rows[10*int(pages)-10:10*int(pages)])
            self.comboBox_page.setCurrentText(pages)
            
    def prev_page(self):   
        if self.label_page.text() > str(1):
            self.label_page.setText(str(int(self.label_page.text()) - 1))
            pages = self.label_page.text()
            ToTableView(self, self.rows[10*int(pages)-10:10*int(pages)])
            self.comboBox_page.setCurrentText(pages)

    def first_page(self):
        self.label_page.setText("1")
        pages = self.label_page.text()
        ToTableView(self, self.rows[10*int(pages)-10:10*int(pages)])
        self.comboBox_page.setCurrentIndex(0)
    
    def last_page(self):
        lastpage = self.label_totalpage.text()
        self.label_page.setText(lastpage)
        pages = self.label_page.text()
        ToTableView(self, self.rows[10*int(pages)-10:10*int(pages)])
        self.comboBox_page.setCurrentText(pages)

    def appEXIT(self):
        self.conn.close() # close database
        self.close() # close app
    
    def call_subWin(self, mi):
        # create a sub-window
        self.anotherwindow = AnotherWindow()
        # pass information to sub-window
        if 'Abstract' in self.df.columns:
            col_list = list(self.df.columns)
        else:
            print('No Abstract from the Query')
            return
        self.anotherwindow.rowSelected(self.df.iloc[mi.row(), col_list.index('Abstract')],
                                       self.df.iloc[mi.row(), col_list.index('PaperText')],
                                       self.df.iloc[mi.row(), col_list.index('Title')],
                                       self.df.iloc[mi.row(), 0],
                                       self.df.iloc[mi.row(), col_list.index('imgfile')])
        # ready to accept a singal from sub-window
        # self.anotherwindow.submitted.connect(self.update_info)
        self.anotherwindow.show()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn

def select_table(self, tborder):
    sql = tborder
    SQLExecute(self, sql)
    #ToTableView(self, self.rows)
     
def SQLExecute(self, SQL):
    """
    Execute a SQL command and display the requested items on the QTableView
    :param conn: SQL command
    :return: None
    """
    self.cur = self.conn.cursor()
    self.cur.execute(SQL)
    rows = self.cur.fetchall()

    if len(rows) == 0: # nothing found
        # raise a messageBox here
        dlg = QMessageBox(self)
        dlg.setWindowTitle("SQL Information: ")
        dlg.setText("Nothing Found !!!")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
        buttonY = dlg.button(QMessageBox.StandardButton.Yes)
        buttonY.setText('OK')
        dlg.setIcon(QMessageBox.Icon.Information)
        button = dlg.exec()
    return rows
     
    # Process fetched output
    #names = [description[0] for description in cur.description]# extract column names
    #self.df = pd.DataFrame(rows)
    #self.model = TableModel(self.df)
    #self.table.setModel(self.model)
    #self.df.columns = names
    #self.table.resizeColumnToContents(0) # resize the width of the 1st column

def ToTableView(self, rows):
    names = [description[0] for description in self.cur.description] # extract column names
    self.df = pd.DataFrame(rows) # convert to dataframe
    self.model = TableModel(self.df) # convert to model
    self.table.setModel(self.model) # display on the table
    self.df.columns = names # assign column names
    self.df.index = range(1, len(rows)+1) # assign row names
    
   
def show_authors(self, paperid):
    sql = "select name from authors A, paperauthors B where B.paperid="+str(paperid)+" and A.id=B.authorid"
    with self.conn:
        self.rows = SQLExecute(self, sql)
        names =""
        for row in self.rows:
            names = names + row[0] +"; "
        self.textBrowser_authors.setText(names)

 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()