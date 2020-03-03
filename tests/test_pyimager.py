from pyimager.pyimager import *

def test_stype():
    img_array = reducolor(0, 'tests/mandrill.jpg')
    color_n = len(np.unique(img_array.reshape(np.prod(img_array.shape[:2]),3), axis=0))
    assert color_n == 2, f'Should return two colors only, {color_n} colors are returned'
    img_array = reducolor(1, 'tests/mandrill.jpg')
    color_n = len(np.unique(img_array.reshape(np.prod(img_array.shape[:2]),3), axis=0))
    assert color_n == 24, f'Should return eight colors, {color_n} colors are returned'    
    try:
        img_array = reducolor(2, 'tests/mandrill.jpg')
    except StyleException:
        pass
    else:
        assert False, f'Should not allow code other than 0 and 1 and raise StyleException'
