var center = [39.4, -78];

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    osm = L.tileLayer(osmUrl, {maxZoom: 18, attribution: osmAttrib});

map = new L.Map('map', {layers: [osm], center: new L.LatLng(center[0], center[1]), zoom: 7});

var options = {
	duration: 800,
	fps : 32,
	opacityRange: [ 1, 0 ],
	radiusRange: [ 5, 12 ]
};

var pingLayer = L.pingLayer(options).addTo(map);
pingLayer.radiusScale().range([2, 18]);
pingLayer.opacityScale().range([1, 0]);

pingLayer
	.lng(function(d) { return d[0]; })
  .lat(function(d) { return d[1]; });


var latFn = d3.randomNormal(center[0], 1);
var longFn = d3.randomNormal(center[1], 1);

var paused = false;
var update = function(){
    if(!paused) {
    	pingLayer.ping([longFn(), latFn()], (Math.random() > 0.5)? 'red' : 'blue' );
	    window.setTimeout(update, 100 + Math.random()*400);
    }
};
window.setTimeout(update);

function togglePlay() {
    paused = !paused;
    d3.select('button').text((paused)? 'Play' : 'Pause');

    if(!paused) {
        window.setTimeout(update);
    }
}