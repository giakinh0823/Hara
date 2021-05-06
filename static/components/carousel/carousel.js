$(document).ready(function () {
    $(".owl-carousel").owlCarousel({
        items: 4,
        autoplay: false,
        margin: 35,
        loop: true,
        nav: true,
        responsive: {
            300: {
                items: 1,
            },
            600: {
                items: 2,
            },
            900: {
                items: 3,
            },
            1200: {
                item: 4,
            }
        },
        navText: ["<i class=\"bi bi-caret-left\"></i>", "<i class=\"bi bi-caret-right\"></i>"],
    });
});