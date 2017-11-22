import numpy as np
import math

#   load my  data
[x, y] = np.load('myData.npy')

#   plot my data
import matplotlib.pyplot as plt
plt.figure()
plt.plot(x,y, 'ok')
plt.grid(True)
plt.show()
plt.savefig('myData.png', dpi=300, type='png')

#   define a function to calculate the log likiehood
def calcLogLikelihood(guess, true, n):
    error = true-guess
    sigma = np.std(error)
    f = ((1.0/(2.0*math.pi*sigma*sigma))**(n/2))* \
        np.exp(-1*((np.dot(error.T,error))/(2*sigma*sigma)))
    return np.log(f)
    
#   define my function which will return the objective function to be minimized
def myFunction(var):
    yGuess = (var[2]*(x**2)) + (var[1]*x) + var[0]
    f = calcLogLikelihood(yGuess, y, float(len(yGuess)))
    return (-1*f)
    
#    Let's pick some random starting points for the optimizaiton    
nvar = 3
var = np.zeros(nvar)
var[0] = -15.5
var[1] = 19.5
var[2] = -1.0

#   let's maximize the liklihood (minimize -1*max(likelihood)
from scipy.optimize import minimize
res = minimize(myFunction, var, method='BFGS',
                options={'disp': True})
                
#   pefrom least squres fit using scikitlearn
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
model = Pipeline([('poly', PolynomialFeatures(degree=2)),
    ('linear', LinearRegression(fit_intercept=False))])

model = model.fit(x[:, np.newaxis], y)
coefs = model.named_steps['linear'].coef_

#   plot the data and model fits
plt.figure()
plt.plot(x,y, 'ok')
plt.plot(x,model.predict(x[:,np.newaxis]), '-r', label='Least Squres')
plt.plot(x,(res.x[2]*(x**2)) + (res.x[1]*x) + res.x[0], '--b', label='Max Likelihood')
plt.grid(True)
plt.legend(loc=2)
plt.show()
plt.savefig('maxLikelihoodComp.png', dpi=300, type='png')

                
    