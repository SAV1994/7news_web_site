$(function() {

    $('.login').click(function() {
        $('.modal-container').css('display', 'flex');
        $('body').addClass('stop-scrolling');
    });

    $('.btn-close').click(function() {
        $('.modal-container').css('display', 'none');
        $('body').removeClass('stop-scrolling');
    });
})