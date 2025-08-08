# Astro Image Processor

## Project Overview

**Astro Image Processor** is a python application designed for amateur astronomers and astrophotographers to process, analyze, and visualize astronomical images from FITS files they create or find online. It provides tools for combining RGB channels, adjusting image parameters, detecting stars, overlaying scientific metadata, and exporting processed images.  Our goal was to create a citizen science app to allow users to create pretty images as well as learn from said images.

---

## Purpose

To streamline the workflow of astronomical image processing, making scientific analysis accessible and interactive through a user-friendly desktop interface.

---

## Design & Implementation

### 1. User Interface (UI)

- **Framework**: 
  - Built with `tkinter` for the main GUI
  - Enhanced using `customtkinter` widgets

- **Main Components**:
  - **Main Window** (`main_window.py`): Manages canvas, sidebar, menus, and project state
  - **Sidebar**:
    - **Image Controls**: Sliders for ZScale contrast, Lupton stretch, Q, and minimum values
    - **Metadata Cell**: Star/object detection controls and metadata display
  - **Canvas**: Custom `ZoomableImageViewer` for pan/zoom image display
  - **FITS Upload Modal**: Dialog for selecting and validating FITS files for R, G, B channels

### 2. Image Processing

- **FITS Handling**:
  - Reads FITS files
  - Extracts image data
  - Combines RGB channels using the Lupton algorithm (`image_processing.py`)

- **Parameter Adjustment**:
  - Real-time sliders for contrast, stretch, and brightness

- **Exporting**:
  - Save final processed image as PNG or JPEG

### 3. Scientific Analysis

- **Star Detection**:
  - Uses `photutils` to detect and mark stars
  - Highlights the brightest stars with circles

- **Object Identification**:
  - Uses `astroquery` to query SIMBAD for nearby astronomical objects
  - Overlays object names/positions on the image

- **Metadata Extraction**:
  - Extracts FITS header info (e.g., exposure time, focal length, RA/Dec)

### 4. Project Management

- **Project Files**:
  - Saved as `.aip` (JSON format)
  - Includes:
    - Project name & creation date
    - Base64-encoded FITS binaries
    - Image processing parameters
    - PNG binary of processed image

- **Persistence**:
  - Save, load, and export projects and images

### 5. Modularity

- **Code Structure**:
  - `core/`: Image processing, metadata, and project logic
  - `ui/`: Components for sidebar, viewport, dialogs
  - `Resources/`: Requirements and documentation

---

## Key Technologies Used

- **Python** (GUI and backend logic)
- **tkinter** and **customtkinter** (GUI)
- **Astropy** (FITS handling, WCS, visualization)
- **Photutils** (Star detection)
- **Astroquery** (SIMBAD object queries)
- **OpenCV** (Overlay drawing)
- **Pillow** (Image manipulation)
- **NumPy** (Array operations)

---

## Typical Workflow

1. Start a new project or open an existing one
2. Upload FITS files for R, G, B channels
3. Adjust image parameters with sidebar sliders
4. Analyze: Detect stars, identify objects, inspect metadata
5. Export the image or save the project

---

## Getting Started
- **Python 3.10+**
- **Required Packages**:
    - astropy, Pillow, tkinter, customtkinter, numpy, photoutils, open-cv, astroquery 

## Installation
```
pip install astropy Pillow tkinter customtkinter numpy photoutils open-cv astroquery
```

## Running the App
```
python Astro-processing-tool/main.py
```


## Summary

This tool is designed to streamline the workflow of processing astronomical images, making scientific analysis accessible and interactive for users. Its modular structure and use of scientific Python libraries enable robust image processing and metadata extraction, all within an intuitive desktop interface.

## Credits
Developed by Josh and Nico 

Wentworth Insitute of Technology


Class of 2025


Uses open-source scientific Python libraries

