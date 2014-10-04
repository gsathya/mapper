## Neighborhood mapper

Map the neighbourhoods between two given (lat, long) co-ords

## Setup
### OSX

    # download all the data
    * $ python get_shp_files.py
    * $ mkdir data
    * $ cp *.zip data/
    * $ cd data/
    * $ unzip \*.zip
    * $ cd ..
    
    # install and start the app
    * $ brew install gdal
    * $ brew install geos
    * $ pip install cython numpy fiona shapely flask    
    * $ python shaper.py server data

## Easter egg(?)

This also runs as a cli!
