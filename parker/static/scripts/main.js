var map;

var boundsEventTimer;
boundsTimerDelay = 250;

var markersArray = new Array();


function initMap() {
  map = new google.maps.Map( document.getElementById('map') , {
    center: {lat: -33.870384731980205, lng: 151.200569099426275},
    zoom: 14
  });
	
	function onBoundsChanged(){
		latlongbound = map.getBounds();
		sw = latlongbound.getSouthWest();
		ne = latlongbound.getNorthEast();
		
		sLat = sw.lat();
		wLong = sw.lng();
		nLat = ne.lat();
		eLong = ne.lng();
		
		minLat = Math.min(sLat, nLat);
		maxLat = Math.max(sLat, nLat);
		
		// Will be a problem in case of 180 meridian crossing
		minLong = Math.min(wLong, eLong);
		maxLong = Math.max(wLong, eLong);

		//alert("Current bounds:\nMin Lat" + minLat + ", Max Lat: " + maxLat + "\nMin Long: " + minLong + ", MaxLong: " + maxLong);
		findParkingsByLatlong(minLat, maxLat, minLong, maxLong);
	}
	
	map.addListener('bounds_changed', function() {
		// Here is a timer used to eliminate execution of event fired too close to each other
		// For example, when you drag the map or zooming in/out.
		clearTimeout(boundsEventTimer); 
    boundsEventTimer = setTimeout(onBoundsChanged, boundsTimerDelay)
  });

}

function findParkingsByLatlong(minlat, maxlat, minlong, maxlong) {
	$.ajax({
		method: "GET",
		url: "/api/parkings",
		data: { "minlat": minlat, 
						"maxlat": maxlat, 
						"minlong": minlong, 
						"maxlong": maxlong },
		success: function(data) {
			if (data.length > 0) {
				//alert(data[0]['lat'] + ",,, " + data[0]['long']);
				processParkingData(data);
			} else { 
				alert("No parkings found"); }
		},			
		error: function(textStatus, errorThrown) {
			alert("Error happened: " + textStatus + ", " + errorThrown);
		}
	});
}

function processParkingData(data) {	
	// Add markers to the map
	for (i = 0, len = data.length; i < len; i++) { 
			latlong = 
				new google.maps.LatLng({
					lat: Number(data[i]['lat']), 
					lng: Number(data[i]['long'])
				}); 
			
			markersArray[i] = 
				new google.maps.Marker({
					position: latlong,
					map: map,
					title: data[i].label
				});
	}
}
	
function globalInit() {
	initMap();
}

$( document ).ready( globalInit );