// preloader.js
window.addEventListener("load", function () {
    const preloader = document.getElementById("preloader");
    
    // Minimum display time for the preloader (1 second)
    setTimeout(function() {
        preloader.style.transition = "opacity 0.5s ease, visibility 0.5s ease";
        preloader.style.opacity = "0";
        preloader.style.visibility = "hidden";
    }, 1000); // Preloader visible for at least 1 second
});
