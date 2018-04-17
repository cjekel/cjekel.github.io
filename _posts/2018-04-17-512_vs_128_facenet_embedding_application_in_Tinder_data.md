---
title:  "512 vs 128 FaceNet embeddings on Tinder dataset"
date:   2018-04-17 13:35:00
description: Comparing the new 512 embedding facenet models with the old 128 embedding models on my Tinder dataset.
keywords: [facenet, tinder classifcation, python facenet, face classification, 512 vs 128 facial embedding ]
---

In [Classifying Online Dating Profiles on Tinder using FaceNet Facial Embeddings](https://arxiv.org/abs/1803.04347) I said that the different [facenet](https://github.com/davidsandberg/facenet) models didn't influence the results by much. Here I'll show by just how much different facenet models change my overall accuracy.

# New facenet models
Previously I have used the [20170512](https://drive.google.com/file/d/0B5MzpY9kBtDVZ2RpVDYwWmxoSUk/edit) [(mirror)](https://mega.nz/#!d6gxFL5b!ZLINGZKxdAQ-H7ZguAibd6GmXFXCcr39XxAvIjmTKew) facenet model in my work. It scored a 0.99 LFW [1] accuracy, and was sufficient for building a classification model to my Tinder dataset.

Now there are two new facenet models available for download. The [20180402](https://drive.google.com/file/d/1EXPBSXwTaqrSC0OhUdXNmKSh9qJUQ55-/view) model was trained on VGGFace2 dataset [2], and scores a 0.9965 LFW accuracy (this might be the highest LFW accuracy of a facenet model thus far released). The [20180408](https://drive.google.com/file/d/1R77HmFADxe87GmoLwzfgMu_HY0IhcyBz/view) model was  trained on CASIA-WebFace dataset [3], and scores a 0.9905 LFW accuracy.

The major difference with these two new models, and the previous models is that the dimensions of the embeddings vector has been increased from 128 to 512. Essentially the last layer in the new models now has 512 nodes, where the previous models used 128 nodes. Naturally I was interested if this increased dimension had any effect on the accuracy on my Tinder dataset using my previous methodology.

# Test method
My dataset had 8,130 different profiles, and I'll train logistic regression models to the average profile embeddings. These logistic regression models are trained on just 10, 20, 40, 81, or 406 profiles and the remainder of the profiles are used for validation. Just to be clear, I'll train a model on just 10 profiles and validate the model on the remaining 8,120 profiles. The training sets were drawn at random 10,000 times. It turns out there are lots of ways you can randomly draw 10 profiles from 8,130... The results will show the mean validation accuracy and standard deviation from all of the 10,000 different training samples.

I don't enforce that the training samples are the same between different facenet models. This adds variability to the results. Although you'll see it isn't by much.

# Results

You'll see the results for each facenet model in the flowing tables. The mean accuracies don't change by much, but the 20180402 model does appear to have the highest mean accuracy. The 20180402 model also happens to have the highest LFW score. Though the difference in mean accuracies are mostly at the third digit, which isn't really important for my application. It appears that the standard deviations were lowest with the 20170512 model that used 128 embeddings.

## 20170512 model (128 embeddings)

|  # of training profiles     | Mean accuracy| Standard deviation  |
| -------------: |:-------------:| :-----:|
|10| 0.644 | 0.061 |
|20| 0.660 | 0.041 |
|40| 0.673 | 0.029 |
|81| 0.687 | 0.021|
|406| 0.716| 0.009 |

## 20180402 model (512 embeddings)

|  # of training profiles     | Mean accuracy| Standard deviation  |
| -------------: |:-------------:| :-----:|
|10| 0.645| 0.062 |
|20| 0.663 | 0.042 |
|40| 0.676 | 0.030 |
|81| 0.692 | 0.021|
|406| 0.718 | 0.009 |

## 20180408 mode (512 embeddings)

|  # of training profiles     | Mean accuracy| Standard deviation  |
| -------------: |:-------------:| :-----:|
|10| 0.640| 0.067 |
|20| 0.657 | 0.044 |
|40| 0.669 | 0.031 |
|81| 0.683 | 0.022|
|406| 0.709 | 0.009 |

# Conclusion

Overall the different facenet models don't really change the overall accuracy of classifying my Tinder dataset. The focus in improving the classification methodology should focus on dealing with different methods to consider the variable length of profile photos.

# References
[1] Gary B. Huang, Manu Ramesh, Tamara Berg, and Erik Learned-Miller.
Labeled Faces in the Wild: A Database for Studying Face Recognition in Unconstrained Environments.
University of Massachusetts, Amherst, Technical Report 07-49, October, 2007.
[pdf](http://vis-www.cs.umass.edu/lfw/lfw.pdf)

[2] Cao Q, Shen L, Xie W, Parkhi OM, Zisserman A. VGGFace2: A dataset for recognising faces across pose and age. arXiv preprint [arXiv:1710.08092](https://arxiv.org/abs/1710.08092). 2017 Oct 23. [pdf](https://arxiv.org/pdf/1710.08092.pdf)

[3] Dong Yi, Zhen Lei, Shengcai Liao and Stan Z. Li, Learning Face Representation from Scratch. arXiv preprint [arXiv:1411.7923](https://arxiv.org/abs/1411.7923). 2014. [pdf](https://arxiv.org/abs/1411.7923.pdf)
