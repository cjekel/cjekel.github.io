---
title:  "Using the validate function to compare different FaceNet models in tindetheus"
date:   2018-12-03 17:00:00
description: Comparing different facenet models on a hot-or-not dataset using the new validate function in tindetheus.
keywords: [facenet models, tinder classification, validate tindetheus, personal tinder classification model, compare tinder like models ]
---

This post will compare the results of different pre-trained [facenet](https://github.com/davidsandberg/facenet) models when using [tindetheus](https://github.com/cjekel/tindetheus) to build a personalized classification model for a single [Tinder](https://tinder.com) user. Tindetheus currently states the training accuracy, recall (true positive rate), and specificity (true negative rate) after training. However, it may be more interesting to visualize the trained tindetheus models on an external dataset. The new *validate* function within tindetheus allows for a user to evaluate the trained tindetheus model on a new image database. This new function will be used to visualize the difference of using different pre-trained facenet models on a small validation dataset. While the training accuracy of the different pre-trained facenet models are subtle, the models predict different faces will be liked on a small validation dataset.

# Training data

A user browsed 146 Tinder profiles using tindetheus with a total of 859 images. There were 745 images in which the MTCNN [1] was able to detect and bound a face in the image, as tindetheus only considers the images with just one face. Each of the 146 browsed Tinder profiles had at least one image witha  unique face. On average each profile had 5 images, with a standard deviation of 2. Different pre-trained facenet models will be used to train a classification model in tindetheus to this user's Tinder history.

# Facenet models

There are three pre-trained facenet models which I will use: 20170512, 20180402, and 20180408. I used the 2017 model in the paper which described how tindetheus works [2]. One difference between the 2017 and 2018 models is the length of the last layer in the facenet models. The 2017 model uses a vector of length 128, while the 2018 models use a vector of length 512. There are also changes to the training data and image pre-conditioning which you'll have to check the [repo](https://github.com/davidsandberg/facenet) for more information.

I have [previously investigated](https://jekel.me/2018/512_vs_128_facenet_embedding_application_in_Tinder_data/) the differences between these pre-trained models. This was on a much larger training dataset, in which I did not notice much overall difference between the facenet models. This post will investigate a much smaller training dataset, and attempt to visualize the difference between the pre-trained facenet models when using tindetheus.

# Hot or not dataset

The [Hot or not dataset](http://vision.cs.utexas.edu/projects/rationales/) contains 1000 female and 1000 male images from the old hotornot.com. The dataset was used to annotate labels in images, in an effort to find the features related to classifying an individual as *hot* or *not* [3]. It's interesting to use the entire hot or not dataset to validate a tindetheus model, but it would be too much to show the results on all of the 1000 images. Thus, I've created a small subset of 16 females from the hot or not dataset which you can download [here](https://drive.google.com/file/d/13cNUzP_eXKsq8ABHwXHn4b9UgRbk-5oP/view?usp=sharing). 


# Results

Tindetheus was trained three times using the different pretrained facenet models. You can view the results of the training accuracy, recall (true positive rate), and specificity (true negative rate) on the training data in the following table. Looking at these numbers, it appears that the 20170512 facenet model has a slight edge on the other facenet models. All of the models produce a training accuracy in the ballpark of 0.75. The 2018 facenet models appear to produce results that are very similar to each other. 

| Model | Training accuracy| Recall  | Specificity |
| :------------- |:-------:|:-----:|:-----:|
| 20170512 | 0.78 | 0.85 | 0.71 |
| 20180402 | 0.73 | 0.82 | 0.65 |
| 20180408 | 0.74 | 0.84 | 0.65 |

Each trained model was run on the small hot or not validation dataset. Bellow you will find the faces that each model predicted the user would like or dislike. You'll see that each facenet model resulted in slightly different faces being *liked* or *disliked*.

**20170512 Dislike** ![20170512 Dislike]({{ "/" | relative_url  }}assets/2018-12-03/Dislike_2017_05_12.png)
**20170512 Like** ![20170512 Like]({{ "/" | relative_url  }}assets/2018-12-03/Like_2017_05_12.png)
**20180402 Dislike** ![20180402 Dislike]({{ "/" | relative_url  }}assets/2018-12-03/Dislike_2018_04_02.png)
**20180402 Like** ![20180402 Like]({{ "/" | relative_url  }}assets/2018-12-03/Like_2018_04_02.png)
**20180408 Dislike** ![20180408 Dislike]({{ "/" | relative_url  }}assets/2018-12-03/Dislike_2018_04_08.png)
**20180408 Like** ![20180408 Like]({{ "/" | relative_url  }}assets/2018-12-03/Like_2018_04_08.png)

# Discussion
There is only one face difference between the predicted like and dislikes when comparing the 20170512 and 20180402 facenet models on the small subset of the hot or not dataset. However, there are five different face predictions between the 20170512 and 20180408 facenet models. This is a significant difference as there was only 16 validation photos. 

The validate function was added to tindetheus such that users could apply their trained tindetheus model to other images. This presents an interesting opportunity to visualize the effect of using a different pre-trained facenet model in tindetheus. For this users who reviewed 146 Tinder profiles, the choice of facenet model results in different predictions on this small hot or not subset. The visual difference of the predictions may influence which facenet model the tindetheus user would preferred.

# References

[1] Zhang, K., Zhang, Z., Li, Z. and Qiao, Y., 2016. Joint face detection and alignment using multitask cascaded convolutional networks. IEEE Signal Processing Letters, 23(10), pp.1499-1503.

[2] Jekel, C.F. and Haftka, R.T., 2018. Classifying Online Dating Profiles on Tinder using FaceNet Facial Embeddings. arXiv preprint arXiv:1803.04347.

[3] Donahue, J., & Grauman, K. (2011). Annotator rationales for visual recognition. http://vision.cs.utexas.edu/projects/rationales/
