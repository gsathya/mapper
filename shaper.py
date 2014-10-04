import sys

import fiona

from shapely.geometry import Point, LineString

def run():
    start = Point(33.7758, 84.3947)
    end = Point(32.0784, -81.0988)
    line = LineString([start, end])

    print line
    with fiona.open("GA/ZillowNeighborhoods-GA.shp", "r") as input:
        for f in input:
            print f

if __name__ == '__main__':
    run()
