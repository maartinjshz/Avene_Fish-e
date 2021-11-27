$(document).ready(function(){
    var currentMousePos = { x: -1, y: -1 };
    $('#flesh').mousemove(function(e) {
        currentMousePos.x = e.pageX;
        currentMousePos.y = e.pageY;
      
      $('#bone').css('-webkit-mask-position-x', currentMousePos.x - 75);
      $('#bone').css('-webkit-mask-position-y', currentMousePos.y - 240)
    });
});