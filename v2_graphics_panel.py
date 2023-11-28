#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 11:48:49 2023

@author: krishna
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox


import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import netCDF4 as nc

import matplotlib as mpl
import pyart
import cartopy.crs as ccrs


class RadarPlotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Radar Plotting Application")
        self.geometry("800x600")  # Set a default window size
        # Initialize variables for graphics options
        self.draw_map = tk.BooleanVar(value=False)
        self.selected_colormap = tk.StringVar(value='viridis')

        self.create_menu()
        self.create_graphics_panel()

        # Initialize plot (without displaying it initially)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        # Canvas widget is now initialized but not yet displayed

        self.radar_data = None  # Variable to store radar data
        self.colorbar = None    # Variable to store the colorbar
       
    def create_graphics_panel(self):
        graphics_panel = tk.Frame(self)
        graphics_panel.pack(side=tk.TOP, fill=tk.X)

        # Radio button to toggle map
        map_toggle = tk.Checkbutton(graphics_panel, text="Draw Map", variable=self.draw_map, command=self.update_plot)
        map_toggle.pack(side=tk.LEFT)

        # Dropdown for colormap selection
        colormap_label = tk.Label(graphics_panel, text="Colormap:")
        colormap_label.pack(side=tk.LEFT)

        colormap_options = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']  # Add more colormaps as needed
        colormap_dropdown = ttk.Combobox(graphics_panel, textvariable=self.selected_colormap, values=colormap_options, state="readonly")
        colormap_dropdown.pack(side=tk.LEFT)
        colormap_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_plot())


    def create_menu(self):
        # Create a menu bar
        menu_bar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save Image", command=self.save_image)
        file_menu.add_command(label="Print", command=self.print_plot)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Graphics menu
        graphics_menu = tk.Menu(menu_bar, tearoff=0)
        graphics_menu.add_command(label="Customize Plot", command=self.customize_plot)
        graphics_menu.add_command(label="Change Colorbar", command=self.change_colorbar)
        graphics_menu.add_command(label="Change Min and Max", command=self.change_min_max)
        menu_bar.add_cascade(label="Graphics", menu=graphics_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="FAQ", command=self.show_faq)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def open_file(self):
        # Open file dialog and get the file path
        file_path = filedialog.askopenfilename(filetypes=[("NetCDF files", "*.nc"), ("Precipitation files", "*")])
        
        if file_path:
            # Check file extension to determine the file type
            _, file_ext = os.path.splitext(file_path)

            if file_ext == '.nc':
                # Handle NetCDF file
                self.read_netcdf_file(file_path)
            else:
                # Handle precipitation file (no extension)
                self.read_precipitation_file(file_path)

    def read_netcdf_file(self, file_path):
        try:
            dataset = nc.Dataset(file_path)
            # Assuming 'REF' is the variable name and storing it in the class attribute
            self.radar_data = dataset.variables['REF'][0, :, :]
            self.plot_data(self.radar_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read NetCDF file: {e}")

    def read_precipitation_file(self, file_path):
        # Read precipitation file and plot
        # This depends on the file format and might require Py-ART or similar
        try:
            # Implement reading and plotting logic here
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read precipitation file: {e}")

    def update_plot(self):
        if self.radar_data is not None:
            self.plot_data(self.radar_data)

        else:
            messagebox.showinfo("Info", "No radar data available to update plot.")


    def plot_data(self, data):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection=ccrs.PlateCarree())  # Use Cartopy for geo-referenced data

        if self.draw_map.get():
            self.ax.coastlines(resolution='10m')

        # Plot data

        reflectivity = self.ax.imshow(data, origin='lower', cmap=self.selected_colormap.get(), extent=[-95.75, -95, 29.5, 30.25])


        if self.colorbar:
            self.colorbar.remove()
        self.colorbar = self.fig.colorbar(reflectivity, ax=self.ax, orientation='vertical', pad=0.05, aspect=50)
        self.colorbar.set_label('Reflectivity (dBZ)')

        self.canvas.draw()
        if not self.canvas_widget.winfo_ismapped():
            self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        # Redraw the canvas
        self.canvas.draw()

        # Add map if the option is selected
        if self.draw_map.get():
            self.ax.coastlines()

        # Plot data with selected colormap
        colormap = self.selected_colormap.get()
        reflectivity = self.ax.imshow(data, origin='lower', cmap=colormap, extent=[-180, 180, -90, 90])  # Adjust as needed

        self.canvas.draw()


    def save_image(self):
        # Logic to save the current plot as an image
        pass

    def print_plot(self):
        # Logic to print the plot
        pass

    def customize_plot(self):
        # Logic to customize the plot
        pass

    def change_colorbar(self):
        # Logic to change the colorbar
        pass

    def change_min_max(self):
        # Logic to change min and max values of the plot
        pass

    def show_help(self):
        messagebox.showinfo("Help", "Help information goes here.")

    def show_faq(self):
        messagebox.showinfo("FAQ", "Frequently Asked Questions.")

    def show_about(self):
        messagebox.showinfo("About", "About this application.")

if __name__ == "__main__":
    app = RadarPlotApp()
    app.mainloop()
