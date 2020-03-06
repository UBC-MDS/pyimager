import sys
import os
import pytest
from pyimager.pyimager import *

input_path = "./tests/milad.jpg"
def test_circropper_output():
    img = Image.open(input_path).convert("RGB")
    imgArray_1 = np.array(img)
    imgArray_2 = circropper(input_path, "result.png", 0)
    assert imgArray_1.shape[0] == imgArray_2.shape[0] 
    assert imgArray_1.shape[1] == imgArray_2.shape[1] 
    assert imgArray_1.shape[2] == imgArray_2.shape[2]-1

def test_circropper_input_value():
    try:
        imgArray_2 = circropper(input_path, "result.png", 1000)
    except ValueError:
        pass
    else:
        print("not error happens")

def test_reducolor():
    img_array = reducolor(0, 'tests/mandrill.jpg')
    color_n = len(np.unique(img_array.reshape(np.prod(img_array.shape[:2]),3), axis=0))
    assert color_n == 2, f'Should return two colors only, {color_n} colors are returned'
    img_array = reducolor(1, 'tests/mandrill.jpg')
    color_n = len(np.unique(img_array.reshape(np.prod(img_array.shape[:2]),3), axis=0))
    assert color_n == 8, f'Should return eight colors, {color_n} colors are returned'    
    try:
        img_array = reducolor(2, 'tests/mandrill.jpg')
    except AssertionError:
        pass
    else:
        assert False, f'AssertionError should be raised. Should not allow code other than 0 and 1'

def test_reduce_dimensions(): 
    shape_even = reduce_dimensions("images/mandrill.jpg","images/reduced_mandrill.jpg",200,200).shape
    assert shape_even == (200,200,3)
    shape_odd = reduce_dimensions("images/mandrill.jpg","images/reduced_mandrill.jpg",205,210).shape
    assert shape_odd == (205,210,3)
    diff_dimension = reduce_dimensions("images/mandrill.jpg","images/reduced_mandrill.jpg",201,202).shape
    assert diff_dimension == (201,202,3)

def test_img_filter():
    # test assertion error for strength input type
    try:
        img_filter('images/mandrill.jpg', filter_type='blur', strength = '5')
    except AssertionError:
        pass
    else:
        assert False, f'AssertionError should be raised.\n Should not allow type other than int or float for strength parameter.'
    # test assertion error for strength input value
    try:
        img_filter('images/mandrill.jpg', filter_type='blur', strength = -1.5)
    except AssertionError:
        pass
    else:
        assert False, f'AssertionError should be raised.\n Should not allow numbers less than 0 for strength parameter.'
    # test assertion error for strength input value
    try:
        img_filter('images/mandrill.jpg', filter_type='blur', strength = 1.5)
    except AssertionError:
        pass
    else:
        assert False, f'AssertionError should be raised.\n Should not allow numbers greater than 1 for strength parameter.'
    # test assertion error for filter_type input value
    try:
        img_filter('images/mandrill.jpg', filter_type='3D', strength = 0.4)
    except AssertionError:
        pass
    else:
        assert False, f"AssertionError should be raised.\n Should not options other than 'blur' or 'sharpen' for filter_type parameter."

