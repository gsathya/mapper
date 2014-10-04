import sys
import os

import fiona

from flask import Flask, send_from_directory, request, jsonify
from shapely.geometry import Point, LineString, shape, MultiPolygon, mapping

app = Flask(__name__)
current_path = os.path.abspath(os.path.dirname(__file__))

# this is list of data we load into memory on startup
polygons = []

@app.route("/")
def main():
    return send_from_directory(current_path, "index.html")

@app.route("/css/<file>")
def get_css(file):
    path = os.path.abspath(os.path.join(current_path, 'static' , "css"))
    return send_from_directory(path, file)

@app.route("/static/js/<file>")
def get_js(file):
    path = os.path.abspath(os.path.join(current_path, 'static', "js"))
    return send_from_directory(path, file)

@app.route("/location")
def get_locations():
    # counties is our GeoJSON
    counties = {}
    counties['type'] = 'FeatureCollection'
    counties['features'] = []

    args = request.args

    try:
        start_long = float(args.get('start_long'))
        start_lat = float(args.get('start_lat'))
        start = Point(start_long, start_lat)

        end_long = float(args.get('end_long'))
        end_lat = float(args.get('end_lat'))
        end = Point(end_long, end_lat)
    
        line = LineString([start, end])

        for id, place in enumerate(find_counties(line)):
            county = {}
            county['type'] = 'Feature'
            county['id'] = id
            county['properties'] = {'name': place[1]}
            county['geometry'] = mapping(place[0])
            counties['features'].append(county)

    except Exception, e:
        print "Wrong request %s" % (e)

    return jsonify(counties=counties)

def load(data_dir):
    for file_name in os.listdir(data_dir):
        if not file_name.endswith(".shp"):
            continue

        file_path = os.path.join(data_dir, file_name)
        with fiona.open(file_path, "r") as input_fh:
            for data in input_fh:
                # get the co-ordinates
                neighborhood = shape(data['geometry'])
                # append the co-ords and the name
                polygons.append((neighborhood, data['properties']['NAME']))

def find_counties(line):
    county = []

    for polygon, name in polygons:
        if line.intersects(polygon):
            county.append((polygon, name))

    return county

def usage():
    print "$python shaper.py server /path/to/data"
    print "$python shaper.py /path/to/data long1 lat1 long2 lat2"

if __name__ == '__main__':
    # use the webapp
    if len(sys.argv) == 3 and sys.argv[1] == "server":
        data_dir = sys.argv[2]
        # load the data
        load(data_dir)

        # start the server
        app.run(debug=True)

    # use this as a cli app
    elif len(sys.argv) == 6:
        try:
            #load the data
            data_dir = sys.argv[1]
            load(data_dir)

            # find our points and create the line
            start = Point(float(sys.argv[2]), float(sys.argv[3]))
            end = Point(float(sys.argv[4]), float(sys.argv[5]))
            line = LineString([start, end])
        except ValueError:
            usage()
            sys.exit()

        for county, name in find_counties(line):
            print name
    # ok, we need to teach the user how to use this
    else:
        usage()
