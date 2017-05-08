#!/usr/bin/env python
import numpy as np
def del_verts_outside_image(vertices, regions, ridge_vertices, ResolutionX, ResolutionY, pixel):
    for i in range(len(vertices)-1,-1,-1):
        if (vertices[i,0] < pixel
        or vertices[i,0] > ResolutionX-pixel
        or vertices[i,1] > ResolutionY-pixel
        or vertices[i,1] < pixel):
            for n in range(len(regions)-1,-1,-1):
                if i in regions[n]:
                    del regions[n]
            for p in range(len(ridge_vertices)-1,-1,-1):
                if i in ridge_vertices[p]:
                    del ridge_vertices[p]                        
    return vertices, regions, ridge_vertices

def calculate_regularity(vertices,regions):
    regularity = np.zeros(len(regions))
    distance = np.zeros(6)
    for i in range(len(regions)):
        verts = vertices[regions[i]]
        if len(verts) == 6:
            for n in range(-1,5):
                distance[n] = np.sqrt((verts[n][0]-verts[n+1][0])**2+(verts[n][1]-verts[n+1][1])**2)
            regularity[i] = np.min(distance)/np.max(distance)
            
    return regularity