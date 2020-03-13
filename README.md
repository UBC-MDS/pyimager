# pyimager 

![](https://github.com/UBC-MDS/pyimager/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/UBC-MDS/pyimager/branch/master/graph/badge.svg)](https://codecov.io/gh/UBC-MDS/pyimager) ![Release](https://github.com/UBC-MDS/pyimager/workflows/Release/badge.svg)

[![Documentation Status](https://readthedocs.org/projects/pyimager/badge/?version=latest)](https://pyimager.readthedocs.io/en/latest/?badge=latest)

The pyimager package contains functions that aid in image manipulation and processing.

This package was developed as a project for DSCI-524.

## Creators

| Name | GitHub |
|---|---|
| Keanna Knebel| [Keanna-K](https://github.com/Keanna-K) |
| Mohammed Salama | [dataubc](https://github.com/dataubc) |
| Zhengyang (Zoe) Pan | [zoepan00](https://github.com/zoepan00) |
| Haoyu (Clara) Su | [clsu22](https://github.com/clsu22) |

To contribute to this project, you must adhere to the terms outlined in our [Code of Conduct.](https://github.com/UBC-MDS/pyimager/blob/master/CONDUCT.md)

## Overview:

Want to edit an image in the shell instead of GUI applications? `pyimager` is a python package that provides a quick and easy way to do some simple image processings and graphic editings. Based on the main needs of graphic editings, the package integrates four functionalities. It includes reduce the size of the image, crop image into a circle, reduce image colors, and apply cool effect filters. By input the path of the image, users can run any of these functions with one line of code to get a desired or interesting images.

## Our package in python ecosystem:

There are existing packages to process images. For example `scikit-image`[here](https://scikit-image.org/docs/stable/auto_examples/), `PIL`[here](https://pillow.readthedocs.io/en/stable/handbook/index.html) are popular packages that can be used to resize, cut images and apply filters. The goal of this package is either to utilize packages like `matplotlib`, `PIL` to improve the pre-existing functions or to re-implement code manually with `numpy`. Also it automates the image editing process, producing the altered image by one line of code.

## Installation:

In your console, type:

```
pip install -i https://test.pypi.org/simple/ pyimager
```

## Functions:

- `circropper`: This function crops the input image into a circle. This can be useful when you want to make icons from images. 
- `redusize`: This function reduces the dimension of a given image by removing vertical and horizontal seams.
- `imgfilter`: This function applies a filter to a given image, altering the visual aesthetic. This includes options to blur and sharpen the image with varying degrees of strength. This filter effect is achieved through the application of a matrix convolution with the filter kernel and original image.  
- `reducolor`: This function reduces the image colors to get the cartoonized color effect. This can be either white and black images or eight colors images. 


## Dependencies:
- Python 3.7 or greater
    - numpy = "^1.18.1"
    - Pillow = "^7.0.0"
    - scipy = "^1.4.1"
    - matplotlib = "^3.2.0"

## Usage Examples 

We will use `mandrill.jpg` saved in the `images` folder of this repository for the examples.

![mandill.jpg](images/mandrill.jpg)

### `circropper(input_path, margin, output_path=None)` 
```python
from pyimager import pyimager

circropper(input_path='images/mandrill.jpg', margin=0, output_path='images/mandrill_circropper.png')
```
![images/mandrill_circropper.png](images/mandrill_circropper.png)
```python 
from pyimager import pyimager

pyimager.reducolor(0, 'images/mandrill.jpg', 'images/mandrill_new.jpg')
```

```python
from pyimager import pyimager

pyimager.imgfilter("images/mandrill.jpg", "blur", 0.4)
```

### `reducolor(style, input_path, output_path=None)`  

```python
from pyimager import pyimager
#style 0, reduce the image color to white and black and save the new image mandrill_reducolor0.jpg in the images folder
pyimager.reducolor(style=0, input_path='images/mandrill.jpg', output_path='images/mandrill_reducolor0.jpg')
```
![mandrill_reducolor0.jpg](images/mandrill_reducolor0.jpg)

```python
#style 1, reduce the image color to 8 colors and save the new image mandrill_reducolor1.jpg in the images folder
pyimager.reducolor(style=1, input_path='images/mandrill.jpg', output_path='images/mandrill_reducolor1.jpg')
```
![mandrill_reducolor0.jpg](images/mandrill_reducolor1.jpg)

```python
from pyimager import pyimager
pyimager.redusize("images/mandrill.jpg", "images/reduced_mandrill.jpg", 200, 300)
```
## Documentation
The official documentation is hosted on Read the Docs: <https://pyimager.readthedocs.io/en/latest/>

## Package in R

We have a package with the same functionalities in R : `rimager`. See [here](https://github.com/UBC-MDS/rimager)  

### Credits
This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
