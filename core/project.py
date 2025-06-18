from dataclasses import dataclass
from typing import Dict, Optional
import json
import os
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
from astropy.io import fits


@dataclass
class Project:
    """Represents an image processing project"""
    name: str                            # Project Name 
    created_date: str                    # Creation date 
    fit_files: Dict[str, Optional[str]]  # variable to hold the fit files
    settings: Dict[str, float]           # These are the parameters 
    image_binary: Optional[bytes] = None # Encoded binary image 
    fit_binaries: Dict[str, Optional[bytes]] = None  # Field for binary data if fit files   

    @classmethod
    def create_new(cls):
        # Create a new empty project
        return cls(
            name="Untitled",                              # Default project name
            created_date=datetime.now().isoformat(),      # Set the created date 
            fit_files={'R': None, 'G': None, 'B': None},  # Original file paths
            settings={                                    # Parameter settings (there may be more added and these values are subject to change)
                'zscale_contrast': 0.25,
                'stretch_a': 0.1,
                'stretch_factor': 3.0
            },
            image_binary=None,                              # No image upon starting of a new project
            fit_binaries={'R': None, 'G': None, 'B': None}  # Binary storage of fit files
        )

    def save_fits_file(self, channel: str, filepath: str):
        """Store FITS file binary data"""
        if filepath and os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self.fit_binaries[channel] = f.read()

    def get_fits_data(self, channel: str):
        """Get FITS data from stored binary"""
        if self.fit_binaries.get(channel):
            buffer = BytesIO(self.fit_binaries[channel])
            return fits.open(buffer)[0].data
        return None
    
    def get_processed_image(self) -> Optional[Image.Image]:
        """Convert stored binary data back to PIL Image"""
        if self.image_binary:
            try:
                return Image.open(BytesIO(self.image_binary))
            except Exception as e:
                print(f"Error loading image from binary: {e}")
        return None

    def save(self, filepath: str):
        """Save project with all binary data"""
        # Convert binaries to base64 for JSON storage
        encoded_image = base64.b64encode(self.image_binary).decode('utf-8') if self.image_binary else None
        encoded_fits = {}
        for channel, binary in self.fit_binaries.items():
            encoded_fits[channel] = base64.b64encode(binary).decode('utf-8') if binary else None

        # Dictionary to represent a projects data (includes all fields that a project object has)
        project_data = {
            'name': self.name,
            'created_date': self.created_date,
            'fit_files': self.fit_files,  
            'settings': self.settings,
            'image_binary': encoded_image,
            'fit_binaries': encoded_fits
        }
        
        # Write out the project's data to a json file (our aip file)
        with open(filepath, 'w') as f:
            json.dump(project_data, f)

    @classmethod
    def load(cls, filepath: str):
        """Load project and decode all binary data"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        # Decode base64 data back to binary
        if data.get('image_binary'):
            data['image_binary'] = base64.b64decode(data['image_binary'])
            
        fit_binaries = {}
        for channel, encoded in data.get('fit_binaries', {}).items():
            fit_binaries[channel] = base64.b64decode(encoded) if encoded else None
        data['fit_binaries'] = fit_binaries
        
        # Ensure fit_files exists
        if 'fit_files' not in data:
            data['fit_files'] = {'R': None, 'G': None, 'B': None}
            
        return cls(**data)

    def save_image(self, pil_image: Image.Image):
        """Convert PIL Image to binary and store"""
        if pil_image:
            buffer = BytesIO()
            pil_image.save(buffer, format='PNG')
            self.image_binary = buffer.getvalue()

    def get_image(self) -> Optional[Image.Image]:
        """Get stored binary as PIL Image"""
        if self.image_binary:
            return Image.open(BytesIO(self.image_binary))
        return None

    def update_name(self, new_name: str):
        """Update project name and return True if successful"""
        if new_name:
            self.name = new_name
            return True
        return False