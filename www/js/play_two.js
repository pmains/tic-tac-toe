MY_TURN = true;

function reset() {
  $(".square").text("");
  turn = 0;
}

function click_square(square) {
  if( $(square.target).text() == "" ) {
    $(square.target).text(markers[turn]);
    flip_turn();
    if( check_winner() != null ) {
      reset();
    }
  }
}
