import tkinter as tk
import tkinter.font as TkFont
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
from imageManager import load_image, save_image
from registration import register, rgb2gray

figsize = (3,3)
master_image = None
slave_image = None
output_image = None


def selectMaster():
  path = filedialog.askopenfilename(initialdir = "/",title = "Select master")
  global  master_image
  master_image = load_image(path)
  ax = master_fig.axes[0]
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)

  if gray_scale_val.get():
    ax.imshow(rgb2gray(master_image), cmap = 'gray')
  else:
    ax.imshow(master_image)
  
  if grid_val.get():
    ax.get_xaxis().set_visible(True)
    ax.get_yaxis().set_visible(True)
    ax.grid(color='r', linewidth=2)

  master_canvas.draw()

  return master_image

def selectSlave():
  path = filedialog.askopenfilename(initialdir = "/",title = "Select master")
  global slave_image 
  slave_image = load_image(path)
  ax = slave_fig.axes[0]
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)

  if gray_scale_val.get():
    ax.imshow(rgb2gray(slave_image), cmap = 'gray')
  else:
    ax.imshow(slave_image)

  if grid_val.get():
    ax.get_xaxis().set_visible(True)
    ax.get_yaxis().set_visible(True)
    ax.grid(color='r', linewidth=2)

  slave_canvas.draw()


def registerImage():
  ax = out_fig.axes[0]
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)
  
  global output_image 
  output_image = register(master_image, slave_image, registration_type = warp_type.get())

  t = np.arange(0, 3, .01)

  if gray_scale_val.get():
    ax.imshow(rgb2gray(output_image), cmap = 'gray')
    output_image = rgb2gray(output_image)
  else:
    ax.imshow(output_image)

  if grid_val.get():
    ax.get_xaxis().set_visible(True)
    ax.get_yaxis().set_visible(True)
    ax.grid(color='r', linewidth=2)
  

  out_canvas.draw()


def saveResult():
  save_image(output_image, format_type.get())

root = tk.Tk()
root.title("Images Registration Tool")
root.geometry("930x430")
root.resizable(False, False)
helv36 = TkFont.Font(root, family="Helvetica",size=20)#,weight="bold")



setting_frame = tk.Frame(root)
setting_frame.pack(side=tk.TOP)

warp_type = tk.StringVar()
warp_affine = tk.Radiobutton(setting_frame, text="Warp affine", variable=warp_type, value='warp_affine', font=helv36)
warp_affine.grid(row=1, column=1, sticky=tk.W)
warp_perspective = tk.Radiobutton(setting_frame, text="Warp perspective", variable=warp_type, value='warp_perspective', font=helv36)
warp_perspective.grid(row=2, column=1, sticky=tk.W)

grid_val = tk.BooleanVar()
grid_plot = tk.Checkbutton(setting_frame, text="Grid", variable=grid_val, font=helv36)
grid_plot.grid(row=1, column=2, sticky=tk.W)

gray_scale_val = tk.BooleanVar()
gray_scale = tk.Checkbutton(setting_frame, text="Grayscale", variable=gray_scale_val, font=helv36)
gray_scale.grid(row=2, column=2, sticky=tk.W)

format_type = tk.StringVar()
format_png = tk.Radiobutton(setting_frame, text="PNG", variable=format_type, value='png', font=helv36)
format_png.grid(row=1, column=3, sticky=tk.W)
format_tif = tk.Radiobutton(setting_frame, text="TIF", variable=format_type, value='tif', font=helv36)
format_tif.grid(row=2, column=3, sticky=tk.W)


images_frame = tk.Frame(root)
images_frame.pack(side=tk.TOP)

#-------------------------------- MASTER IMAGE --------------------------------
master_frame = tk.Frame(images_frame)
master_frame.grid(row=1, column=1, sticky=tk.W)
master_fig = Figure(figsize=figsize, dpi=100)
master_fig.add_subplot(111)
master_fig.subplots_adjust(left=0.03, bottom=0.07, right=0.98, top=0.97, wspace=0, hspace=0)
ax = master_fig.axes[0]
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
master_canvas = FigureCanvasTkAgg(master_fig, master=master_frame)  # A tk.DrawingArea.
master_canvas.get_tk_widget().grid(row=2, column=1, sticky=tk.W)
select_master = tk.Button(master_frame, text='SELECT MASTER', height=1, width=20, font=helv36, command = selectMaster)
select_master.grid(row=3, column=1)

#--------------------------------- SLAVE IMAGE --------------------------------
slave_frame = tk.Frame(images_frame)
slave_frame.grid(row=1, column=2, sticky=tk.W)
slave_fig = Figure(figsize=figsize, dpi=100)
slave_fig.add_subplot(111)
slave_fig.subplots_adjust(left=0.03, bottom=0.07, right=0.98, top=0.97, wspace=0, hspace=0)
ax = slave_fig.axes[0]
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
slave_canvas = FigureCanvasTkAgg(slave_fig, master=slave_frame)  # A tk.DrawingArea.
slave_canvas.get_tk_widget().grid(row=2, column=2, sticky=tk.W)
select_slave = tk.Button(slave_frame, text='SELECT SLAVE', height=1, width=20, font=helv36, command = selectSlave)
select_slave.grid(row=3, column=2, sticky=tk.W, padx=30)


#---------------------------------- OUT IMAGE ----------------------------------
out_frame = tk.Frame(images_frame)
out_frame.grid(row=1, column=3, sticky=tk.W)
out_fig = Figure(figsize=figsize, dpi=100)
out_fig.add_subplot(111)
out_fig.subplots_adjust(left=0.03, bottom=0.07, right=0.98, top=0.97, wspace=0, hspace=0)
ax = out_fig.axes[0]
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
out_canvas = FigureCanvasTkAgg(out_fig, master=out_frame)  # A tk.DrawingArea.
out_canvas.get_tk_widget().grid(row=2, column=3, sticky=tk.W)
register_btn = tk.Button(out_frame, text='REGISTER', height=1, width=20, font=helv36, command = registerImage)
register_btn.grid(row=3, column=3, sticky=tk.W, padx=30)

save_frame = tk.Frame(root)
save_frame.pack(side=tk.TOP)

save = tk.Button(save_frame, text='SAVE', height=1, width=20, font=helv36, command = saveResult)
save.grid(row=1, column=1, sticky=tk.W)


root.mainloop()