# The Urban Heat Island Effect in Vancouver
This repo contains the [paper](https://github.com/liam-ilan/geography-ia/blob/master/paper.pdf) and software used to answer the question:
> Does Vancouver, a mid-latitude coastal city, have a defined urban heat island? What factors influence temperature patterns in Vancouver? 

## About
This repo contains my IB Geography Internal Assesment for the May 2023 examanation session. It can be found [here](https://github.com/liam-ilan/geography-ia/blob/master/paper.pdf). A large component of writing the paper involved creating isotherms and other maps. These maps were generated with Python, and can be found under `/graphs`.

## Development
To Regenerate all the maps, run
```
python3 main.py graphs/building.png -bu && python3 main.py graphs/vegetation.png -ve && python3 main.py graphs/isotherm.png -co && python3 main.py graphs/tags.png -ta && python3 main.py graphs/tempratures.png -te && python3 3d.py graphs/3d-full.png -f && python3 3d.py graphs/3d-contour.png -c
```

The temperature, vegetation, and building data the paper is based on can be found under `./data`. The satelite imagery can be found under `back.png` and `back-bright.png`.

`main.py` handles generation of the contour maps. To generate contour maps, run
```
python3 main.py path_to_output.png options
```

where `options` is
1. `-co` for isotherms
2. `-te` for individual temperatures
3. `-ta` for letter tags
4. `-bu` for buildings
5. `-ve` for vegetation

`3d.py` handles generation of the 3d maps. To generate 3d maps, run
```
python3 3d.py path_to_output.png options
```

where `options` is
1. `-f` for filled graphs
2. `-c` for contours

All graphs used in the paper can be found under `./graphs`.

## Credit
- Written by Liam Ilan
- Thanks to Christoph Heindl for his implementation of the Thin Plate Spline algorithim, used in generating contours, found under `/thinplate`. The repo can be found at https://github.com/cheind/py-thin-plate-spline.