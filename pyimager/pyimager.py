import numpy as np
from PIL import Image, ImageDraw
from matplotlib.image import imsave
import matplotlib.pyplot as plt
from scipy.ndimage.filters import convolve
import os
import re


def circropper(input_path, margin, output_path=None):
    """
    Crops an image into a circle and leave some margin as you defined

    Parameters
    -----------
    input_path: string
        The file path of the image to be cropped
    margin: float or int
        The distance between circle boundary and the original image boundary
    output_path: string
        The path to the output image

    Returns
    --------
        A new cropped Image object

    Examples
    ---------
    >>> from pyimager import pyimager
    >>> circropper('images/mandrill.jpg', 0, 'images/mandrill_circropper.png')
    """
    # Test argument
    if type(input_path) != str and type(margin) != float and type(
            margin) != int:
        raise TypeError(
            "The 'input_path' argument must be a string and the margin "
            "argument must be a number")
    if type(input_path) != str:
        raise TypeError("The 'input_path' argument must be a string")
    if type(margin) != float and type(margin) != int:
        raise TypeError("The 'margin' argument must be a float")

    # Test valid image path
    if not os.path.exists(input_path):
        raise FileNotFoundError("The input file does not exist")

    # Read in and convert image to np.array
    img = Image.open(input_path).convert("RGB")
    imgArray = np.array(img)
    height, width = img.size

    # Check valid margin value
    if margin > min(height, width):
        raise ValueError(
            "The margin should be smaller than {0}".format(min(height, width)))

    # Create circle mask layer and crop
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice([margin, margin, height - margin, width - margin], 0, 360,
                  fill=255)
    mask_array = np.array(mask)
    imgArray = np.dstack((imgArray, mask_array))
    Image.fromarray(imgArray)

    if output_path is not None:
        Image.fromarray(imgArray).save(output_path)
        print(f'New image saved in {output_path}')

    return Image.fromarray(imgArray)


def redusize(input_file, output_file, new_height, new_width):
    """
    A function to reduce the dimension of a given image by removing vertical
    and horizontal seams

    Parameters
    ----------
    input_file : str
        path to the input image
    output_file : str
        path to the output image
    new_width : int
        new width the output image
    new_height : int
        new height of the output image

    Returns
    -------
    A new image with new width and height

    Examples
    ---------
    >>> from pyimager import pyimager
    >>> pyimager.redusize("bear.jpg", "result.png", 33, 33)
    # A file named "result.png" with the width 33 and height 33 will be
    # generated in the current folder.
    """
    # reading the image's original dimension
    image = plt.imread(input_file)
    width = image.shape[1]
    height = image.shape[0]
    # asserting that the new dimensions are less than the original dimensions
    if new_width > width:
        raise AssertionError(
            "New width should be less than the original width")
    if new_height > height:
        raise AssertionError(
            "New height should be less than the original height")
    # reducing the width dimension
    for i in range(0, (width - new_width)):
        dx = np.array([-1, 0, 1])[None, :, None]
        dy = np.array([-1, 0, 1])[:, None, None]
        energy_img = convolve(image, dx) ** 2 + convolve(image, dy) ** 2
        v_seam = np.zeros(energy_img.shape[0])
        lin_inds = np.array(v_seam) + np.arange(image.shape[0]) * image.shape[
            1]
        new_image = np.zeros(
            (height, image.shape[1] - 1, image.shape[-1]), dtype=image.dtype)
        for j in range(image.shape[-1]):
            temp = np.delete(image[:, :, j], lin_inds.astype(int))
            temp = np.reshape(temp, (height, image.shape[1] - 1))
            new_image[:, :, j] = temp
        image = new_image
    width = image.shape[1]
    height = image.shape[0]
    # reducing the height dimension
    for i in range(0, (height - new_height)):
        image = np.transpose(image, (1, 0, 2))
        dx = np.array([-1, 0, 1])[None, :, None]
        dy = np.array([-1, 0, 1])[:, None, None]
        energy_img = convolve(image, dx) ** 2 + convolve(image, dy) ** 2

        h_seam = np.zeros(energy_img.shape[0])
        lin_inds = np.array(h_seam) + np.arange(image.shape[0]) * image.shape[
            1]
        new_image = np.zeros(
            (width, image.shape[1] - 1, image.shape[-1]), dtype=image.dtype)
        for c in range(image.shape[-1]):
            temp = np.delete(image[:, :, c], lin_inds.astype(int))
            temp = np.reshape(temp, (width, image.shape[1] - 1))
            new_image[:, :, c] = temp
        image = np.transpose(new_image, (1, 0, 2))

    assert (image.shape[0] == new_height)
    assert (image.shape[1] == new_width)

    plt.imsave(output_file, image)
    return image


def imgfilter(input_path, filter_type, strength, output_path=None):
    """
    Applies a filter to a given image to edit the visual aesthetic.

    The filter types include 'blur' and 'sharpen'; where
    blur blends neighboring pixels and sharpen enhances edges.
    The strength of the filter indicates how much of effect is apllied
    to the image; where 0 is no effect and 1 is very strong effect.

    Parameters
    ----------
    input_path : str
        path to the input image
    filter_type : str
        filter to be applied to the input image
        options: 'blur', 'sharpen'
    strength: int or float (0 to 1)
        the strength of the selected filter effect
    output_path: str or None (default = None)
        path to the modified output image file;
        if None, the image will not be saved to a file

    Returns
    -------
    np.array
        Array of pixels which comprises the original image with
        the applied filter

    Examples
    ---------
    >>> from pyimager import pyimager
    >>> pyimager.imgfilter("images/mandrill.jpg", "blur", 0.4)
    # An array of pixels resulting in an image with a
    # moderate blurred effect.
    """

    # assert strength is an int or float between 0 and 1
    if type(strength) != int and type(strength) != float:
        raise TypeError(
            "The 'strength' parameter inputs should be of type 'integer' or "
            "'float'")
    if strength < 0 or strength > 1:
        raise ValueError(
            "The 'strength' parameter can only take on values from 0 to 1")

    # assert filter_type is one of the valid option
    if filter_type != 'blur' and filter_type != 'sharpen':
        raise ValueError("The fliter_type entered is not a valid option")

    # assert input_path for img exists
    if not os.path.exists(input_path):
        raise FileNotFoundError("The input file does not exist")

    # Read in and convert image to np.array
    img = Image.open(input_path)
    input_array = np.array(img)
    h, w = img.size
    output_array = input_array.copy()

    if filter_type == 'blur':
        # create blur filter
        filt = np.full((int(h * strength / 10), int(w * strength / 10)),
                       1 / (int(h * strength / 10) * int(w * strength / 10)))
    else:
        # create sharpen filter
        filt = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) + np.array(
            [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]) * strength * 2

    # get coordinates for the middle of the filter
    filt_h = filt.shape[0]
    filt_w = filt.shape[1]
    offset_w = filt_w // 2
    offset_h = filt_h // 2

    # Compute convolution with kernel/filter
    for col in range(offset_w, w - offset_w):
        for row in range(offset_h, h - offset_h):

            new_rgb = [0, 0, 0]

            for x in range(filt_h):
                for y in range(filt_w):
                    # get coords for current filter position
                    x_new = col + x - offset_h
                    y_new = row + y - offset_w

                    # multiply pixel rgb by filter value
                    pixel_rgb = input_array[x_new, y_new]
                    new_rgb += pixel_rgb * filt[x][y]

            if filter_type == 'blur':
                output_array[col, row] = new_rgb
            else:
                output_array[col, row] = input_array[col, row] + (
                        input_array[col, row] - new_rgb) * strength * 10

    # crop image to remove boundary pixels
    output_array = output_array[offset_h:h - offset_h, offset_w:w - offset_w,
                                :]

    if output_path is not None:
        Image.fromarray(output_array).save(output_path)
        print(f'New image saved in {output_path}')

    return output_array


def reducolor(input_path, style, output_path=None):
    """
    Reduce image colors to have the cartoonized effect

    Parameters
    -----------
    input_path: string
        The file path of the image
    style: list,
        either two colors from ['white', 'black', 'red', 'green', 'blue', \
        'yellow', 'pink', 'aqua']
        or ['eight'] for eight colors
    output_path: string or None(default)
        if None, the modified image will not be saved
        if 'auto', the modified image will be saved in the same folder \
        as the image
        or the modified image will be saved in the provided folder path

    Returns
    --------
    numpy.ndarray
    the altered image and the image is saved in the designated path if \
    output_path is not None

    Examples
    ---------
    >>> from pyimager import pyimager
    >>> pyimager.reducolor('tests/mandrill.jpg', ['eight'], 'auto')
    >>> pyimager.reducolor('tests/mandrill.jpg', ['white', 'black'], 'auto')
    """

    color_dict = {'white': [1, 1, 1], 'black': [0, 0, 0], 'red': [1, 0, 0],
                  'green': [0, 1, 0], 'blue': [0, 0, 1], 'yellow': [1, 1, 0],
                  'pink': [1, 0.686, 0.843], 'aqua': [0, 1, 1]}

    img = plt.imread(input_path) / 255

    assert isinstance(style, list), 'style input must be a list'

    assert len(style) == 1 or len(style) == 2, f'style list ' \
                                               f'must be of length 1 or 2'

    if len(style) == 2:  # two color
        assert style[0] in color_dict.keys(), f'{style[0]} is not ' \
                                              f'available, please choose ' \
                                              f'from {list(color_dict.keys())}'
        assert style[1] in color_dict.keys(), f'{style[1]} is not available,' \
                                              f' please choose ' \
                                              f'from {list(color_dict.keys())}'
        assert style[0] != style[1], f'Two colors must be different.'
        new_img = img.copy()
        new_img[(img.mean(axis=2) < np.median(img)), :] = np.array(
            color_dict[style[0]])
        new_img[(img.mean(axis=2) >= np.median(img)), :] = np.array(
            color_dict[style[1]])

    elif len(style) == 1:
        assert style[0] == 'eight', 'Please put \'eight\' for eight colors'
        red = img[:, :, 0]
        red[red < np.median(red)] = np.min(red)
        red[red >= np.median(red)] = np.max(red)
        green = img[:, :, 1]
        green[green < np.median(green)] = np.min(green)
        green[green >= np.median(green)] = np.max(green)
        blue = img[:, :, 2]
        blue[blue < np.median(blue)] = np.min(blue)
        blue[blue >= np.median(blue)] = np.max(blue)
        new_img = np.zeros(img.shape)
        new_img[:, :, 0] = red
        new_img[:, :, 1] = green
        new_img[:, :, 2] = blue

    if output_path == 'auto':
        output_path = input_path
        while os.path.exists(output_path):
            output_path = re.sub(r'\.[jp][ pn]g$', '_reducolor.jpg', 
                                 output_path)
        imsave(f'{output_path}', new_img)
        print(f'New image saved in {output_path}')
    elif output_path is not None:
        imsave(f'{output_path}', new_img)
        print(f'New image saved in {output_path}')

    return Image.fromarray((new_img * 255).astype(np.uint8))
