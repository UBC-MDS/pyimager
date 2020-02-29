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

`pyimager` is a python package that provides a quick and easy way to do some simple image processings and editings. By input the path of the image, users can run functions from `pyimager` to reduce the size of the image, crop image into a circle, reduce image colors, or apply cool effect filters.

## Installation:

In your console, type:

```
pip install -i https://test.pypi.org/simple/ pyimager
```

## Functions:

- `circropper`: This function crops the input image into a circle. This can be useful when you want to make icons from images. 
- `reduce_dimensions`: This function reduces the dimension of a given image by removing vertical and horizontal seams.
- `img_filter`: This function applies a filter to a given image, altering the visual aesthetic. This includes options to 
blur, emboss, and colorize the image. 
- `redu_color`: This function reduces number of colors appearing on the image to have cartoonized color effect.

## Our package in python ecosystem:

There are existing packages to process images. For example `skimage`, `PIL` are popular packages that can be used to resize, cut images and apply filters.  

## Dependencies:
- Python 3.6 or greater
- numpy
- PIL

## Usage:

``` python
from pyimager import pyimager
```

## Documentation
The official documentation is hosted on Read the Docs: <https://pyimager.readthedocs.io/en/latest/>

### Credits
This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
