# This file should hold all imports and functions needed for fancy science shiz
from photutils.detection import DAOStarFinder
from photutils.aperture import CircularAperture
from astropy.stats import sigma_clipped_stats
from PIL import Image
import cv2
import numpy as np


"""Star detection function

Keyword arguments:
pil_image -- current canvas image (must be passed in)
fit_files -- one of the fits channels R, G, or B it can be either one
Return: An image with circles around the stahs (Boston Accent)
"""

brightest = None
numStars = None

def source_detect(pil_image, fit_files, starsToDetect):
        global brightest
        global numStars
        # Perform star detection using photutils
        mean, median, std = sigma_clipped_stats(fit_files, sigma=3.0)
        findStars = DAOStarFinder(fwhm=3.0, threshold=3.0 * std)
        starTable = findStars(fit_files - median)
        starTable.sort('mag') #sort stars by their brightest
        brightest = starTable[0]['mag']
        numStars = len(starTable)
        starTable = starTable[:starsToDetect] #shorten the list to 100

        starXList = starTable['xcentroid'].data
        starYList = starTable['ycentroid'].data

        # Get the current processed image into np array form
        if pil_image is None:
            return
        imageNp = np.array(pil_image)
        imageNp = imageNp.copy() # Make a writable copy 

        #cirlce info
        radius = 15  
        color = (0, 255, 0)  
        thickness = 2  

        for xPixel, yPixel in zip(starXList, starYList):
            # OpenCV's circle function expects integer coordinates
            centerX = int(xPixel)
            centerY = int(yPixel)

            # Check if the pixel coords are within the image bounds
            imageH, imageW, _ = imageNp.shape
            if 0 <= centerX < imageW and 0 <= centerY < imageH:
                cv2.circle(imageNp, (centerX, centerY), radius, color, thickness) #then add circle

            # Convert np array back to PIL Image and display
            pil_image = Image.fromarray(imageNp, mode='RGB')
            
        return pil_image

def getBrightest():
     return brightest

def getnumStars():
     return numStars
     