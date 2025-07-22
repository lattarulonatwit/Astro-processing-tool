# Class to represent the UI widgets for the metadata cell  
import tkinter as tk
from tkinter import ttk
class MetadataCell(tk.Frame):
     def __init__(self, parent, starsToDetect, on_starID):
        super().__init__(parent)
        self.on_starID = on_starID
        self.starsToDetect = starsToDetect
        for name, var, from_, to, resolution in [
            ("Number of stars to detect", self.starsToDetect, 1, 100, 1),
        ]:
            frame = tk.Frame(self)
            frame.pack(pady=5, fill='x', padx=5)
            tk.Label(frame, text=name).pack(side='top', anchor='w')
            slider = tk.Scale(
                frame,
                variable=var,
                from_=from_,
                to=to,
                resolution=resolution,
                orient='horizontal'
            )
            slider.pack(fill='x', expand=True)

        starID_button = tk.Button(
            self,
            text="Identify Stars",
            command= self.on_starID
        )
        starID_button.pack(pady=10)

        
          #tab to switch views
        self.dataTabControl = ttk.Notebook(self)    
        self.dataTabControl.pack(pady=5, fill='both')

        self.captureTab = ttk.Frame(self.dataTabControl)
        self.astroTab = ttk.Frame(self.dataTabControl)
        self.dataTabControl.add(self.captureTab, text="Image Data")
        self.dataTabControl.add(self.astroTab, text = "Astro Data")

        
        #labels for image info
        #imaga data

        self.focalLengthLabel = tk.Label(self.captureTab, text = "Telescope Focal length: N/A")
        self.focalLengthLabel.grid(row = 1, column = 0, sticky = "ew", pady = (5, 0))

        self.shutterSpeedLabel = tk.Label(self.captureTab, text = "Camera exposure time: N/A")
        self.shutterSpeedLabel.grid(row = 2, column = 0, sticky = "ew", pady = (5, 0))

        self.integrationTimeLabel = tk.Label(self.captureTab, text = "Total Image Exposure Time (minutes): N/A")
        self.integrationTimeLabel.grid(row = 3, column = 0, sticky = "ew", pady = (5, 0))

        self.ISOLabel = tk.Label(self.captureTab, text="Sensor gain: N/A")
        self.ISOLabel.grid(row=4, column=0, sticky="ew", pady=(5, 0))

        #star data
        self.pixelScaleLabel = tk.Label(self.astroTab, text = "Image Pixel Scale: N/A")
        self.pixelScaleLabel.grid(row = 1, column = 0, sticky = "ew", pady = (5, 0))

        self.RALabel = tk.Label(self.astroTab, text = "Image Right Asension: N/A")
        self.RALabel.grid(row = 2, column = 0, sticky = "ew", pady = (5, 0))

        self.DecLabel = tk.Label(self.astroTab, text = "Image Declination: N/A")
        self.DecLabel.grid(row = 3, column = 0, sticky = "ew", pady = (5, 0))

        self.numStarsLabel = tk.Label(self.astroTab, text = "Number of stars found: N/A")
        self.numStarsLabel.grid(row = 4, column = 0, sticky = "ew", pady = (5, 0))

        self.brightestLabel = tk.Label(self.astroTab, text="Brightest Star Magnitude: N/A")
        self.brightestLabel.grid(row=5, column=0, sticky="ew", pady=(5, 0))

     def updateLabels(self, focalLength, shutterSpeed, integrationTime, ISO, imageRA, imageDec, pixelScale, numStars, brightest):
        #Mess with the labels
        self.focalLengthLabel["text"] = f"Telescope Focal Length: {focalLength} mm"
        self.shutterSpeedLabel["text"]= f"Camera Exposure Time: {shutterSpeed} s"
        self.integrationTimeLabel["text"]= f"Total Image Exposure Time: {int(integrationTime.pop())/60} s"
        self.ISOLabel["text"] = f"Sensor gain: {ISO}"

        self.RALabel["text"]= f"Image Right Ascension: {imageRA}" 
        self.DecLabel["text"]= f"Image Declination: {imageDec}" 
        self.pixelScaleLabel["text"] = f"Image Pixel Scale: {int(pixelScale.pop()):.8f} Arcsecond / pixel"
        self.brightestLabel["text"] = f"Brightest Star Magnitude: {brightest:.2f}"
        self.numStarsLabel["text"]= f"Number of Stars Detected: {numStars}" 

