---
title:  "Visual Studio Code Python Setup"
date:   2018-07-29 14:15:00
description: Visual Studio Code is my favorite editor to write Python code. This post shows you how to setup Code so that you can begin using Code to write better Python!
keywords: [Python Code setup, Visual studio Code Python setup, Python linting in Code, flake8 Code setup python]
---

Visual Studio Code has become my absolute favorite IDE / text editor. I highly recommend those who work with Python to consider using Code for their work. If I were to revisit my [Python course](https://github.com/cjekel/Introduction-to-Python-Numerical-Analysis-for-Engineers-and-Scientist), I would spend a lecture going over setting up Code for working with Python. Right now

Some of the reasons I like Visual Studio Code:
- Code opens fast
- Code works on multiple operating systems (Linux/Windows/Mac)
- Code includes useful features by default (keyboard column selection, indentation conversion, terminal, and so much more)
- Code plays nice with git
- Code is free and [open source](https://github.com/Microsoft/vscode)

# Basic Python setup

Go [download Code](https://code.visualstudio.com/Download) and install for your system. Open Code and go to the extensions tabs.

![Code extensions]({{ "/" | relative_url  }}assets/2018-07-29/ext.png)

Now search for Python in the Marketplace Extension.

![Python marketplace extensions]({{ "/" | relative_url  }}assets/2018-07-29/py_mark.png)

The Microsoft Python extension includes many useful features for Python development, including: linting, debugging, and more. Install the Python extension. I also like to have a spell checking extension, but that is up to you. 

![Install Python extension]({{ "/" | relative_url  }}assets/2018-07-29/install_py.png)

Now you need to install a Python linter. A linter will help you write better code, and display possible errors before you run your code. My favorite Python linter is [flake8](https://pypi.org/project/flake8/), which will help you write Python code to the pep8 style guidelines. Open a terminal/prompt and install flake8. 

If you are using conda run:
```
conda install flake8
```
or you can install with pip using:
```
pip install flake8
```
You may also need to install [pylint](https://pypi.org/project/pylint/), which can be installed with either conda or pip. It is worthwhile to note that if you are using several Python environments, you may want to install flake8 in each of them. There will be more on multiple Python environments later.

Now you need to tell Code that you want to use the flake8 Python linter. Go to your settings.

![Go to Code settings]({{ "/" | relative_url  }}assets/2018-07-29/go_to_settings.png)

Settings in Code are a text file (although there is much work on a new settings editor). I really like the text settings, because you can quickly search and view the defaults. You should see two planes; On the left will be the default user settings, and on the right will be your personal user settings. Anything you type in the right will override the default settings.

# What does Python linting do?

![Code settings]({{ "/" | relative_url  }}assets/2018-07-29/settings.png)

My user settings look like:
```
{
    "python.linting.flake8Enabled": true,
    "files.autoSave": "afterDelay"
}
```
which tells Code to use the flake8 Python linter, and enables autosaving. Some people will hate autosaving (which is disabled by default), so you can decide if it's a feature you'll appreciate. I like autosaving, because sometimes I forget to save my script before running it in IPython.

Now go ahead and create a new Python file as demo.py with the following code.
```
import numpy as np
import matplotlib.pyplot as plt
def a_root_of_x(a, x):
    # take the a root of x
    return x**(1.0/a)
x = np.linspace(1.0, 3.0, 10)
y = a_root_of_x(3,x)
```

You may see a few warnings at the bottom of the screen.
![Code errors]({{ "/" | relative_url  }}assets/2018-07-29/errors.png)

These errors because we haven't selected a Python environment yet. Click on Select Python Environment on the bottom bar of Code. Then choose your desired Python environment at the top of the screen. Code is very good at automatically finding your Python environments on your system. I usually run at least two Python enviorments (2 and 3).

![Set up Python enviorment]({{ "/" | relative_url  }}assets/2018-07-29/pyenv.png)

Now since I selected my Anaconda Python environment, I can see Anaconda 5.2.0 at the bottom of Code. You can easily switch your Python environment anytime by clicking on Anaconda 5.2.0.

![Python environment Anaconda]({{ "/" | relative_url  }}assets/2018-07-29/anaconda.png)

If everything is working correctly, you should start to see some red underlines on the Python code for the demo.py file.

![red underlines in Code]({{ "/" | relative_url  }}assets/2018-07-29/demo.png)

We can take a look at what these underlines mean by clicking on the warnings at the bottom of Code.

![Code warnings]({{ "/" | relative_url  }}assets/2018-07-29/warn.png)

There are several problems with our code, however none of the issues will keep our code from running. Most of these issues are related to not following the Python [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide. If we fix our code we'll no longer have any warnings or problems.

![Code warnings]({{ "/" | relative_url  }}assets/2018-07-29/noissues.png)

# How to run Python scripts from Code

Now you can run your python scripts from Code using the terminal at the bottom of the screen. We can click on the terminal tab and we'll see something like the following depending on your system. "ctrl + shift + `" is the shortcut for opening the terminal in Code.

![Code terminal]({{ "/" | relative_url  }}assets/2018-07-29/term.png)

Alternatively we can press F1 to pull up the commands, and select Python: Run Python File in Terminal to run the file.

![Code terminal]({{ "/" | relative_url  }}assets/2018-07-29/run.png)

Which will run the script in the terminal (and set up the paths if you are on Windows).

![Code terminal]({{ "/" | relative_url  }}assets/2018-07-29/runscript.png)

Now I prefer to run my scripts using [IPython](https://pypi.org/project/ipython/) (You may need to install ipython using pip or conda if you don't have ipython), which creates an interactive Python experience. We can type ipython into the terminal to start an ipython session.

![Code terminal]({{ "/" | relative_url  }}assets/2018-07-29/ipython.png)

We can use the IPython magic command %run to run our script.
```
%run demo.py
```
![Code terminal]({{ "/" | relative_url  }}assets/2018-07-29/ipythonrun.png)

The majority of my work now is run with an IPython terminal in Code. Now it's time for you to start writing your own Python code! Hopefully this post has helped you get set up with Visual Studio Code and Python.
