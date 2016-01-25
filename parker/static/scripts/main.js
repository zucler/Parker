var map;

var boundsEventTimer;
boundsTimerDelay = 250;

var markersArray = new Array();


function initMap() {
  map = new google.maps.Map( document.getElementById('map') , {
    center: {lat: -33.870384731980205, lng: 151.200569099426275},
    zoom: 14,
		mapTypeControl: true,
    mapTypeControlOptions: {
        style: google.maps.MapTypeControlStyle.DEFAULT,
        position: google.maps.ControlPosition.LEFT_BOTTOM
    },
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
	
	// Create search box
	var controlDiv = document.createElement('div');
	createSearchControl(controlDiv);
	controlDiv.index = 1;
	map.controls[google.maps.ControlPosition.TOP_LEFT].push(controlDiv);
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
	
function createSearchControl(parentDiv) {
	parentDiv.id = "search-box"
	// Set CSS for the control border
	var controlUI = document.createElement('div');
	controlUI.style.backgroundColor = '#fff';
	controlUI.style.border = '2px solid #fff';
	controlUI.style.cursor = 'pointer';
	controlUI.style.marginBottom = '22px';
	controlUI.style.textAlign = 'center';
	//controlUI.title = 'Click to recenter the map';
	parentDiv.appendChild(controlUI);

	// Set CSS for the control interior
	var controlText = document.createElement('input');
	controlText.style.color = 'rgb(25,25,25)';
	controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
	controlText.style.fontSize = '16px';
	controlText.style.lineHeight = '38px';
	controlText.style.paddingLeft = '5px';
	controlText.style.paddingRight = '5px';
	controlText.innerHTML = 'Center Map';
	controlUI.appendChild(controlText);
	
	attachSearchControl(controlText);
}

function attachSearchControl (parentDiv) {
	var AustraliaBounds = new google.maps.LatLngBounds(
		new google.maps.LatLng(-40, 111),
		new google.maps.LatLng(-7.5, 157));

	var searchBox = new google.maps.places.SearchBox(parentDiv, {
		bounds: AustraliaBounds
	});
}
	
function globalInit() {
	initMap();
}

$( document ).ready( globalInit );