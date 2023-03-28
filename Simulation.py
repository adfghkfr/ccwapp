#評估不能用的點的比例
import numpy as np
from scipy.stats import uniform
import matplotlib.pyplot as plt
import random

def f_x(x, y):
    x^2 * (1+np.sin(3*y)*np.cos(8*x))+y^2*(2+np.cos(5*x)*np.cos(8*y))

#curve(h)
random.seed(1)
x = uniform.rvs(10^5)
y = uniform.rvs(10^5)
plt.plot(x, y)

#ind=h(x,y)<1 #定義域
#points(x[ind],y[ind],col="red",pch=19,cex=.1) #定義域的點
#sum(ind)/10^5 #0.42759 #定義域只佔所有點的58%
