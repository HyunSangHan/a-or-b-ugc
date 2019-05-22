$(document).ready(() => {
    $('.toggle-comments').on('click', function() {
        $(this).next().slideDown();
        $(this).hide();
    })
    $('.more-js-btn').on('click', function() {
        $(this).next().toggle();
    })
})