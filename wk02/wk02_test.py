# -*- coding: utf-8 -*-
"""
Created on Fri May 30 10:22:49 2025

@author: skrisliu
"""

import rasterio
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import TwoSlopeNorm


DATAMODE = '500m' # 1km or 500m

if DATAMODE=='1km':
    hdf_file_prefire = "MOD13A2.A2024353.h08v05.061.2025003234940.hdf" # compare with 16 days ago
    # hdf_file_prefire = "MOD13A2.A2024017.h08v05.061.2024038041203.hdf"  # compare with 1 year ago
    hdf_file_postfire = "MOD13A2.A2025017.h08v05.061.2025035162811.hdf"
elif DATAMODE=='500m':
    hdf_file_prefire = "MOD13A1.A2024353.h08v05.061.2025003235038.hdf"
    hdf_file_postfire = "MOD13A1.A2025017.h08v05.061.2025035162850.hdf"
else:
    print('ERROR: UNKNOWN DATAMODE')


#%% List layers
print("Available subdatasets:")
for i, sd in enumerate(rasterio.open(hdf_file_prefire).subdatasets):
    print(f"{i}: {sd}")

# notice that the first one is NDVI, normalized dfference vegetation index
# commonly used vegetation index: NDVI, EVI

#%% Load NDVI image data
ndvi_prefire = rasterio.open(hdf_file_prefire).subdatasets[0]
ndvi_postfire = rasterio.open(hdf_file_postfire).subdatasets[0]


im_ndvi_pre = rasterio.open(ndvi_prefire).read(1)
im_ndvi_post = rasterio.open(ndvi_postfire).read(1)


#%% subset data to Los Angeles
if DATAMODE=='1km':
    xmin,xmax = 0, 400
    ymin,ymax = 500, 800
    im_ndvi_pre = im_ndvi_pre[ymin:ymax,xmin:xmax]
    im_ndvi_post = im_ndvi_post[ymin:ymax,xmin:xmax]
elif DATAMODE=='500m':
    xmin,xmax = 200, 800
    ymin,ymax = 1200, 1600
    im_ndvi_pre = im_ndvi_pre[ymin:ymax,xmin:xmax]
    im_ndvi_post = im_ndvi_post[ymin:ymax,xmin:xmax]


#%% plot data
fig = plt.figure(figsize=(17, 8), dpi=200)
gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 0.05], wspace=0.05)

# First subplot (left)
ax1 = fig.add_subplot(gs[0])
im1 = ax1.imshow(im_ndvi_pre, cmap='YlGn', vmin=0, vmax=10000)
ax1.set_title('NDVI (PREFIRE)')
ax1.axis('off')

# Second subplot (middle)
ax2 = fig.add_subplot(gs[1])
im2 = ax2.imshow(im_ndvi_post, cmap='YlGn', vmin=0, vmax=10000)
ax2.set_title('NDVI (POSTFIRE)')
ax2.axis('off')

# Colorbar (right, narrow)
cax = fig.add_subplot(gs[2])
cbar = fig.colorbar(im2, cax=cax)
cbar.set_label('NDVI (scaled by 10000)')

plt.show()



#%% Compute the difference
diff = im_ndvi_post - im_ndvi_pre

# Set symmetric range
vmax = 8000

plt.figure(figsize=(8, 5), dpi=200)
plt.imshow(diff, cmap='RdBu', norm=TwoSlopeNorm(vcenter=0, vmin=-vmax, vmax=vmax))
plt.colorbar(label='NDVI Change (Post - Pre)')
plt.xticks([])
plt.yticks([])
plt.title('NDVI Difference Map')
plt.show()






















