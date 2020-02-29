def reducolor(input_path, output_path=None, ncolor):
    '''
    Reduce image colors

    Parameters:
    -----------
    input_path: string
        The file path of the image
    output_path: string or None
        if not None, the modified image will be saved
        in the provided folder path
    ncolor: int
        Number of colors to be reduced to

    Returns:
    --------
    numpy.ndarray of the image
    
    Examples:
    ---------
    reducolor('images/milad.jpg', 'images', 4)
    '''
