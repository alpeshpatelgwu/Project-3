var stations;

markers = [];
geo = [];

d3.json("https://gbfs.citibikenyc.com/gbfs/en/station_information.json", function(data) {

  stations = data.data.stations;

  stations.forEach(function(d){
    bikeMarker = L.marker([d.lat, d.lon])
      .bindPopup("<h3>" + d.name + "<h3><h3>Capacity: " + d.capacity + "<h3>");

    markers.push(bikeMarker);
    geo.push(d.lat);
  });

//  console.log(stations);
});

console.log(geo);

//data = response.data.stations;


markers = [];
/*
stations.forEach(function(d){
  bikeMarker = L.marker([d.lat, d.lon])
    .bindPopup("<h3>" + d.name + "<h3><h3>Capacity: " + d.capacity + "<h3>");

  markers.push(bikeMarker);
});

*/
