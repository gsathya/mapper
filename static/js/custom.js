var map = L.map('map').setView([51.505, -0.09], 3);
var osmAttr = '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

L.tileLayer(osmUrl, {
    attribution: osmAttr,
    maxZoom: 18
}).addTo(map);

var points = []

function onMapClick(e) {
    var marker = L.marker(e.latlng).addTo(map);
    console.log(e.latlng);
    points.push(e.latlng);

    points_len = points.length;
    if (points_len % 2 === 0){
        start = points[points_len-1]
        end = points[points_len-2]

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
    $.get("/location", data)
        .done(function(data){
            console.log(data['counties']);
            L.geoJson(data['counties']).addTo(map);
        });

}

map.on('click', onMapClick);
