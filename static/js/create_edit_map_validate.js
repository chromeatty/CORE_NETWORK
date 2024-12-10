
document.addEventListener("DOMContentLoaded", function() {
    var locationTypeField = document.getElementById("id_location_type");
    var addressFieldDiv = document.getElementById("div_id_address");
    var latitudeFieldDiv = document.getElementById("div_id_latitude");
    var longitudeFieldDiv = document.getElementById("div_id_longitude");

    function toggleLocationFields() {
        var selectedValue = locationTypeField.value;
        if (selectedValue === "address") {
            addressFieldDiv.style.display = "block";
            latitudeFieldDiv.style.display = "none";
            longitudeFieldDiv.style.display = "none";
        } else if (selectedValue === "coordinates") {
            addressFieldDiv.style.display = "none";
            latitudeFieldDiv.style.display = "block";
            longitudeFieldDiv.style.display = "block";
        } else {
            // dont show location fields if there is no selection
            addressFieldDiv.style.display = "none";
            latitudeFieldDiv.style.display = "none";
            longitudeFieldDiv.style.display = "none";
        }
    }

    // make sure the location fields are displayed correctly when the page
    toggleLocationFields();

    // use an event listener to update the location fields when the location type is changed
    locationTypeField.addEventListener('change', toggleLocationFields);
});
