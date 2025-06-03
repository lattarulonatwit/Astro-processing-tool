import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import astropy as ap


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
        )
        
        # If a file was selected, store it
        if filename:
            self.fits_files[channel] = filename
            # Show filename in label
            # TODO: Add label to show selected filename
            print(f"Selected {channel} channel file: {filename}")

        # Update preview (we don't currently have a preview)

    def validate_files(self):
        # Check if all files selected
        # Validate FITS format
        # Check dimensions match
        pass

    def build_image(self):
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