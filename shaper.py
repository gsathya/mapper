import sys

import fiona

from shapely.geometry import Point, LineString, shape, MultiPolygon

def run():
    start = Point(-84.395953, 33.777085)
    end = Point(-84.280820, 33.797427)
    line = LineString([start, end])

    with fiona.open("GA/ZillowNeighborhoods-GA.shp", "r") as input:
        for f in input:
            neighborhood = shape(f['geometry'])
            if line.intersects(neighborhood):
                print f['properties']['NAME']

if __name__ == '__main__':
    run()
