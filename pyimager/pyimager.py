import numpy as np
from PIL import Image, ImageDraw
from matplotlib.image import imsave
import matplotlib.pyplot as plt
from scipy.ndimage.filters import convolve
import os


def circropper(input_path, margin):
    """
    Crops an image into a circle and leave some margin as you defined 

    Parameters:
    -----------
    input_path: string 
        The file path of the image to be cropped
    margin: float or int 
        The distance between circle boundary and the original image boundary
    
    Returns:
    --------
        A new cropped Image object 
        
    Examples:
    ---------
    >>> from pyimager import pyimager
    >>> circropper("bear.jpg", 0)
    A Image is cropped to a circle with no margin 
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

    Examples:
    ---------
    >>> from pyimager import pyimager
    >>> pyimager.redusize("bear.jpg", "result.png", 33, 33)
    A file named "result.png"  with the width 33 and height 33 will be
    generated in the current folder.
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
    
    # examples :       
    # python -c'import pyimager;pyimager.redusize(
    # "../images/mandrill.jpg","../images/reduced_mandrill.jpg",210,200)'


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

    Examples:
    ---------
    >>> from pyimager import pyimager
    >>> pyimager.imgfilter("bear.jpg", "blur", 0.4)
    An array of pixels resulting in an image with a 
    moderate blurred effect.
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


def reducolor(style, input_path, output_path=None):
    """
    Reduce image colors to have the cartoonized effect

    Parameters:
    -----------
    style: int, either 0 or 1
        0 for white and black colors
        1 for 8 colors
    input_path: string
        The file path of the image
    output_path: string or None(default)
        if not None, the modified image will be saved
        in the provided folder path and name

    Returns:
    --------
    numpy.ndarray of the image and an image saved in the designated path

    Examples:
    ---------
    reducolor(0, 'tests/mandrill.jpg', 'tests/mandrill_new.jpg')
    """
    
    img = plt.imread(input_path) / 255
    
    assert style == 0 or style == 1, f'{style} is invalid for the style ' \
                                     f'argument.\n Please enter either 0 for ' \
                                     f'' \
                                     f'' \
                                     f'' \
                                     f'' \
                                     f'' \
                                     f'' \
                                     f'' \
                                     f'' \
                                     f'black and white color, 1 for eight ' \
                                     f'color scales '
    
    if style == 0:  # black and white color
        new_img = img.copy()
        new_img[(img.mean(axis=2) < 0.5), :] = np.array(
            [0, 0, 0])  # less than gray
        new_img[(img.mean(axis=2) >= 0.5), :] = np.array([1, 1, 1])
    
    elif style == 1:
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
    
    if output_path is not None:
        imsave(f'{output_path}', new_img)
        print(f'New image saved in {output_path}')
    
    return new_img
