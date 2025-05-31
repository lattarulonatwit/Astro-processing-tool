import tkinter as tk


# Class that creates Main window 
class MainWindow:

    #function to intialize the window 
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x800")
        self.root.title("Astro Image Processor")
        
        #Call to create each UI element
        self.setup_menu_items()
        self.create_canvas()
        self.setup_sidebar()

    # UI Elements are created via the functions below
    def setup_menu_items(self):
        # Create menu bar
        menu_bar = tk.Menu(self.root)
        
        # Define menu items with categories and commands
        menu_data = {
            "File": [
                ("New", lambda: print("New clicked")),
                ("Open", lambda: print("Open clicked")),
                ("Save Project", lambda: print("Save Project clicked"))
            ],
            "Export": [
                ("Export Image", lambda: print("Export Image clicked")),
            ],
            "Upload": [
                ("Upload Fits", lambda: print("Upload Fits clicked"))
            ]
        }

        # Create menu items (no dropdowns just yet)
        for category, items in menu_data.items():
            for label, command in items:
                menu_bar.add_command(label=label, command=command)
            
        # Attach menu bar to root window
        self.root.config(menu=menu_bar)

    def create_canvas(self):
        # Placeholder for canvas creation code
        pass

    def setup_sidebar(self):
        # Placeholder for sidebar setup
        pass
