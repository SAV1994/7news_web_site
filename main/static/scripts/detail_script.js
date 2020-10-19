$(function () {
    function CheckForm() {
        if ($('#id_text').val() !== '') {
            $('.button-comment').prop('disabled', false);
        } else {
            $('.button-comment').prop('disabled', true);
        }
    }
    setInterval(CheckForm, 1000);
    $('.button-reply').on('click', function () {
        let pk = this.dataset.replyId
        $('#id_comment').val(pk)
    })
})