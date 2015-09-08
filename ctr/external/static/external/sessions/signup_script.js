var submit_callback = submit_button_clicked;

$('.submit-button').click(function() {
  //displaying the overlay
   var clickBtnValue = $(this).val();
   current_overlay_course = this.getAttribute('data-course');
   current_overlay_date = this.getAttribute('data-date');
    current_overlay_id = this.getAttribute('data-session-id');
    
  //if signing up for a second session, some housekeeping is in order
  (document.getElementById('sign-me-up')).innerHTML = "Sign Me Up!" ;
  $('#student-id').show();
  $('#thank-you-note').hide();
  submit_callback = submit_button_clicked;

  $('#sign-up-overlay').fadeIn(1000);
  $('#overlay-container').fadeIn(500);   
});

function submit_button_clicked(e) {
  e.preventDefault();
  var button = $('#sign-me-up');
  var email = (document.getElementById('student-id').value);
  validate(button, email, switch_buttons_animation, failure_animation);
}

function validate(button, email, onSuccess, onFailure) {
  $.ajax({ url: 'attend/'+ email +'/' + current_overlay_id,
//         data: {student_id: email, course: current_overlay_course, date: current_overlay_date, session_id: current_overlay_id},
         type: 'get',
         success: function(data) {
          $('#error').hide(1000);
          onSuccess(button, email);
          submit_callback = close_overlay;
                  },
          error: function() {
            failure_animation(button, email);
          }
        });
}

function close_overlay(e) {
  if (e != null) {
    e.preventDefault();
  }
  $('#sign-up-overlay').fadeOut(1000);
  $('#overlay-container').fadeOut(500); 
}

function switch_buttons_animation(button, email) {
  button.fadeOut(1000, function() {
    (document.getElementById('sign-me-up')).innerHTML = "<img src='http://jimpunk.net/Loading/wp-content/uploads/loading81.gif' width='50' height='50'>" ;
  });
  button.fadeIn(500, function() {
    $('#thank-you-note').show(1000);
  });
  button.delay(500).fadeOut(500, function() { 
  (document.getElementById('sign-me-up')).innerHTML = "Thank you!" ;
    $('#student-id').hide(500);
  });
  button.fadeIn(500, function() {
  });
}

function failure_animation(button, email) {
  button.fadeOut(1000, function() {
    (document.getElementById('sign-me-up')).innerHTML = "<img src='http://jimpunk.net/Loading/wp-content/uploads/loading81.gif' width='50' height='50'>" ;
  });
  button.fadeIn(500, function() {
    $('#error').show(1000);
  });
  button.delay(500).fadeOut(500, function() { 
    (document.getElementById('sign-me-up')).innerHTML = "Sign Me Up!" ;
  });
  button.fadeIn(500, function() {
  });
}

$('#sign-up-overlay').unbind('submit').submit(function(e){submit_callback(e)});

$('#close-icon').click(function() {
  close_overlay(null);
})  


 /* $.ajax({ url: './sendEmail.php',
         data: {action: 'send_email', student_id: email, course: current_overlay_course, date: current_overlay_date, session_id: current_overlay_id},
         type: 'post',
         success: function() {
                  }
});
*/
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}