---
title:  "Least Squares Ellipsoid Fit"
date:   2020-09-20 15:00:00
description: How to fit an ellipsoid to data points using the least squares method with a simple Python example.
keywords: [Python, least squares fit, ellipsoid fit, Python ellipsoid fit, fitting ellipsoids]
---

*Edit 2021 December 4. In many cases you'll need to do a non-linear fit to find optimal ellipsoid parameters which I discuss in a newer post as [a better way to fit ellipsoids](https://jekel.me/2021/A-better-way-to-fit-Ellipsoids/).*


In one of my previous posts, I demonstrated [how to fit a sphere using the least squares](https://jekel.me/2015/Least-Squares-Sphere-Fit/) method. In this post I'll show how you can also fit an ellipsoid using a least squares fit. It ends up being a bit simpler than the sphere. I'll also include a simple Python example to perform least square ellipsoid fits.

# Least-squares method

## Mathematical background

The equation of a three dimensional ellipsoid can be described as
<div>
$$
\frac{x^2}{a^2} + \frac{y^2}{b^2} + \frac{z^2}{c^2} = 1
$$
</div>
where <span>\\( x \\)</span>, <span>\\( y \\)</span>, and <span>\\( z \\)</span> are the cartesian coordinates of some dataset. Now let's rearrange the equation to become
<div>
$$
\beta_a x^2 + \beta_b y^2 + \beta_c z^2 = 1
$$
</div>
where <span>\\( \beta_a = 1 / a^2 \\)</span>, <span>\\( \beta_b = 1 / b^2 \\)</span>, and <span>\\( \beta_c = 1/c^2 \\)</span>. Now we can express the problem in matrix form as the following linear system of equations as
<div>
$$
\mathbf{A} \mathbf{B} = \mathbf{O}
$$
</div> where <span>\\( \mathbf{A} \\)</span> is a matrix of our squared data components, <span>\\( \mathbf{B} \\)</span> is a vector of <span>\\( \beta \\)</span> parameters of the ellipsoid that we intend to solve for, and <span>\\( \mathbf{O} \\)</span> is a vector of ones. To be explicit we have
<div>
$$
\begin{bmatrix}
x_{1}^2 & y_{1}^2 & z_{1}^2 \\
x_{2}^2 & y_{2}^2 & z_{2}^2 \\
\vdots & \vdots & \vdots  \\
x_{n}^2 & y_{n}^2 & z_{n}^2 \\
\end{bmatrix} \begin{bmatrix}
\beta_a \\
\beta_b \\
\beta_c \\
\end{bmatrix} = \begin{bmatrix}
1.0 \\
1.0 \\
\vdots \\
1.0
\end{bmatrix}
$$
</div>
for <span>\\( n \\)</span> number of data points.

Now a [least squares problem](https://en.wikipedia.org/wiki/Least_squares) is a simple optimization which finds the model parameters which minimize the L2 norm between the model and the data. This can be expressed as
<div>
$$
\mathrm{arg\,min}_{\mathbf{B}} (\mathbf{A} \mathbf{B} - \mathbf{O})^2
$$
</div>
and it happens to have a solution of
<div>
$$
\mathbf{B} = (\mathbf{A}^\mathrm{T}\mathbf{A})^{-1} \mathbf{A}^\mathrm{T} \mathbf{O}
$$
</div>
which is found by setting the first derivative of the linear equation to zero. 

Once <span>\\( \mathbf{B} \\)</span> is solved for, it is only a simple rearrangement to solve for <span>\\( a \\)</span>, <span>\\( b \\)</span>, and <span>\\( c \\)</span>.
<div>
$$
a = \sqrt{\frac{1}{\beta_a}} \\
b = \sqrt{\frac{1}{\beta_b}} \\
c = \sqrt{\frac{1}{\beta_c}} \\
$$
</div>


## Example ellipsoid data

Let's generate data for an ellipsoid where <span>\\( a = 1.2 \\)</span>, <span>\\( b = 0.2 \\)</span>, and <span>\\( c = 0.9 \\)</span>. This is easiest using parametric equation as
<div>
$$
x	=	a \cos u \sin v	\\
y	=	b \sin u \sin v	\\
z	=	c \cos v
$$
</div>
where <span>\\( u \in [0, 2\pi] \\)</span> and <span>\\( v \in [0, \pi] \\)</span>. 

We can quickly generate the cartesian points in Python for this ellipsoid using the following code.

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

a = 1.2
b = 0.2
c = 0.9

u = np.linspace(0., np.pi*2., 20)
v = np.linspace(0., np.pi, 20)
u, v = np.meshgrid(u,v)

x = a*np.cos(u)*np.sin(v)
y = b*np.sin(u)*np.sin(v)
z = c*np.cos(v)

# turn this data into 1d arrays
x = x.flatten()
y = y.flatten()
z = z.flatten()

#   3D plot of ellipsoid
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, zdir='z', s=20, c='b',rasterized=True)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
```
Which gives us the following data and plot in cartesian coordinates.

![Example ellipsoid for a=1.2, b = 0.3, and c=0.9]({{ "/" | relative_url  }}assets/2020-09-20/myellipsoid.png)

## Python code to fit ellipsoid

Now in order to fit an ellipsoid to the above data, we need to create the matrix <span>\\( \mathbf{A} \\)</span> and vector  <span>\\( \mathbf{O} \\)</span>. Then we'll use [numpy's least squares](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html) solver to find the parameters of the ellipsoid. Lastly we'll adjust the parameters such that our ellipse is in standard form.

```python
# build our regression matrix
A = np.array([x**2, y**2, z**2]).T

# vector of ones
O = np.ones(len(x))

# least squares solver
B, resids, rank, s = np.linalg.lstsq(A, O)

# solving for a, b, c
a_ls = np.sqrt(1.0/B[0])
b_ls = np.sqrt(1.0/B[1])
c_ls = np.sqrt(1.0/B[2])

print(a_ls, b_ls, c_ls)
```

Running all of the code together will give you a_ls=1.1999999999999995, b_ls=0.19999999999999993 and c_ls=0.9000000000000006. This is double precision error on our original ellipsoid of <span>\\( a = 1.2 \\)</span>, <span>\\( b = 0.2 \\)</span>, and <span>\\( c = 0.9 \\)</span>. Not too bad! Hopefully you can use this to formulate other least squares problems, or ellipsoids in higher dimensions. 

# Arbitrary ellipsoids in space

The above least squares problem works well if you data is centered at <span>\\( x_0 = 0 \\)</span>, <span>\\( y_0 = 0 \\)</span>, and <span>\\( z_0 = 0 \\)</span>. Unfortunately, many practical problems will have data that is not centered around the origin. For these cases, we will need to formulate a more expensive non-linear regression problem that uses optimization to find the ellipsoid parameters. We will use [jax.numpy](https://jax.readthedocs.io/en/latest/jax.numpy.html) as an automatic differentiation code to easily compute derivatives for our custom non-linear regression.

So an arbitrary ellipsoid in 3D space can be defined as
<div>
$$
\frac{(x-x_0)^2}{a^2} + \frac{(y-y_0)^2}{b^2} + \frac{(z-z_0)^2}{c^2} = 1
$$
</div>
where our ellipsoid parameters are <span>\\( x_0 \\)</span>, <span>\\( y_0 \\)</span>, <span>\\( z_0 \\)</span>, <span>\\( a \\)</span>, <span>\\( b \\)</span>, and <span>\\( c \\)</span>. We can then setup an optimization formulation to find the best six parameters to some arbitrary collection of data in 3D space. Given these six parameters, we can go on to calculate an error between the six parameter ellipsoid and the data set. Optimization will then be used to find the six parameters that minimizes this error.

Given six ellipsoid parameters and any observed data point as <span>\\( x_i \\)</span>, <span>\\( y_i \\)</span>, and <span>\\( z_i \\)</span>, we can predict three separate ellipsoids. This may sound strange at first, but what we are essentially after are three predictions <span>\\( \hat{x}_i \\)</span>, <span>\\( \hat{y}_i \\)</span>, and <span>\\( \hat{z}_i \\)</span>. These predictions are generated by the following equations.

<div>
$$
(\hat{x} - x_0)^2 = a^2 \bigg ( 1 - \frac{(z_i-z_0)^2}{c^2} - \frac{(y_i-y_0)^2}{b^2} \bigg )
$$
</div>