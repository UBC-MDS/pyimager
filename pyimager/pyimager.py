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
    >>> from pyimager import circropper
    >>> circropper("bear.jpg", "result.png")
    A file named "result.png" will be generated in the your
    designated folder.
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
        A function to reduce the dimension of a give image by removing vertical and horizontal seams
        
        Parameters
        ----------
        input_file : path to the image to the input image
        output_file : path to the image to the output image
        newdim: new width the output image
        height:new height of the output image
        
        Returns
        -------
        A new image with new width and height

         Examples:
        ---------
        reduce_dimensions(bear.jpg", "result.png", 33, 33)
        A file named "result.png"  with the width 33 and height 33 will be generated in the your
         designated folder.
        """

