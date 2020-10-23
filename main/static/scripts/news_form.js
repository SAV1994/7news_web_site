$(function () {

    function CheckForm() {
        if ($('#id_header').val() !== '' && $('#id_sub_header').val() !== '' && $('#id_image').val() !== '' && $('#id_teaser').val() !== '' && $('#id_full_text').val() !== '') {
            $('.button-save').prop('disabled', false);
        } else {
            $('.button-save').prop('disabled', true);
        }
    }

    if (location.pathname !== '/news/') {
        let fileName = $('#div_id_image div a').text();
        $('.file-name').text(fileName);
    }

    setInterval(CheckForm, 1000);

    $('.btn-reset').click(function() {
        $('.clearablefileinput').val('');
        $('.file-name').text('');
    });

    $('.clearablefileinput').focus(function () {
        $('.image-input label').addClass('focus');
    });

    $('.clearablefileinput').focusout(function () {
        $('.image-input label').removeClass('focus');
    });

    $('.clearablefileinput').change(function() {
        let fileName = $('.clearablefileinput').val();
        $('.file-name').text(fileName);
    });
})
