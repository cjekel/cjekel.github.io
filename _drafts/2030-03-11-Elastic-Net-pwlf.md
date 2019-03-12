---
title:  "Elastic net stuff"
date:   2030-03-11 11:20:00
description: elastic net stuff
keywords: [ piecewise linear fit, Python, pwlf, fitting picewsie lines, best piecewise linear fit]
---

There have been a number of people asking how to use [pwlf](https://github.com/cjekel/piecewise_linear_fit_py) when you don't know how many line segments to use. I've been recomending the use of a regularization technique which [penalizes the number of line segments](https://github.com/cjekel/piecewise_linear_fit_py/blob/master/examples/run_opt_to_find_best_number_of_line_segments.py) (or model complexity). This is problematic in a few ways:
1. It's an expensive three layer optimization problem (least squares fit, find break point locations, find number of line segments).
2. The result will be dependant upon the penalty parameter which is problem specific. Something like cross validation could be used to select the parameter, but again this can be expensive.

The 0.4.0 version of pwlf will include some functions to deal with this.

A large portion of the expense results from searching for breakpoints on a continous domain. Once the breakpoint locations are known, then the resulting piecewise contionus model is just a simple least squares fit. In many applications it is reasonable to assume some discrete set of possible breakpoint locations. For instance, it may be reasonable to assume that a breakpoint can only occur at the observed locations in the data. This would work well for a large amount of data that is evenly distributed in the domain. Alternatively, one could specify a large number of possible breakpoint locations over the domain. 

A least squares fit can be used to solve for the model parameters <span>\\((\mathbf{\beta}) \\)</span> from the discrete list of possible breakpoint locations. Then a changes between consecutive model parameters <span>\\((|\beta_3 - \beta_2|) \\)</span> would tell whether a breakpoint was significant. The following example demonstrates this on a simple example with two distinct line segments.

```python
import numpy as np
import matplotlib.pyplot as plt
import pwlf

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
y = np.array([5, 7, 9, 11, 13, 15, 28.92, 42.81, 56.7, 70.59,
              84.47, 98.36, 112.25, 126.14, 140.03])

# initialize pwlf on data
my_pwlf = pwlf.PiecewiseLinFit(x, y)
# perform a least squares fit with the breakpoints
# occuring at the exact x locaitons
ssr = my_pwlf.fit_with_breaks(x.copy())

# predict on the domain
xhat = np.linspace(x.min(), x.max(), 100)
yhat = my_pwlf.predict(xhat)
```

This results on the following fit which appears excellent.

![excellent fit]({{ "/" | relative_url  }}assets/2019-03-11/simpleex.png)

Let's take a look at the model parameters.

```python
print(my_pwlf.beta)
```
```
[ 5.00000000e+00  2.00000000e+00 -8.72635297e-14  4.06341627e-14
 -1.99840144e-15 -6.66133815e-16  1.19200000e+01 -3.00000000e-02
 -1.24344979e-14  1.29896094e-14 -1.00000000e-02  1.00000000e-02
  2.06085149e-14 -5.27564104e-14  7.40345285e-14]
```

The first parameter is the model offset and the second parameter is the slope of the first line. The remaining parameters are related to the slopes of subsequent lines. The small and near zero parameters imply that the slope didn't change from the previous breakpoint. We can see that seventh parameter is significant as the seventh data point indicates the first data point on the second line.

There are a few obvious problems with this method. One problem is that the least squares problem becomes ill-posed in the case when you have more unknowns than data points. Additionally, this method is likely to result in a poor model that overfits the data. The following example follows the same procedure to fit a contionus peicewise linear model to a noisy sine wave.

```python
# select random seed for reproducibility
np.random.seed(123)
# generate sin wave data
x = np.linspace(0, 10, num=1000)
y = np.sin(x * np.pi / 2)
yture = y.copy()
# add noise to the data
y = np.random.normal(0, 0.05, 100) + ytrue

# initialize pwlf on data
my_pwlf = pwlf.PiecewiseLinFit(x, y)
# perform a least squares fit with the breakpoints
# occuring at the exact x locaitons
ssr = my_pwlf.fit_with_breaks(x.copy())

# predict on the domain
xhat = np.linspace(x.min(), x.max(), 100)
yhat = my_pwlf.predict(xhat)
```

![Overfit of the sine wave]({{ "/" | relative_url  }}assets/2019-03-11/sin_of.png)

The result was a continuous piecewise linear function that has overfit the data. You'll find that most of the <span>\\((\mathbf{\beta}) \\)</span> parameters are active, with an average absolute value of 1.1. 

We can use a linear model regularizer such as [Elastic Net](https://en.wikipedia.org/wiki/Elastic_net_regularization) to prevent this overfitting. The least squares problem minimizes
<div>
$$
\mathbf{\hat{\beta}} = {\underset {\mathbf{\beta} }{\operatorname {argmin} }}( \|\mathbf{y}-\mathbf{A}\mathbf{\beta} \|^{2} )
$$
</div>
which is prone to overfitting when there are a lot of possible <span>\\((\mathbf{\beta}) \\)</span> parameters. The Elastic Net uses both L1 (LASSO) and L2 (Ridge regression) penalties on the model complexity to prevent overfitting, which minimizes
<div>
$$
\mathbf{\hat{\beta}} = {\underset {\mathbf{\beta} }{\operatorname {argmin} }}( \|\mathbf{y}-\mathbf{A}\mathbf{\beta} \|^{2} + \lambda_2 \|\mathbf{\beta} \|^{2} + \lambda_1 \|\mathbf{\beta} \|_{1})
$$
</div>
for some <span>\\((\lambda_1, \lambda_2) \\)</span> penalty parameters. The Elastic Net solution stats each <span>\\((\mathbf{\beta}) \\)</span> parameter at zero, and slowly activate a parameter at a time through the iterations until it converges. This work well for continuous picewise linear functions, where a zero parameter value corresponds to that breakpoint being inactive. 

[Scikit-learn](http://scikit-learn.org/) has implented the Elastic Net reguilizer in [ElasticNet](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html. The important penalty parameters to select will be *l1_ratio* and *alpha*. However, we'll use [ElasticNetCV](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNetCV.html) which will automatically select these parameters based on the cross validation results. The following example perform the Elastic Net fit to the noisy sine wave.

```python
from sklearn.linear_model import ElasticNetCV
my_pwlf_en = pwlf.PiecewiseLinFit(x, y)
# copy the x data to use as break points
breaks = my_pwlf_en.x_data.copy()
# new in 0.4.0; creates the linear regression matrix A 
A = my_pwlf_en.assemble_regression_matrix(breaks, my_pwlf_en.x_data)

# set up the elastic net
en_model = ElasticNetCV(cv=5, l1_ratio=[.1, .5, .7, .9, .95, .99, 1],
                        fit_intercept=False, max_iter=1000000, n_jobs=-1)
# fit the model using the elastic net
en_model.fit(A, my_pwlf_en.y_data)

# predict from the elastic net paramters
xhat = np.linspace(x.min(), x.max(), 1000)
yhat_en = my_pwlf_en.predict(xhat, breaks=breaks, beta=en_model.coef_)
```
![Fit of the sine wave]({{ "/" | relative_url  }}assets/2019-03-11/sin.png)

We can see the Elastic Net results are a much better fit to the sine wave than the least squares fit. The first two parameters are related to the first line segment, so we'll always want to grab the first to parameters. However, after the first two parameters we'll only grab the parameters where there is a change that is greater than a threshold to select important breakpoints. 

```python
true_list = np.zeros(breaks.size, dtype=bool)
true_list[:2] = True
for i in range(breaks.size):
    if np.abs(en_model.coef_[i] - en_model.coef_[i - 1]) > 1e-2:
        true_list[i] = True
    else:
        true_list[i] = False
new_breaks = breaks[true_list]
n_segments = new_breaks.size - 1.

ybreaks = my_pwlf_en.predict(new_breaks)
```

![breakpoint locations]({{ "/" | relative_url  }}assets/2019-03-11/sin_new.png)

This results in 59 parameters 

# pwlf improvements in 0.2.0 release
- **much faster** at finding optimum break point locations due to new derivation of regression problem
- pwlf now uses pure numpy instead of Python to solve continuous piecewise linear fit
- new mathematical derivation (defined below)
- pep8 style naming for class, variables, and functions
- old naming convention still usable, but will be depreciated at some time
- Available soon on [github](https://github.com/cjekel/piecewise_linear_fit_py) or [pypi](https://pypi.python.org/pypi/pwlf)

# New derivation

There was nothing wrong with [Golovchenko (2004)](https://golovchenko.org/docs/ContinuousPiecewiseLinearFit.pdf), which was the basis for the the first release of pwlf. I've always knew that the for loops used to assemble the regression matrix were slow, and this was killing the performance for large problems. After reading [this](https://www.regressionist.com/2018/02/07/continuous-piecewise-linear-fitting/), I felt a bit inspired to do something about it. The [pwlf library](https://github.com/cjekel/piecewise_linear_fit_py) has been modified to solve the linear regression matrix directly, where previously a square matrix was assembled (as oppose to the regression matrix). The result is that more of the code is solved in numpy (which is fast), instead of Python.

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
\beta_1 \\
\beta_2 \\
\vdots \\
\beta_{n_b}
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
where <span>\\(\mathbf{A} \\)</span> is our regression matrix, <span>\\(\mathbf{\beta} \\)</span> is our unknown set of parameters, and <span>\\(\mathbf{y} \\)</span> is our vector of <span>\\(y \\)</span> values. We can use a least squares solver to solve for <span>\\(\mathbf{\beta} \\)</span>. In Python, I like to use the [numpy lstsq](https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq) solver which uses [LAPACK](https://www.netlib.org/lapack/explore-html/d7/d3b/group__double_g_esolve_ga94bd4a63a6dacf523e25ff617719f752) to solve the matrix.

Once you have found your set of optimal parameters <span>\\(\mathbf{\beta} \\)</span>, then you can predict for new <span>\\(x \\)</span> values by assembling your regression matrix <span>\\(\mathbf{A} \\)</span> for the new <span>\\(x \\)</span> values. The new <span>\\(y \\)</span> values are solved by multiplying
<div>
$$
\mathbf{A} \mathbf{\beta} = \mathbf{y}
$$
</div>
the new regression matrix with the determined set of parameters.
