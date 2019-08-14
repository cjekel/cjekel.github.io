---
title:  "Comparing measures of similarity between curves"
date:   2017-07-02 11:11:00
description: There are many different metrics that can be minimized to determine how similar two different curves are. This post looks at fitting a line to data points by minimizing different metrics of similarity. A least squares optimization is done which minimizes the sum-of-squares. The traditional least squares fit is compared to minimizing the discrete Fréchet distance, the dynamic time warping (DTW) distance, and my own area metric.
keywords: [similarity between two curves, Fréchet distance, dynamic time warping, DTW, Python]
---

#### Edit: July 15, 2018
I've published a paper on this topic aimed at identifying unique material load/unload curves [doi:10.1007/s12289-018-1421-8](https://doi.org/10.1007/s12289-018-1421-8) [pdf]({{ "/" | relative_url  }}assets/papers/JekelArea_IJMF_rev05_final.pdf). Additionally I've created a Python library called [similaritymeasures](https://github.com/cjekel/similarity_measures) which includes the Partial Curve Mapping method, Area between two curves, Discrete Fréchet distance, and Curve Length based similarity measures. These methods are useful for quantifying the differences between 2D curves.

---

A simple regression problem is set up to compare the effect of minimizing the sum-of-squares, discrete Fréchet distance, dynamic time warping (DTW) distance, and the area between two curves. The sum-of-squares is minimized with a traditional least squares fit. The discrete Fréchet distance is an approximation of the Fréchet distance which measures the similarity between two curves.  The Fréchet distance is famously described with the walking dog analogy. For more on the Fréchet distance, check out this [wiki](https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance). Dynamic time warping (DTW) has been used famously for speech recognition, and essentially calculates a metric of the similarity between two curves. The wiki page on [DTW](https://en.wikipedia.org/wiki/Dynamic_time_warping) is pretty useful. I've create an algorithm to calculate the area between two curves. The area between two curves can be used as another metric of similarity.

With regression, model parameters are determined by minimizing some measure of the similarity between two curves. With the sum-of-squares error metric, parameters are determined with a least-squares fit. A least squares fit is an easy to solve optimization problem. However model parameters can also be determined with a more expensive global optimization method by minimizing any one of the discrete Fréchet distance, DTW, or area metrics.

## Methodology
Data is generated from <span>\\( y = 2x + 1 \\)</span> for <span>\\( 0 \leq x \leq 10 \\)</span>. A line is fit to the data with the <span>\\( y = mx + b \\)</span> where <span>\\( m \\)</span> and <span>\\( b \\)</span> are the two parameters of the line. Various outliers are created by adding or subtracting 10 to the <span>\\( y \\)</span> value at a particular <span>\\( x \\)</span> location. Various lines are fit with different outliers to the data. Additionally the number of data points are varied. Lines are fit to the various data sets by minimizing either the sum-of-squares, discrete Fréchet distance, DTW, and area between curves. The intention is to compare the lines from the different metrics of similarity between two curves.

## Results
Various fits were attempted by varying the number of data points and outliers. Plots of the fits are shown bellow.

### n = 50, no outlier
![n = 50, no outlier]({{ "/" | relative_url  }}assets/2017-07-02/0.png)

### n = 50, one outlier, towards ends
![n = 50, one outlier, towards ends]({{ "/" | relative_url  }}assets/2017-07-02/1.png)

### n = 50, two outlier, towards ends
![n = 50, two outlier, towards ends]({{ "/" | relative_url  }}assets/2017-07-02/2.png)

### n = 50, three outlier, towards ends
![n = 50, three outlier, towards ends]({{ "/" | relative_url  }}assets/2017-07-02/3.png)

### n = 50, one outlier, towards center
![n = 50, one outlier, towards center]({{ "/" | relative_url  }}assets/2017-07-02/4.png)

### n = 50, two outlier, opposite ends
![n = 50, two outlier, opposite ends]({{ "/" | relative_url  }}assets/2017-07-02/5.png)

### n = 100, one outlier, towards center
![n = 100, one outlier, towards center]({{ "/" | relative_url  }}assets/2017-07-02/6.png)

### n = 100, two outlier, towards center
![n = 100, two outlier, towards center]({{ "/" | relative_url  }}assets/2017-07-02/7.png)

### n = 100, three outlier, towards center
![n = 100, three outlier, towards center]({{ "/" | relative_url  }}assets/2017-07-02/8.png)

## Conclusion
Minimizing the sum-of-squares creates a model that is a compromise between the outlier and the data. The line from the sum-of-squares minimization is slightly effected by the outlier, as the lines move slightly from the true trend. Minimizing the Fréchet distance is strongly susceptible to outliers. In this example minimizing the Fréchet distance appears to be analogous to minimizing the maximum absolute error. I was surprised to find that minimizing the DTW or area between curves produced the same results. Both the DTW and area metrics completely ignore outliers and find the true line.
