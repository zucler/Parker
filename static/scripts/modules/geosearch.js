var map;

var boundsEventTimer;
boundsTimerDelay = 250;

var parkingInfoWindow;

var markersParking = new Array();
var windowsParking = new Array();

// TODO: Use only one InfoWindow for all markers and fill it with content when opening.

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

		debug("s: " + sLat + ", w: " + wLong + "<br>n: " + nLat + ", e: " + eLong);

		findParkingsByLatlong(sLat, wLong, nLat, eLong);
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

	parkingInfoWindow = new google.maps.InfoWindow({content: "Loading..."})
}


function findParkingsByLatlong(s, w, n, e) {
	$.ajax({
		method: "GET",
		url: "/api/parkings",
		data: { "s": s,
						"w": w,
						"n": n,
						"e": e },
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
	// derefMarkers(markersParking);
	derefWindows(windowsParking);

	data = filterDataByMarkers(data, markersParking)
	// TODO: Also clean unused markers (those who out of screen)

	console.log("Filtered data size: " + data.length);

	// FIXME: When moving or zooming, markers and windows will disappear.
	// Need to make workaround to not delete opened window.
	// And to not delete and not add markers already added to map.
	// For that need to use parking unique ID array

	data.forEach(function(dataItem) {
		var latlong =
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

		marker.parkingID = dataItem.parkingID;

		var ratetype = dataItem['ratetype'][0];
		var ratetypeInfo = "";

		if (typeof ratetype !== 'undefined'){
			ratetypeInfo =
				"DayOfWeek: " + ratetype['day_of_week'] + "<br>" +
				"Start time: " + ratetype['start_time'] + "<br>" +
				"End time: " + ratetype['end_time'] + "<br>" +
				"Rate Type: " + ratetype['rate_type'] + "<br>" +
				"Label: " + ratetype['label'] + "<br>";

			var priceTable = "";

			ratetype.rateprice.forEach(function(rpItem) {
				priceTable += "<tr>" +
					"<td>" + rpItem.rateID_id + "</td>" +
					"<td>" + rpItem.duration + "</td>" +
					"<td>" + rpItem.price + "</td>" +
					"</tr>";
			})

			priceTable = "<table><th>RateID</th><th>Duration</th><th>Price</th>" + priceTable + "</table>";

			ratetypeInfo += "<br>Prices:<br>" + priceTable;
		}

		var infowindow = new google.maps.InfoWindow({
			content: dataItem.label + "<br>Address: " + dataItem.address + "<br>" + ratetypeInfo,
			//TODO: More info
		});

		var content = dataItem.label + "<br>Address: " + dataItem.address + "<br>" + ratetypeInfo;

		marker.infoWindowContent = content

		marker.addListener('click', function() {
				parkingInfoWindow.close();
				parkingInfoWindow.setContent(marker.infoWindowContent);
				parkingInfoWindow.open(map, marker); // FIXME: Window position has erroneous offset
			});

		markersParking.push(marker);
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

// Reuses markers that already exist
// Removes items from data array of associated markers
// Not yet true: Assumes that there is no possibility to have two parkings at exactly same position
// Returns filtered data items array
function filterDataByMarkers(itemsArray, markerArray) {
	markerArray.forEach(function(marker) {
		currentParkingID = marker.parkingID;

		// Look for already existing items
		itemsArray = itemsArray.filter(function(item, index, arr) {
			return item.parkingID != currentParkingID;
		})

      //marker.setMap(null);
    });

	return itemsArray
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

// $( document ).ready( globalInit );
define(['gmaps', 'jquery', 'bootstrap'], function(gmaps, $, bstrp){
    // shorter namespace, no need to type "google.maps" all the time
    globalInit();
});
