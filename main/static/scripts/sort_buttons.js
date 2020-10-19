$(function () {
     if (location.pathname === '/by_comments/') {
        $('.sort-by-date').removeClass('button-pressed');
        $('.sort-by-comments').addClass('button-pressed');
    }
})