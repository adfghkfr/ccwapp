import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt, QAbstractTableModel
import pyqtgraph as pg
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
from scipy.stats import multivariate_normal
from sklearn.model_selection import train_test_split

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn import datasets, neighbors
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
 
    def rowCount(self, index):
        return self._data.shape[0]
 
    def columnCount(self, parnet=None):
        return self._data.shape[1]
 
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
 
 
    
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('HW1_page2.ui', self)
        self.setWindowTitle('Show constraints of simulation of different distribution')
        
        #增加或減少table的column數量
        #self.checkBox_reg.stateChanged.connect(self.update_model)
        #self.checkBox_aug.stateChanged.connect(self.update_model)
        #self.checkBox_logis.stateChanged.connect(self.update_model)
        #self.checkBox_lda.stateChanged.connect(self.update_model)
        #self.checkBox_qda.stateChanged.connect(self.update_model)
        #self.checkBox_knn.stateChanged.connect(self.update_model)
        #self.checkBox_ann.stateChanged.connect(self.update_model)

        #改變knn的參數值
        #self.spinBox_knn.valueChanged.connect(self.knn_model)

        #改變起始資料
        self.lineEdit_sampleA.returnPressed.connect(self.update_plot)
        self.lineEdit_sampleB.returnPressed.connect(self.update_plot)
        self.lineEdit_sampleC.returnPressed.connect(self.update_plot)

        self.lineEdit_muA11.returnPressed.connect(self.update_plot)
        self.lineEdit_muA12.returnPressed.connect(self.update_plot)
        self.lineEdit_muB11.returnPressed.connect(self.update_plot)
        self.lineEdit_muB12.returnPressed.connect(self.update_plot)
        self.lineEdit_muC11.returnPressed.connect(self.update_plot)
        self.lineEdit_muC12.returnPressed.connect(self.update_plot)

        self.lineEdit_muA21.returnPressed.connect(self.update_plot)
        self.lineEdit_muA21.returnPressed.connect(self.update_plot)
        self.lineEdit_muA21.returnPressed.connect(self.update_plot)
        self.lineEdit_muA21.returnPressed.connect(self.update_plot)
        self.lineEdit_muA21.returnPressed.connect(self.update_plot)
        self.lineEdit_muA21.returnPressed.connect(self.update_plot)

        self.lineEdit_sigmaA.returnPressed.connect(self.update_plot)
        self.lineEdit_sigmaB.returnPressed.connect(self.update_plot)
        self.lineEdit_sigmaC.returnPressed.connect(self.update_plot)

        #self.df = pd.DataFrame([[0.481, 0.493, 0.408, 0.405, 0.401, 0.288, 0.404],
        #                       [0.477, 0.489, 0.413, 0.415, 0.388, 0.437, 0.415], ],
        #                       columns = ["Regression", "Augmented Regression", "Logistic Regression", "LDA", "QDA", "KNN", "ANN"],
        #                       index = ["Training error", "Testing error"])
        self.df = pd.DataFrame([[0.481, 0.477],[0.493, 0.489], [0.408, 0.413], [0.405, 0.415],
                                [0.401, 0.388], [0.288, 0.437], [0.404, 0.415], ],
                               index = ["Regression", "Augmented Regression", "Logistic Regression", "LDA", "QDA", "KNN", "ANN"],
                               columns = ["Training error", "Testing error"])
        
        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)

    #slot
    #改變起始資料
    def knn_model(self):
        K1 = eval(self.spinBox_knn.setText())
    

    def update_plot(self):
        def param3(n1, n2, n3, mean1, mean2, mean3, mean4, mean5, mean6, val1, val2, val3):
                m1, m2, m3 = np.array([mean1, mean2]), np.array([mean3, mean4]), np.array([mean5, mean6])
                Cov1 = np.array([[1, val1], [val1, 1]])
                Cov2 = np.array([[1, val2], [val2, 1]])
                Cov3 = np.array([[1, val3], [val3, 1]])
                mvn1 = multivariate_normal(mean = m1, cov = Cov1)
                mvn2 = multivariate_normal(mean = m2, cov = Cov2)
                mvn3 = multivariate_normal(mean = m3, cov = Cov3)
                A = mvn1.rvs(n1)
                B = mvn2.rvs(n2)
                C = mvn2.rvs(n3)
                Xvar = np.vstack((A, B, C))#2000*1矩陣\
                y = np.hstack((np.zeros(n1), np.ones(n2), np.ones(n3)+1))#2000
                param3 = np.c_[Xvar, y]
                return param3
    
        mean1 = eval(self.lineEdit_muA11.text())
        mean2 = eval(self.lineEdit_muA12.text())
        val1 = eval(self.lineEdit_sigmaA.text())

        n1 = eval(self.lineEdit_sampleA.text())

        mean3 = eval(self.lineEdit_muB11.text())
        mean4 = eval(self.lineEdit_muB12.text())
        val2 = eval(self.lineEdit_sigmaB.text())

        n2 = eval(self.lineEdit_sampleB.text())

        mean5 = eval(self.lineEdit_muB11.text())
        mean6 = eval(self.lineEdit_muB12.text())
        val3 = eval(self.lineEdit_sigmaC.text())

        n3 = eval(self.lineEdit_sampleC.text())

        D = param3(n1, n2, n3, mean1, mean2, mean3, mean4, mean5, mean6, val1, val2, val3)
        data = X = D[:, 0:2]
        label = y = D[:, 2]

        n =100 #模擬次數
        Lineartrainerror = np.zeros(n)
        Lineartesterror = np.zeros(n)
        Augmentedtrainerror = np.zeros(n)
        Augmentedtesterror = np.zeros(n)
        Logistictrainerror = np.zeros(n)
        Logistictesterror = np.zeros(n)
        LDAtrainingError = np.zeros(n) #用來存取訓練誤差
        LDAtestingError = np.zeros(n) #存取測試誤差
        QDAtrainingError = np.zeros(n)
        QDAtestingError = np.zeros(n)
        KNNtrainingError = np.zeros(n)
        KNNtraingError = np.zeros(n)
        ANNtrainerror = np.zeros(n)
        ANNtesterror = np.zeros(n)

        Mdl = LinearRegression()
        Lda = LinearDiscriminantAnalysis(tol = 1e-6)
        Qda = QuadraticDiscriminantAnalysis(tol = 1e-6, store_covariance = True)
        logreg = LogisticRegression(multi_class='multinomial', solver='lbfgs', class_weight='balanced',
                                    max_iter=1000)
        
        K1 = self.spinBox_knn.text()
        weights = "uniform"
        Knn = neighbors.KNeighborsClassifier(K1, weights = weights)

        hidden_layers = (30, )
        solver = "adam"
        clf = MLPClassifier(max_iter = 10000, solver = solver, hidden_layer_sizes = hidden_layers, 
                            verbose = True, activation = "logistic", tol = 1e-6, random_state = 0)
        for i in range(n) :
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
        # --------------------------------------------------
        Mdl.fit(X_train, y_train) 
        y_hat = Mdl.predict(X_train) 
        y_pretrain = [1 if i > 0.5 else 0 for i in y_hat]
        Lineartrainerror[i] = 1- np.mean(y_pretrain == y_train)
        
        y_hat = Mdl.predict(X_test) 
        y_pretest = [1 if i > 0.5 else 0 for i in y_hat]
        Lineartesterror[i] = 1 - np.mean(y_pretest == y_test)
        # ---------------------------------------------------
        x1 = X_train[:,0:1] 
        x2 = X_train[:,1:2]
        XX = np.hstack((x1, x2, x1 * x2, x1 ** 2, x2 ** 2))
        Mdl.fit(XX, y_train) 
        y_hat = Mdl.predict(XX) 
        y_pretrain = [1 if i > 0.5 else 0 for i in y_hat]
        Augmentedtrainerror[i] = 1 - np.mean(y_pretrain == y_train)
        
        x1 = X_test[:,0:1]
        x2 = X_test[:,1:2]
        XX = np.hstack((x1, x2, x1 * x2, x1 ** 2, x2 ** 2))
        y_hat = Mdl.predict(XX) 
        y_pretest = [1 if i > 0.5 else 0 for i in y_hat]
        Augmentedtesterror[i] = 1 - np.mean(y_pretest == y_test)
        # ---------------------------------------------------
        logreg.fit(X_train, y_train)
        y_predict = logreg.predict(X_test)
        Logistictrainerror[i] = 1 - logreg.score(X_train, y_train)
        Logistictesterror[i] = 1 - logreg.score(X_test, y_test)
        # ---------------------------------------------------
        Lda.fit(X_train, y_train)
        Lda.predict(X_test)
        LDAtrainingError[i] = 1 - Lda.score(X_train, y_train)
        LDAtestingError[i] = 1 - Lda.score(X_test, y_test)
        # ---------------------------------------------------
        Qda.fit(X_train, y_train)
        Qda.predict(X_test)
        QDAtrainingError = 1 - Qda.score(X_train, y_train)
        QDAtestingError = 1 - Qda.score(X_test, y_test)
        # ---------------------------------------------------
        Knn.fit(X_train, y_train)
        Knn.predict(X_test)
        KNNtrainingError = 1 - Knn.score(X_train, y_train)
        KNNtestingError = 1 - Knn.score(X_test, y_test)
        # ---------------------------------------------------
        clf.fit(X_train, y_train)
        y_test_hat = clf.predict(X_test)
        ANNtrainerror[i] = 1 - clf.score(X_train, y_train)
        ANNtesterror[i] = 1 - clf.score(X_test, y_test)

        self.df[0, 0] = Lineartrainerror.mean()
        self.df[1, 0] = Augmentedtrainerror.mean()
        self.df[2, 0] = Logistictrainerror.mean()
        self.df[3, 0] = LDAtrainingError.mean()
        self.df[4, 0] = QDAtrainingError.mean()
        self.df[5, 0] = KNNtrainingError.mean()
        self.df[6, 0] = ANNtrainerror.mean()

        self.df[0, 1] = Lineartesterror.mean()
        self.df[1, 1] = Augmentedtesterror.mean()
        self.df[2, 1] = Logistictesterror.mean()
        self.df[3, 1] = LDAtestingError.mean()
        self.df[4, 1] = QDAtestingError.mean()
        self.df[5, 1] = KNNtestingError.mean()
        self.df[6, 1] = ANNtesterror.mean()
        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()
