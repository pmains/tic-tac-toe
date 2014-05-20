markers = ["X","O"]
turn = 0

function flip_turn() {
  turn = (turn + 1) % 2;
}

function build_grid() {
  grid = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
  ];
  
  square_objs = $(".square");
  // Use "for" rather than "for ... in" for IE compatibility
  for(var i=0; i<square_objs.length; i++) {
    x = parseInt($(square_objs[i]).attr("x"));
    y = parseInt($(square_objs[i]).attr("y"));
    grid[x][y] = $(square_objs[i]).text();
  }

  return grid;
}

function cats_game() {
  alert("Cat's Game");
  flip_turn();
  reset();
}

function check_winner() {
  var data = JSON.stringify(build_grid());
  var winner = null;

  $.ajax({type:"PUT",
    url:"/check_winner/",
    data:data,
    success:function(result){
      if(result != null) {
        alert(result + " is the winner!");
        winner = result;
      }
    },
    data_type:"json",
    async: false
  });

  return winner;
}

$(document).ready(function() {
  $(".square").bind("click", click_square);
  $("#reset").bind("click", reset);
});
