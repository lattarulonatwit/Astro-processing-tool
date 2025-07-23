# This file should hold all imports and functions needed for fancy science shiz
from photutils.detection import DAOStarFinder
from photutils.aperture import CircularAperture
from astropy.stats import sigma_clipped_stats
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
from astroquery.simbad import Simbad
import astropy.units as u
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

        # Get the current processed image into np array form
        if pil_image is None:
            return
        imageNp = np.array(pil_image)
        imageNp = imageNp.copy() # Make a writable copy 

        #cirlce info
        radius = 15   
        thickness = 2  

        for i, star in enumerate(starTable):
            if i == 0:
                 color = (255, 0, 0)
            else:
                 color = (0, 255, 0)
            # OpenCV's circle function expects integer coordinates
            centerX = int(star['xcentroid'])
            centerY = int(star['ycentroid'])

            # Check if the pixel coords are within the image bounds
            imageH, imageW, _ = imageNp.shape
            if 0 <= centerX < imageW and 0 <= centerY < imageH:
                cv2.circle(imageNp, (centerX, centerY), radius, color, thickness) #then add circle

            # Convert np array back to PIL Image and display
            pil_image = Image.fromarray(imageNp, mode='RGB')
            
        return pil_image


def nameObject(pil_image, fitsHeader, objectToDetect):
        print(objectToDetect)
        npData = np.array(pil_image)
        wcs = WCS(fitsHeader) #Creates a world coordinate system object based off the header which will factor various conversion values. 
        coords = SkyCoord(ra= fitsHeader['RA'] * u.deg, dec= fitsHeader['DEC'] * u.deg, frame='icrs') #Create a 'skycoord' object which holds the coordinates as well as format

        searchDist = 5 * u.deg # 6 degree search distance. Plan to adjust to degrees fov
        searchFilter = "otype = 'Sy2' OR otype = 'AGN' OR otype = 'GNe' OR otype = 'PN' OR otype = 'SFR' OR otype = 'OpC' OR otype = 'GiC' OR otype = 'GiG' OR otype = 'HII' OR otype = 'RAD'" #keywords for different types of objects

        Simbad.add_votable_fields('otype', 'main_id', 'ra', 'dec', 'V') # request certain fields from simbad    
        simbadQuery = Simbad.query_region(coords, radius= searchDist, criteria=searchFilter) # send in request 
        if simbadQuery:
            simbadQuery.sort('V') #order the results by brightness to find the most prominent objects
       
        radius = 100
        color = (0, 0, 255)
        thickness = 10

        #store sky coordinates from simbad
        for i in range(objectToDetect.get()):
             rightAscension = (simbadQuery[i]['ra'])
             declination = (simbadQuery[i]['dec'])
             objName = (simbadQuery[i]['main_id'])
        
             # convert ra/dec to xy using wcs data
             xyCoords = wcs.all_world2pix([[rightAscension, declination]], 1) #convert ra/dec coordinates to xy for circle placement
             #get x and y from result
             xPx = xyCoords[0][0]
             yPx = xyCoords[0][1]

             #add circles and label within bounds of image
             if 0 <= xPx < npData.shape[1] and 0 <= yPx < npData.shape[0]:
                cv2.circle(npData, (int(xPx), int(yPx)), radius, color, thickness) #add object circle

               # Add the label to the object
                nameLabel = objName
                cv2.putText(npData, nameLabel, (int(xPx), int(yPx)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 2, cv2.LINE_AA)

                cv2.circle(npData, (int(xPx), int(yPx)), radius, color, thickness) #add object circle


        # Convert np array back to pil_image to return and be displayed
        pil_image = Image.fromarray(npData, mode='RGB')
        return pil_image

#getter functions for values from DAO star find
def getBrightest():
     return brightest

def getnumStars():
     return numStars
     