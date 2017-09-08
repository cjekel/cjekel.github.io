import numpy as np
import matplotlib.pyplot as plt
import math
from ctypes import c_double
x = np.linspace(0.0,10.0, num=100)
a = 4.0
b = -3.5
c = 0.0
y = (a*(x**2)) + (b*x) + c 

#   let's add noise to the data
#   np.random.normal(mean, standardDeviation, num)
noise = np.random.normal(0, 10., 100)
y = y+noise

#   guess the fit
a = 3.3
b = -6.0
c = 1.0
yGuess = (a*(x**2)) + (b*x) + c 



#   define a function to calculate the log likiehood
def calcLogLikelihood(guess, true, n):
    error = true-guess
    sigma = np.std(error)
    f = ((1.0/(2.0*math.pi*sigma*sigma))**(n/2))*np.exp(-1*((np.dot(error.T,error))/(2*sigma*sigma)))

    return np.log(f)
    
#   define a function to calculate the rms
def calcRMS(guess, true, n):
    error = true-guess
    
    r = (1/n)*np.dot(error.T,error)
    return np.sqrt(r)


#   pefrom least squres fit using scikitlearn
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
model = Pipeline([('poly', PolynomialFeatures(degree=2)),('linear', LinearRegression(fit_intercept=False))])

model = model.fit(x[:, np.newaxis], y)
coefs = model.named_steps['linear'].coef_


#   define myevalute function
def myEvaluate(var, obj, g, param):
    var = (c_double * 3).from_buffer(var)[:]

    yGuess = (var[2]*(x**2)) + (var[1]*x) + var[0]
    f = calcLogLikelihood(yGuess, y, 100)
    obj.value = (-1*f)
def myEvaluate2(var, obj, g, param):
    var = (c_double * 3).from_buffer(var)[:]

    yGuess = (var[2]*(x**2)) + (var[1]*x) + var[0]
    f = calcRMS(yGuess, y, 100)
    obj.value = (-1*f)



#   define my function
def myFunction(var):
    var = (c_double * 3).from_buffer(var)[:]

    yGuess = (var[2]*(x**2)) + (var[1]*x) + var[0]
    f = calcLogLikelihood(yGuess, y, 100.0)
    return (-1*f)
#   define my function
def myFunction2(var):
    var = (c_double * 3).from_buffer(var)[:]

    yGuess = (var[2]*(x**2)) + (var[1]*x) + var[0]
    f = calcRMS(yGuess, y, 100.0)
    return (f)
from scipy.optimize import minimize

optWinner = []
for i in range(0,10000):
    var = (40.0*np.random.rand(3))-20.0
    betaMLE = minimize(myFunction, var, method='BFGS',
                options={'disp': True})
    betaRMS = minimize(myFunction2, var, method='BFGS',
                options={'disp': True})
    yMLE = (betaMLE.x[2]*(x**2)) + (betaMLE.x[1]*x) + betaMLE.x[0]
    yRMS = (betaRMS.x[2]*(x**2)) + (betaRMS.x[1]*x) + betaRMS.x[0]
    rmsMLE = calcRMS(yMLE, y, 100.0)
    rmsRMS = calcRMS(yRMS, y, 100.0)
    if np.isclose(rmsMLE,rmsRMS) is True:
        optWinner.append(0)
    elif rmsMLE < rmsRMS:
        optWinner.append(1)
    else:
        optWinner.append(2)
np.save('optWinner',optWinner)    

#optWinner = np.load('optWinner.npy')
countOfSame = (optWinner == 0).sum()
countOfMLE = (optWinner == 1).sum()
countOfRMS = (optWinner == 2).sum()
totalRuns = len(optWinner)
def calcFrac(count, total):
    return 100.0 * (count/float(total))
fracSame = calcFrac(countOfSame,totalRuns)
fracMLE = calcFrac(countOfMLE,totalRuns)
fracRMS = calcFrac(countOfRMS,totalRuns)


from pylab import *

# make a square figure and axes
figure(1, figsize=(6,6))
ax = axes([0.1, 0.1, 0.8, 0.8])

# The slices will be ordered and plotted counter-clockwise.
labels = 'MLE and RMSE equivalent', 'MLE is better', 'RMSE is better'
fracs = [fracSame, fracMLE, fracRMS]
explode=(0.05, 0.05, 0.05)

pie(fracs, explode=explode, labels=labels,
                autopct='%1.1f%%', shadow=True, startangle=90)
                # The default startangle is 0, which would start
                # the Frogs slice on the x-axis.  With startangle=90,
                # everything is rotated counter-clockwise by 90 degrees,
                # so the plotting starts on the positive y-axis.


show()
savefig('maxLikelihoodComp.png', dpi=300, type='png', bbox_inches='tight')



