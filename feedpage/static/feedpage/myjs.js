$(document).ready(() => {
    $('.toggle-comments').on('click', () => {
        $('.all-comments').slideDown();
        $('.toggle-comments').hide();
    })
})