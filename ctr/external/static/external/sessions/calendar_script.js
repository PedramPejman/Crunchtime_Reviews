var clickEvent = ('ontouchstart' in window) ? 'touchstart' : 'click';

$('.session-day').on(clickEvent, function() {
	$( ".sexytabs" ).tabs( "option", "active", 0 );
	var that = this;
	$( ".sexytabs" ).on( "tabsactivate", function( event, ui ) {
		var day = $(that).text();
	    var session = $("*[data-day='" + day +"']");
	    console.log(session);
	    setTimeout(function() {
	    	session.click();
	    }, 150);
	});
});
