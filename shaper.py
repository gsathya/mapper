import sys
import os

import fiona

from flask import Flask, send_from_directory, request, jsonify
from shapely.geometry import Point, LineString, shape, MultiPolygon, mapping

app = Flask(__name__)
polygons = []

@app.route("/", methods=["GET"])
def main():
    path = os.path.abspath(os.path.dirname( __file__ ))
    return send_from_directory(path, "index.html")

@app.route("/css/<file>", methods=["GET"])
def get_css(file):
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'static' , "css"))
    return send_from_directory(path, file)

@app.route("/static/js/<file>", methods=["GET"])
def get_js(file):
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'static', "js"))
    return send_from_directory(path, file)

@app.route("/location")
def get_locations():
    counties = {}
    counties['type'] = 'FeatureCollection'
    counties['features'] = []

    args = request.args

    try:
        start = Point(float(args.get('start_long')), float(args.get('start_lat')))
        end = Point(float(args.get('end_long')), float(args.get('end_lat')))
    
        line = LineString([start, end])

        for id, n in enumerate(find_counties(line)):
            county = {}
            print n[1]
            county['type'] = 'Feature'
            county['id'] = id
            county['properties'] = {'name': n[1]}
            county['geometry'] = mapping(n[0])
            counties['features'].append(county)

    except Exception, e:
        print "Wrong request %s" % (e)

    return jsonify(counties=counties)

def load(data_dir):
    for file_name in os.listdir(data_dir):
        if not file_name.endswith(".shp"):
            continue

        file_path = os.path.join(data_dir, file_name)
        with fiona.open(file_path, "r") as input:
            for f in input:
                neighborhood = shape(f['geometry'])
                polygons.append((neighborhood, f['properties']['NAME']))

def find_counties(line):
    county = []

    for polygon in polygons:
        if line.intersects(polygon[0]):
            county.append(polygon)

    return county

def usage():
    print "$python shaper.py server /path/to/data"
    print "$python shaper.py /path/to/data lat1 long1 lat2 long2"

if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == "server":
        data_dir = sys.argv[2]
        load(data_dir)
        app.run(debug=True)
    elif len(sys.argv) == 6:
        try:
            data_dir = sys.argv[1]
            load(data_dir)
        
            start = Point(float(sys.argv[2]), float(sys.argv[3]))
            end = Point(float(sys.argv[4]), float(sys.argv[5]))
            line = LineString([start, end])
        except ValueError:
            usage()
            sys.exit()

        for county, name in find_counties(line):
            print name
    else:
        usage()
