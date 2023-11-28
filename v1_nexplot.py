#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 11:48:49 2023

@author: krishna
"""

import tkinter as tk
from tkinter import filedialog, messagebox
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
        self.create_menu()

        # Initialize plot (this can be adjusted as per your plotting logic)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

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
            # Extract the REF variable
            ref_data = dataset.variables['REF'][0, :, :]  # Assuming 'REF' is the variable name

            # Plot the REF data
            self.plot_data(ref_data)
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

    def plot_data(self, data):
        # Clear existing plot
        self.ax.clear()

        # Set up a map projection (if necessary)
        projection = ccrs.PlateCarree()  # Example projection, adjust as needed
        self.ax = plt.axes(projection=projection)

        # Plot data
        reflectivity = self.ax.imshow(data, origin='lower', cmap='viridis', extent=[-180, 180, -90, 90], transform=projection)

        # Add coastlines
        self.ax.coastlines('10m')
        # Customize gridlines
        gl = self.ax.gridlines(draw_labels=True)
        gl.top_labels = False  # Disable top x-axis labels
        gl.right_labels = False  # Disable right y-axis labels

        # Add a color bar
        cbar = plt.colorbar(reflectivity, ax=self.ax, orientation='vertical', pad=0.05, aspect=50)
        cbar.set_label('Reflectivity (dBZ)')

        # Redraw the canvas
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
