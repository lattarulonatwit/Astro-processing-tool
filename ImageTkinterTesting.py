import tkinter as tk
from PIL import Image, ImageTk
import os


root = tk.Tk()

root.title("Frame Demo")
root.geometry("1200x800")
root.config(bg="#FF00FF")
#Create a dummy UI that looks like what we are trying to achieve
#in the space photoshop app s

# Lets start by making bar across the top 
# This is gonna be a dictionary of lists of tuples
menu_data = {

    "File": [
        ("New", lambda: print("New clicked")),
        ("Open", lambda: print("Open clicked")),
        ("---", None),  # Separator
        ("Exit", root.quit)
    ],

    "Edit": [

        ("Undo", lambda: print("Undo Clicked")),

    ],

    "Upload Fits": [
        ("Upload RGB Images", lambda: print("Upload Fits clicked")),
        #This will likely open a dialog that will have user enter the 3 images

    ],

    "Save Image": [
        ("Save Image", lambda: print("Save Image clicked")),

    ]
}

menu_bar = tk.Menu(root)

# Loop over the dictionary to create each menu and its items
for menu_name, items in menu_data.items():
    menu = tk.Menu(menu_bar, tearoff=0) #tear off defines if control can be detached into its own floating window 
    for label, command in items:
        if label == "---":
            menu.add_separator()
        else:
            menu.add_command(label=label, command=command)
    menu_bar.add_cascade(label=menu_name, menu=menu)

# Attach menu bar to the root window
root.config(menu=menu_bar)

# #Custom view port class (likely to change)
# class ScrollableViewPort(tk.Frame):
#     def __init__(self, parent, width=400, height=300, **kwargs):
#         super().__init__(parent, **kwargs)

#         canvas = tk.Canvas(self, width=width, height=height, bg="white")
#         scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)

#         self.inner_frame = tk.Frame(canvas)
#         self.inner_frame.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

#         canvas.create_window((0,0), window=self.inner_frame, anchor="nw")
#         canvas.configure (yscrollcommand=scrollbar.set)


#         canvas.pack(side="left", fill="both", expand=True)
#         scrollbar.pack(side="right", fill="y")

#         self.canvas = canvas

#     def add_content(self, widget):
#         widget.pack(in_=self.inner_frame, pady=5)


class ZoomableImageViewer(tk.Frame):
    def __init__(self, master, image_path):
        super().__init__(master)
        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image = Image.open(image_path)
        self.zoom_level = 1.0
        self.display_image = ImageTk.PhotoImage(self.image)
        self.image_id = self.canvas.create_image(0, 0, anchor="center", image=self.display_image)

        self.canvas.bind("<Configure>", self.center_image)  # Recenter on resize
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.do_pan)


    def center_image(self, event=None):
        # Center the image in the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.canvas.coords(self.image_id, canvas_width // 2, canvas_height // 2)

    def start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)
    
    def do_pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoom(self, event):
        if event.delta > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level /= 1.1

        new_size = (
            int(self.image.width * self.zoom_level),
            int(self.image.height * self.zoom_level)
        )
        resized_image = self.image.resize(new_size, Image.LANCZOS)
        self.display_image = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.image_id, image=self.display_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))





#  Main layout container 
# Main layout container
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Viewport on the Left
viewport = tk.Frame(main_frame, bg="lightblue")
viewport.grid(row=0, column=0, rowspan=2, sticky="nsew")

output_dir = "OutputImage"  # This folder is created inside project now
os.makedirs(output_dir, exist_ok=True)  # Make sure it exists

example_file = os.path.join(output_dir, "ngc6976-example.jpeg")

# Place the zoomable image viewer in the viewport
viewer = ZoomableImageViewer(viewport, example_file)
viewer.pack(fill=tk.BOTH, expand=True)
# viewport = ScrollableViewPort(root)
# viewport.pack(padx=10, pady=10)

# Right side cells 
cell1 = tk.Frame(main_frame, bg="lightgray")
cell1.grid(row=0,column=1, sticky="nsew")

cell2 = tk.Frame(main_frame, bg="lightyellow")
cell2.grid(row=1, column=1, sticky="nsew")

# Grid Configuration
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=6) # Fixed width for viewport
main_frame.grid_columnconfigure(1, weight=4) # Exapandable area 



# Try the output of chat jippity for the custom viewport

root.mainloop()