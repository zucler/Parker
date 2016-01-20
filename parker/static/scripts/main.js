var map;

var boundsEventTimer;
boundsTimerDelay = 150;

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

		alert("Current bounds:\nMin Lat" + minLat + ", Max Lat: " + maxLat + "\nMin Long: " + minLong + ", MaxLong: " + maxLong);
	}
	
	map.addListener('bounds_changed', function() {
		// Here is a timer used to eliminate execution of event fired too close to each other
		// For example, when you drag the map or zooming in/out.
		clearTimeout(boundsEventTimer); 
    boundsEventTimer = setTimeout(onBoundsChanged, boundsTimerDelay)
  });

}

function globalInit() {
	initMap();
}

$( document ).ready( globalInit );