var center = [38.907192, -77.036873];

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    osm = L.tileLayer(osmUrl, {maxZoom: 18, attribution: osmAttrib});

map = new L.Map('map', {layers: [osm], center: new L.LatLng(center[0], center[1]), zoom: 10});

var options = {
	duration: 800, //Default: 800 - Sets the transition duration for the ping layer
	fps : 32, //Default: 32 - Sets the target framerate for the ping animation
	opacityRange: [ 1, 0 ],  //Default: [ 1, 0 ] - Sets the range of the opacity scale used to fade out the pings as they age
	radiusRange: [ 2, 6 ] //Default: [ 3, 15 ] - Sets the range of the radius scale used to size the pings as they age
};

var pingLayer = L.pingLayer(options).addTo(map);  //adds pingLayer to map w/ options created above

pingLayer
	.lng(function(d) { return d[0]; })          //returns long?
    .lat(function(d) { return d[1]; });         //returns lat?




d3.json("https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Transportation_WebMercator/MapServer/5/query?where=1%3D1&outFields=*&outSR=4326&f=json", createFirstDict);


function createFirstDict(response){

    var bikeDict = [];
    var bikeRacks = response.features;

    
    for (var i = 0; i < bikeRacks.length; i++) {
        bikeDict.push({
            ID:   bikeRacks[i].attributes.ID,
            lat: bikeRacks[i].attributes.LATITUDE,
            long: bikeRacks[i].attributes.LONGITUDE,
            bikeTotal: bikeRacks[i].attributes.NUMBER_OF_BIKES
        });
    }
    console.log(bikeDict);

}


d3.json("https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Transportation_WebMercator/MapServer/5/query?where=1%3D1&outFields=*&outSR=4326&f=json", createPings);

function createPings(response){

    // Pull the "bikeRack" property off of response.data
    var bikeRacks = response.features;

    // Loop through the bikeRack array
    for (var i = 0; i < bikeRacks.length; i++) {
        var bikeRack = bikeRacks[i].attributes;
        var bikeDict_update = [];

        bikeDict_update.push({
            ID:   bikeRacks[i].attributes.ID,
            lat: bikeRacks[i].attributes.LATITUDE,
            long: bikeRacks[i].attributes.LONGITUDE,
            bikeTotal: bikeRacks[i].attributes.NUMBER_OF_BIKES
        });

        console.log(bikeDict_update);

        if (bikeDict_update.bikeTotal - bikeDict.bikeTotal > 0){
            // For each bikeRack, create a ping if bike is added to the bike rack
            var bikePing_add = [bikeRack.LATITUDE, bikeRack.LONGITUDE];
            console.log(bikePing_add);
        }
        
        else if (bikeDict_update.bikeTotal - bikeDict.bikeTotal < 0){
            // For each bikeRack, create a ping if bike is removed to the bike rack
            var bikePing_remove = [bikeRack.LATITUDE, bikeRack.LONGITUDE];
            console.log(bikePing_remove);
        }


        // Add the marker to the bikeMarkers array
        bikePings_remove.push(bikePing_remove);
        bikePings_add.push(bikePing_add);

    }


      
    var paused = false;
    var update = function(){
        if(!paused) {
            pingLayer.ping(bikePings_add, 'red');
            pingLayer.ping(bikePings_remove, 'green');

            window.setTimeout(update, 3000);
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
    
    //uncomment below for recursive program... may freeze?
    // d3.json("https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Transportation_WebMercator/MapServer/5/query?where=1%3D1&outFields=*&outSR=4326&f=json", createPings);


}

