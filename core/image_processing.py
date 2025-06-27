# This file is meant to hold functionality for image processing 
from astropy.io import fits 
from astropy.visualization import ZScaleInterval, AsinhStretch, make_lupton_rgb
import numpy as np
from PIL import Image

def read_fits_data(fits_binary):
    """Read FITS data from binary (as stored in project)"""
    from io import BytesIO
    with fits.open(BytesIO(fits_binary)) as hdul:
        return hdul[0].data
    

def create_rgb_image(r_data, g_data, b_data, stretch = 0.5, Q=8, minimum=0):
    """Stack R, G, B channels into a PIL RGB image"""
    # RGB array is now made using make_lupton algo
    rgb_array = make_lupton_rgb(r_data, g_data, b_data, stretch=stretch, Q=Q, minimum=minimum)

    return Image.fromarray(rgb_array, mode='RGB')

def process_fits_binaries(fit_binaries, zscale_contrast=0.25, lupton_stretch=0.5, lupton_Q=0.5, lupton_minimum=0):
    """
    Given a dict of {'R': binary, 'G': binary, 'B': binary}, process and return a PIL Image.
    """
    channels = {}
    for channel in ['R', 'G', 'B']:
        data = read_fits_data(fit_binaries[channel])
        # Only apply zscale for normalization, do NOT asinh/stretch for Lupton
        zscale = ZScaleInterval(contrast=zscale_contrast)
        data = zscale(data)
        data = np.nan_to_num(data)
        channels[channel] = data
    return create_rgb_image(
        channels['R'], channels['G'], channels['B'],
        stretch=lupton_stretch, Q=lupton_Q, minimum=lupton_minimum
    )
