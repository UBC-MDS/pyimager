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

    import numpy as np
    from scipy.ndimage.filters import convolve
    import matplotlib.pyplot as plt
    image = plt.imread("mandrill.jpg")

    new_width = 200
    new_height = 280

    def pyimager(input_file,output_file,new_width,new_height):
        image = plt.imread(input_file)
        width = image.shape[1] 
        height = image.shape[0]
        for i in range(0,(width-new_width)):

            dx = np.array([-1, 0, 1])[None, :, None]
            dy = np.array([-1, 0, 1])[:, None, None]    
            energy_img = convolve(image, dx)**2 + convolve(image, dy)**2

            v_seam = np.zeros(energy_img.shape[0])
            lin_inds = np.array(v_seam)+np.arange(image.shape[0])*image.shape[1]
            new_image = np.zeros(
                (height, image.shape[1]-1, image.shape[-1]), dtype=image.dtype) 
            for j in range(image.shape[-1]):
                temp = np.delete(image[:, :, j], lin_inds.astype(int))
                temp = np.reshape(temp, (height, image.shape[1]-1))
                new_image[:, :, j] = temp
            image=new_image


        width = image.shape[1] 
        height = image.shape[0]

        for i in range(0,(height-new_height)):
            image= np.transpose(image, (1, 0, 2)) 
            dx = np.array([-1, 0, 1])[None, :, None]
            dy = np.array([-1, 0, 1])[:, None, None]    
            energy_img = convolve(image, dx)**2 + convolve(image, dy)**2

            h_seam = np.zeros(energy_img.shape[0])
            lin_inds = np.array(h_seam)+np.arange(image.shape[0])*image.shape[1]
            new_image = np.zeros(
                (width, image.shape[1]-1, image.shape[-1]), dtype=image.dtype) 
            for c in range(image.shape[-1]):
                temp = np.delete(image[:, :, c], lin_inds.astype(int))
                temp = np.reshape(temp, (width, image.shape[1]-1))
                new_image[:, :, c] = temp
            image=np.transpose(new_image,(1, 0, 2))
            
        assert(image.shape[0] ==new_height)
        assert(image.shape[1] ==new_width)
            
        plt.imsave(output_file, image)
        return(image)

    # examples : just for test will be deleted later      
    r = pyimager("mandrill.jpg","images/reduced.jpg",210,200)
    print(r.shape[0])
    print(r.shape[1])


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
    
