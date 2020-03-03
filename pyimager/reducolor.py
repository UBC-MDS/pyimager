import numpy as np
from matplotlib.image import imsave
import matplotlib.pyplot as plt 

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
    numpy.ndarray of the image
    
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
        raise Exception('Please enter valid style code.\n 0 for black and white color, 1 for eight color scales')
    
    if output_path is not None:
       imsave(f'{output_path}', new_img) 
    
    return new_img