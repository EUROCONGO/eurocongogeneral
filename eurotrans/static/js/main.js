// Back to Top Button
$(window).scroll(function() {
    if ($(this).scrollTop() > 300) {
        $('#backToTop').fadeIn();
    } else {
        $('#backToTop').fadeOut();
    }
});

$('#backToTop').click(function() {
    $('html, body').animate({scrollTop: 0}, 'slow');
    return false;
});

// Navbar scroll effect
$(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
        $('.navbar').addClass('scrolled');
    } else {
        $('.navbar').removeClass('scrolled');
    }
});

// Smooth scrolling for anchor links
$('a[href*="#"]').not('[href="#"]').not('[href="#0"]').click(function(event) {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        if (target.length) {
            event.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 1000, function() {
                var $target = $(target);
                $target.focus();
                if ($target.is(":focus")) {
                    return false;
                } else {
                    $target.attr('tabindex','-1');
                    $target.focus();
                }
            });
        }
    }
});

// Initialize tooltips
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

// Counter animation
$(window).scroll(function() {
    $('.counter-box').each(function() {
        var pos = $(this).offset().top;
        var winTop = $(window).scrollTop();
        if (pos < winTop + $(window).height() - 100 && !$(this).hasClass('animated')) {
            $(this).addClass('animated');
            var countTo = $(this).find('h2').text();
            $(this).find('h2').countTo({
                from: 0,
                to: parseInt(countTo),
                speed: 2000,
                refreshInterval: 50
            });
        }
    });
});