
angular.module('oddsDirectives', [])
.directive('parlay',  
function() {
    return {
        restrict: 'A',
        link: function() {
            var tooltipSpan,
                x,
                y;
           //Find the element which will contain tooltip
            parlayContainer = document.getElementById('parlay-container');
            console.log(parlayContainer)
            //Bind mousemove event to the element which will show tooltip
            $("#odds").mousemove(function(e) {
                //find X & Y coodrinates
                x = e.pageX,
                y = e.pageY - window.pageYOffset;
                
                //Set tooltip position according to mouse position
                parlayContainer.style.top = (y + 20) + 'px';
                parlayContainer.style.left = (x + 20) + 'px';
            });
               
        }
    };
});
