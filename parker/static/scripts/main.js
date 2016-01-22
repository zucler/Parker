var map;

var boundsEventTimer;
boundsTimerDelay = 250;


function initMap() {
  map = new google.maps.Map( document.getElementById('map') , {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
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
		find_parkings_by_latlong(minLat, maxLat, minLong, maxLong);
	}
	
	map.addListener('bounds_changed', function() {
		// Here is a timer used to eliminate execution of event fired too close to each other
		// For example, when you drag the map or zooming in/out.
		clearTimeout(boundsEventTimer); 
    boundsEventTimer = setTimeout(onBoundsChanged, boundsTimerDelay)
  });

}

function find_parkings_by_latlong(minlat, maxlat, minlong, maxlong) {
	$.ajax({
		method: "GET",
		url: "/api/parkings",
		data: { "minlat": minlat, 
						"maxlat": maxlat, 
						"minlong": minlong, 
						"maxlong": maxlong },
		success: function(data) {
			if (data.length > 0) {
				alert(data[0].label);
			} else { 
				alert("No parkings found"); }
		},			
		error: function(textStatus, errorThrown) {
			alert("Error happened: " + textStatus + ", " + errorThrown);
		}
	});
}
	
function globalInit() {
	initMap();
}

$( document ).ready( globalInit );