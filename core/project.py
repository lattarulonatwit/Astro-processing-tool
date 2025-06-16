from dataclasses import dataclass
from typing import Dict, Optional
import json 
import os 
from datetime import datetime

@dataclass 
class Project:
    """Represents an image processing project"""
    # str is a built in type that represents string data types
    name: str
    created_date: str
    fit_files: Dict[str, Optional[str]] # RGB channel paths
    settings: Dict[str, float] # Processing parameters


    @classmethod
    def create_new(cls, name: str="Untitled Project"):
        # Create a new empty project
        # cls refers to the class itself not an instance of the class
        return cls(
            name=name,
            created_date=datetime.now().isoformat(),
            fit_files={'R': None, 'G': None, 'B': None},
            settings={
                'zscale_contrast': 0.25,
                'stretch_a': 0.1,
                'stretch_factor': 3.0
            }
        )



    def save(self, directory: str):
        """Save project as .aip file (JSON format with custom extensions)"""
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Use custom aip extension
        filepath = os.path.join(directory, f"{self.name}.aip")

        # Save as JSON format internally 
        with open(filepath, 'w') as f:
            json.dump({
                'name': self.name,
                'created_date': self.created_date,
                'fit_files': self.fit_files,
                'settings': self.settings}
                , f, indent=4)


    @classmethod
    def load(cls, filepath:str):
        """Load . aip project file"""
        try:
            if not filepath.endswith('.aip'):
                raise ValueError("File must have .aip extension")
            
            with open(filepath, 'r') as f:
                data= json.load(f)

            # Ensure required fields of json exist (save file is not malformed)
            required_fields = ['name', 'created_date','fit_files', 'settings']
            if not all(field in data for field in required_fields):
                raise ValueError("Invalid project file: missing required fields")
            
            return cls(
                name=data['name'],
                created_date=data['created_date'],
                fit_files=data['fit_files'],
                settings=data['settings']
            )
        except json.JSONDecodeError:
            raise ValueError("Invalid project file: not a valid JSON format")
        except Exception as e:
            raise ValueError(f"Failed to load project: {str(e)}")
    
   
    
    def update_name(self, new_name: str):
        """Update project name and return True if successful"""
        if new_name:
            self.name = new_name
            return True
        return False