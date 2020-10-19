$(function () {
    function CheckForm() {
        if ($('#id_header').val() !== '' && $('#id_sub_header').val() !== '' && $('#id_image').val() !== '' && $('#id_teaser').val() !== '' && $('#id_full_text').val() !== '') {
            $('.button-save').prop('disabled', false);
        } else {
            $('.button-save').prop('disabled', true);
        }
    }
    if (location.pathname === '/news/') {
        setInterval(CheckForm, 1000);
    }
})