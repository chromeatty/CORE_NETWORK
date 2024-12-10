
document.addEventListener("DOMContentLoaded", function() {
    // get the location data from the map element
    var mapElement = document.getElementById('map');
    var locationType = mapElement.dataset.locationType;
    var address = mapElement.dataset.address;
    var latitude = mapElement.dataset.latitude;
    var longitude = mapElement.dataset.longitude;

    if (locationType === 'address') {
        // use the Geocoding API to get the coordinates of the address
        fetch('https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(address))
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                if (data && data.length > 0) {
                    var latitude = parseFloat(data[0].lat);
                    var longitude = parseFloat(data[0].lon);

                    // initalise the map at the coordinates
                    var map = L.map('map').setView([latitude, longitude], 12);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; OpenStreetMap contributors'
                    }).addTo(map);
                    L.marker([latitude, longitude]).addTo(map)
                        .bindPopup(address)
                        .openPopup();
                } else {
                    console.error('Address not found');
                    alert('Address not found');
                }
            })
            .catch(function(err) {
                console.error('Error in geocoding', err);
                alert('Error in geocoding');
            });
    } else if (locationType === 'coordinates') {
        if (latitude !== null && longitude !== null) {
            // initialize the map at the provided coordinates
            var map = L.map('map').setView([latitude, longitude], 12);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);
            L.marker([latitude, longitude]).addTo(map)
                .bindPopup("Request Location")
                .openPopup();
        } else {
            console.error('Invalid coordinates');
            alert('Invalid coordinates');
        }
    } else {
        console.error('No valid location data provided');
        alert('No valid location data provided');
    }
});
