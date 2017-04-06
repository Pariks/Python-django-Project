(function(){

  var parallax = document.querySelectorAll(".parallax"),
      speed = 0.5;

  $(window).onscroll = function(){
      console.log('test');
    [].slice.call(parallax).forEach(function(el,i){

      var windowYOffset = window.pageYOffset,
          elBackgrounPos = "0 " + (windowYOffset * speed) + "px";
      
      el.style.backgroundPosition = elBackgrounPos;

    });
  };

})();