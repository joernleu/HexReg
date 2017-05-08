#!/usr/bin/env python
#Test the regularity analysis
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from skimage.filter import threshold_otsu, threshold_adaptive
from skimage.color import rgb2gray
from skimage import data, util
from skimage.measure import regionprops,label
from scipy import ndimage as ndi
from skimage.morphology import disk, erosion, dilation, \
                                opening, closing, white_tophat, \
                                black_tophat, \
                                convex_hull_image, watershed
from skimage.feature import peak_local_max
from scipy.spatial import Voronoi, voronoi_plot_2d
import src.tifffile as tiff
# my functions
from src.image_info import image_info
from src.calc_regularity import del_verts_outside_image, calculate_regularity




# Import SEM Image tif
SEM_image = r'test_images\UTAM_test_image.TIF'
original_image = tiff.imread(SEM_image)

# Get SEM image information, ResolutionX, ResolutionY, HFW, VFW, PixelWidth, PixelHeight
info = image_info(SEM_image)

# Convert to gray image
image = rgb2gray(original_image)

# Remove infobar from image
image = image[0:info[1], :]
infobar = original_image[info[1]+1: ,: ,:]

# Thresholding
thresh = threshold_otsu(image)
image = image > thresh
# Invert image
image = np.absolute(image - 255)

#Find Centroids
label_img = label(image, connectivity=2)
res = regionprops(label_img, ['Area', 'Centroid'])
centroids = np.array([entry['Centroid'] for entry in res])
centroids = np.delete(centroids, 0, 0)
centroids[:, [0, 1]] = centroids[:, [1, 0]]

# compute Voronoi tesselation
vor = Voronoi(centroids)

# Delete Vertices outside ROI 
pixel = 50
vertices, regions, ridge_vertices = del_verts_outside_image(vor.vertices, vor.regions,vor.ridge_vertices, info[0], info[1], pixel)

#Calculate the regularity
regularity = calculate_regularity(vertices, regions)

#Calculate mean regularity
mean_regularity = np.sum(regularity)/len(regularity)

#Mirror image
vertices[:,1] = np.absolute(vertices[:,1] - np.shape(image)[0] - np.shape(infobar)[0])
original_image = np.flipud(original_image)

my_dpi = 76
fig = plt.figure(figsize=(np.shape(original_image)[1]/my_dpi, np.shape(original_image)[0]/my_dpi), dpi=my_dpi)
im = plt.imshow(original_image,
                interpolation = 'bilinear',
                cmap = cm.gray,
                origin = 'lower',
                extent = [0, np.shape(original_image)[1],
                          0, np.shape(original_image)[0]])

# colorize
colors = cm.jet(np.linspace(0, 1, len(regions)))

i=0
for region in regions:
    polygon = vertices[region]   
    plt.fill(*zip(*polygon), color=colors[int(regularity[i]*len(regions))], alpha=0.5)
    i+=1

for vpair in ridge_vertices:
    if vpair[0] >= 0 and vpair[1] >= 0:
        v0 = vertices[vpair[0]]
        v1 = vertices[vpair[1]]
        # Draw a line from v0 to v1.
        plt.plot([v0[0], v1[0]], [v0[1], v1[1]], 'k', linewidth=1)

plt.plot(centroids[:, 0], np.absolute(centroids[:,1] - np.shape(image)[0] - np.shape(infobar)[0]), 'ko')
plt.xlim(0,np.shape(original_image)[1])
plt.ylim(0,np.shape(original_image)[0])
a=fig.gca()
a.set_frame_on(False)
a.set_xticks([]); a.set_yticks([])
plt.axis('off')
fig.savefig('test_images/Processed_image', transparent=True, bbox_inches='tight', \
                    pad_inches=0)
plt.show()