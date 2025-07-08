import tkinter as tk
from .fits_upload_modal import FitsUploadModal
from astropy.io import fits
from astropy.visualization import ZScaleInterval, AsinhStretch
import numpy as np
from PIL import Image, ImageTk
from .viewport.zoomable_viewer import ZoomableImageViewer
from functools import partial
import time
import os
from core.project import Project
from core.image_processing import process_fits_binaries
from ui.sidebar.image_controls import ImageControlsCell
from ui.sidebar.metadata_cell import MetadataCell
from core.metadata import source_detect



# Class that creates Main window 
class MainWindow:

    #function to intialize the window 
    def __init__(self, root):
        self.root = root

        # Initalize current project path
        self.current_project_path=None


        # Initialize image control variables for image 
        self.zscale_contrast = tk.DoubleVar(value = 0.25)
        self.lupton_stretch = tk.DoubleVar(value=0.5)
        self.lupton_Q = tk.DoubleVar(value=8.0)
        self.lupton_minimum = tk.DoubleVar(value=0.0)


        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)  # Set minimum width and height
        self.root.title("Astro Image Processor")
        
        # Initalize current project 
        self.current_project = Project.create_new()
        self.update_window_title()

        # Configure root grid weights for responsive layout
        self.root.grid_columnconfigure(0, weight=4)  # Canvas gets more space
        self.root.grid_columnconfigure(1, weight=3)  # Sidebar gets less space
        self.root.grid_rowconfigure(0, weight=1)     # Row expands
        
        # Initialize canvas image 
        self.pil_image = None
        
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
                ("New", lambda: self.new_project()),
                ("Open", lambda: self.load_project()),
                ("Save", lambda: self.save_project()),
                ("Save As", lambda: self.save_project_as())
            ],
            "Export": [
                ("Export Image", lambda: self.export_image()),
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
        
        

        # START OF CELL CREATION

        # Create Control cell

        self.image_controls_cell = ImageControlsCell(
        self.sidebar_frame,
        self.zscale_contrast,
        self.lupton_stretch,
        self.lupton_Q,
        self.lupton_minimum,
        self.update_image_processing,  # Pass the function to call on apply
        )

        # Place it
        self.image_controls_cell.grid(row=0, column=0, sticky="nsew")

        # Create Metadata cell
        self.metadata_cell = MetadataCell(
        self.sidebar_frame, # Parent is the sidebar frame
        self.update_metadata_cell
        )
        self.metadata_cell.grid(row=1, column=0, sticky="nsew")
        # END OF CELL CREATION


    def update_image_processing(self):
        """Update image when sliders change"""
        if hasattr(self.current_project, 'fit_binaries'):
            self.pil_image = process_fits_binaries(
                 self.current_project.fit_binaries,
                 zscale_contrast=self.zscale_contrast.get(),
                 lupton_stretch=self.lupton_stretch.get(),
                 lupton_Q=self.lupton_Q.get(),
                 lupton_minimum=self.lupton_minimum.get(),

            )
            self.image_viewer.load_image(self.pil_image)
            self.current_project.save_image(self.pil_image)

    def update_metadata_cell(self):
        print("button pressed")
        """Update image from scientific analysis"""
        # I believe this should just check if there's currently an image on the canvas
        if self.pil_image is not None:

            self.pil_image = source_detect(self.pil_image, self.current_project.get_fits_data('R')) # Pass in canvas image and one fits channel            
            self.image_viewer.load_image(self.pil_image)
            self.current_project.save_image(self.pil_image)
            

    def close_current_project(self):
        """Close and cleanup current project"""
        try:
            # Clear image viewer
            if hasattr(self, 'image_viewer'):
                self.image_viewer.load_image(None)
            
            # Clear stored FITS files
            if hasattr(self, 'current_fit_files'):
                delattr(self, 'current_fit_files')
                
            # Clear current image reference
            if hasattr(self, 'current_image'):
                delattr(self, 'current_image')
                
            return True
        except Exception as e:
            tk.messagebox.showerror(
                "Error Closing Project",
                f"Failed to close project: {str(e)}"
            )
            return False

    # New Project 
    def new_project(self):
        """Create a new empty project"""
        # Ask for confirmation if there's a current project
        if hasattr(self, 'current_project'):
            if tk.messagebox.askyesno(
                "New Project",
                "Do you want to close the current project and create a new one?"
            ):
                if not self.close_current_project():
                    return
            else:
                return
                
        try:
            # Create new project with default settings
            self.current_project = Project.create_new()
            self.image_viewer.clear()


            # Reset UI controls to default values
            self.zscale_contrast.set(self.current_project.settings['zscale_contrast'])
            self.lupton_stretch.set(self.current_project.settings['lupton_stretch'])
            self.lupton_Q.set(self.current_project.settings['lupton_Q'])
            self.lupton_minimum.set(self.current_project.settings['lupton_minimum'])
            


            # Update window title
            self.update_window_title()
            
        except Exception as e:
            tk.messagebox.showerror(
                "Error Creating New Project",
                f"Failed to create new project: {str(e)}"
            )

            
    # Save Project As
    def save_project_as(self):
        filename = tk.filedialog.asksaveasfilename(
            defaultextension=".aip",
            filetypes=[
                ("Astro Image Project", "*.aip"),
                ("All Files", "*.*")
            ]
        )
        
        if filename:
            try:
                # Update project settings
                self.current_project.settings.update({
                    'zscale_contrast': self.zscale_contrast.get(),
                    'lupton_stretch': self.lupton_stretch.get(),
                    'lupton_Q': self.lupton_Q.get(),
                    'lupton_minimum': self.lupton_minimum.get(),
                })
                
                # Store FITS file data
                if hasattr(self, 'current_fit_files'):
                    for channel, filepath in self.current_fit_files.items():
                        self.current_project.save_fits_file(channel, filepath)
                
                # Update the image 
                self.update_project_settings_and_image()
                
                # Save project file
                self.current_project.name = os.path.splitext(os.path.basename(filename))[0]
                self.current_project.save(filename)
                self.current_project_path = filename
                self.update_window_title()
                
            except Exception as e:
                tk.messagebox.showerror(
                    "Error Saving Project",
                    f"Failed to save project: {str(e)}"
                )


    # Save Project
    def save_project(self):
        if hasattr(self, 'current_project_path') and self.current_project_path:
            self.update_project_settings_and_image()
            self.current_project.save(self.current_project_path)
        else:
            self.save_project_as()

    def export_image(self):
        image = self.current_project.get_image()
        if image:
            filename = tk.filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image", "*png"), ("JPEG Image", "*.jpg"), ("All Files","*.*")]

            )
            if filename:
                image.save(filename)
        else:
            tk.messagebox.showerror("Export Error", "No image to export.")

    
    # Update image parameters 
    def update_project_settings_and_image(self):
        # Update project settings from current UI values
        self.current_project.settings.update({
            'zscale_contrast': self.zscale_contrast.get(),
            'lupton_stretch': self.lupton_stretch.get(),
            'lupton_Q': self.lupton_Q.get(),
            'lupton_minimum': self.lupton_minimum.get()
        })

        # Process image and save it 
        pil_image = process_fits_binaries(

            self.current_project.fit_binaries,
            zscale_contrast=self.zscale_contrast.get(),
            lupton_stretch=self.lupton_stretch.get(),
            lupton_Q=self.lupton_Q.get(),
            lupton_minimum=self.lupton_minimum.get(),
        )

        self.current_project.save_image(pil_image)


    # Load project 
    def load_project(self):
        """Load an existing .aip project file"""
        filename = tk.filedialog.askopenfilename(
            defaultextension=".aip",
            filetypes=[
                ("Astro Image Project", "*.aip"),
                ("All Files", "*.*")
            ]
        )

        if filename:
            try:
                # Load Project 
                self.current_project = Project.load(filename)
                self.current_project_path = filename # Set the current file path to enable saving
                self.update_window_title()
        
                # Update UI with saved parameter values 
                self.zscale_contrast.set(self.current_project.settings['zscale_contrast'])
                self.lupton_stretch.set(self.current_project.settings['lupton_stretch'])
                self.lupton_Q.set(self.current_project.settings['lupton_Q'])
                self.lupton_minimum.set(self.current_project.settings['lupton_minimum'])

                
                
                
                # Display saved image if available
                saved_image = self.current_project.get_processed_image()
                if saved_image:
                    self.image_viewer.load_image(saved_image)
 
                self.update_image_processing()
            
            except Exception as e:
                tk.messagebox.showerror(
                    "Error Loading Project",
                    f"Failed to load project: {str(e)}"
                )

    def update_window_title(self):
        """Update window title with project name"""
        self.root.title(f"Astro Image Processor - {self.current_project.name}")

    # Function to open the fits file upload
    def show_fits_upload(self):
        dialog = FitsUploadModal(self.root)
        dialog.grab_set()  # Make dialog modal
        self.root.wait_window(dialog)  # Wait for dialog to close
        #self.fits_header = dialog.getHeader()
        # The above is a blocking command meaning the code come back here once it is closed
        # The modal returns the fits files when "Build Image is clicked "

        # Get the files selected in the dialog
        if hasattr(dialog, 'fit_files'):
            self.process_fit_files(dialog.fit_files)

    # Function to process fits files 
    # Steps are Load them -> Process the data -> Create the RGB Image -> Display on canvas
    def process_fit_files(self, fit_files):
        if all(fit_files.values()):  # Check if all channels have files
            try:
                
                # Save FITS binaries to project 
                for channel, filepath in fit_files.items():
                    self.current_project.save_fits_file(channel, filepath)
                
                # Update image using new binaries 
                self.update_image_processing()
                
                
            except Exception as e:
                print(f"Error processing FITS files: {e}")
