import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

n_one = 20
np.random.seed(123)
noise = np.random.normal(size=(n_one*n_one), loc=0, scale=1e-2)

u = np.linspace(0., np.pi*2., n_one)
v = np.linspace(0., np.pi, n_one)
u, v = np.meshgrid(u, v)
a = 1.2
b = 0.2
c = 0.9
x = a*np.cos(u)*np.sin(v)
y = b*np.sin(u)*np.sin(v)
z = c*np.cos(v)

x = x.flatten() + noise
y = y.flatten() + noise
z = z.flatten() + noise

x0 = 1.1
y0 = 0.7
z0 = 0.3

x += x0
y += y0
z += z0

import jax.numpy as jnp
from jax import grad
from jax import random
from jax.config import config
config.update('jax_enable_x64', True)
key = random.PRNGKey(0)

gamma_guess = np.random.random(6)
gamma_guess[0] = x.mean()
gamma_guess[1] = y.mean()
gamma_guess[2] = z.mean()
gamma_guess = jnp.array(gamma_guess)

print(gamma_guess)


def predict(gamma):
    # compute f hat
    x0 = gamma[0]
    y0 = gamma[1]
    z0 = gamma[2]
    a2 = gamma[3]**2
    b2 = gamma[4]**2
    c2 = gamma[5]**2
    zeta0 = (x - x0)**2 / a2
    zeta1 = (y - y0)**2 / b2
    zeta2 = (z - z0)**2 / c2
    return zeta0 + zeta1 + zeta2


def loss(g):
    # compute mean squared error
    pred = predict(g)
    target = jnp.ones_like(pred)
    mse = jnp.square(pred-target).mean()
    return mse


print(loss(gamma_guess))
print(grad(loss)(gamma_guess))

from scipy.optimize import fmin_bfgs

res = fmin_bfgs(
    loss,
    gamma_guess,
    fprime=grad(loss),
    norm=2.0,
    args=(),
    gtol=1e-17,
    maxiter=None,
    full_output=1,
    disp=1,
    retall=0,
    callback=None
)
print(res)

# plot the predictions
u, v = np.meshgrid(np.linspace(0, np.pi*2, 40), np.linspace(0, np.pi, 20))
r = 1.0 / np.sqrt((np.cos(u)/res[0][3])**2 + (((np.sin(u)/res[0][4])**2)*np.sin(v)**2) + ((np.cos(v)/res[0][5])**2))
xhat = np.cos(u)*np.sin(v)*r
yhat = np.sin(u)*np.sin(v)*r
zhat = np.cos(v)*r
xhat = xhat + res[0][0]
yhat = yhat + res[0][1]
zhat = zhat + res[0][2]

#   3D plot of Ellipsoid
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, zdir='z', s=20, c='b', rasterized=True)
ax.plot_wireframe(xhat, yhat, zhat, color="r")

plt.savefig('result.png', format='png', dpi=300, bbox_inches='tight')
plt.show()
