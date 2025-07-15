import tkinter as tk
from PIL import Image, ImageTk

class ZoomableImageViewer(tk.Frame):
    """A custom frame that provides zoomable and pannable image viewing"""
    
    def __init__(self, master):
        super().__init__(master)
        
        # Create canvas for image display
        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize state variables
        self.zoom_level = 1.0
        self.image = None
        self.display_image = None
        self.image_id = None

        # Bind mouse events
        self.canvas.bind("<Configure>", self.center_image)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan)

    def load_image(self, image):
        """Load a PIL Image into the viewer"""
        self.image = image
        self.fit_to_canvas()

    def update_display(self):
        """Update the displayed image with current zoom level"""
        if not self.image:
            return

        # Calculate new size
        new_width = int(self.image.width * self.zoom_level)
        new_height = int(self.image.height * self.zoom_level)
        
        # Use faster resize for larger images 
        if new_width * new_height > 2000 * 2000:
            resample_method = Image.NEAREST
        else:
            resample_method = Image.LANCZOS


        # Resize image
        resized = self.image.resize((new_width, new_height), resample_method)
        self.display_image = ImageTk.PhotoImage(resized)

        # Update or create image on canvas
        if self.image_id:
            self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            image=self.display_image,
            anchor="center"
        )
    
    def fit_to_canvas(self):
        """Zoom out so entire image fits in canvas"""
        if not self.image:
            return
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width < 1 or canvas_height < 1:
            # Canvas not initalized yet
            self.after(10, self.fit_to_canvas)
        
        scale_w = canvas_width /self.image.width
        scale_h = canvas_height / self.image.height
        self.zoom_level = min(scale_w, scale_h, 1.0)
        self.update_display()
        self.center_image()

    def center_image(self, event=None):
        """Center the image in the canvas"""
        if self.image_id:
            self.canvas.update_idletasks()
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            self.canvas.coords(
                self.image_id,
                canvas_width // 2,
                canvas_height // 2
            )

    def zoom(self, event):
        """Handle mouse wheel zoom events"""
        if not self.image:
            return

        # Calculate zoom direction
        if event.delta > 0:
            self.zoom_level *= 1.3
        else:
            self.zoom_level /= 1.3

        # Limit zoom range
        self.zoom_level = min(max(0.1, self.zoom_level), 2.5)
        
        # Update display
        self.update_display()

    def start_pan(self, event):
        """Start panning the image"""
        self.canvas.scan_mark(event.x, event.y)

    def pan(self, event):
        """Pan the image"""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def clear(self):
        """Clear canvas and reset the zoom"""
        self.image = None
        self.display_image = None
        if self.image_id:
            self.canvas.delete(self.image_id)
            self.image_id = None

        self.zoom_level = 1.0
