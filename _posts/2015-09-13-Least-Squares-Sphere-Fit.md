---
title:  "Least Squares Sphere Fit"
date:   2015-09-13 22:00:00
description: Fitting a sphere to data points using the least squares method
keywords: [Python, least squares fit, sphere fit, Python sphere fit]
---
*Update: 2016-01-22 I have added the code I used to make the plot of the 3D data and sphere!*

It may not be intuitive to fit a sphere to three dimensional data points using the least squares method. This post demonstrates how the equation of a sphere can be rearranged to formulate the least squares problem. A Python function, which determines the sphere of best fit, is then presented.

So let's say you have a three dimensional data set. The data points plotted in three dimensional space resemble a sphere, so you'd like to know the sphere that would fit your data set the best. Well I have a sample data set that is well suited for a spherical fit using the least squares method. A plot of data points in three dimensional space can be seen in the following image. Now let's go through the process fitting a sphere to this data set.

![Data points in three dimensions]({{ "/" | relative_url  }}assets/2015-09-13/pointsIn3DSpace.png)


The general equation of a sphere  in <span>\\( x \\)</span>, <span>\\( y \\)</span>, and <span>\\( z \\)</span> coordinates can be seen below. The center point of the sphere with radius <span>\\( r \\)</span> is found at the point ( <span>\\( x\_{0} \\)</span>, <span>\\( y\_0 \\)</span>, <span>\\( z\_0 \\)</span> ). We must rearrange the terms of the equation in order to use the least squares method.

<div>
$$
(x - x_0)^2 + (y - y_0)^2 + (z - z_0)^2 = r^2
$$
</div>

After expanding and rearranging the terms, the new equation of a sphere is expressed below. This equation can now be expressed in vector/matrix notation.

<div>
$$
x^2 + y^2 + z^2 = 2xx_0 + 2yy_0 + 2zz_0 + r^2 - x_0^2 - y_0^2 - z_0^2
$$
</div>

The <span>\\( \vec{f} \\)</span> vector, the <span>\\( A \\)</span> matrix, and the <span>\\( \vec{c} \\)</span> vector represents the consolidated terms of the expanded sphere equation. The terms <span>\\( x\_{i} \\)</span>, <span>\\( y\_i \\)</span>, and <span>\\( z\_i \\)</span> represent the first data point, while <span>\\( x\_n \\)</span>, <span>\\( y\_n \\)</span>, and <span>\\( z\_n \\)</span> represent the last data point in the data set.

<div>
$$
\vec{f} = \begin{bmatrix}
  x_i^2 + y_i^2 + z_i^2 \\
  x_{i+1}^2 + y_{i+1}^2 + z_{i+1}^2 \\
  \vdots \\
  x_{n}^2 + y_{n}^2 + z_{n}^2
 \end{bmatrix}
$$
</div>

<div>
$$
A = \begin{bmatrix}
  2x_i & 2y_i & 2z_i & 1 \\
  2x_{i+1} & 2y_{i+1} & 2z_{i+1} & 1 \\
  \vdots & \vdots & \vdots & \vdots \\
  2x_n & 2y_n & 2z_n & 1 \\
 \end{bmatrix}
$$
</div>


<div>
$$
\vec{c} = \begin{bmatrix}
  x_0 \\
  y_0 \\
  z_0 \\
  r^2 - x_{0}^2 - y_{0}^2 - z_{0}^2
 \end{bmatrix}
$$
</div>

We now have an over-determined system suitable for the least squares method of a spherical fit. The new equation is seen below. The fit determines the best <span>\\( \vec{c} \\)</span> from the data points. We can then calculate the sphere's radius using the terms in the <span>\\( \vec{c} \\)</span>.

<div>
$$
\vec{f} = A\vec{c}
$$
</div>

We can use the above equation to define a simple Python function that will fit a sphere to <span>\\( x \\)</span>, <span>\\( y \\)</span>, and <span>\\( z \\)</span> data points. The Python NumPy library includes a least squares function that is used to determine the best <span>\\( \vec{c} \\)</span>. The function then returns the radius and center coordinates of the sphere.

```python
import numpy as np
#	fit a sphere to X,Y, and Z data points
#	returns the radius and center points of
#	the best fit sphere
def sphereFit(spX,spY,spZ):
    #   Assemble the A matrix
    spX = np.array(spX)
    spY = np.array(spY)
    spZ = np.array(spZ)
    A = np.zeros((len(spX),4))
    A[:,0] = spX*2
    A[:,1] = spY*2
    A[:,2] = spZ*2
    A[:,3] = 1

    #   Assemble the f matrix
    f = np.zeros((len(spX),1))
    f[:,0] = (spX*spX) + (spY*spY) + (spZ*spZ)
    C, residules, rank, singval = np.linalg.lstsq(A,f)

    #   solve for the radius
	t = (C[0]*C[0])+(C[1]*C[1])+(C[2]*C[2])+C[3]
    radius = math.sqrt(t)

    return radius, C[0], C[1], C[2]
```

We can easily fit a sphere to our original data set using this function. The resulting sphere of best fit plotted with the original data points can be seen in the following image.

![fitted data points in three dimensions]({{ "/" | relative_url  }}assets/2015-09-13/fittedPointsIn3DSpace.png)

The above 3D plot of the fitted sphere and data was created using the following code.
```python
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
#   3D plot of the
import matplotlib.pyplot as plt

r, x0, y0, z0 = sphereFit(correctX,correctY,correctZ)
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x=np.cos(u)*np.sin(v)*r
y=np.sin(u)*np.sin(v)*r
z=np.cos(v)*r
x = x + x0
y = y + y0
z = z + z0

#   3D plot of Sphere
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(correctX, correctY, correctZ, zdir='z', s=20, c='b',rasterized=True)
ax.plot_wireframe(x, y, z, color="r")
ax.set_aspect('equal')
ax.set_xlim3d(-35, 35)
ax.set_ylim3d(-35,35)
ax.set_zlim3d(-70,0)
ax.set_xlabel('$x$ (mm)',fontsize=16)
ax.set_ylabel('\n$y$ (mm)',fontsize=16)
zlabel = ax.set_zlabel('\n$z$ (mm)',fontsize=16)
plt.show()
plt.savefig('steelBallFitted.pdf', format='pdf', dpi=300, bbox_extra_artists=[zlabel], bbox_inches='tight')
```

Please let me know if you found this post useful!  

Please cite this work as:
```bibtex
@book{Jekel2016,
 author = {Jekel, Charles F},
 booktitle = {Obtaining non-linear orthotropic material
              models for pvc-coated polyester via inverse
              bubble inflation},
 chapter = {Appendix A},
 organization = {Stellenbosch University},
 pages = {83--87},
 title = {Digital Image Correlation on Steel Ball},
 url = {http://hdl.handle.net/10019.1/98627},
 year = {2016}
}
```
