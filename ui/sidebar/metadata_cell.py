# Class to represent the UI widgets for the metadata cell  
import tkinter as tk
class MetadataCell(tk.Frame):
     def __init__(self, parent, on_starID):
        super().__init__(parent)
        self.on_starID = on_starID
        starID_button = tk.Button(
            self,
            text="Identify Stars",
            command=self.on_starID
        )
        starID_button.pack(pady=10)