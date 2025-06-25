# This file is meant to hold functionality for image processing 
from astropy.io import fits 
from astropy.visualization import ZScaleInterval, AsinhStretch
import numpy as np
from PIL import Image

def read_fits_data(fits_binary):
    """Read FITS data from binary (as stored in project)"""
    from io import BytesIO
    with fits.open(BytesIO(fits_binary)) as hdul:
        return hdul[0].data
    
def process_channel(data, zscale_contrast=0.25, stretch_a=0.1, stretch_factor=3.0):
    """Apply zscale and asinh stretch to a single channel"""

    zscale = ZScaleInterval(contrast = zscale_contrast)
    data = zscale(data)
    stretch = AsinhStretch(a=stretch_a)
    data = stretch(data* stretch_factor)
    data= np.nan_to_num(data)
    data = (data * 255).astype(np.uint8)
    return data

def create_rgb_image(r_data, g_data, b_data):
    """Stack R, G, B channels into a PIL RGB image"""

    rgb_array = np.stack([r_data, g_data, b_data], axis=-1)
    return Image.fromarray(rgb_array, mode='RGB')

def process_fits_binaries(fit_binaries, zscale_contrast=0.25, stretch_a=0.1, stretch_factor=3.0):
    """
    Given a dict of {'R': binary, 'G': binary, 'B': binary}, process and return a PIL Image.
    """
    channels = {}
    for channel in ['R', 'G', 'B']:
        data = read_fits_data(fit_binaries[channel])
        channels[channel] = process_channel(data, zscale_contrast, stretch_a, stretch_factor)
    return create_rgb_image(channels['R'], channels['G'], channels['B'])

