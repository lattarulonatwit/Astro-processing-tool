# Class to represent the UI widgets for the metadata cell  
import tkinter as tk
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