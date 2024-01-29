import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore # 這個宣告會引用 PyQt 的 QtGui, QtCore
import pandas as pd

# define the data
category = 'Accounting'
ranking_type = 'Score' # 根據什麼來做排名
            # 讀入該學科的csv檔案
catdf = pd.read_excel("/Users/guoyixuan/Documents/pythoncode/ccwapp/ranking_" + category + ".xlsx")
            # 選擇美國的大學
catdf = catdf[catdf['Location'] == 'United States']
            # 按照ranking的方式進行排序
catdf = catdf.sort_values(by=[ranking_type], ascending = False)
#print(catdf)
#print(float(catdf[ranking_type][4]))
print(type(catdf[ranking_type][4]))


y = [float(catdf[ranking_type].iloc[0]), float(catdf[ranking_type].iloc[1]), float(catdf[ranking_type].iloc[2]), float(catdf[ranking_type].iloc[3]),
     float(catdf[ranking_type].iloc[4]), float(catdf[ranking_type].iloc[5]), float(catdf[ranking_type].iloc[6]), float(catdf[ranking_type].iloc[7]),
     float(catdf[ranking_type].iloc[8]), float(catdf[ranking_type].iloc[9])]
x = [1,2,3,4,5,6,7,8,9,10]
Ticks = catdf['Institution'][0:10].values.tolist() 
barItem = pg.BarGraphItem(x = x, height = y, width = 0.3, brush=(200,200,224))

plt = pg.plot()
plt.addItem(barItem)
plt.getAxis('bottom').setTicks([[(i, Ticks[i-1]) for i in x]])
plt.getAxis("bottom").setTextPen(color='g')
plt.getAxis("bottom").setPen(color='y')
plt.setTitle('美國大學排名')
# main method
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication.instance()
    sys.exit(app.exec())