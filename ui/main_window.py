import tkinter as tk
from .fits_upload_modal import FitsUploadModal
from astropy.io import fits
from astropy.visualization import ZScaleInterval, AsinhStretch
import numpy as np
from PIL import Image, ImageTk
from .viewport.zoomable_viewer import ZoomableImageViewer
from functools import partial
import time


# Class that creates Main window 
class MainWindow:

    #function to intialize the window 
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)  # Set minimum width and height
        self.root.title("Astro Image Processor")
        
        # Configure root grid weights for responsive layout
        self.root.grid_columnconfigure(0, weight=4)  # Canvas gets more space
        self.root.grid_columnconfigure(1, weight=3)  # Sidebar gets less space
        self.root.grid_rowconfigure(0, weight=1)     # Row expands
        
        #Call to create each UI element
        self.setup_menu_items()
        self.create_canvas()
        self.setup_sidebar()

        self.last_update = 0
        self.update_delay = 0.1  # 100ms delay between updates
        
    # UI Elements are created via the functions below
    def setup_menu_items(self):
        # Create menu bar
        menu_bar = tk.Menu(self.root)
        
        # Define menu items with categories and commands
        menu_data = {
            "File": [
                ("New", lambda: print("New clicked")),
                ("Open", lambda: print("Open clicked")),
                ("Save Project", lambda: print("Save Project clicked"))
            ],
            "Export": [
                ("Export Image", lambda: print("Export Image clicked")),
            ],
            "Upload": [
                ("Upload Fits", lambda: self.show_fits_upload())  # Change this line
            ]
        }

        # Create menu items (no dropdowns just yet)
        for category, items in menu_data.items():
            for label, command in items:
                menu_bar.add_command(label=label, command=command)
            
        # Attach menu bar to root window
        self.root.config(menu=menu_bar)

    # Function to create the canvas for the image
    def create_canvas(self):

        # Create the frame to hold the canvas 
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=0, column=0, sticky="nsew")
        

        self.image_viewer = ZoomableImageViewer(self.canvas_frame)
        self.image_viewer.pack(fill="both", expand=True)


        # self.canvas = tk.Canvas(
        #     self.canvas_frame,
        #     background="black"
        # )
        # self.canvas.pack(fill="both", expand=True)


    def setup_sidebar(self):

        # Create the frame to hold the cells 
        self.sidebar_frame = tk.Frame(self.root)
        self.sidebar_frame.grid(row=0, column=1, sticky="nsew")
        
        # Configure sidebar grid
        self.sidebar_frame.grid_rowconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        
        # Create cells

        # Create control cell
        control_cell = tk.Frame(self.sidebar_frame, bg='lightgray')
        control_cell.grid(row=0, column=0, sticky="nsew")
        
        # Add image control sliders
        self.add_control_sliders(control_cell)

        # Create Metadata cell
        metadata_cell = tk.Frame(self.sidebar_frame, bg='lightyellow')
        metadata_cell.grid(row=1, column=0, sticky="nsew")

    def add_control_sliders(self, parent):
        """Add sliders and apply button for image processing parameters"""
        # Initialize default values
        self.zscale_contrast = tk.DoubleVar(value=0.25)
        self.stretch_a = tk.DoubleVar(value=0.1)
        self.stretch_factor = tk.DoubleVar(value=3.0)
        
        # Create frames for each parameter
        for name, var, from_, to, resolution in [
            ("ZScale Contrast", self.zscale_contrast, 0.1, 1.0, 0.05),
            ("Stretch A", self.stretch_a, 0.01, 1.0, 0.01),
            ("Stretch Factor", self.stretch_factor, 0.1, 10.0, 0.1)
        ]:
            frame = tk.Frame(parent)
            frame.pack(pady=5, fill='x', padx=5)
            
            tk.Label(frame, text=name).pack(side='top', anchor='w')
            
            # Remove debounce from sliders
            slider = tk.Scale(
                frame,
                variable=var,
                from_=from_,
                to=to,
                resolution=resolution,
                orient='horizontal'
            )
            slider.pack(fill='x', expand=True)

        # Add Apply Changes button
        apply_button = tk.Button(
            parent,
            text="Apply Changes",
            command=self.update_image_processing
        )
        apply_button.pack(pady=10)

    def update_image_processing(self):
        """Update image when sliders change"""
        if hasattr(self, 'current_fits_files'):
            self.process_fits_files(self.current_fits_files)

    # Function to open the fits file upload
    def show_fits_upload(self):
        dialog = FitsUploadModal(self.root)
        dialog.grab_set()  # Make dialog modal
        self.root.wait_window(dialog)  # Wait for dialog to close
        
        # The above is a blocking command meaning the code come back here once it is closed
        # The modal returns the fits files when "Build Image is clicked "

        # Get the files selected in the dialog
        if hasattr(dialog, 'fits_files'):
            self.process_fits_files(dialog.fits_files)

    # Function to process fits files 
    # Steps are Load them -> Process the data -> Create the RGB Image -> Display on canvas
    def process_fits_files(self, fits_files):
        if all(fits_files.values()):  # Check if all channels have files
            try:
                # Store files for reprocessing when sliders change
                self.current_fits_files = fits_files
                
                # Load each FITS file
                rgb_data = {}
                for channel, filepath in fits_files.items():
                    with fits.open(filepath) as hdul:
                        # Get the image data and process it
                        data = hdul[0].data
                        
                        # Apply ZScale normalization with slider value
                        zscale = ZScaleInterval(contrast=self.zscale_contrast.get())
                        data = zscale(data)
                        
                        # Apply stretch with slider values
                        stretch = AsinhStretch(a=self.stretch_a.get())
                        data = stretch(data * self.stretch_factor.get())
                        
                        # Scale to 0-255 range for display
                        data = (data * 255).astype(np.uint8)
                        
                        rgb_data[channel] = data
                
                # Create RGB image array
                rgb_array = np.stack([
                    rgb_data['R'],
                    rgb_data['G'],
                    rgb_data['B']
                ], axis=-1)

                # Create PIL Image and display
                image = Image.fromarray(rgb_array, mode='RGB')
                self.image_viewer.load_image(image)
                
                # Store reference
                self.current_image = ImageTk.PhotoImage(image)
                
            except Exception as e:
                print(f"Error processing FITS files: {e}")