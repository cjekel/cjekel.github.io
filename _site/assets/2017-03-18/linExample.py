import numpy as np
import matplotlib.pyplot as plt
#   data
x = np.array([1.0, 1.0, 2.0, 3.3, 3.3, 4.0, 4.0, 4.0, 4.7, 5.0, 5.6,
    5.6, 5.6, 6.0, 6.0, 6.5, 6.92])
y = np.array([10.84, 9.30, 16.35, 22.88, 24.35, 24.56, 25.86, 29.46,
    24.59, 22.25, 25.90, 27.20, 25.61, 25.45, 26.56, 21.03, 21.46])

#   fit a linear model
A = np.ones([len(x), 2])
A[:,1] = x
beta, SSe, rank, s = np.linalg.lstsq(A,y)
xl = np.linspace(min(x),max(x),num=100)
Al = np.ones([len(xl), 2])
Al[:,1] = xl
yl = np.dot(Al,beta)
yhat = np.dot(A,beta)
#   plot
plt.figure()
plt.plot(x,y,'ok')
plt.plot(xl,yl,'-b')
plt.grid(True)
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.show()
#plt.savefig('dataAndFit.png', ftype='png', dpi=300)

#   compute the sum of squares of pure error
level = np.array([1.0, 2.0, 3.3, 4.0, 4.7, 5.0, 5.6, 6.0, 6.5, 6.92])
levelIndex = [y[0:2], y[2], y[3:5], y[5:8], y[8], y[9],
    y[10:13], y[13:15], y[15], y[16]]
ybarLevels = []
for i in levelIndex:
    ybarLevels.append(np.mean(i))
SSpe = 0
for i, r in enumerate(levelIndex):
    SSpe += np.sum((r-ybarLevels[i])**2)

#   compute the sum of squares lack of fit
nl = len(level)
SSlof = 0
Alevel = np.ones([nl,2])
Alevel[:,1] = level
yhatLevel = np.dot(Alevel,beta)
for i, j in enumerate(ybarLevels):
    ni = np.size(levelIndex[i])
    SSlof+= ni*((j-yhatLevel[i])**2)
    
#   Statistical test for lack of fit
m = len(ybarLevels)
n = len(x)
p = len(beta)
F0 = (SSlof / (m-p)) / (SSpe / (n-m))

#   test for lack of fit
from scipy.stats import f
pValue = 1.0 - f.cdf(F0,m-p,n-m)
#   since pValue is very small we reject the case 
