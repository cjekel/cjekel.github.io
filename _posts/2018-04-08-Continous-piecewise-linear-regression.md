---
title:  "pwlf update: fitting continuous piecewise linear models to data"
date:   2018-04-08 17:20:00
description: New derivation used in pwlf library for fitting continuous piecewise linear functions to data.
keywords: [ piecewise linear fit, Python, pwlf, fitting picewsie lines, best piecewise linear fit]
---

# pwlf improvements in 0.2.0 release
- **much faster** at finding optimum break point locations due to new derivation of regression problem
- pwlf now uses pure numpy instead of Python to solve continuous piecewise linear fit
- new mathematical derivation (defined below)
- pep8 style naming for class, variables, and functions
- old naming convention still usable, but will be depreciated at some time
- Available soon on [github](https://github.com/cjekel/piecewise_linear_fit_py) or [pypi](https://pypi.python.org/pypi/pwlf)

# New derivation

There was nothing wrong with [Golovchenko (2004)](http://golovchenko.org/docs/ContinuousPiecewiseLinearFit.pdf), which was the basis for the the first release of pwlf. I've always knew that the for loops used to assemble the regression matrix were slow, and this was killing the performance for large problems. After reading [this](http://www.regressionist.com/2018/02/07/continuous-piecewise-linear-fitting/), I felt a bit inspired to do something about it. The [pwlf library](https://github.com/cjekel/piecewise_linear_fit_py) has been modified to solve the linear regression matrix directly, where previously a square matrix was assembled (as oppose to the regression matrix). The result is that more of the code is solved in numpy (which is fast), instead of Python.

Let's assume we have a one dimensional data set. In this case we will assume <span>\\(\mathbf{x} \\)</span> is the independent variable and <span>\\(\mathbf{y} \\)</span> is dependent on <span>\\(\mathbf{x} \\)</span> such that <span>\\(\mathbf{y}(\mathbf{x}) \\)</span>. Our data is paired as
<div>
$$
\begin{bmatrix}
x_1 & y_1 \\
x_2 & y_2 \\
x_3 & y_3 \\
\vdots & \vdots \\
x_n & y_n \\
\end{bmatrix}
$$
</div>
where <span>\\((x_1, y_1) \\)</span> represents the first data point and the data points have been ordered according to <span>\\( x_1 < x_2 < x_3 < \cdots < x_n \\)</span> for <span>\\(n \\)</span> number of data points. A piecewise linear function can be constructed to the function as follows
<div>
$$
\mathbf{y}(x) = \begin{cases}
      \eta_1 + \beta_1(x-b_1) & b_1 < x \leq b_2 \\
      \eta_2 + \beta_2(x-b_2) & b_2 < x \leq b_3 \\
      \vdots & \vdots \\
      \eta_n + \beta_{n_b}(x-b_{n_b-1}) & b_{n-1} < x \leq b_{n_b} \\
\end{cases}
$$
</div>
where <span>\\(b_1 \\)</span> is the <span>\\(x \\)</span> location of the first break point, <span>\\(b_2 \\)</span> is the <span>\\(x \\)</span> location of the second break point, and so forth until the last break point <span>\\(b_{n_b} \\)</span> for <span>\\(n_b \\)</span> number of break points. The break points are also ordered as <span>\\(b_1 < b_2 < \cdots < b_{n_b} \\)</span>. Additionally the first break point is always <span>\\(b_1 = x_1 \\)</span>, and the last break point is always <span>\\(b_{n_b} = x_n \\)</span>. This initialization of the data seems tedious at first, but some magic will happen later on if you arrange the data this way.

Now if we enforce that the piecewise linear functions be continuous on the domain, we'll end up with
<div>
$$
\mathbf{y}(x) = \begin{cases}
      \beta_1 + \beta_2(x-b_1) & b_1 \leq x \leq b_2 \\
      \beta_1 + \beta_2(x-b_1) + \beta_3(x-b_2) & b_2 < x \leq b_3 \\
      \vdots & \vdots \\
      \beta_1 + \beta_2(x-b_1) + \beta_3(x-b_2) + \cdots + \beta_{n_b+1}(x-b_{n_b-1}) & b_{n-1} < x \leq b_{n_b} \\
\end{cases}
$$
</div>
as our continuous piecewise linear function. This can be extended in Matrix form as
<div>
$$
\begin{bmatrix}
1 & x_1-b_1 & (x_1-b_2)1_{x_1 > b_2} & (x_1-b_3)1_{x_1 > b_3} & \cdots & (x_1-b_{n_b-1})1_{x_1 > b_{n_b-1}} \\
1 & x_2-b_1 & (x_2-b_2)1_{x_2 > b_2} & (x_2-b_3)1_{x_2 > b_3} & \cdots & (x_2-b_{n_b-1})1_{x_2 > b_{n_b-1}} \\
\vdots & \vdots & \vdots & \vdots &  \ddots & \vdots \\
1 & x_n-b_1 & (x_n-b_2)1_{x_n > b_2} & (x_n-b_3)1_{x_n > b_3} & \cdots & (x_n-b_{n_b-1})1_{x_n > b_{n_b-1}} \\
\end{bmatrix} \begin{bmatrix}
\beta_1 \\y_0 \\

\beta_2 \\
\vdots \\
\beta_{n_b+1}
\end{bmatrix} = \begin{bmatrix}
y_1 \\
y_2 \\
\vdots \\
y_n
\end{bmatrix}
$$
</div> where <span>\\(1_{x_n > b_1} \\)</span> represents the piecewise function of form
<div>
$$
1_{x_n > b_2} = \begin{cases}
      0 & x_n \leq b_2 \\
	  1 & x_n > b_2 \\
\end{cases}
$$
</div>
and <span>\\(1_{x_n > b_3} \\)</span> represents
<div>
$$
1_{x_n > b_3} = \begin{cases}
      0 & x_n \leq b_3 \\
	  1 & x_n > b_3 \\
\end{cases}
$$
</div> and so forth. This is where the magic happens! If you've ordered your data, the result will be a regression matrix that's already in a lower triangular style. Since <span>\\(\mathbf{x} \\)</span> was initially sorted from min to max, the matrix can be assembled quickly by replacing only the non-zero values. This won't be a big deal if you know the break point locations <span>\\(\mathbf{b} \\)</span>. However if you were running an optimization to find the ideal location for break points (as in pwlf), you may need to assemble the regression matrix thousands of times.

We can express the matrix expression as a linear equation
<div>
$$
\mathbf{A} \mathbf{\beta} = \mathbf{y}
$$
</div>
where <span>\\(\mathbf{A} \\)</span> is our regression matrix, <span>\\(\mathbf{\beta} \\)</span> is our unknown set of parameters, and <span>\\(\mathbf{y} \\)</span> is our vector of <span>\\(y \\)</span> values. We can use a least squares solver to solve for <span>\\(\mathbf{\beta} \\)</span>. In Python, I like to use the [numpy lstsq](https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq) solver which uses [LAPACK](http://www.netlib.org/lapack/explore-html/d7/d3b/group__double_g_esolve_ga94bd4a63a6dacf523e25ff617719f752) to solve the matrix.

Once you have found your set of optimal parameters <span>\\(\mathbf{\beta} \\)</span>, then you can predict for new <span>\\(x \\)</span> values by assembling your regression matrix <span>\\(\mathbf{A} \\)</span> for the new <span>\\(x \\)</span> values. The new <span>\\(y \\)</span> values are solved by multiplying
<div>
$$
\mathbf{A} \mathbf{\beta} = \mathbf{y}
$$
</div>
the new regression matrix with the determined set of parameters.
