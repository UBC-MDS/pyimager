
import sys
import os
import pytest
from pyimager.pyimager import *

fname = os.path.join(os.path.dirname(__file__), './tests/imgs/milad.jpg')

def test_inputs():
    with pytest.raises(TypeError):
        circropper(18, 20, 10) # Not a string for the file path
    with pytest.raises(TypeError):
        circropper(fname, "result.png", "one") # Not a valid margin value

    with pytest.raises(ValueError):
        circropper(fname, "result.png", 500) # margin value is out of scope 

    with pytest.raises(FileNotFoundError):
        circropper("./tests/imgs/Path.jpg", "result.png", 10) # Incorrect directory/file not in location

def test_stype():
    img_array = reducolor(0, 'tests/mandrill.jpg')
    color_n = len(np.unique(img_array.reshape(np.prod(img_array.shape[:2]),3), axis=0))
    assert color_n == 2, f'Should return two colors only, {color_n} colors are returned'
    img_array = reducolor(1, 'tests/mandrill.jpg')
    color_n = len(np.unique(img_array.reshape(np.prod(img_array.shape[:2]),3), axis=0))
    assert color_n == 8, f'Should return eight colors, {color_n} colors are returned'    
    try:
        img_array = reducolor(2, 'tests/mandrill.jpg')  
    except StyleException:
        pass
    else:
        assert False, f'Should not allow code other than 0 and 1 and raise StyleException'
