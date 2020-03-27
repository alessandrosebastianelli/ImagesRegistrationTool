import tkinter as tk
import tkinter.font as TkFont
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np


master_image = None
slave_image = None
output_image = None


def selectMaster():
  path = filedialog.askopenfilename(initialdir = "/",title = "Select master")
  ax = master_fig.axes[0]
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)

  t = np.arange(0, 3, .01)
  ax.plot(t, 2 * np.sin(2 * np.pi * t))
  master_canvas.draw()
  
  print(path)

def selectSlave():
  path = filedialog.askopenfilename(initialdir = "/",title = "Select master")
  ax = slave_fig.axes[0]
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)

  t = np.arange(0, 3, .01)
  ax.plot(t, 2 * np.sin(2 * np.pi * t))
  slave_canvas.draw()
  
  print(path)


root = tk.Tk()
root.geometry("900x600")
root.resizable(False, False)
helv36 = TkFont.Font(root, family="Helvetica",size=20)#,weight="bold")


setting_frame = tk.Frame(root)
setting_frame.pack(side=tk.TOP)

warp_type = tk.StringVar()
warp_type = 'warp_affine'
warp_affine = tk.Radiobutton(setting_frame, text="Warp affine", variable=warp_type, value='warp_affine', font=helv36)
warp_affine.grid(row=1, column=1, sticky=tk.W)
warp_perspective = tk.Radiobutton(setting_frame, text="Warp perspective", variable=warp_type, value='warp_perspective', font=helv36)
warp_perspective.grid(row=2, column=1, sticky=tk.W)

grid_val = tk.BooleanVar()
grid_plot = tk.Checkbutton(setting_frame, text="Grid", variable=grid_val, font=helv36)
grid_plot.grid(row=1, column=2, sticky=tk.W)

gray_scale_val = tk.BooleanVar()
gray_scale = tk.Checkbutton(setting_frame, text="Gray Scale", variable=gray_scale_val, font=helv36)
gray_scale.grid(row=2, column=2, sticky=tk.W)

format_type = tk.StringVar()
format_type = 'tif'
format_png = tk.Radiobutton(setting_frame, text="PNG", variable=format_type, value='png', font=helv36)
format_png.grid(row=1, column=3, sticky=tk.W)
format_tif = tk.Radiobutton(setting_frame, text="TIF", variable=format_type, value='tif', font=helv36)
format_tif.grid(row=2, column=3, sticky=tk.W)


images_frame = tk.Frame(root)
images_frame.pack(side=tk.TOP)

#-------------------------------- MASTER IMAGE --------------------------------
master_frame = tk.Frame(images_frame)
master_frame.grid(row=1, column=1, sticky=tk.W)
master_fig = Figure(figsize=(3, 3), dpi=100)
master_fig.add_subplot(111)
master_canvas = FigureCanvasTkAgg(master_fig, master=master_frame)  # A tk.DrawingArea.
master_canvas.get_tk_widget().grid(row=2, column=1)
select_master = tk.Button(master_frame, text='SELECT MASTER', height=1, width=20, font=helv36, command = selectMaster)
select_master.grid(row=3, column=1)

#--------------------------------- SLAVE IMAGE --------------------------------
slave_frame = tk.Frame(images_frame)
slave_frame.grid(row=1, column=2, sticky=tk.W)
slave_fig = Figure(figsize=(3, 3), dpi=100)
slave_fig.add_subplot(111)
slave_canvas = FigureCanvasTkAgg(slave_fig, master=slave_frame)  # A tk.DrawingArea.
slave_canvas.get_tk_widget().grid(row=2, column=2)
select_slave = tk.Button(slave_frame, text='SELECT SLAVE', height=1, width=20, font=helv36, command = selectSlave)
select_slave.grid(row=3, column=2, sticky=tk.W)

#---------------------------------- OUT IMAGE ----------------------------------
out_frame = tk.Frame(images_frame)
out_frame.grid(row=1, column=3, sticky=tk.W)
out_fig = Figure(figsize=(3, 3), dpi=100)
out_fig.add_subplot(111)
out_canvas = FigureCanvasTkAgg(out_fig, master=out_frame)  # A tk.DrawingArea.
out_canvas.get_tk_widget().grid(row=2, column=3)
register = tk.Button(out_frame, text='REGISTER', height=1, width=20, font=helv36)
register.grid(row=3, column=3, sticky=tk.W)

save_frame = tk.Frame(root)
save_frame.pack(side=tk.TOP)

save = tk.Button(save_frame, text='SAVE', height=1, width=20, font=helv36)
save.grid(row=1, column=1, sticky=tk.W)


root.mainloop()