// create a new map
var map = L.map('map').setView([37.8, -96], 4);

// attribute
var osmAttr = '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';

// download those tiles!
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

// create a control panel to show neighborhood
var info = L.control();

// all our point data
var points = [];

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
            L.geoJson(data['counties'], {onEachFeature: onEachFeature}).addTo(map);
        });
}

function showNeighborhood(e) {
    var layer = e.target;
    info.update(layer.feature.properties);
}

function clearNeighborhood(e) {
    info.update();
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: showNeighborhood,
        mouseout: clearNeighborhood
    });
}

// data info control panel
info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>'+ (props? props.title: 'Hover over a neighborhood') +'</h4>';
};

info.addTo(map);
// set up our map
L.tileLayer(osmUrl, {
    attribution: osmAttr,
    maxZoom: 18
}).addTo(map);

// register on click handlers
map.on('click', onMapClick);
