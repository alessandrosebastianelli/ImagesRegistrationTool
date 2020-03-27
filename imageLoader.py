import numpy as np
import matplotlib.pyplot as plt
import rasterio

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
      
  return image 