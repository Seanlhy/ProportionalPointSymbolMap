import sys
sys.path.append('/Users/seanlim/Library/Mobile Documents/com~apple~CloudDocs/OSU/AU20/GEOG 5222/gisalgs')
from geom.shapex import *
from geom.centroid import *
from geom.point import *
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch

# source: https://github.com/gisalgs/geom/blob/master/paths.py
def make_path(polygon):
    '''Creates a matplotlib path for a polygon that may have holes.
    
    This function requires to import the following modules
       from matplotlib.path import Path
       from matplotlib.patches import PathPatch

    Input: 
       polygon     [ [ [x,y], [x,y],... ],    # exterior
                     [ [x,y], [x,y],... ],    # first interior ring (optional)
                     [ [x,y], [x,y],... ],   # second interior ring (optional)
                     ... ]                   # there can be more rings (optional)
    Output:
       path: a Path object'''
    
    def _path_codes(n):
        codes = [Path.LINETO for i in range(n)]
        codes[0] = Path.MOVETO
        return codes

    verts = []
    codes = []
    for ring in polygon:
        verts.extend(ring)
        codes += _path_codes(len(ring))
    return Path(verts, codes)

file_loc = '/Users/seanlim/Downloads/cb_2018_us_state_500k/cb_2018_us_state_500k.shp'
shape = shapex(file_loc)

_, ax = plt.subplots()
attributes = []
centroids = []
for x in range(len(shape)):
    coords = shape[x]['geometry']['coordinates']
    polyType = shape[x]['geometry']['type']
    attributes.append(shape[x]['properties']['AWATER']) # gets the quantitative attribute values

    if polyType == 'Polygon':
        path = make_path(coords)
        patch = PathPatch(path,facecolor='#CDCDCD',edgecolor='darkgrey')
        ax.add_patch(patch)
        poly = [Point(p[0],p[1]) for p in coords[0]]
        area, center = centroid(poly)
        centroids.append(center)

    elif polyType == 'MultiPolygon':  # accesses the polygons in the multipolygons each iteration
        for i in range(len(coords)): 
            path = make_path(coords[i])
            patch = PathPatch(path,edgecolor='darkgrey',facecolor='lightgrey')
            ax.add_patch(patch)
        poly = [Point(p[0],p[1]) for p in coords[0][0]]
        area, center = centroid(poly)
        centroids.append(center)

maxAtt = max(attributes)
sizes = [1000*(value/maxAtt)**0.5 for value in attributes]

for i in range(len(shape)):
    ax.scatter([p.x for p in centroids],[p.y for p in centroids], color='lightblue', edgecolor='darkblue',alpha=0.2, marker='o',zorder=2,s=[s for s in sizes])

ax.set_aspect(1)
ax.axis('equal')
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
ax.set_frame_on(False)
plt.title('Proportional Point Symbol Map of the US (Statewide Water Area)',loc='center')
plt.show()