// create a new map
var map = L.map('map').setView([37.8, -96], 4);

// attribute
var osmAttr = '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';

// download those tiles!
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

// all our point data
var points = []

function onMapClick(e) {
    var marker = L.marker(e.latlng).addTo(map);

    // push the co-ords in to our list of points
    points.push(e.latlng);

    points_len = points.length;

    // do we have two points to plot a line?
    if (points_len % 2 === 0){

        // plot a line with the latest two points
        start = points[points_len-1]
        end = points[points_len-2]

        // plot the neighborhoods
        plot_neighborhoods(start, end);
    }
}

function plot_neighborhoods(start, end){
    // create a red polyline from an arrays of LatLng points
    var polyline = L.polyline([start, end], {color: 'red'}).addTo(map);

    // zoom the map to the polyline
    map.fitBounds(polyline.getBounds());

    var data = {
        'start_lat': start.lat,
        'start_long': start.lng,
        'end_lat': end.lat,
        'end_long': end.lng
    }

    // find the locations of neighborhoods
    $.get("/location", data)
        .done(function(data){
            L.geoJson(data['counties']).addTo(map);
        });
}

// set up our map
L.tileLayer(osmUrl, {
    attribution: osmAttr,
    maxZoom: 18
}).addTo(map);

// register on click handlers
map.on('click', onMapClick);
