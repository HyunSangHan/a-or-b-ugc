$(document).ready(() => {
    $('.toggle-comments').on('click', () => {
        $('.all-comments').slideDown();
        $('.toggle-comments').hide();
    })
    $('.mdl-js-button').on('click', () => {
        $('.more-info').fadeToggle();
        $('.transp-bg').toggle();
    })
    $('.transp-bg').on('click', () => {
        $('.more-info').hide();
        $('.transp-bg').hide();
    })
})