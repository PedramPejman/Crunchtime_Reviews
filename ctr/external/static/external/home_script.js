$('.nav-button').hover(show_nav_label, hide_nav_label);


//HELPER FUNCTIONS

function show_nav_label() {
	//$(this).find('.icon-title').animate({top:"+=50"},100);
	$(this).find('.icon-title').velocity({
		top: ["+=10", [50,5]]
	}, {
		duration: 600
	});
}

function hide_nav_label() {
	$(this).find('.icon-title').velocity({
		top: ["-=10", [500,10]]
	}, {
		duration: 600
	});
}

//Typer
var TxtRotate = function(el, toRotate, period) {
  this.toRotate = toRotate;
  this.el = el;
  this.loopNum = 0;
  this.period = parseInt(period, 10) || 2000;
  this.txt = '';
  this.tick();
  this.isDeleting = false;
};

TxtRotate.prototype.tick = function() {
  var i = this.loopNum % this.toRotate.length;
  var fullTxt = this.toRotate[i];
  var offset = 1;
  if (("<>".indexOf(fullTxt.charAt(this.txt.length))) > -1){
    offset = 4;
  }

  if (this.isDeleting) {
    this.txt = fullTxt.substring(0, this.txt.length - offset);
  } else {
    this.txt = fullTxt.substring(0, this.txt.length + offset);
  }

  this.el.innerHTML = '<span class="wrap">'+this.txt+'</span>';

  var that = this;
  var delta = 200 - Math.random() * 100;

  if (this.isDeleting) { delta /= 2; }

  if (!this.isDeleting && this.txt === fullTxt) {
    delta = this.period;
    this.isDeleting = true;
  } else if (this.isDeleting && this.txt === '') {
    this.isDeleting = false;
    this.loopNum++;
    delta = 500;
  }

  setTimeout(function() {
    that.tick();
  }, delta);
};

window.onload = function() {
  var elements = document.getElementsByClassName('txt-rotate');
  for (var i=0; i<elements.length; i++) {
    var toRotate = elements[i].getAttribute('data-rotate');
    var period = elements[i].getAttribute('data-period');
    if (toRotate) {
      new TxtRotate(elements[i], JSON.parse(toRotate), period);
    }
  }
  // INJECT CSS
  var css = document.createElement("style");
  css.type = "text/css";
  css.innerHTML = ".txt-rotate > .wrap { border-right: 0.08em solid #666 }";
  document.body.appendChild(css);
};