MY_TURN = true;

function reset() {
  $(".square").text("");
  turn = 0;

  if($(".marker.active").text() == "O") {
    computer_play();
  }
}

function click_square(square) {
  if( $(square.target).text() == "" ) {
    $(square.target).text(markers[turn]);
    flip_turn();
    if(check_winner() != null ) {
      reset();
      return;
    }
    
    // if no winner and all squares filled
    if( $(".square:empty").length == 0 ) {
      cats_game();
    } else {
      computer_play();
    }
  }
}

function computer_play() {
  data = JSON.stringify(build_grid());

  $.ajax({type:"PUT",
    url:"/find_best_move/" + markers[turn],
    data:data,
    success:function(coordinates){
      if(coordinates == null) {
        cats_game();
      }
      else {
        x = coordinates[0];
        y = coordinates[1];
        square = $(".square[x=" + x + "][y=" + y + "]")[0];
        $(square).text(markers[turn]);
        flip_turn();
        if(check_winner() != null) {
          reset();
          return;
        }
      }
    },
    data_type:"json",
    async:false
  });
}

function click_marker(marker) {
  $(".marker").removeClass("active");
  target = $(marker.target);
  target.addClass("active");
  reset();
}

$(document).ready(function() {
  $(".marker").bind("click", click_marker);
});
