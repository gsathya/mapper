import sys
import os

import fiona

from flask import Flask, send_from_directory
from shapely.geometry import Point, LineString, shape, MultiPolygon

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    path = os.path.abspath(os.path.dirname( __file__ ))
    return send_from_directory(path, "index.html")

@app.route("/css/<file>", methods=["GET"])
def get_css(file):
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'static' , "css"))
    return send_from_directory(path, file)

@app.route("/js/<file>", methods=["GET"])
def get_js(file):
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'static', "js"))
    return send_from_directory(path, file)

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
        app.run(debug=True)
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
