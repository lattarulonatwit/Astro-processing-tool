# Class to represent the UI widgets for the image control cell 
import tkinter as tk 
class ImageControlsCell(tk.Frame):
    def __init__(self, parent, zscale_contrast, stretch_a, stretch_factor, on_apply):
        super().__init__(parent)
        self.zscale_contrast = zscale_contrast
        self.stretch_a = stretch_a
        self.stretch_factor = stretch_factor
        self.on_apply = on_apply

        for name, var, from_, to, resolution in [
            ("ZScale Contrast", self.zscale_contrast, 0.1, 1.0, 0.05),
            ("Stretch A", self.stretch_a, 0.01, 1.0, 0.01),
            ("Stretch Factor", self.stretch_factor, 0.1, 10.0, 0.1)
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

        apply_button = tk.Button(
            self,
            text="Apply Changes",
            command=self.on_apply
        )
        apply_button.pack(pady=10)