import os
import numpy as np
from PIL import Image
import pytest
from pyimager.pyimager import circropper, imgfilter, redusize, reducolor


def test_circropper():
    """
    unit test for the circropper function
    """
    input_path = "./tests/mandrill.jpg"

    # Test argument type
    try:
        circropper(1, "one")
    except TypeError:
        pass

    try:
        circropper(1, 10)
    except TypeError:
        pass

    try:
        circropper(input_path, "one")
    except TypeError:
        pass

    # Test valid image path
    try:
        circropper("tests/wrong.jpg", 0)
    except FileNotFoundError:
        pass

    # Test margin value
    try:
        circropper(input_path, 1000)
    except ValueError:
        pass

    # Test output
    img = Image.open(input_path).convert("RGB")
    imgArray_1 = np.array(img)
    imgArray_2 = np.array(circropper(input_path, 0, 'images/mandrill_new.png'))
    os.remove('images/mandrill_new.png')
    assert imgArray_1.shape[0] == imgArray_2.shape[0]
    assert imgArray_1.shape[1] == imgArray_2.shape[1]
    assert imgArray_1.shape[2] == imgArray_2.shape[2] - 1
    assert os.path.exists('images/mandrill_new.png') is False, \
        'File should not be saved'
    print("All tests pass! ")


def test_reducolor():
    '''
    Unit test for the reducolor function
    '''
    img_array = reducolor(0, 'tests/mandrill.jpg')
    color_n = len(np.unique(img_array.reshape(
        np.prod(img_array.shape[:2]), 3), axis=0))
    assert color_n == 2, f'Should return two colors only, \
    {color_n} colors are returned'
    img_array = reducolor(1, 'tests/mandrill.jpg')
    color_n = len(np.unique(img_array.reshape(
        np.prod(img_array.shape[:2]), 3), axis=0))
    assert color_n == 8, f'Should return eight colors, \
    {color_n} colors are returned'

    # Style must be either 0 or 1. AssertionError should be raised
    with pytest.raises(AssertionError):
        img_array = reducolor(2, 'tests/mandrill.jpg')

    # FileNotFoundError should be raised for non-existant files
    with pytest.raises(FileNotFoundError):
        img_array = reducolor(2, 'tests/wrong.jpg')

    reducolor(0, 'tests/mandrill.jpg', 'tests/mandrill_new.jpg')
    assert os.path.exists(
        'tests/mandrill_new.jpg'), \
        'File should be saved to the provided output path'
    os.remove('tests/mandrill_new.jpg')


def test_redusize():
    '''
    Unit test for redusize function
    '''
    # test assertion error for even width and height
    shape_even = np.array(redusize(
        "images/mandrill.jpg", "images/test_reduced_mandrill.jpg", 200, 200)).shape
    assert shape_even == (200, 200, 3)
    # test assertion error for odd width and height
    shape_odd = np.array(redusize(
        "images/mandrill.jpg", "images/test_reduced_mandrill.jpg", 205, 210)).shape
    assert shape_odd == (205, 210, 3)
    # test assertion error for when width and the height are not the same
    diff_dimension = np.array(redusize(
        "images/mandrill.jpg", "images/test_reduced_mandrill.jpg", 201, 202)).shape
    assert diff_dimension == (201, 202, 3)
    # test assertion error for very small output image
    shape_small = np.array(redusize(
        "images/mandrill.jpg", "images/test_reduced_mandrill.jpg", 20, 20)).shape
    assert shape_small == (20, 20, 3)
    # exception error when the the width larger than the original width
    with pytest.raises(AssertionError):
        redusize(
            "images/mandrill.jpg", "images/test_reduced_mandrill.jpg", 300, 200)
    # exception error when the the height larger than the original height
    with pytest.raises(AssertionError):
        redusize(
            "images/mandrill.jpg", "images/test_reduced_mandrill.jpg", 200, 300)
    redusize(
        "images/mandrill.jpg", "images/test_reduced_mandrill.jpg", 200, 200)
    #  testing that the function writes the image to the provided output path
    assert os.path.exists(
        "images/reduced_mandrill.jpg"), \
        'No imaged found in the output path'
    os.remove("images/test_reduced_mandrill.jpg")


def test_imgfilter():
    '''
    Unit test for the imgfilter function
    '''
    # test assertion error for strength input type
    with pytest.raises(TypeError):
        imgfilter('images/mandrill.jpg', filter_type='blur', strength='5')

    # test assertion errors for strength input value
    with pytest.raises(ValueError):
        imgfilter('images/mandrill.jpg', filter_type='blur', strength=-1.5)

    with pytest.raises(ValueError):
        imgfilter('images/mandrill.jpg', filter_type='blur', strength=1.5)

    # test assertion error for filter_type input value
    with pytest.raises(ValueError):
        imgfilter('images/mandrill.jpg', filter_type='3D', strength=0.4)

    # test FileNotFoundError for input_path
    with pytest.raises(FileNotFoundError):
        imgfilter('images/wrong.jpg', filter_type='blur', strength=0.4)

    # test that if output_path is not None the file is saved
    imgfilter('images/mandrill.jpg', filter_type='blur',
              strength=0.1, output_path='images/mandrill_new.jpg')
    assert os.path.exists('images/mandrill_new.jpg'), \
        'File should be saved to the provided output path'
    os.remove('images/mandrill_new.jpg')

    # test that if output_path is None the file is not saved
    output_test = imgfilter('images/mandrill.jpg',
                            filter_type='blur', strength=0.1, output_path=None)
    assert os.path.exists('images/mandrill_new.jpg') is False, \
        'File should not be saved'

    # test that output image array is smaller or equal
    # in size to original image array
    img = Image.open('images/mandrill.jpg')
    input_test = np.array(img)
    assert output_test.shape[0] <= input_test.shape[0], \
        'Output image should have equal or smaller dimensions than original ' \
        'image.'
    assert output_test.shape[1] <= input_test.shape[1], \
        'Output image should have equal or smaller dimensions than original ' \
        'image.'

    # test output image array dimensions are correct when using sharpen filter
    output_test = imgfilter('images/mandrill.jpg',
                            filter_type='sharpen', strength=0.5)
    assert output_test.shape[0] == input_test.shape[0] - 2, \
        'Output image has wrong width.'
    assert output_test.shape[1] <= input_test.shape[1] - 2, \
        'Output image has wrong height.'
