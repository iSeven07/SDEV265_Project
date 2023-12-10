document.addEventListener('DOMContentLoaded', function() {

    var path = window.location.pathname;
    var navLinks = document.querySelectorAll('.navbar-nav a.nav-link');
    
    navLinks.forEach(function(link) {
        if (link.getAttribute('href') === path) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});