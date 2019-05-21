$(document).ready(() => {
    $('.toggle-comments').on('click', function() {
        $(this).next().slideDown();
        $(this).hide();
    })
    $('.mdl-js-button').on('click', function() {
        $(this).next().toggle();
    })
})