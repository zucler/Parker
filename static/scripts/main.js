/*

    <script src="https://maps.googleapis.com/maps/api/js?v=3&key={{google_maps_api_key}}&libraries=places"></script>
    <script src="{% static 'scripts/jquery-1.12.0.min.js' %}"></script>
    <script defer src="{% static 'scripts/main.js' %}"></script>

    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>


*/

var GOOGLE_MAPS_API_KEY = "AIzaSyA5MZPwIeHVdTYLtZg_o8FVEihohTz7bXw";
var STATIC_URL = "/extras/scripts";

requirejs.config({
    baseUrl: '',
    paths: {
		async: STATIC_URL + '/lib/async',
        modules: STATIC_URL + '/modules/',
		jquery: STATIC_URL + '/vendor/jquery-1.12.0.min',
		bootstrap: '//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min'
    }
});

/*
define(['async!https://maps.googleapis.com/maps/api/js?v=3&key=' + GOOGLE_MAPS_API_KEY + '&libraries=places'],
function(){
    // google.maps is ready
});
*/

define('gmaps', ['async!https://maps.googleapis.com/maps/api/js?v=3&key=' + GOOGLE_MAPS_API_KEY + '&libraries=places'],
function(){
    // return the gmaps namespace for brevity
    return window.google.maps;
});

/*
define(['gmaps'], function(gmaps){
    // shorter namespace, no need to type "google.maps" all the time
    var map = new gmaps.Map(myDiv, mapOpts);
});
*/
requirejs(["modules/geosearch"]);
