---
title:  "Tindetheus: automatically like users on Tinder based on your own preference - How to install on Windows 10"
date:   2018-01-02 11:52:00
description: Tindetheus makes it easy for a user to build and apply their own personalized machine learning model on Tinder. These models can be used to automatically like or dislike users, and take advantage of recent developments in computer vision to find a pattern in the faces you find attractive. The post goes on to describe how to install tindetheus on a Windows 10 PC.
keywords: [tindetheus, Tinder machine learning, personalized like model, automatically like people on Tinder, create Tinder database, facenet]
---

### What is tindetheus
I created [tindetheus](https://github.com/cjekel/tindetheus) which is a Python application that allows users to build their own personalized machine learning model for Tinder. Essentially tindetheus has three major functions:
1. Browse Tinder profiles while creating a personal database of the profiles you've liked and disliked.
2. Train a model to your personal database.
3. Use the trained model to automatically like and dislike new profiles.

Tindetheus allows you to browse the Tinder profiles near you like you would on your phone. Every profile you review is stored in your own personal database. Tindetheus then includes a methodology to train your own classification model to your database. The model will predict whether you'll like or dislike a profile based on your historical preference.

The training first uses a [MTCNN](https://kpzhang93.github.io/MTCNN_face_detection_alignment/) to detect and box the faces in your database. Then a [facenet](https://github.com/davidsandberg/facenet) model is run on the faces to extract the embeddings (the last layer of the CNN from the facial classification model). These embeddings can be thought of as the set of features that describe an individual's face. It just so happens that these features are somewhat related to facial attractiveness.  A logistic regression model is then fit to the embeddings of the faces you have liked and disliked. The trained model can then be evaluated to automatically like and dislike new profiles.

### How to install tindetheus on Windows 10
I'm going to describe how to install tindetheus on a Windows 10 machine for someone who has never used Python before.

1. You need to download and install Anaconda. Visit the [Anaconda download site](https://www.anaconda.com/download/) and follow the instructions to install the latest version of Anaconda.
2. You need to install [TensorFlow](https://www.tensorflow.org/install/install_windows). Create a conda environment named *tensorflow* by running the following command in a Windows command prompt.
```dos
C:> conda create -n tensorflow python=3.5
```
3. Each time you want to run tindetheus, you'll need to activate the tensorflow enviorment. In the command prompt execute
```dos
C:> activate tensorflow
```
and your prompt should change to something like *(tensorflow) C:>*.
4. You need to install TensorFlow inside your tensorflow enviorment. I recommend you install the CPU-only version of TensorFlow unless you know what you are doing!  Run
```dos
(tensorflow) C:> pip install --ignore-installed --upgrade tensorflow
```
in your command prompt to install TensorFlow.
5. You need to ensure that all of tindetheus dependencies are installed in the tensorflow environment. Run the following command
```dos
(tensorflow) C:> conda install --update-dependencies numpy matplotlib imageio scikit-learn scikit-image tensorflow pandas scipy opencv
```
in the command prompt and you should be prompted with a long list of libraries that need to be installed. You will see something like
```dos
Proceed ([y]/n)?
```
where you'll need to type *y* and then press enter. This will take some time to install all of the dependencies of tindetheus. You'll know the installation has been completed when you see the follwoing:
```dos
(tensorflow) C:>
```
6. You can now install tindetheus. Run
```dos
(tensorflow) C:> pip install tindetheus
```
in your command prompt. You should see
```dos
Successfully built tindetheus
Installing collected packages: tindetheus
Successfully installed tindetheus-0.2.0
```
when tindetheus is successfully installed.
7. Almost done, but now you need to install git for windows. Download and install git for Windows from [here](https://git-scm.com/download/win).
8. You need to configure git to your identity. Close the command prompt you've had open and run the following in a new command prompt.
```dos
C:> git config --global user.name "John Doe"
C:> git config --global user.email johndoe@example.com
```
You should probably replace John Doe with your name and email...
9. Now you need to install [pynder](https://github.com/charliewolf/pynder). Unfortunately the latest version of pynder isn't on pypi, so we'll have to install pynder from source. In your command prompt run
```dos
C:> git clone https://github.com/charliewolf/pynder
```
where you should see something like
```dos
Cloning into 'pynder'...
remote: Counting objects: 770, done.
remote: Total 770 (delta 0), reused 0 (delta 0), pack-reused 770
Receiving objects: 100% (770/770), 120.24 KiB | 977.00 KiB/s, done.
Resolving deltas: 100% (467/467), done.
```
Now activate the tensorflow enviorment by running
```dos
C:> activate tensorflow
```
and install pynder by running
```dos
(tensorflow) C:> pip install --upgrade .\pynder
```
where you should see something like
```dos
Running setup.py install for pynder ... done
Successfully installed pynder-0.0.13
```
letting you know that pynder has been installed.
10. Now you need to test that tindetheus can be executed without error. Execute the tindetheus in your command prompt by
```dos
(tensorflow) C:> tindetheus
```
and you should see
```dos
No config.txt found
You must create a config.txt file as specified in the README
usage: tindetheus [-h] [--distance DISTANCE] function
tindetheus: error: the following arguments are required: function
```
which let's you know that tindetheus has been correctly installed.
11. You have installed tindetheus and are ready to read the [Getting Staring](https://github.com/cjekel/tindetheus#getting-started) guide in the README. Remember that each time you want to execute tindetheus you must do so from the tensorflow environment (by running *activate tensorflow* in the command prompt first).
