import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


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


        self.preview_frame = None
        self.validation_label = None

    def setup_modal_ui(self):
        # Create file selection buttons
        # Create preview area
        # Create validation
        # Create build image button
        pass

    def select_fits_file(self, channel):
        # Open windows file dialog 
        # Store selected file 
        # Update preview
        pass
    def validate_files(self):
        # Check if all files selected
        # Validate FITS format
        # Check dimensions match
        pass

    def build_image(self):
        # Ensure validation passes 
        # Return selected files 
        # Close modal 
        pass
    def cancel(self):
        # Clear selections
        # Close modal 
        pass