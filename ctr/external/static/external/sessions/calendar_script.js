var clickEvent = ('ontouchstart' in window) ? 'touchstart' : 'click';
var that = null;

$('.session-day').on(clickEvent, function() {
	$( ".sexytabs" ).tabs( "option", "active", 0 );
	that = this;
});

$( ".sexytabs" ).on( "tabsactivate", function( event, ui ) {
		if (that) {
			var day = $(that).text();
		    var session = $("*[data-day='" + day +"']");
		    console.log(session);
		    setTimeout(function() {
		    	session.click();
		    }, 150);
		    that = null;
		}
	});
