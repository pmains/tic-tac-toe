MY_TURN = false;
PLAYER_NAME = null;

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
      /**
      TODO: save game board and notify other player
      **/
    }
  }
}

function get_player() {
  return $("#player-name").val();
}

function ok_player_name() {
  console.log("ok player name");
  
  var player_name = $("#player-name-input").val();
  
  $.ajax({type:"PUT",
    url:"/player/" + player_name,
    success:function(response, status){
      console.log("success");
      console.log("response: " + response);
      console.log("status: " + status);
      // Hide warning text
      $("#player-modal .text-warning").hide();
      // Close modal
      $("#player-modal").hide();
      $("#player-name").val($("#player-name-input").val());
    },
    error:function(response, status, error){
      console.log("failure");
      console.log("error: " + error);
      console.log("status: " + status);
      $("#server-error").show();
    },
    data_type:"json"
  });  
}

function find_opponents() {
  $("#opponent-modal").show();

  var player_name = $("#player-name").val();
  $("#opponent-list").html("");

  $.ajax({type:"GET",
    url:"/find_opponents/" + player_name,
    success:function(players){
      console.log("players: " + players);
      for(var i=0; i<players.length; i++) {
        $("#opponent-list").append("<option value='" + players[i] + "'>" + players[i] + "</option>");
      }
    },
    data_type:"json"
  });
}

function cancel_modal() {
  $(".modal").hide();
}

function ok_opponent() {
  // Opponent has been chosen. Now start a new game.
  player1 = get_player();
  player2 = $("#opponent-list").val();

  console.log("opponent chosen");
  
  // Start a new game
  $.ajax({type:"PUT",
    url:"/game/" + player1 + "/" + player2,
    success:function(game_id){
      // Set field values
      $("#opponent-modal").hide();
      $("#game-id").val(game_id);
    },
    error:function(response, error, status) {
      console.log("failure");
      console.log("error: " + error);
      console.log("status: " + status);
    },
    data_type:"json"
  });
}

function find_game() {
  // Find a current game that the player belongs to
  $.ajax({type:"GET",
    url:"/game/" + get_player(),
    success:function(response){
      // Extract game dict from response object
      var game = response['game']
      
      var opponent = game['player1']
      if(game['player1'] == get_player()) {
        opponent = game['player2']
      }

      // Set value of game-id hidden field based on 
      $("#game-id").val(response['game_id']);
      
      $("#join-game-modal #msg").text("Join game against " + opponent);
      $("#join-game-modal").show();
    },
    error:function() {
      console.log("Could not retrieve game.");
    },
    data_type:"json"
  });
}

function ok_join_game() {
  // Hide the game modal
  $("#join-game-modal").hide();
  /**
  TODO: fetch the game board and information
  **/
}

function click_marker(marker) {
  $(".marker").removeClass("active");
  target = $(marker.target);
  target.addClass("active");
  reset();
}

$(document).ready(function() {
  // Reset button not needed until game started
  $("#reset").hide();
  // Player must enter a user name in order to play
  $("#player-modal").show();

  // Find Opponent modal buttons
  $("#cancel-opponent").bind("click", cancel_modal);
  $("#ok-opponent").bind("click", ok_opponent);

  // Join Game modal buttons
  $("#cancel-join-game").bind("click", cancel_modal);
  $("#ok-join-game").bind("click", ok_join_game);

  // Player Name modal buttons
  $("#ok-player-name").bind("click", ok_player_name);

  // Buttons below board
  $("#find-game").bind("click", find_game);
  $("#find-opponents").bind("click", find_opponents);
});
