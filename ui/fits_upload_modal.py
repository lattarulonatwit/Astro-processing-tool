import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from astropy.io import fits

import os


# Class to create the dialog for the modal
# Parenthese is how to denote inheritance in Python (looks like a function parameter lol)
class FitsUploadModal(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Upload FITS Files")
        self.geometry("500x400")
        
        # Dictionary to store file paths they are set to None by default
        self.fits_files = {
            'R': None,
            'G': None,
            'B': None
        }

        # Dictionary to store filenames for label
        self.filename_labels = {}

        self.preview_frame = None
        self.validation_label = None
        
        # Call setup_modal_ui to initialize the UI
        self.setup_modal_ui()

    def setup_modal_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=3)  # File selection gets more space
        self.grid_rowconfigure(1, weight=1)  # Button row gets less space

        # Creating frame for file selection buttons
        file_selection_frame = tk.Frame(self)
        file_selection_frame.grid(row=0, column=0, pady=20, sticky="nsew")
        
        # Configure grid columns in file selection frame
        file_selection_frame.grid_columnconfigure(1, weight=1)  # Make filename column expandable
        
        # Create channel rows
        for idx, channel in enumerate(['R', 'G', 'B']):
            tk.Label(file_selection_frame, text=f"{channel} Channel:").grid(
                row=idx, column=0, padx=5, pady=5)
            #These call the select fits file on click 
            tk.Button(file_selection_frame, text="Select File", command=lambda ch=channel: self.select_fits_file(ch)).grid(
                row=idx, column=1, padx=5, pady=5)
            
            # Filename labels 
            self.filename_labels[channel] = tk.Label(file_selection_frame, text="No file selected")
            self.filename_labels[channel].grid(row=idx, column=2, padx=5, pady=5, sticky="w")

        # Add build button in bottom row
        build_button = tk.Button(self, text="Build Image", command=self.build_image)
        build_button.grid(row=1, column=0, pady=20)

        

        # These could be implemented later but are not essential 
        # Create Preview Area
        # Create validation


    def select_fits_file(self, channel):
        # Open file dialog to select FITS file
        filename = filedialog.askopenfilename(
            title=f"Select {channel} Channel FITS File",
            filetypes=[
                ("FITS files", "*.fit"),
                ("FITS files", "*.fits"),
                ("FITS files", "*.fts"),
                ("All files", "*.*")
            ]
            # The above just denotes what kinds of files can be selected in this Dialog
        )
        
        # If a file was selected, store it
        if filename:
            self.fits_files[channel] = filename
            # Show filename in label
            self.filename_labels[channel].config(text=os.path.basename(filename))
            print(f"Selected {channel} channel file: {filename}")

        # Update preview (we don't currently have a preview)

    # This function is called as soon as build button is clicked
    # ******** THIS FUNCTION NEEDS TESTING WITH DIFFERENT FIT FILES*******
    # Tests:
    # Try uploading files that don't correspond to eachother (size mismatch)
    # Try only uploading 2 files
    # 
    def validate_files(self):

        # Check if all files selected

        # loop through channels and check if any of the files are not uploaded (we currently only handle 3)
        missing_channels = [channel for channel, filepath in self.fits_files.items() if filepath is None]


        # Show an error box if any of the channels are empty
        if missing_channels:
            messagebox.showerror(
                "Missing Files",
                f"Please select files for channels: {', '.join(missing_channels)}"
            )
            # Return False for this function if channels are empty
            return False

        # Check if files are .fit files

        # Ideally this should never happen but it's good to check 
        for channel, filepath in self.fits_files.items():
            if not filepath.lower().endswith(('.fit','.fits', '.fts')):
                messagebox.showerror(
                    "Invalid File",
                    f"File for {channel} channel is not a FITS file"
                )
                # Return False if any of the files are not FIT files
                return False

        

        # Check dimensions match
        success, message = self.check_rgb_sized(
            self.fits_files['R'],
            self.fits_files['G'],
            self.fits_files['B']
        )

        # If the sizes do not match return an error screen
        if not success:
            messagebox.showerror("Size Mismatch", message)
            return False

        # TODO Validate FITS format
        # Ask Nico if this is necessary 
        # This is referring to ensuring that this is a valid fits file
        # -that it is not malformed/corrupted/ or missing data 
        
        
        # If no check is tripped then this is true -> the image can be built
        return True

    # Helper function to validate that the dimensions match 
    def check_rgb_sized(self, red_path, green_path, blue_path):
        def get_size(filepath):
            with fits.open(filepath) as hdul:
                header = hdul[0].header
                if header.get('NAXIS', 0) >= 2:
                    return header['NAXIS1'], header['NAXIS2']
                else:
                    return None
        r_size = get_size(red_path)
        g_size = get_size(green_path)
        b_size = get_size(blue_path)

        if None in (r_size, g_size, b_size):
            return False, "One or more files have no valid 2D image data"
        
        if r_size == g_size == b_size:
            return True, f"All Channels match size: {r_size}"
        else:
            return False, f"Size mismatch: Red {r_size}, Green {g_size}, Blue {b_size}"

    def build_image(self):

        # Since validate_files returns bools this is how you would check if true/false
        if not self.validate_files():
            return # Exit if validation fails
    
        # Store selected files before destroying window
        selected_files = self.fits_files.copy()
        
        # Close the modal
        self.destroy()
        
        # Return the selected files
        return selected_files

    def cancel(self):
        # Clear selections
        # Close modal 
        pass