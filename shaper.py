import sys
import os

import fiona

from flask import Flask
from shapely.geometry import Point, LineString, shape, MultiPolygon

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

def run(data_dir, line):
    for file_name in os.listdir(data_dir):
        if not file_name.endswith(".shp"):
            continue

        file_path = os.path.join(data_dir, file_name)
        with fiona.open(file_path, "r") as input:
            for f in input:
                neighborhood = shape(f['geometry'])
                if line.intersects(neighborhood):
                    print f['properties']['NAME']

def usage():
    print "$python shaper.py server"
    print "$python shaper.py /path/to/data lat1 long1 lat2 long2"

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "server":
        app.run()
    elif len(sys.argv) == 6:
        data_dir = sys.argv[1]

        try:
            start = Point(float(sys.argv[2]), float(sys.argv[3]))
            end = Point(float(sys.argv[4]), float(sys.argv[5]))
            line = LineString([start, end])
        except ValueError:
            usage()
            sys.exit()

        run(data_dir, line)
    else:
        usage()
