import numpy as np
import matplotlib.pyplot as plt
import rasterio
from PIL import Image

def load_image(path, normalization='minmax'):
    
  if '.tif' in path:
      
    dataset = rasterio.open(path)
    img = dataset.read()

    image = np.zeros(tuple(reversed(img.shape)))
    
    for i in range(image.shape[len(image.shape)-1]):
      image[..., i] = dataset.read(i+1)
        
    dataset.close()
  else:
    image = plt.imread(path)
      
  if normalization == 'minmax':
    image = (image - image.min())/(image.max() - image.min())
    image = np.clip(image, 0.0, 1.0)
  elif normalization == 'max':
    image = image/image.max()
    image = np.clip(image, 0.0, 1.0)
  elif normalization == 'std':
    image = (image - image.mean())/(image.std())
    image = np.clip(image, 0.0, 1.0)
      
  if img.shape[0] == 1:
    return image[...,0]
  else:
    return image

def save_image(image, t):

  if 'tif' in t:
    dataset = rasterio.open("registered_slave.tif",'w',driver='GTiff',height=image.shape[0],width=image.shape[1],count=image.shape[2],dtype=image.dtype)
    for i in range(image.shape[2]):
      dataset.write(image[...,i], i+1)
    
    dataset.close()
  else:
    im = Image.fromarray((image * 255).astype(np.uint8))
    im.save("registered_slave.png")
