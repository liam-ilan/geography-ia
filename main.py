import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
import thinplate as tps # from https://github.com/cheind/py-thin-plate-spline

# fonts
normalFont = 17
titleFont = 24
axesFont = 22

# get output path
path = 'graph.png' if len(sys.argv) < 2 else sys.argv[1]

# get option for what to label (tags, temperatures, or contours) (-ta, -te, -co)
mode = '-co' if len(sys.argv) < 3 else sys.argv[2]

# get data
coord_raw = open('data/coordinates.csv', 'r').readlines()
temps_raw = open('data/temps.csv', 'r').readlines()

# process temps
processed_temps = [line.replace('\n', '').replace(' ', '').split(',') for line in temps_raw]
processed_temps = {item[0]: float(item[1]) for item in processed_temps}

# set up final data
# structure: [[x, y, temp],...]
data = [line.replace('\n', '').split(',') for line in coord_raw]

# label all points with tags
if mode == '-ta':
  [plt.text(
    float(line[2]), 
    float(line[1]), 
    line[0], 
    horizontalalignment='center', 
    verticalalignment='center', 
    fontsize=normalFont, 
    color='white',
    zorder=100000,
    path_effects=[pe.withStroke(
      linewidth=4, 
      foreground="black"
    )]
  ) for line in data]

# label all points with temperatures
if mode == '-te':
  [plt.text(
    float(line[2]), 
    float(line[1]), 
    processed_temps[line[0]], 
    horizontalalignment='center', 
    verticalalignment='center', 
    fontsize=normalFont, 
    color='white',
    zorder=100000,
    path_effects=[pe.withStroke(
      linewidth=4, 
      foreground="black"
    )]
  ) for line in data]

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

# set plot size
plt.gcf().set_size_inches(16, 10)

# make grid
grid_res = 500
grid = tps.uniform_grid((grid_res, grid_res)) * (
  abs(max_lat - min_lat),
  abs(max_long - min_long)
) + (-abs(min_lat), abs(min_long))

# get predicted temperatures
predicted_temps = tps.TPS.z(grid.reshape((-1,2)), points, spline).reshape(grid_res, grid_res)

# background image
im = plt.imread("back.png")
implot = plt.imshow(im, extent=[min_lat, max_lat, min_long, max_long])

# set up color map
cmap = mpl.colors.LinearSegmentedColormap.from_list('', ['#00e', '#e00'])

# draw contour
if mode == '-co':
  contour = plt.contour(
    grid[...,0], grid[...,1], 
    predicted_temps, 
    [min_temp + i/2 for i in range(2 * (int(max_temp) - int(min_temp)))], 
    cmap=cmap
  )

# plot points
x_points = [[p[0] for p in points]]
y_points = [[p[1] for p in points]]
temp_points = [[p[2] for p in points]]

# scatter points
plt.scatter(x_points, y_points, c=temp_points, marker='o', s=80, edgecolor='black', linewidth=2, cmap=cmap, zorder=1000)

# cbd
plt.text(
  -123.12080249820562, 
  49.28303110427836, 
  'CBD',  
  fontsize=normalFont, 
  horizontalalignment='center', 
  verticalalignment='bottom', 
  zorder=3000000,
  color='#0e0',
  path_effects=[pe.withStroke(
    linewidth=4,
    foreground="black"
  )]
)

plt.plot( 
  -123.12080249820562, 
  49.28203110427836,
  marker='o', 
  markersize=10,
  zorder=3000000,
  color='#0e0',
  path_effects=[pe.withStroke(
    linewidth=4,
    foreground="black"
  )]
)
  
if mode == '-co':
  # label contour lines
  label_levels = list(filter(lambda x: x % 1 == 0, contour.levels))
  clabels = plt.clabel(contour, inline=False, fontsize=normalFont, levels=label_levels, colors='white', zorder=2000)

  # border for labels
  [l.set_path_effects([pe.withStroke(
      linewidth=4, 
      foreground="black"
    )]
  ) for l in clabels]

# color bar
if mode == '-co':
  bar = plt.colorbar(format='%1.1f°C', fraction=0.030, pad=0.04)
  bar.ax.tick_params(labelsize=normalFont)

# axes
axes = plt.gca()
axes.tick_params(labelsize=normalFont)
if mode == '-co':
  axes.set_title('Isotherm Map for Temperature Distribution Across Vancouver', size=titleFont)
elif mode == '-ta':
  axes.set_title('Tags for Data Collection Spots Across Vancouver', size=titleFont)
elif mode == '-te':
  axes.set_title('Tempreatures Collected Across Vancouver', size=titleFont)


axes.set_xlabel('Longitude (°E)', fontsize=axesFont)
axes.set_ylabel('Latitude (°N)', fontsize=axesFont)

# scale axes
plt.gca().set_aspect(1.5)

# arrow
plt.text(
  -123.216, 
  49.283, 
  '➤', 
  c='white', 
  fontsize=60, 
  rotation=90, 
  path_effects=[pe.withStroke(
    linewidth=4, 
    foreground="black"
  )]
)

# save
plt.savefig(path, dpi=300)
