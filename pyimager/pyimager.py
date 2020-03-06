import numpy as np
from PIL import Image, ImageDraw

def circropper(input_path, output_path):
    """
    Crops an image into the circle shape.

    Parameters:
    -----------
    input_path: string 
        The file path of the image to be cropped
    output_path: string
        The file path for cropped image 
    
    Examples:
    ---------
    >>> from pyimager import pyimager
    >>> pyimager.circropper("bear.jpg", "result.png")
    A file named "result.png" will be generated in the current folder.
    """
    # Read in and convert image to np.array
    img=Image.open(input_path).convert("RGB")
    imgArray=np.array(img)
    height,weight=img.size

    # Create circle mask layer and crop 
    mask = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice([0,0,height,weight],0,360,fill=255)
    maskArray=np.array(mask)
    imgArray=np.dstack((imgArray,maskArray))

    # Output image 
    Image.fromarray(imgArray).save(output_path)

def reduce_dimensions(input_file, output_file, width, height):
	"""  
    A function to reduce the dimension of a given image by removing vertical and horizontal seams
        
    Parameters
    ----------
    input_file : str
        path to the input image
    output_file : str
        path to the output image
    width : int
        new width the output image
    height : int
        new height of the output image
        
    Returns
    -------
    A new image with new width and height

    Examples:
    ---------
    >>> from pyimager import pyimager
    >>> pyimager.reduce_dimensions("bear.jpg", "result.png", 33, 33)
    A file named "result.png"  with the width 33 and height 33 will be generated in the
    current folder.
    """

def img_filter(input_path, filter_type, strength):
	"""  
    Applies a filter to a given image to edit the visual aesthetic. 

    The filter types include 'blur', 'emboss', and 'grayscale'; where
    blur blends neighboring pixels, emboss creates a '3D like' impression, 
    and grayscale returns a black and white image. 
    The strength of the filter indicates how much of effect is apllied
    to the image; where 0 is no effect and 1 is very strong effect.
        
    Parameters
    ----------
    input_path : str
        path to the input image
    filter_type : str
        filter to be applied to the input image
        options: 'blur', 'emboss', 'grayscale' 
    strength: int or float (0 to 1)
        the strength of the selected filter effect

    Returns
    -------
    np.array
        Array of pixels which comprises the original image with the applied filter

    Examples:
    ---------
    >>> from pyimager import pyimager
    >>> pyimager.img_filter("bear.jpg", "blur", 0.4)
    An array of pixels resulting in an image the same size as "bear.jpg" with a 
    moderate blured effect.
    """

    # Read in and convert image to np.array
    img = Image.open(input_path).convert("RGB")
    img_array = np.array(img)
    height,width = img.size
    
