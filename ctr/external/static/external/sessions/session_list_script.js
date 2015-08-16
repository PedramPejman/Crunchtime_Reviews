var clickEvent = ('ontouchstart' in window) ? 'touchstart' : 'click';

$('.detail').on(clickEvent, function() {
    $(this).parent('li').toggleClass('open').siblings().removeClass('open');
});
