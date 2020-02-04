// Zapamiętywanie kości






// Losowe ułozenie kości

  dices = $('.dice');

  $.each(dices, function( index, value ) {
    switch(index) {
      case 0:
        xTranslate = Math.random() * 125;
        yTranslate = Math.random() * 325;
        break;
      case 1:
        xTranslate = (Math.random() * 325) + 200;
        yTranslate = Math.random() * 125;
        break;
      case 2:
        xTranslate = Math.random() * 125 + 200;
        yTranslate = Math.random() * 125 + 200;
        break;
      case 3:
        xTranslate = Math.random() * 225;
        yTranslate = Math.random() * 125 + 400;
        break;
      case 4:
        xTranslate = Math.random() * 125 + 400;
        yTranslate = Math.random() * 325 + 200;
        break;
      default:
        // code block
    }
    translate = ' translate(' + xTranslate + 'px, ' + yTranslate + 'px)';
    rotate = 'rotate(' + Math.random() * 100 + 'deg)';
    $(value).css({transform: translate + rotate});
  });