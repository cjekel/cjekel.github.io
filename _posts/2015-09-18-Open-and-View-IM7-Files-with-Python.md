---
title:  "Open and View IM7 Files with Python"
date:   2015-09-18 23:44:00
description: How to open and view LaVision DaVis IM7 files using the wrapper ReadIM and Python
keywords: [Python, LaVision, open IM7 files, how to, open IM7 files in Python]
---
This post will describe how to open and view LaVision DaVis IM7 files in Python.

Digital Image Correlation (DIC) is a non-intrusive optical tool for providing displacement values and strain fields. I use DIC to measure the full displacement field when I test my material samples. In my department, we use the hardware and software of [LaVision](http://www.lavision.de/en/index.php) GMBH for all of our DIC needs. The images captured by the LaVision hardware for my DIC projects are stored in IM7 files. Unfortunately IM7 files can only be opened in DaVis (Unless you are a MATLAB user and can take advantage of [ReadIMX](http://www.lavision.de/en/news/2014/2244/)). It would be nice to open IM7 files, to view the images stored inside, without opening the DaVis software.

Well thanks to [Alan Fleming](https://bitbucket.org/fleming79/), there is now a tool to read IM7 files in Python. [ReadIM](https://pypi.python.org/pypi/ReadIM/0.6.5) is a wrapper that works with the C++ libraries provided by LaVision GMBH. You should be able to install ReadIM with pip on Python versions 2.7, 3.3 and 3.4. If pip fails, you'll have to follow the build instructions [here](https://bitbucket.org/fleming79/readim).

To install with pip simply run the following line in your terminal.
```bash
pip install ReadIM
```

I'm using Python 2.7, and the pip install was successful. We can open an IM7 file in Python with the following commands, where myDavis.im7 is the IM7 file that I'd like to open. We won't be working with vbuff. Since Mr. Fleming informs us that memory cleanup is not automatic, we'll have to manually delete vbuff.

```python
>>> import ReadIM
>>> vbuff, vatts = ReadIM.extra.get_Buffer_andAttributeList('myDaVis.im7')
>>> v_array, vbuff = ReadIM.extra.buffer_as_array(vbuff)
>>> del(vbuff)
```

The contents of the IM7 file can now be found in the numpy array v\_array. By inspecting the shape of v\_array, we'll gain some insight onto how the images are stored.
```python
>>> import numpy as np
>>> np.shape(v_array)
(2L, 2456L, 2058L)
```

We see the shape of v\_array to be 2L, 2456L, 2058L. I use two 5-megapixel cameras in my DIC setup. So the shape of v\_array is starting to make sense. ReadIM has read my IM7 file as a multidimensional numpy array. In my case the array is stored in the following arrangement: [Camera #][Pixels Y][Pixels X]. If we multiply the number of pixels in the Y and X directions, we'll see over 5 million pixels from my 5-megapixel cameras.
```python
>>> 2456 * 2058
5054448
```

We can now create a plot of the first camera image stored in the IM7 file with matplotlib in Python. Since DIC uses contrast values, it makes sense to plot the image as greyscale by setting the cmap parameter.  
```python
>>> import matplotlib.pyplot as plt
>>> import matplotlib.cm as cm
>>> plt.imshow(v_array[0], cmap = cm.Greys_r)
>>> plt.show()
```

The above code generates the following image.
![8bit IM7 Plotted in python with matplotlib]({{ "/" | relative_url  }}assets/2015-09-18/16bitIM7.png)

Everything is really dark, and we can't make out the test specimen in the generated image. Let's take a look at v\_array for the first camera image to give us a clue as to why the image is so dark.
```python
>>> v_array[0]
array([[ 22,  31,  31, ..., 135, 128,  99],
       [ 29,  23,   9, ..., 159, 145, 143],
       [ 42,  19,   4, ..., 107, 156, 150],
       ...,
       [ 19,  19,  28, ..., 166, 144, 147],
       [ 23,  26,  22, ..., 157, 180, 159],
       [ 18,  16,  19, ..., 160, 185, 148]], dtype=uint16)
```

We can see the intensity values for each of the X and Y pixels are stored as 16 bit integers. For recording purposes, we want the largest bit size to capture the entire intensity spectrum as best as possible. However, the 16 bit integers may make it difficult to decipher what exactly is in the image. We can convert from a 16 bit to an 8 bit integer array, and then plot the 8 bit array to view the camera image.
```python
>>> img8 = v_array.astype('uint8')
>>> plt.imshow(img8[0], cmap = cm.Greys_r)
>>> plt.show()
```

The above code creates a new 8 bit integer array from existing 16 bit integer array. By plotting the 8 bit array, we get the following image.
![8bit IM7 Plotted in python with matplotlib]({{ "/" | relative_url  }}assets/2015-09-18/8bitIM7.png)

ReadIM has allowed me to open and view my IM7 files from my DIC projects without needing to open DaVis. If I ever wanted to view all of the IM7 images of a project, I could easily create a script that could loop through all of the IM7 files in a directory. The script could then export each camera image in a traditional file format.
