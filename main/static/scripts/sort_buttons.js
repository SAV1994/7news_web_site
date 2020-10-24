$(function () {

     if (location.pathname.includes('/by_comm')) {
        $('.sort-by-date').removeClass('button-pressed');
        $('.sort-by-comments').addClass('button-pressed');
    }
})