import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.cbook import get_sample_data
import numpy as np
from PIL import Image, ImageEnhance
import thinplate as tps # from https://github.com/cheind/py-thin-plate-spline

# make bright background
# ImageEnhance.Brightness(Image.open('back.png')).enhance(1.5).save('back-bright.png')

# make figure
fig = plt.figure()
ax = plt.axes(projection='3d', computed_zorder=False)

# fonts
normalFont = 17
titleFont = 24
axesFont = 22

# get output path
path = 'graph.png' if len(sys.argv) < 2 else sys.argv[1]

# get options (-c for contour, -f for full)
option = '-c' if len(sys.argv) < 3 else sys.argv[2]

# get data
coord_raw = open('data/coordinates.csv', 'r').readlines()
temps_raw = open('data/temps.csv', 'r').readlines()

# process temps
processed_temps = [line.replace('\n', '').replace(' ', '').split(',') for line in temps_raw]
processed_temps = {item[0]: float(item[1]) for item in processed_temps}

# set up final data
# structure: [[x, y, temp],...]
data = [line.replace('\n', '').split(',') for line in coord_raw]
data = [[float(line[2]), float(line[1]), processed_temps[line[0]]] for line in data]

# convert to np array
points = np.array(data)

# fit on thin plate spline
spline = tps.TPS.fit(points)

# min and max values
min_lat = min([i[0] for i in data])
max_lat = max([i[0] for i in data])
min_long = min([i[1] for i in data])
max_long = max([i[1] for i in data])
min_temp = min([i[2] for i in data])
max_temp = max([i[2] for i in data])
print(
  'Plotting from (' 
  + str(min_long) 
  + ', ' 
  + str(min_lat) 
  + ') to ('
  + str(max_long) 
  + ', ' 
  + str(max_lat) 
  + ')'
)

# make grid
grid_res = 500
grid = tps.uniform_grid((grid_res,grid_res)) * (abs(max_lat - min_lat), abs(max_long - min_long)) + (-abs(min_lat), abs(min_long))

# get predicted temperature
predicted_temps = tps.TPS.z(grid.reshape((-1,2)), points, spline).reshape(grid_res, grid_res)

# set up color map
cmap = mpl.colors.LinearSegmentedColormap.from_list('', ['#00e', '#e00'])

# graph contour/full
if option == '-c':
  ax.contour3D(
    grid[...,0], 
    grid[...,1], 
    predicted_temps, 
    [min_temp + i/2 for i in range(2 * (int(max_temp) - int(min_temp)))],
    cmap=cmap,
    zorder=20000,
  )
  
elif option == '-f':
  ax.plot_surface(grid[...,0], grid[...,1], predicted_temps, cmap=cmap, zorder=20000)

scatter = ax.scatter([i[0] for i in data], [i[1] for i in data], [i[2] for i in data], c=[i[2] for i in data], cmap=cmap)

# label axes and title
ax.set_xlabel('Longitude (°E)')
ax.set_ylabel('Latitude (°N)')
ax.set_zlabel('Temperature (°C)')
ax.set_title(('3d Isotherm of ' if option == '-c' else '3d Surface of ') + 'Temperatures Across Vancouver')

# background
img = plt.imread("back-bright.png")
y, x = np.mgrid[0:img.shape[0], 0:img.shape[1]]

ax.plot_surface(
  x / img.shape[1] * (max_lat - min_lat) + max_lat - (max_lat - min_lat), 
  -y / img.shape[0] * (max_long - min_long) + min_long + (max_long - min_long),
  (0 * x * y) + np.min(predicted_temps),
  rstride=2, cstride=2, facecolors=img
)

# CBD
ax.plot(
  [-123.12080249820562, -123.12080249820562], 
  [49.28303110427836, 49.28303110427836], 
  [np.min(predicted_temps), np.max(predicted_temps)], 
  zorder=10000,
  color='#0e0'
)

ax.text(
  -123.12080249820562, 
  49.28303110427836, 
  np.max(predicted_temps) + 0.6, 
  'CBD', 
  horizontalalignment='center', 
  verticalalignment='bottom',
  color='#0e0',
  weight='bold',
  path_effects=[pe.withStroke(
    linewidth=2,
    foreground="black"
  )]
)

# color bar
bar = fig.colorbar(mappable=scatter, cmap=cmap, format='%1.1f°C')

# save
plt.savefig(path, dpi=300)