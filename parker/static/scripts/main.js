var map;

var boundsEventTimer;
boundsTimerDelay = 250;

var markersParking = new Array();
var markersPlaces = new Array();

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
		// Here is a timer used to eliminate execution of event fired too close to each other
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
		}
	});
}

function processParkingData(data) {	
	// Add markersPlaces to the map
	for (i = 0, len = data.length; i < len; i++) { 
			latlong = 
				new google.maps.LatLng({
					lat: Number(data[i]['lat']), 
					lng: Number(data[i]['long'])
				}); 
			
			markersParking[i] = 
				new google.maps.Marker({
					position: latlong,
					map: map,
					title: data[i].label
				});
	}
}
	
function createSearchControl(parentDiv) {
	parentDiv.id = "search-box"

	/* 
		<div class="input-group input-group-lg">
      <input type="text" class="form-control input-lg" placeholder="Search for...">
      <span class="input-group-btn">
        <button class="btn btn-primary btn-lg" type="button">Search</button>
      </span>
    </div>
	*/
	var controlUI = document.createElement('div');
	controlUI.className += " input-group input-group-lg";
	parentDiv.appendChild(controlUI);
	
	var input = document.createElement('input');
	input.type = 'text';
	input.className += "form-control";
	input.placeholder = "Search for a place";
	controlUI.appendChild(input);
	
	attachSearchControl(input);
	
	var executeInput = function(e) { 
		google.maps.event.trigger( input, 'focus')
		google.maps.event.trigger( input, 'keydown', {keyCode:13})
	}
	
	var span = document.createElement('span');
	span.className += " input-group-btn";
	
	var button = document.createElement('button');
	button.className += " btn btn-primary";
	button.type = "button";
	//button.textContent = 'Go search!';
	button.innerHTML = '<span class="glyphicon glyphicon-search" aria-hidden="true"></span>';
	button.onclick = executeInput;
	button.onkeydown = executeInput;
	
	span.appendChild(button);
	controlUI.appendChild(span);
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

    // Clear out the old markersPlaces.
    markersPlaces.forEach(function(marker) {
      marker.setMap(null);
    });
    markersPlaces = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(placeItem) {
      var icon = {
        url: placeItem.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };
	
			var infowindow = new google.maps.InfoWindow({
				content: placeItem.html_attributions[0]
			});

			var marker = new google.maps.Marker({
        map: map,
        icon: icon,
        title: placeItem.name,
				clickable: true,
				// label: '1', // Shows only if icon is not defined
        position: placeItem.geometry.location,
				place: {
									location: placeItem.geometry.location,
									placeId: placeItem.place_id
								}
      });
			
			marker.addListener('click', function() {
				infowindow.open(map, marker);
			});
		
			
      // Create a marker for each place.
      markersPlaces.push(marker);

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