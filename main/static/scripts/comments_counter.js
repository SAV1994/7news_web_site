$(function() {
    function CommentCountView() {
        $('.comments-counter').each(function(index, counter) {
            const url_request = `${$(location).attr('protocol')}//${$(location).attr('host')}/api/${counter.dataset.newsId}`;
            $.get(url_request, function(response) {
                counter.innerHTML = response['number_of_comments'];
            });
        });
    }
    CommentCountView();
    setInterval(CommentCountView, 30000);
})