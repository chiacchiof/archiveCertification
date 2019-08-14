   function showPosition(){
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(function(position){
                var latitudeInfo = "Latitude: " + position.coords.latitude;
                document.getElementById("LatitudeGPS").innerHTML = latitudeInfo;
                var longitudeInfo = "Longitude: " + position.coords.latitude;
                document.getElementById("LongitudeGPS").innerHTML = longitudeInfo;
            });
        } else{
            alert("Sorry, your browser does not support HTML5 geolocation.");
        }
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position){
        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;
        var coords = new google.maps.LatLng(latitude, longitude);
        var mapOptions = {
            zoom: 15,
            center: coords,
            mapTypeControl: true,
            navigationControlOptions: {
                style: google.maps.NavigationControlStyle.SMALL
            },
            mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            map = new google.maps.Map(
                document.getElementById("mapContainer"), mapOptions
                );
            var marker = new google.maps.Marker({
                    position: coords,
                    map: map,
                    title: "Current Location!"
            });
 
        });
    }else {
        alert("Geolocation API is not supported in your browser.");
    }