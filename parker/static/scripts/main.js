var map;

var boundsEventTimer;
boundsTimerDelay = 250;

var markersParking = new Array();
var windowsParking = new Array();

var markersFoundPlaces = new Array();
var windowsFoundPlaces = new Array();

var debugField = document.getElementById('debug');


function debug(content) {
	debugField.innerHTML = content;
}


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
		
		// FIXME: Will be a problem in case of 180 meridian crossing
		minLong = Math.min(wLong, eLong);
		maxLong = Math.max(wLong, eLong);
		
		debug("minLat: " + minLat + ", minLong: " + minLong + "<br>maxLat: " + maxLat + ", maxLong: " + maxLong);

		findParkingsByLatlong(minLat, maxLat, minLong, maxLong);
	}
	
	map.addListener('bounds_changed', function() {
		// Here is a timer used to eliminate execution of event fired too often
		// For example, when you drag the map or zooming in/out.
		clearTimeout(boundsEventTimer); 
    boundsEventTimer = setTimeout(onBoundsChanged, boundsTimerDelay)
		
		// TODO: No need to look for parking places in case if new bounds cover less area than before
		// 			 ex. If user zooming in
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
				debug("No parkings found"); }
		},			
		error: function(textStatus, errorThrown) {
			alert("Error happened: " + textStatus + ", " + errorThrown);
			// FIXME: Should start ajax command again
		}
	});
}


function processParkingData(data) {	
	derefMarkers(markersParking);
	derefWindows(windowsParking);
	
	// FIXME: When moving or zooming, markers and windows will disappear.
	// Need to make workaround to not delete opened window.
	// And to not delete and not add markers already added to map.
	// For that need to use parking unique ID array
	
	data.forEach(function(dataItem) {
		latlong = 
				new google.maps.LatLng({
					lat: Number(dataItem['lat']), 
					lng: Number(dataItem['long'])
				}); 
			
		var marker = 
			new google.maps.Marker({
				position: latlong,
				map: map,
				clickable: true,
				title: dataItem.label,
			});
			
		var infowindow = new google.maps.InfoWindow({
			content: dataItem.label + "<br>Address: " + dataItem.address,
			//TODO: More info
		});
		
		marker.addListener('click', function() {
				windowsParking.forEach(function(window){ window.close(); })
				infowindow.open(map, marker); // FIXME: Window position has erroneous offset
			});
			
		markersParking.push(marker);
		windowsParking.push(infowindow);
	});
		
}
	
	
function createSearchControl(parentDiv) {
	parentDiv.id = "search-box"

	/*<div class="input-group input-group-lg">
      <input type="text" class="form-control input-lg" placeholder="Search for...">
      <span class="input-group-btn">
        <button class="btn btn-primary btn-lg" type="button">Search</button>
      </span>
    </div>*/
		
	var controlUI = document.createElement('div');
	controlUI.className += " input-group input-group-lg";
	parentDiv.appendChild(controlUI);
	
	var searchInput = document.createElement('input');
	searchInput.className += "form-control";
	searchInput.type = 'text';
	searchInput.placeholder = "Search for a place";
	controlUI.appendChild(searchInput);
	
	attachSearchControl(searchInput);
	
	var executeInput = function(e) { 
		// SearchBox need that sequence to start searching
		google.maps.event.trigger( searchInput, 'focus')
		google.maps.event.trigger( searchInput, 'keydown', {keyCode:13})
	}
	
	var span = document.createElement('span');
	span.className += " input-group-btn";
	
	var button = document.createElement('button');
	button.className += " btn btn-primary";
	button.type = "button";
	button.innerHTML = '<span class="glyphicon glyphicon-search" aria-hidden="true"></span>';
	button.onclick = executeInput;
	button.onkeydown = executeInput;
	
	span.appendChild(button);
	controlUI.appendChild(span);
}


function derefMarkers(markerArray) { 
	markerArray.forEach(function(marker) {
      marker.setMap(null);
    });
  markerArray = [];
}

function derefWindows(windowsArray) {
	windowsArray.forEach(function(window) {
      window.close();
    });
	windowsArray = [];
}


function attachSearchControl (parentDiv) {
	var AustraliaBounds = new google.maps.LatLngBounds(
		new google.maps.LatLng(-40, 111),
		new google.maps.LatLng(-7.5, 157));

	var searchBox = new google.maps.places.SearchBox(parentDiv, {
		bounds: AustraliaBounds
	});
	
	// Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

		derefMarkers(markersFoundPlaces);
		derefWindows(windowsFoundPlaces);

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(placeItem) {
      var icon = {
        url: placeItem.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(35, 35),
        scaledSize: new google.maps.Size(25, 25)
      };
	
			var infowindow = new google.maps.InfoWindow({
				content: placeItem.name + "<br>Website: " + placeItem.website, 
				// TODO: Need to show more info (https://developers.google.com/maps/documentation/javascript/places#place_details_results)
			});

			var marker = new google.maps.Marker({
        map: map,
        icon: icon,
        title: placeItem.name,
				clickable: true,
        position: placeItem.geometry.location,
				place: {
									location: placeItem.geometry.location,
									placeId: placeItem.place_id
								}
      });
			
			marker.addListener('click', function() {
				windowsFoundPlaces.forEach(function(window){ 
					window.close();
				})
				
				infowindow.open(map, marker); // FIXME: Window position has erroneous offset
			});
		
			
      // Create a marker for each place.
      markersFoundPlaces.push(marker);
			windowsFoundPlaces.push(infowindow);

      if (placeItem.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(placeItem.geometry.viewport);
      } else {
        bounds.extend(placeItem.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });
}
	
	
function globalInit() {
	initMap();
}

$( document ).ready( globalInit );