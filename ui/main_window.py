import tkinter as tk
from .fits_upload_modal import FitsUploadModal
from astropy.io import fits
from astropy.visualization import ZScaleInterval, AsinhStretch
import numpy as np
from PIL import Image, ImageTk


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
        
        self.canvas = tk.Canvas(
            self.canvas_frame,
            background="black"
        )
        self.canvas.pack(fill="both", expand=True)


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
        
        # Create Metadata cell
        metadata_cell = tk.Frame(self.sidebar_frame, bg='lightyellow')
        metadata_cell.grid(row=1, column=0, sticky="nsew")

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
                # Load each FITS file
                rgb_data = {}
                for channel, filepath in fits_files.items():
                    with fits.open(filepath) as hdul:

                        
                        #********** The below is hard coded but it is what we wish to 
                        # edit on the top control cell*****************************

                        # Get the image data and process it
                        data = hdul[0].data
                        
                        # Apply ZScale normalization
                        zscale = ZScaleInterval()
                        data = zscale(data)
                        
                        # Apply stretch to bring out faint details
                        stretch = AsinhStretch()
                        data = stretch(data)
                        
                        # Scale to 0-255 range for display
                        data = (data * 255).astype(np.uint8)
                        
                        rgb_data[channel] = data
                
                # Create RGB image array
                rgb_array = np.stack([
                    rgb_data['R'],
                    rgb_data['G'],
                    rgb_data['B']
                ], axis=-1)  # Stack along the last axis

                # Create PIL Image
                image = Image.fromarray(rgb_array, mode='RGB')
                
                # Convert to PhotoImage for tkinter
                photo = ImageTk.PhotoImage(image)
                
                # Display in canvas
                self.canvas.create_image(
                    self.canvas.winfo_width()//2,
                    self.canvas.winfo_height()//2,
                    image=photo,
                    anchor="center"
                )
                
                # Keep a reference to prevent garbage collection
                self.current_image = photo
                
            except Exception as e:
                print(f"Error processing FITS files: {e}")