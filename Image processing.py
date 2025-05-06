import tkinter as tk
from tkinter import filedialog
from tkinter import *
import customtkinter
from PIL import Image, ImageOps, ImageTk, ImageFilter 
from astropy.io import fits
from astropy.visualization import make_lupton_rgb
from astropy.visualization import make_rgb, ManualInterval
from astropy.visualization import SqrtStretch
import numpy as np

root = tk.Tk()
root.geometry("1400x800")
root.title("Astro processing tool")
root.config(bg="white")

pen_color = "black"
pen_size = 5
file_path = ""
   
R,G,B = np.zeros((1528, 1528)), np.empty((1528, 1528)), np.empty((1528, 1528)) #size of the image

def add_channel(color):
    filepath = filedialog.askopenfilename(initialdir="C:/Users/floresj12/Documents/SpacePhotoshop/Astro-processing-tool")
    if filepath:  # Check if a file was selected
        channel = fits.getdata(filepath)
        update_size = channel.shape
        print(update_size)
        #color.resize(update_size)
        color[:] = channel  # Append the channel to the respective list

# Process the images once they are loaded
def process_images():
    rgb_default = make_lupton_rgb(R,G,B, minimum = minimum.get(), stretch=stretch.get(), Q =Q.get(), filename="ngc6976-fart.jpeg")
    disp = Image.open("C:/Users/floresj12/Documents/SpacePhotoshop/ngc6976-fart.jpeg")
    width, height = int(disp.width /2), int(disp.height /2)
    disp = disp.resize((width, height))
    canvas.config(width = disp.width, height = disp.height)
    disp = ImageTk.PhotoImage(disp)
    canvas.image = disp
    canvas.create_image(0,0, image = disp, anchor="nw")

def stretch_slider(amount):
    stretch_label.configure(text=int(amount))
def min_slider(amount):
   min_label.configure(text=int(amount))  
def Q_slider(amount):
   Q_label.configure(text=int(amount))   
    
#TKinter frame setting 
    #add the left processing bar to the root frame
left = tk.Frame(root, width = 200, height = 600, bg = "white")
left.pack(side = "left", fill = "y")
    #add the canvas for the image
canvas = tk.Canvas(root, width = 750, height = 600)
canvas.pack()
    #add the buttons to upload each image
upload_R = tk.Button(left, text = "upload red image", command=lambda: add_channel(R), bg = "white")
upload_R.pack(padx = 20, pady=10)
upload_G = tk.Button(left, text = "upload green image", command=lambda: add_channel(G), bg = "white")
upload_G.pack(padx = 20, pady=10)
upload_B = tk.Button(left, text = "upload blue image",command=lambda: add_channel(B), bg = "white")
upload_B.pack(padx = 20, pady=10)

    #label to mark stretch adjuster
stretch_title = customtkinter.CTkLabel(left, text="Stretch", font = ("Helvetica", 14), text_color="black")
stretch_title.pack(pady=25)
    #stretch slider
stretch = customtkinter.CTkSlider(left, from_=100, to=15000, command = stretch_slider)
stretch.pack(pady=5)
    #label for stretch value
stretch_label = customtkinter.CTkLabel(left, text="", font = ("Helvetica", 14), text_color="black")
stretch_label.pack()


    #label to mark min adjuster
min_title = customtkinter.CTkLabel(left, text="Minimum", font = ("Helvetica", 14), text_color="black")
min_title.pack(pady=5)
    #min slider
minimum = customtkinter.CTkSlider(left, from_=10, to=500, command = min_slider)
minimum.pack(pady=5)
    #label for min value
min_label = customtkinter.CTkLabel(left, text="", font = ("Helvetica", 14), text_color="black")
min_label.pack()

    #label to mark Q adjuster
Q_title = customtkinter.CTkLabel(left, text="Q", font = ("Helvetica", 14), text_color="black")
Q_title.pack(pady=5)
    #Q slider
Q = customtkinter.CTkSlider(left, from_=1, to=50, command = Q_slider)
Q.pack(pady=5)
    #label for Q value
Q_label = customtkinter.CTkLabel(left, text="", font = ("Helvetica", 14), text_color="black")
Q_label.pack()

    #apply button
process_btn = tk.Button(left, text="apply", command=process_images, bg="white")
process_btn.pack(padx=20, pady=35)

root.mainloop()
