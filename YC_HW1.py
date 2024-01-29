#---------shallow machine learning------------------
import sys
import numpy as np
import pyqtgraph as pg
from PyQt6.QtGui import QColor
from PyQt6 import QtWidgets, uic , QtCore ,QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap 
from scipy.stats import binom
from scipy.stats import norm
from scipy.stats import multivariate_normal
import pandas as pd
from pathlib import Path
import sklearn.linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split

#-------image tab-----------------------
import sys
import os
import matplotlib.image as mpimg
import pyqtgraph as pg
import numpy as np
from skimage.filters import threshold_otsu
import cv2 as cv
from numpy.linalg import svd
#------------------------------------------

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
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('Assignment2.ui', self)
        self.tabWidget.setCurrentIndex(0)
        self.setWindowTitle('An application with multiple pages')
#         win = self.graphLayout
#         self.plt1 = win.addPlot()
#         self.plt2 = win.addPlot()
#         win.nextRow()
#         self.plt3 = win.addPlot()
        
        # page 1
#         self.LE_samples_size.returnPressed.connect(self.update_plot_clt)
#         self.CBX_distribution.currentTextChanged.connect(self.update_plot_clt)
#         self.update_plot_clt()
#------------------------------------------------------
         # page 2
#         self.update_plot_int()
        win1 = self.graphLayoutWidget
         
        self.plt1 = win1.addPlot(title="")
#         win1.nextRow()
#         self.plt2 = win1.addPlot(title="")
        win1.nextRow()
        self.plt3 = win1.addPlot(title="")
        self.comboBox_col.currentTextChanged.connect(self.update_plt1)
#         self.comboBox_col_scatter_1.currentTextChanged.connect(self.update_plt2)
#         self.comboBox_col_scatter_2.currentTextChanged.connect(self.update_plt2)
        self.comboBox_col_scatter_1.currentTextChanged.connect(self.update_plt3)
        self.comboBox_col_scatter_2.currentTextChanged.connect(self.update_plt3)
        self.comboBox_col_target.currentTextChanged.connect(self.update_plt3)
        self.comboBox_col_target.currentTextChanged.connect(self.go)
#         self.BTN_go.clicked.connect(self.go)
        self.LE_feature.returnPressed.connect(self.go)
        #Signals
        self.actionExit.triggered.connect(self.fileExit)
        self.actionOpen.triggered.connect(self.fileOpen)
   
            
    #Signals
        self.actionExit.triggered.connect(self.fileExit)
        self.actionOpen.triggered.connect(self.fileOpen)

#------------------------------------------------------
         # page 3
    
#         self.setWindowTitle('Show images on the label widget')
        self.file_src = "./image/"
        self.picName = os.listdir(self.file_src)
        self.currIndex = 0
        
        # Create the view
#         win = pg.g_view(show=True, title="Basic plotting examples")
        # plt1 = win.addPlot()
        # plt2 = win.addPlot()
        
        # Signals
        self.CMBX_img.currentIndexChanged.connect(self.showImg)
        self.CMBX_img.addItems(self.picName)
        self.PTBN_first.clicked.connect(lambda: self.showImg(0))
        self.PTBN_undo.clicked.connect(lambda: self.showImg(self.currIndex-1)                                        if self.currIndex-1 >= 0 else None)
        self.PTBN_next.clicked.connect(lambda: self.showImg(self.currIndex+1)                                       if self.currIndex+1 < len(self.picName) else None)
        self.PTBN_last.clicked.connect(lambda: self.showImg(len(self.picName)-1))
        
        self.RTBN_grayscale.toggled.connect(lambda: self.showImg(self.currIndex))
        self.RBTN_original.toggled.connect(lambda: self.showImg(self.currIndex))
        self.RTBN_thresholding.toggled.connect(lambda: self.showImg(self.currIndex))
        self.RTBN_histgram.toggled.connect(lambda: self.showImg(self.currIndex))
        self.PTBN_rotation.clicked.connect(lambda: self.showImg(self.currIndex))
#--------------------------------------------------------------------------------------
    
        self.RTBN_edge.toggled.connect(lambda: self.showImg(self.currIndex))
        self.RTBN_corner.toggled.connect(lambda: self.showImg(self.currIndex))
        self.RTBN_svd.toggled.connect(lambda: self.showImg(self.currIndex))
        self.LE_feature_2.returnPressed.connect(lambda: self.showImg(self.currIndex))
        
        self.showImg()




#------------------------------------------------------
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
 
            self.label_variable.setText(str(self.df.shape[1]))
            self.label_size.setText(str(self.df.shape[0]))
            self.comboBox_col.clear()
            self.comboBox_col_scatter_1.clear()
            self.comboBox_col_scatter_2.clear()
            self.comboBox_col_target.clear()
            
            self.comboBox_col.addItems(self.df.columns)
            self.comboBox_col_scatter_1.addItems(self.df.columns)
            self.comboBox_col_scatter_2.addItems(self.df.columns)
            self.comboBox_col_target.addItems(self.df.columns)
            self.comboBox_col_target.setCurrentIndex(self.comboBox_col_target.count()-1)
            self.LE_feature.setText(str(len(self.df.columns)))
            self.update_plt1()
#             self.update_plt2()
            self.update_plt3()
             
    def update_plt1(self):
        self.plt1.clear()
        
        col = self.comboBox_col.currentText()
        y, x = np.histogram(self.df[col])
        # self.plt1.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        barItem = pg.BarGraphItem(x = x[0:len(y)-1], height = y, width = (x.max()-x.min())/len(x), brush=(107,200,224))
        self.plt1.addItem(barItem)
        self.plt1.setTitle(col)
 
    def update_plt2(self):
        self.plt2.clear()
        col_1 = self.comboBox_col_scatter_1.currentText()
        col_2 = self.comboBox_col_scatter_2.currentText()
        if isinstance(self.df[self.df.columns[0]][0], str) or isinstance(self.df[self.df.columns[1]][0], str) :
            self.plt2.setLabel('bottom',"")   
            self.plt2.setLabel('left',"")
            return
        else :
        # if self.df[self.df.columns[0]][0]== float and self.df[self.df.columns[1]][0]== float :
            self.plt2.plot(self.df[col_1], self.df[col_2], pen=None, symbol='o', symbolSize=5)
            self.plt2.setLabel('bottom',col_1)   
            self.plt2.setLabel('left',col_2)  
            
    def update_plt3(self):
        self.plt3.clear()
        col_1 = self.comboBox_col_scatter_1.currentText()
        col_2 = self.comboBox_col_scatter_2.currentText()
        target = self.comboBox_col_target.currentText()
        C = self.df[target]
        uni = np.unique(C)
        color_dict = {}
        colors = ['red', 'blue', 'green', 'yellow', 'orange']  # Define a list of colors

        for i, c in enumerate(uni):
            color_dict[c] = colors[i % len(colors)]

            # Now you can use the color_dict to assign a color to each value in the target column
        scatter_colors = [color_dict[val] for val in C]

       

        if isinstance(self.df[self.df.columns[0]][0], str) or isinstance(self.df[self.df.columns[1]][0], str):
            self.plt3.setLabel('bottom', "")   
            self.plt3.setLabel('left', "")
            return
        else:
            self.plt3.plot(self.df[col_1], self.df[col_2], pen=None, symbol='o', symbolSize=5, symbolBrush=scatter_colors)
            self.plt3.setLabel('bottom', col_1)   
            self.plt3.setLabel('left', col_2)
            self.plt3.setLimits(xMin=min(self.df[col_1])-3, xMax=max(self.df[col_1])+3                                        , yMin=min(self.df[col_2])-3, yMax=max(self.df[col_2])+3)


            
#             contour.setParentItem(img)
#             contour.setData(Z)
#             self.plt3.contour(xx, yy, Z, colors='black', linewidths=1)
 
    def go(self):
        target = self.comboBox_col_target.currentText()
        C = self.df[target]
        mask = self.df != C
        X = self.df.drop(columns=[target]).values
        y = C.values
        feature =  int((self.LE_feature.text()))
        # 假設 X 是我們的特徵資料，y 是對應的目標變數
        rf = RandomForestRegressor()
        rf.fit(X, y)

        # 取得所有特徵的重要程度分數
        importances = rf.feature_importances_

        # 用 argsort 取得按照重要程度排序後的索引值
        sorted_indexes = importances.argsort()

        # 按照重要程度由低到高，把特徵的名稱存入一個陣列
        feature_names = pd.DataFrame(X).columns
        sorted_feature_names = feature_names[sorted_indexes]

        # 把重要程度分數也按照排序順序排列
        sorted_importances = importances[sorted_indexes]
        # 取得前x個重要特徵的索引值
        top_x_indexes = sorted_indexes[-feature:]

        # 取得前x個重要特徵對應的資料
        top_x_features = X[:, top_x_indexes]
        top_x_features_train, top_x_features_test, y_train, y_test =                             train_test_split(top_x_features, y, test_size = 0.2)
        str1 = self.comboBox_distribution.currentText()
        if str1=="Logisitic Regression":
            clf = sklearn.linear_model.LogisticRegression(C=1e5, max_iter=1000)
            clf.fit(top_x_features_train, y_train)
            
            acc = clf.score(top_x_features_train, y_train)
            acc_2 = clf.score( top_x_features_test,  y_test )
            self.label_accuracy.setText(f"Training Accuracy: {acc:.2f}")
            self.label_accuracy_2.setText(f"Testing Accuracy: {acc_2:.2f}")
        
        elif str1=="LDA":
            Lda = LinearDiscriminantAnalysis(tol = 1e-6)
            Lda.fit(top_x_features_train, y_train)
            acc = Lda.score(top_x_features_train, y_train)
            acc_2 = Lda.score( top_x_features_test,  y_test )
            self.label_accuracy.setText(f"Training Accuracy: {acc:.2f}")
            self.label_accuracy_2.setText(f"Testing Accuracy: {acc_2:.2f}")

            
            
    # Slots
    def showImg(self, index=None):
       
        self.g_view.clear()
        img_dir = "./image/"
        if index is None:
            img_name = self.CMBX_img.currentText()
            self.currIndex = self.CMBX_img.currentIndex()
        else:
            self.currIndex = index
            img_name = self.picName[self.currIndex]
            self.CMBX_img.setCurrentIndex(self.currIndex) 
        img_name = self.CMBX_img.currentText()
        image = mpimg.imread(img_dir + img_name)
        # image = np.rot90(image)
        
        
        
        
        # Apply grayscale filter if grayscale radio button is checked
        if self.RTBN_grayscale.isChecked():
            # image = np.mean(image, axis=2)
            image = 0.3*image[:,:,0] + 0.59*image[:,:,1] + 0.11*image[:,:,2]
        if self.RTBN_thresholding.isChecked():
            #  global thresholding
            
            # image = np.mean(image, axis=2) 
            image = 0.3*image[:,:,0] + 0.59*image[:,:,1] + 0.11*image[:,:,2]
            # 計算最佳閾值
            threshold_value = threshold_otsu(image)
            image[image <= threshold_value] = 0 
            image[image > threshold_value] = 255 
            
        if self.RTBN_edge.isChecked():
            
            if len(image.shape) > 2:
                # 將 R,G,B 三個 channel 平均
                image = 0.3*image[:,:,0] + 0.59*image[:,:,1] + 0.11*image[:,:,2] 
            
            else :
                image=image
            
            
            normalized_img = ((image*255).astype(np.float32) - 127)
            template = np.array([[-1,0,1],[-1,0,1],[-1,0,1]], dtype=np.float32)*1
            w, h = template.shape[::-1]

            # All the 5 methods for comparison in a list
            methods = ['cv.TM_CCOEFF']
            for meth in methods:
                method = eval(meth)
                # Apply template Matching
                res = cv.matchTemplate(normalized_img,template,method)
                # Store the result to plot later
                
                # Threshold the result to identify locations with a high match score
                threshold = int((self.LE_feature_2.text()))
                loc = np.where(res >= threshold)
                # Draw a rectangle around the identified location
                for pt in zip(*loc[::-1]):
                    image=cv.rectangle(res, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
#             img_item = pg.ImageItem(image, autoLevels=True, levels=[0,255], \
#                         axisOrder='row-major', \
#                         mode="gray")
#             self.g_view.addItem(img_item)
    
            
        if self.RTBN_corner.isChecked():           
            if len(image.shape) > 2:
                # 將 R,G,B 三個 channel 平均
                image = 0.3*image[:,:,0] + 0.59*image[:,:,1] + 0.11*image[:,:,2] 
            
            else :
                image=image
                
                
            
            template = np.array([[-4,5,5],[-4,5,5],[-4,-4,-4]], dtype=np.float32)*1
            
            normalized_img = ((image*255).astype(np.float32) - 127)
    
            # 抓出圖片的size
            H, W = image.shape
            h, w = template.shape

            # filter 從左上角開始掃描圖片，每次移動一個像素
            # stride = 1
            # kernal size = (template.shape[0] , template.shape[1])

            result = np.zeros((H-h+1, W-w+1))
        #     result1 = np.zeros((H-h+1, W-w+1))
            for i in range(H-h+1):
                for j in range(W-w+1):
                    patch = normalized_img[i:i+h, j:j+w]
                    # convolution
                    corr = np.sum(patch * template)

                    #計算  feature map 
                    norm1 = np.sqrt(np.sum(patch ** 2))
                    norm2 = np.sqrt(np.sum(template ** 2))
                    result[i,j] = corr/(norm1*norm2)

#             image=result

            threshold = float((self.LE_feature_2.text()))
            loc = np.where(result >= threshold)
                # Draw a rectangle around the identified location
            for pt in zip(*loc[::-1]):
                image=cv.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        # Set image mode to 'rgb' if original radio button is checked
        
        
        
        
        if self.RTBN_svd.isChecked(): 
            if len(image.shape) > 2:
                # 將 R,G,B 三個 channel 平均
                image = 0.3*image[:,:,0] + 0.59*image[:,:,1] + 0.11*image[:,:,2] 
            
            else :
                image=image
                
                
            U , E , VT = svd(image , full_matrices=False) 
           
            # q = np.array([1,5,25])
            q= int((self.LE_feature_2.text()))

           
            
            image= U[:,:q]@np.diag(E[:q])@VT[:q,:]
#             image = U
            

           

                
        
        if self.RBTN_original.isChecked():
            mode = 'rgb'
            img_item = pg.ImageItem(image, autoLevels=True, levels=[0,255],                         axisOrder='row-major',                         mode=mode)
            self.g_view.addItem(img_item)
                
        else:
            mode = None
            img_item = pg.ImageItem(image, autoLevels=True, levels=[0,255],                         axisOrder='row-major',                         mode=mode)
            self.g_view.addItem(img_item)
            
            
#         if self.RTBN_histgram.isChecked():
#             self.g_view.clear()
#             image = 0.3*image[:,:,0] + 0.59*image[:,:,1] + 0.11*image[:,:,2]
#             y, x = np.histogram(image.ravel()*255, bins=255)

#             img_item = pg.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
#             self.g_view.addItem(img_item)
            
        
        

       
            



        
        self.g_view.invertY(True)
        self.g_view.getAxis('bottom').setTicks('')
        self.g_view.getAxis('left').setTicks('')
        self.g_view.setAspectLocked(lock=True, ratio=1)  
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()
    

