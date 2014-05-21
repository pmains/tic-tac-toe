MY_TURN = false;
MY_MARKER = null;
UPDATE_INTERVAL = null;

/* Clear the board */
function reset() {
  $(".square").text("");
  
  if(MY_MARKER == 0) { // Player is X
    MY_TURN = true;
  } else { // Player is O
    MY_TURN = false;
  }

  save_game(function() { console.log("game restart"); });
}

/* Bound to click action on the board's squares */
function click_square(square) {
  if( MY_TURN && $(square.target).text() == "" ) {
    // Mark the square
    $(square.target).text(markers[MY_MARKER]);
   
    var player = get_player();
    var game_id = get_game_id();
    var board = build_grid();

    save_game(function(){ MY_TURN = false; });
  }

  check_outcome();
}

/* Update the board on set time intervals */
function update_interval() {
  var refreshInterval = setInterval(function(){
    update_game();
    check_outcome();
  }, 3000);
}

/* See if there is a winner */
function check_outcome() {
  // Check if there was a winner
  if(check_winner() != null ) {
    reset();
    return;
  }    
  // If no winner and all squares filled
  if( $(".square:empty").length == 0 ) {
    alert("Cat's Game!");
    reset();
  }
}

/* Determine if it's my turn */
function my_turn() {
  var is_my_turn = null;

  // Give server the game id and player name
  $.ajax({type:"GET",
    url:"/game/turn/" + get_game_id() + "/" + get_player(),
    success:function(response) {
      is_my_turn = response;
    },
    async:false
  });

  return is_my_turn;
}

/* Retrieve game data from the server */
function get_game() {
  var game_id = get_game_id();
  var game = null;
  $.ajax({type:"GET",
    url:"/game/" + game_id,
    success:function(response) {
      game = response;
    },
    async:false
  });
  return game;
}

/* Save game board */
function save_game(success_callback) {
  game_id = get_game_id();
  player = get_player();

  $.ajax({type:"PUT",
    url:"/game/" + game_id + "/" + player,
    // Data needs to be passed as a string
    data: JSON.stringify(build_grid()),
    success:success_callback,
    error:function() {
      alert("Could not save game");
      // Set board to pre-click
      board = get_game()['board'];
      populate_board(board);
    }
  });
}

/* Given an array representing the current board state, populate each square */
function populate_board(board) {
  for(var x=0; x<board.length; x++) {
    for(var y=0; y<board.length; y++) {
      var square = $(".square[x=" + x + "][y=" + y + "]");
      square.text(board[x][y]);
    }
  }
}

/* Get and set the name of the local player */
function get_player() {
  return $("#player-name").val();
}

/* Get and set the id of the current game */
function get_game_id() {
  return $("#game-id").val();
}

/* When player clicks OK on name entry modal */
function ok_player_name() {
  console.log("ok player name");

  /* Retrieve player name */
  var player_name = $("#player-name-input").val();

  /* Save the player */
  $.ajax({type:"PUT",
    url:"/player/" + player_name,
    success:function(response, status){
      // Hide warning text
      $("#player-modal .text-warning").hide();
      // Close modal
      $("#player-modal").hide();
      $("#player-name").val($("#player-name-input").val());
    },
    error:function(response, status, error){
      $("#server-error").show();
    },
    data_type:"json"
  });  
}

/* Show modal with list of available opponents */
function find_opponents() {
  // Show the modal
  $("#opponent-modal").show();

  var opponent_list = $("#opponent-list");
  opponent_list.html("");

  /* Retrieve available players, excluding the current player */
  $.ajax({type:"GET",
    url:"/find_opponents/" + get_player(),
    success:function(players){
      for(var i=0; i<players.length; i++) {
        opponent_list.append("<option value='" + players[i] + "'>" + players[i] + "</option>");
      }
    },
    data_type:"json"
  });
}

/* Close the open modal */
function cancel_modal() {
  $(".modal").hide();
}

/* Click OK on "Find Opponents" modal */
function ok_opponent() {
  // Opponent has been chosen. Now start a new game.
  player1 = get_player();
  player2 = $("#opponent-list").val();
  
  // Start a new game
  $.ajax({type:"PUT",
    url:"/game/start/" + player1 + "/" + player2,
    success:function(game_id){
      // Set field values
      $("#opponent-modal").hide();
      $("#game-id").val(game_id);
      // Since you're starting the game, you go first
      MY_TURN = true;
      MY_MARKER = 0;
      $(".marker").removeClass("active");
      $("#marker-x").addClass("active");
    },
    error:function(response, error, status) {
      console.log("failure");
      console.log("error: " + error);
      console.log("status: " + status);
    },
    data_type:"json"
  });

  update_interval();
}

/* Find the current game for the local player, if one exists */
function find_game() {
  // Find a current game that the player belongs to
  $.ajax({type:"GET",
    url:"/game/find/" + get_player(),
    success:function(response){
      // Extract game dict from response object
      var game = response['game']

      /* Find the opponent */
      var opponent = null
      $(".marker").removeClass("active");
      if(game['player1'] == get_player()) {
        opponent = game['player2'];
      } else {
        opponent = game['player1'];
      }

      // Set value of game-id hidden field based on 
      $("#game-id").val(response['game_id']);

      /* Ask local user if he wants to join the game */
      $("#join-game-modal #msg").text("Join game against " + opponent);
      $("#join-game-modal").show();
    },
    error:function() {
      console.log("Could not retrieve game.");
    },
    data_type:"json"
  });
}

/* Accept game invitation */
function ok_join_game() {
  $("#marker-o").addClass("active");
  MY_MARKER = 1;
  update_game();
  $(".modal").hide()

  update_interval();
}

/* Refresh the game board with latest server information */
function update_game() {
  var game_id = get_game_id()
  var board = null

  // Retrieve latest game state
  $.ajax({type:"GET",
    url:"/game/" + game_id,
    success:function(game){
      // Update the current game board
      board = game['board']
      populate_board(board);

      // Determine if it is the local player's turn
      if(game['turn'] == get_player()) {
        MY_TURN = true;      
      } else {
        MY_TURN = false;
      }
    },
    error:function(response, error, status) {
      console.log("update_game failure");
      console.log("error: " + error);
      console.log("status: " + status);
    },
    data_type:"json"
  });
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
  $("#refresh").bind("click", update_game);
});
