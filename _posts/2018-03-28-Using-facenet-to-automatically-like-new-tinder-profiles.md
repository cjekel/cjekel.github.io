---
title:  "Using facenet to automatically review Tinder profiles"
date:   2018-03-28 10:11:00
description: I used facenet to find a pattern in the Tinder profiles I liked and disliked. This post explains how I did it.
keywords: [facenet, automated tinder, tinder facenet, tindetheus, facial recognition python]
---

tl;dr I swiped thousands of Tinder profiles so you wouldn't have to. I used facenet to find a pattern in the Tinder profiles I liked and disliked. You can build your own models to automatically like Tinder profiles based on your historical preference using [tindetheus](https://github.com/cjekel/tindetheus).

It takes a lot of time to review Tinder profiles. Before [Tinder gold](https://www.help.tinder.com/hc/en-us/articles/115004487406-Tinder-Plus-and-Tinder-Gold-), you'd have to review hundreds of profiles of individuals who weren't that interested in you. Let's say you like one out of five profiles, of which one out of ten profiles you'd like would result in a match. This means you'd have to review 50 profiles to get a match. If you're an average looking guy, you may end up needing to review many additional profiles before getting a match. Then there is always the chance that the individual you match with, as it turns out, is not that interested in you.

Machine learning can save a Tinder user a lot of time. A computer model can learn the characteristics of the profiles you like, to automatically review new profiles based on your own historical preference. This allows users to spend more of their time on establishing a connection with their matches, rather than reviewing new profiles. Now the computer models do come with a cost. While they can save the user time, they won't be as accurate as manually reviewing the profiles. Well not yet...

### My Tinder database

When I was on Tinder, I recorded everything about each profile I liked and disliked. In total I reviewed over 8,500 profiles. For months I struggled to find any pattern in my custom database. I was almost convinced that the profiles I liked were at random, and was just about to give up on building a model to my database.

I ended up stumbling onto the [facenet](https://github.com/davidsandberg/facenet) library, which includes pre-trained models which you can apply to your own facial recognition / classification project. The facenet library aimed to recreate the Google FaceNet paper of [1], which demonstrated that a face recognition and face verification system could be applied at scale to achieve 99% accuracy. I ended up using a facenet model to find a pattern in the online dating profiles I reviewed.

### How I used facenet to review Tinder profiles

So let's say we come across the following dating profile.
![Sasha Pieterse Tinder profile]({{ "/" | relative_url  }}assets/2018-03-28/step1.png)

First I use a [pre-trained](https://kpzhang93.github.io/MTCNN_face_detection_alignment/index.html) model to detect and box the faces in the profile.
![Sasha Pieterse boxed faces]({{ "/" | relative_url  }}assets/2018-03-28/step2.png)

Then I consider only the images that contained just one face in the picture. I think it's fair to assume that if an individual uploads a picture with one face, then this face is of the individual. Sometimes it's difficult to spot the user from the group pictures anyways. As it turned out, 95% of the profiles I reviewed had at least one picture with just one face.
![Sasha Pieterse only one face in image]({{ "/" | relative_url  }}assets/2018-03-28/step2.5.png)

We can take these boxed faces and evaluate pre-trained facenet model on them. This calculates the features that uniquely identify the individual's face. The output is a vector of 128 numbers that represent the face from each image.
![Sasha Pieterse facenet calc]({{ "/" | relative_url  }}assets/2018-03-28/step3.png)

In this case we need to go from three vectors of 128 numbers to a single vector that describes the profiles. In [2] I took two different approaches that were approximately equivalent. What's implemented into tindetheus is just the average.

<div>
$$
\mathbf{i}_{\text{avg}} = \begin{bmatrix}
\frac{x_1 + y_1 + z_1}{3} \\
\frac{x_2 + y_2 + z_2}{3} \\
\vdots \\
\frac{x_{128} + y_{128} + z_{128}}{3} \\
\end{bmatrix}
$$
</div>

The result is a vector <span>\\( \mathbf{i}_{\text{avg}} \\)</span> of 128 numbers that uniquely describe the facial features of a profile. A classification model can be trained using <span>\\( \mathbf{i}_{\text{avg}} \\)</span>  as the input vector, with either **like** or **dislike** as the output for each profile. In my case, it didn't really matter which classification model I used. I ended up using logistic regression in tindetheus, because it's an easy model to work with that is quick to train.

This same procedure is repeated to calculate <span>\\( \mathbf{i}_{\text{avg}} \\)</span>  for new profiles. The trained classification model can be evaluated to **like** or **dislike** the new profile using <span>\\( \mathbf{i}_{\text{avg}} \\)</span> as the input. This processes is completely automated in tindetheus.

![Sasha Pieterse like]({{ "/" | relative_url  }}assets/2018-03-28/step5.png)

### My results

The most surprising result I found was that I could build a reasonable model, with a mean accuracy of 65% using just 10 Tinder profiles. This accuracy increased as I reviewed more profiles. On 80 profiles, I could obtain a mean accuracy of about 70%. The following figure shows a probability distribution function for validation accuracy with training on 10, 20, 40, 81, or 406 profiles. The model becomes more accurate with less variability as you review additional profiles.

![PDF of validation accuracy]({{ "/" | relative_url  }}assets/2018-03-28/pdf_val_acc.png)

The final model had an accuracy of about 75%. This is comparable to the work done by [3], which achieved an average accuracy of 75% for male users.

### Conclusion

Manually reviewing tinder profiles takes a lot of time. That time could be better spent communicating with your matches. After struggling for many months, I was finally able to find a pattern in my Tinder database by using [facenet](https://github.com/davidsandberg/facenet) to calculate facial features. The method used is described in this post, and in [2]. I then created [tindetheus](https://github.com/cjekel/tindetheus) such that users can use this method to automatically review new Tinder profiles.

Highlights:
- The number of profiles you need to train a successful model may be lower than you think. I was able to achieve a 67% validation accuracy on just 20 profiles.
- Reviewing profiles in a deterministic way (such as using tindetheus), allows a user to A/B test their profile. This can give you an idea of what picture you should put first, or how to phrase your bio.
- The accuracy will vary from user to user, but in general the more profiles you review the more accurate the model will become.

Thoughts for improvement:
- Include [NLP](https://en.wikipedia.org/wiki/Neuro-linguistic_programming) to find a pattern in user biographies. About one out of three Tinder profiles I reviewed didn't contain a single character in the bio. I didn't include any bio information in this model, however I know that the bio was definitely a factor in how I evaluated a profile.
- It would be very interesting to see how this method works at scale for a lot of users. While the method worked well with my data, it's likely to work both better and worse depending on the individual. It would be interesting to see how much does the accuracy vary from user to user. Unfortunately this requires users to have reviewed a lot of profiles.
- There is very little research on using computer models to find what women find attractive in male faces. I'd be very interested to see if this method works for women who are interested in men. 


### References

[1] Schroff F, Kalenichenko D, Philbin J. Facenet: A unified embedding for face recognition and clustering. InProceedings of the IEEE conference on computer vision and pattern recognition 2015 (pp. 815-823). [Pdf](https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Schroff_FaceNet_A_Unified_2015_CVPR_paper.pdf)

[2] Jekel CF, Haftka RT. Classifying Online Dating Profiles on Tinder using FaceNet Facial Embeddings. arXiv preprint arXiv:1803.04347. 2018 Mar 12. [Pdf](https://arxiv.org/pdf/1803.04347.pdf)

[3] Rothe R, Timofte R, Van Gool L. Some like it hot-visual guidance for preference prediction. InProceedings CVPR 2016 2016 Jan 1 (pp. 1-9). [Pdf](https://www.cv-foundation.org/openaccess/content_cvpr_2016/app/S24-04.pdf)
