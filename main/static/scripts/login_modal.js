$(function() {
    $('.login').click(function() {
        $('.modal-container').show();
        $('body').addClass('stop-scrolling');
    });
    $('.modal-container').click(function(event) {
        if (event.target === this) {
            $(this).hide();
            $('body').removeClass('stop-scrolling');
        }
    });
})