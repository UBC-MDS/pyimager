import numpy as np
from PIL import Image, ImageDraw
from matplotlib.image import imsave
import matplotlib.pyplot as plt 

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
   
class StyleException(Exception):
    pass

def reducolor(style, input_path, output_path=None):
    '''
    Reduce image colors

    Parameters:
    -----------
    style: int, either 0 or 1
        0 for white and black colors
        1 for 8 colors
    input_path: string
        The file path of the image
    output_path: string or None
        if not None, the modified image will be saved
        in the provided folder path and name

    Returns:
    --------
    numpy.ndarray of the image and an image saved in the designated path 
    
    Examples:
    ---------
    reducolor(0, 'tests/mandrill.jpg', 'tests/mandrill_new.jpg')
    '''
    
    img = plt.imread(input_path)/255    

    if style==0:  #black and white color
        new_img = img.copy()
        new_img[(img.mean(axis=2)<0.5), :] = np.array([0, 0, 0])  #less than gray
        new_img[(img.mean(axis=2)>=0.5), :] = np.array([1, 1, 1])
    
    elif style==1:
        red = img[:,:,0]
        red[red<np.median(red)] = np.min(red)
        red[red>np.median(red)] = np.max(red)
        green = img[:,:,1]
        green[green<np.median(green)] = np.min(green)
        green[green>np.median(green)] = np.max(green)
        blue = img[:,:,2]
        blue[blue<np.median(blue)] = np.min(blue)
        blue[blue>np.median(blue) ]= np.max(blue)
        new_img = np.zeros(img.shape)
        new_img[:, :, 0] = red
        new_img[:, :, 1] = green
        new_img[:, :, 2] = blue
    else:
        raise StyleException('Please enter valid style code.\n 0 for black and white color, 1 for eight color scales')
    
    if output_path is not None:
       imsave(f'{output_path}', new_img)
       print(f'New image saved in {output_path}')
    
    return new_img
