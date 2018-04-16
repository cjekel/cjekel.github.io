---
title:  "Force piecewise linear fit through data"
date:   2018-04-15 23:55:00
description: Now you can use pwlf to force a fit through any set of data points! This is done as a constrained least squares problem.
keywords: [ piecewise linear fit, constrained piecewsise fit, force pwlf through origin, Python, pwlf]
---

I've received a few request for [pwlf](https://github.com/cjekel/piecewise_linear_fit_py) to perform fits through a particular data point, or set of data points. For instance, you may know that your model must go through the origin (0, 0). We can use Lagrange multipliers to solve a constrained least squares problem to find the best piecewise linear fit while forcing the fit through a set of data points.  

# Constrained least squares fit
So from my [previous post](http://jekel.me/2018/Continous-piecewise-linear-regression/), we have defined a piecewise linear regression problem as
<div>
$$
\mathbf{A} \mathbf{\beta} = \mathbf{y}
$$
</div>
where <span>\\(\mathbf{A} \\)</span> is our regression matrix, <span>\\(\mathbf{\beta} \\)</span> is our unknown set of parameters, and <span>\\(\mathbf{y} \\)</span> is our vector of <span>\\(y \\)</span> values. We have a set of data points at <span>\\((\mathbf{w},\mathbf{z}) \\)</span> locations where <span>\\( w\\)</span> is the <span>\\(x \\)</span> locations, and <span>\\( z\\)</span> is the <span>\\(y \\)</span> locations. We we want to force our fit to go through <span>\\((\mathbf{w},\mathbf{z}) \\)</span>.

I searched for a good explanation of constrained least squares problems, and I think the upcoming book by Boyd and Vandenberghe [1] is great. Essentially we need to construct a constraint matrix <span>\\(\mathbf{C} \\)</span>, such that
<div>
$$
\mathbf{C} \mathbf{\beta} = \mathbf{z}
$$
</div>
is strictly enforced. The constraint matrix <span>\\(\mathbf{C} \\)</span>, is of the exact same form as <span>\\(\mathbf{A} \\)</span>, but evaluated at the <span>\\(w \\)</span> values as oppose to the <span>\\(x \\)</span> data points. This means <span>\\(\mathbf{C} \\)</span> will be a matrix with the number of constraints as rows, and one plus the number of line segments as columns. Using a Lagrangian formulation defined in [1], we can set up the constrained least squares problem as
<div>
$$
\begin{bmatrix}
2.0\mathbf{A}^\text{T}\mathbf{A} & \mathbf{C}^\text{T} \\
\mathbf{C} & 0 \\
\end{bmatrix} \begin{bmatrix}
 \mathbf{\beta} \\
 \mathbf{\zeta} \\
 \end{bmatrix} = \begin{bmatrix}
2\mathbf{A}^\text{T}\mathbf{y}
\mathbf{z}
\end{bmatrix}
$$
</div>
where <span>\\(\mathbf{\zeta} \\)</span> is some set of Lagrangian multipliers which will be solved along with <span>\\(\mathbf{\beta} \\)</span>. This is the KKT equations for a constrained least squares problem. We are left with a square matrix, which can be used to solve for our unknown set of <span>\\(\mathbf{\beta} \\)</span> parameters.

# Python implementation in pwlf

This has now been implemented into pwlf with the latest version. You can now fit piecewise linear function for a particular number of line segments, and force the fit to go through a particular set of points.

This example shows how you can force a fit through the origin given a set of x y data.
```python

import numpy as np
import pwlf
# Arbitrary sin wave
x = np.linspace(0.0, 1.0, num=100)
y = np.sin(6.0*x)
# initialize pwlf
myPWLF = pwlf.PiecewiseLinFit(x, y, disp_res=True)
x_c = [0.0]
y_c = [0.0]
# fit three line segments, and force fit through (x_c,y_c)
res = myPWLF.fit(3, x_c, y_c)
```

# References

[1] Boyd, Stephen and Vandenberghe, Lieven. Introduction to Applied Linear Algebra - Vectors, Matrices, and Least Squares. Chapter 16 - Constrained least squares. Cambridge University Press. 2018. [link](https://web.stanford.edu/~boyd/vmls)
