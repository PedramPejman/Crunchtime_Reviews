$(".lazy-load").click(function(e){
  e.preventDefault();  //Disable the link
	var src = $(this).attr("href").split("="),  //Get the unique video ID from the URL
	  width = $(this).width(),  //Get the dimensions of the current block for a seamless replacement
      height = $(this).height(),
      embededMedia = $("<iframe width='" + width + "' height='" + height + "' src='//www.youtube-nocookie.com/embed/" + src[1] + "?autohide=1&autoplay=1&rel=0' frameborder='0' allowfullscreen></iframe>");
      //autohide hides the player controls, autoplay allows one-click video access, rel disables related content
	$(this).replaceWith(embededMedia);  //Replace the link with the video
  $allVideos = $("iframe[src*='//player.vimeo'], iframe[src*='//www.youtube'], object, embed");  //Get all videos again (with new video added in)
  fluidMedia(embededMedia);  //Make it fluid for responsiveness!
});

$(document).ready(function(){
  //Make all existing embeded content fluid for responsiveness
  window.$allVideos = $("iframe[src*='//player.vimeo'], iframe[src*='//www.youtube'], object, embed");  //Get all videos
  fluidMedia($allVideos);
  
  //Maintain aspect ratio during screen resizing
  $(window).resize(function(){
    fluidMediaResize($allVideos);
	});
});

